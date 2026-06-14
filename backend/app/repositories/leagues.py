from __future__ import annotations

from sqlite3 import Connection
from typing import Any

from app.config.leagues import get_target_leagues


def upsert_configured_leagues(connection: Connection) -> None:
    for league in get_target_leagues():
        provider_league_id = league.get("api_football_league_id")
        if provider_league_id is None:
            provider_league_id = -1
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
                league["internal_league_key"],
                "api_football",
                provider_league_id,
                league["display_name"],
                league["country"],
                league["priority"],
                league["status"],
                league.get("active_season"),
                league.get("last_validated_season"),
                league.get("validation_notes"),
            ),
        )
    connection.commit()


def list_leagues(connection: Connection) -> list[dict[str, Any]]:
    rows = connection.execute(
        """
        SELECT
            leagues.*,
            COUNT(DISTINCT player_season_stats.id) AS player_count
        FROM leagues
        LEFT JOIN player_season_stats ON player_season_stats.league_id = leagues.id
        GROUP BY leagues.id
        ORDER BY priority, display_name
        """
    ).fetchall()
    return [dict(row) for row in rows]


def find_league_by_internal_key(connection: Connection, internal_key: str) -> dict[str, Any] | None:
    row = connection.execute(
        "SELECT * FROM leagues WHERE internal_key = ?",
        (internal_key,),
    ).fetchone()
    return dict(row) if row else None

