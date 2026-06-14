from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.core.config import get_settings
from app.db.connection import get_connection
from app.db.schema import initialize_schema
from app.repositories.players import get_player_profile, list_players as list_db_players

router = APIRouter(prefix="/api/players", tags=["players"])


@router.get("")
def list_players(
    league: Optional[str] = None,
    season: Optional[int] = None,
    team: Optional[str] = None,
    position_group: Optional[str] = None,
    minimum_minutes: int = 0,
    nationality: Optional[str] = None,
    search: Optional[str] = None,
    age: Optional[int] = None,
    limit: int = Query(default=100, le=500),
    offset: int = 0,
) -> dict:
    settings = get_settings()
    with get_connection() as connection:
        initialize_schema(connection)
        players = list_db_players(
            connection,
            league_key=league,
            season=season,
            team=team,
            position_group=position_group,
            nationality=nationality,
            search=search,
            age=age,
            minimum_minutes=minimum_minutes,
            limit=limit,
            offset=offset,
        )
    if players:
        return {
            "data_source": "sqlite",
            "mock": False,
            "players": players,
            "count": len(players),
            "metadata": {
                "source": "statsbomb_open",
                "historical_demo": any(player.get("historical_demo") for player in players),
                "metric_definition_version": next(
                    (
                        player.get("metric_definition_version")
                        for player in players
                        if player.get("metric_definition_version")
                    ),
                    None,
                ),
                "last_updated_at": next(
                    (player.get("last_updated_at") for player in players if player.get("last_updated_at")),
                    None,
                ),
            },
        }
    return {
        "data_source": "sqlite",
        "mock": False,
        "players": [],
        "count": 0,
        "message": "Real data has not been ingested yet.",
        "api_football_configured": settings.api_football_configured,
    }


@router.get("/{player_id}")
def player_profile(player_id: int) -> dict:
    with get_connection() as connection:
        initialize_schema(connection)
        profile = get_player_profile(connection, player_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Player not found or real data has not been ingested yet.")
    return {"data_source": "sqlite", "mock": False, "player": profile}
