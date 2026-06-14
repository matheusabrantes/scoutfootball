from __future__ import annotations

from datetime import datetime, timezone
from sqlite3 import Connection
from typing import Any

from app.config.leagues import get_target_leagues
from app.repositories.metrics import extract_metric_values, upsert_metric_values
from app.repositories.players import upsert_player_season_stats
from app.services.providers.api_football import ApiFootballClient


def active_api_football_leagues() -> list[dict[str, Any]]:
    return [
        league
        for league in get_target_leagues()
        if league.get("status") == "active"
        and league.get("api_football_league_id")
        and league.get("active_season")
    ]


def create_ingestion_run(
    connection: Connection,
    league: dict[str, Any],
    started_at: str,
) -> int:
    cursor = connection.execute(
        """
        INSERT INTO ingestion_runs (
            provider, league_internal_key, league_id, season, started_at, status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "api_football",
            league["internal_league_key"],
            league["api_football_league_id"],
            league["active_season"],
            started_at,
            "running",
        ),
    )
    connection.commit()
    return int(cursor.lastrowid)


def finish_ingestion_run(
    connection: Connection,
    run_id: int,
    status: str,
    requests_used: int,
    players_ingested: int,
    error_message: str | None = None,
) -> None:
    connection.execute(
        """
        UPDATE ingestion_runs
        SET finished_at = ?, status = ?, requests_used = ?, players_ingested = ?, error_message = ?
        WHERE id = ?
        """,
        (
            datetime.now(timezone.utc).isoformat(),
            status,
            requests_used,
            players_ingested,
            error_message,
            run_id,
        ),
    )
    connection.commit()


def ingest_league_players(
    connection: Connection,
    client: ApiFootballClient,
    league: dict[str, Any],
    limit_pages: int | None,
) -> dict[str, Any]:
    started_at = datetime.now(timezone.utc).isoformat()
    run_id = create_ingestion_run(connection, league, started_at)
    requests_used = 0
    players_ingested = 0
    try:
        page = 1
        total_pages = 1
        while page <= total_pages:
            response = client.players(
                league_id=league["api_football_league_id"],
                season=league["active_season"],
                page=page,
            )
            requests_used += 1
            total_pages = int((response.get("paging") or {}).get("total") or 1)
            for player_row in response.get("response", []):
                if not player_row.get("statistics"):
                    continue
                statistics = player_row["statistics"][0]
                metric_values = extract_metric_values(statistics)
                if not any(value is not None for value in metric_values.values()):
                    continue
                player_season_stats_id = upsert_player_season_stats(
                    connection,
                    league["internal_league_key"],
                    league["active_season"],
                    player_row,
                )
                upsert_metric_values(
                    connection,
                    player_season_stats_id,
                    metric_values,
                )
                players_ingested += 1
            connection.commit()
            if limit_pages is not None and page >= limit_pages:
                break
            page += 1
        status = "completed" if players_ingested else "completed_no_metric_values"
        finish_ingestion_run(connection, run_id, status, requests_used, players_ingested)
        return {
            "league": league["internal_league_key"],
            "season": league["active_season"],
            "status": status,
            "requests_used": requests_used,
            "players_ingested": players_ingested,
            "total_pages_seen": total_pages,
        }
    except Exception as exc:
        finish_ingestion_run(
            connection,
            run_id,
            "failed",
            requests_used,
            players_ingested,
            str(exc),
        )
        return {
            "league": league["internal_league_key"],
            "season": league["active_season"],
            "status": "failed",
            "requests_used": requests_used,
            "players_ingested": players_ingested,
            "error": str(exc),
        }
