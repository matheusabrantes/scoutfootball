from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Query

from app.db.connection import get_connection
from app.db.schema import initialize_schema

router = APIRouter(prefix="/api/rankings", tags=["rankings"])


@router.get("")
def rankings(
    metric: str = "minutes",
    league: Optional[str] = None,
    competition: Optional[str] = None,
    season: Optional[int] = None,
    team: Optional[str] = None,
    position_group: Optional[str] = None,
    minimum_minutes: int = 0,
    sort: str = "metric_value",
    limit: int = Query(default=100, le=500),
) -> dict:
    filters = [
        "player_metric_values.metric_key = ?",
        "COALESCE(player_season_stats.minutes, 0) >= ?",
    ]
    params: list[Any] = [metric, minimum_minutes]
    league_filter = competition or league
    if league_filter:
        filters.append("leagues.internal_key = ?")
        params.append(league_filter)
    if season:
        filters.append("seasons.year = ?")
        params.append(season)
    if team:
        filters.append("teams.name LIKE ?")
        params.append(f"%{team}%")
    if position_group:
        filters.append("player_season_stats.position_group = ?")
        params.append(position_group)
    order_column = "player_metric_values.percentile" if sort == "percentile" else "player_metric_values.metric_value"
    params.append(limit)
    with get_connection() as connection:
        initialize_schema(connection)
        rows = connection.execute(
            f"""
            SELECT
                players.id,
                players.name,
                players.age,
                players.nationality,
                teams.name AS team_name,
                leagues.internal_key AS league_key,
                leagues.display_name AS league_name,
                seasons.year AS season,
                player_season_stats.position,
                player_season_stats.position_group,
                player_season_stats.minutes,
                player_metric_values.metric_key,
                player_metric_values.metric_value,
                player_metric_values.percentile,
                player_metric_values.peer_count,
                player_metric_values.population_size,
                player_metric_values.minutes_threshold,
                player_season_stats.provider,
                player_season_stats.historical_demo,
                player_season_stats.metric_definition_version,
                player_season_stats.last_updated_at
            FROM player_metric_values
            JOIN player_season_stats ON player_season_stats.id = player_metric_values.player_season_stats_id
            JOIN players ON players.id = player_season_stats.player_id
            JOIN teams ON teams.id = player_season_stats.team_id
            JOIN leagues ON leagues.id = player_season_stats.league_id
            JOIN seasons ON seasons.id = player_season_stats.season_id
            WHERE {" AND ".join(filters)}
            ORDER BY {order_column} DESC NULLS LAST, player_season_stats.minutes DESC
            LIMIT ?
            """,
            params,
        ).fetchall()
    rankings_rows = [dict(row) for row in rows]
    if not rankings_rows:
        return {
            "mock": False,
            "rankings": [],
            "message": "Real data has not been ingested yet.",
        }
    return {
        "data_source": "sqlite",
        "mock": False,
            "metric": metric,
            "rankings": rankings_rows,
            "metadata": {
                "source": "statsbomb_open",
                "historical_demo": any(row.get("historical_demo") for row in rankings_rows),
                "metric_definition_version": next(
                    (
                        row.get("metric_definition_version")
                        for row in rankings_rows
                        if row.get("metric_definition_version")
                    ),
                    None,
                ),
                "last_updated_at": next(
                    (row.get("last_updated_at") for row in rankings_rows if row.get("last_updated_at")),
                    None,
                ),
            },
        }
