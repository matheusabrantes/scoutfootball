from fastapi import APIRouter

from app.db.connection import get_connection
from app.db.schema import initialize_schema

router = APIRouter(prefix="/api/seasons", tags=["seasons"])


@router.get("")
def list_seasons() -> dict:
    with get_connection() as connection:
        initialize_schema(connection)
        rows = connection.execute(
            """
            SELECT
                seasons.id,
                seasons.year,
                seasons.label,
                COUNT(DISTINCT player_season_stats.id) AS player_count
            FROM seasons
            LEFT JOIN player_season_stats ON player_season_stats.season_id = seasons.id
            GROUP BY seasons.id
            ORDER BY seasons.year DESC
            """
        ).fetchall()
    return {
        "data_source": "sqlite",
        "mock": False,
        "seasons": [dict(row) for row in rows],
    }
