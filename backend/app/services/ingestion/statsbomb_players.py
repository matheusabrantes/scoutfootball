from __future__ import annotations

import json
from datetime import datetime, timezone
from sqlite3 import Connection
from typing import Any

from app.config.statsbomb_competitions import find_statsbomb_competition
from app.repositories.metrics import upsert_metric_values


PROVIDER = "statsbomb_open"
METRIC_DEFINITION_VERSION = "statsbomb_open_v1"
PER_90_EXCLUDED_SUFFIXES = ("pct", "percentage", "accuracy", "completion")
PER_90_EXCLUDED_METRICS = {
    "minutes",
    "appearances",
    "starts",
    "pass_completion_pct",
    "forward_pass_completion_pct",
    "save_percentage",
    "long_pass_accuracy",
    "short_pass_completion",
}


def ingest_statsbomb_player_rows(
    connection: Connection,
    competition_id: int,
    season_id: int,
    player_rows: list[dict[str, Any]],
    quality_summary: dict[str, Any],
) -> dict[str, int]:
    config = find_statsbomb_competition(competition_id, season_id)
    if not config:
        raise ValueError(f"StatsBomb competition is not configured: {competition_id}/{season_id}")
    league_id = upsert_statsbomb_league(connection, config)
    db_season_id = upsert_statsbomb_season(connection, config["season_name"])
    result = {"inserted": 0, "updated": 0, "skipped": 0, "failed": 0}
    started_at = datetime.now(timezone.utc).isoformat()
    run_id = create_ingestion_run(connection, config, started_at)
    for row in player_rows:
        try:
            if not row.get("player_id") or not row.get("provider_team_id"):
                result["skipped"] += 1
                continue
            player_id = upsert_statsbomb_player(connection, row)
            team_id = upsert_statsbomb_team(connection, row, league_id, db_season_id)
            existed = player_season_exists(connection, player_id, league_id, db_season_id, team_id)
            player_season_stats_id = upsert_statsbomb_player_season(
                connection,
                row,
                player_id,
                league_id,
                db_season_id,
                team_id,
                competition_id,
                season_id,
                quality_summary,
            )
            upsert_metric_values(connection, player_season_stats_id, metric_values(row))
            result["updated" if existed else "inserted"] += 1
        except Exception:
            result["failed"] += 1
    finish_ingestion_run(connection, run_id, result, None if result["failed"] == 0 else "Some rows failed")
    connection.commit()
    return result


def upsert_statsbomb_league(connection: Connection, config: dict[str, Any]) -> int:
    connection.execute(
        """
        INSERT INTO leagues (
            internal_key, provider, provider_league_id, display_name, country, priority,
            status, active_season, last_validated_season, validation_notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(internal_key) DO UPDATE SET
            provider=excluded.provider,
            provider_league_id=excluded.provider_league_id,
            display_name=excluded.display_name,
            country=excluded.country,
            priority=excluded.priority,
            status=excluded.status,
            active_season=excluded.active_season,
            last_validated_season=excluded.last_validated_season,
            validation_notes=excluded.validation_notes
        """,
        (
            config["internal_key"],
            PROVIDER,
            config["competition_id"],
            config["competition_name"],
            config["country"],
            "P0" if config["status"] == "active" else "P1",
            config["status"],
            int(config["season_name"].split("/")[-1]),
            int(config["season_name"].split("/")[-1]),
            config["notes"],
        ),
    )
    row = connection.execute(
        "SELECT id FROM leagues WHERE internal_key = ?",
        (config["internal_key"],),
    ).fetchone()
    return int(row["id"])


def upsert_statsbomb_season(connection: Connection, season_name: str) -> int:
    year = int(season_name.split("/")[-1])
    connection.execute(
        """
        INSERT INTO seasons (year, label)
        VALUES (?, ?)
        ON CONFLICT(year) DO UPDATE SET label=excluded.label
        """,
        (year, season_name),
    )
    row = connection.execute("SELECT id FROM seasons WHERE year = ?", (year,)).fetchone()
    return int(row["id"])


def upsert_statsbomb_team(
    connection: Connection,
    row: dict[str, Any],
    league_id: int,
    season_id: int,
) -> int:
    connection.execute(
        """
        INSERT INTO teams (provider, provider_team_id, name, logo_url, league_id, season_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(provider, provider_team_id, league_id, season_id) DO UPDATE SET
            name=excluded.name
        """,
        (PROVIDER, row["provider_team_id"], row["team"], None, league_id, season_id),
    )
    team = connection.execute(
        """
        SELECT id FROM teams
        WHERE provider = ? AND provider_team_id = ? AND league_id = ? AND season_id = ?
        """,
        (PROVIDER, row["provider_team_id"], league_id, season_id),
    ).fetchone()
    return int(team["id"])


