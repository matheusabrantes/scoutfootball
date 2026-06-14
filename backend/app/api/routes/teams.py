from __future__ import annotations

from typing import Optional

from fastapi import APIRouter

from app.db.connection import get_connection
from app.db.schema import initialize_schema

router = APIRouter(prefix="/api/teams", tags=["teams"])


@router.get("")
def list_teams(competition: Optional[str] = None, season: Optional[int] = None) -> dict:
    filters = []
    params = []
    if competition:
        filters.append("leagues.internal_key = ?")
        params.append(competition)
    if season:
        filters.append("seasons.year = ?")
        params.append(season)
    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    with get_connection() as connection:
        initialize_schema(connection)
        rows = connection.execute(
            f"""
            SELECT
                teams.id,
                teams.provider,
                teams.provider_team_id,
                teams.name,
                leagues.internal_key AS competition,
                leagues.display_name AS competition_name,
                seasons.year AS season,
                seasons.label AS season_label,
                COUNT(DISTINCT player_season_stats.id) AS player_count
            FROM teams
            JOIN leagues ON leagues.id = teams.league_id
            JOIN seasons ON seasons.id = teams.season_id
            LEFT JOIN player_season_stats ON player_season_stats.team_id = teams.id
            {where_clause}
            GROUP BY teams.id
            ORDER BY teams.name
            """,
            params,
        ).fetchall()
    return {"data_source": "sqlite", "mock": False, "teams": [dict(row) for row in rows]}