def upsert_statsbomb_player(connection: Connection, row: dict[str, Any]) -> int:
    connection.execute(
        """
        INSERT INTO players (provider, provider_player_id, name)
        VALUES (?, ?, ?)
        ON CONFLICT(provider, provider_player_id) DO UPDATE SET name=excluded.name
        """,
        (PROVIDER, row["player_id"], row["player_name"]),
    )
    player = connection.execute(
        "SELECT id FROM players WHERE provider = ? AND provider_player_id = ?",
        (PROVIDER, row["player_id"]),
    ).fetchone()
    return int(player["id"])


def player_season_exists(
    connection: Connection,
    player_id: int,
    league_id: int,
    season_id: int,
    team_id: int,
) -> bool:
    row = connection.execute(
        """
        SELECT id FROM player_season_stats
        WHERE player_id = ? AND league_id = ? AND season_id = ? AND team_id = ?
        """,
        (player_id, league_id, season_id, team_id),
    ).fetchone()
    return row is not None


def upsert_statsbomb_player_season(
    connection: Connection,
    row: dict[str, Any],
    player_id: int,
    league_id: int,
    season_id: int,
    team_id: int,
    competition_id: int,
    provider_season_id: int,
    quality_summary: dict[str, Any],
) -> int:
    connection.execute(
        """
        INSERT INTO player_season_stats (
            player_id, league_id, season_id, team_id, provider, position, position_group,
            appearances, starts, minutes, rating, raw_field_metadata, provider_competition_id,
            provider_season_id, historical_demo, metric_definition_version, ingestion_quality,
            last_updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(player_id, league_id, season_id, team_id) DO UPDATE SET
            position_group=excluded.position_group,
            appearances=excluded.appearances,
            starts=excluded.starts,
            minutes=excluded.minutes,
            raw_field_metadata=excluded.raw_field_metadata,
            provider_competition_id=excluded.provider_competition_id,
            provider_season_id=excluded.provider_season_id,
            historical_demo=excluded.historical_demo,
            metric_definition_version=excluded.metric_definition_version,
            ingestion_quality=excluded.ingestion_quality,
            last_updated_at=excluded.last_updated_at
        """,
        (
            player_id,
            league_id,
            season_id,
            team_id,
            PROVIDER,
            row.get("position_group"),
            row.get("position_group"),
            row.get("appearances"),
            row.get("starts"),
            row.get("minutes"),
            None,
            json.dumps({"available_fields": sorted(row.keys())}),
            competition_id,
            provider_season_id,
            1,
            METRIC_DEFINITION_VERSION,
            json.dumps(quality_summary, sort_keys=True),
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    item = connection.execute(
        """
        SELECT id FROM player_season_stats
        WHERE player_id = ? AND league_id = ? AND season_id = ? AND team_id = ?
        """,
        (player_id, league_id, season_id, team_id),
    ).fetchone()
    return int(item["id"])


def metric_values(row: dict[str, Any]) -> dict[str, float | None]:
    values = {}
    for key, value in row.items():
        if key in {
            "player_id",
            "player_name",
            "provider_team_id",
            "team",
            "competition",
            "season",
            "position_group",
        }:
            continue
        if isinstance(value, (int, float)) or value is None:
            values[key] = None if value is None else float(value)
            if should_add_per_90(key, value, row.get("minutes")):
                values[f"{key}_per_90"] = float(value) / float(row["minutes"]) * 90.0
    for unavailable in ("direct_xa", "psxg", "psxg_minus_goals_allowed"):
        values[unavailable] = None
    for placeholder in ("interceptions_padj", "tackles_padj", "possession_won_padj"):
        values[placeholder] = None
    return values


def should_add_per_90(key: str, value: Any, minutes: Any) -> bool:
    if key in PER_90_EXCLUDED_METRICS or key.endswith(PER_90_EXCLUDED_SUFFIXES):
        return False
    return isinstance(value, (int, float)) and minutes and float(minutes) > 0


def create_ingestion_run(connection: Connection, config: dict[str, Any], started_at: str) -> int:
    connection.execute(
        """
        INSERT INTO ingestion_runs (provider, league_internal_key, league_id, season, started_at, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            PROVIDER,
            config["internal_key"],
            config["competition_id"],
            int(config["season_name"].split("/")[-1]),
            started_at,
            "running",
        ),
    )
    return int(connection.execute("SELECT last_insert_rowid() AS id").fetchone()["id"])


def finish_ingestion_run(
    connection: Connection,
    run_id: int,
    result: dict[str, int],
    error_message: str | None,
) -> None:
    connection.execute(
        """
        UPDATE ingestion_runs
        SET finished_at = ?, status = ?, players_ingested = ?, error_message = ?
        WHERE id = ?
        """,
        (
            datetime.now(timezone.utc).isoformat(),
            "completed" if not error_message else "completed_with_errors",
            result["inserted"] + result["updated"],
            error_message,
            run_id,
        ),
    )
