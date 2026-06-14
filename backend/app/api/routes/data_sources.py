from fastapi import APIRouter

from app.config.statsbomb_competitions import get_statsbomb_competitions
from app.db.connection import get_connection
from app.db.schema import initialize_schema

router = APIRouter(prefix="/api/data-sources", tags=["data-sources"])


@router.get("")
def data_sources() -> dict:
    with get_connection() as connection:
        initialize_schema(connection)
        rows = connection.execute(
            """
            SELECT
                provider,
                COUNT(DISTINCT player_season_stats.id) AS player_rows,
                MAX(last_updated_at) AS last_updated_at
            FROM player_season_stats
            GROUP BY provider
            ORDER BY provider
            """
        ).fetchall()
    return {
        "mock": False,
        "primary_mvp_metrics_provider": "statsbomb_open",
        "mvp_mode": "historical_real_data_mvp",
        "sources": [dict(row) for row in rows],
        "statsbomb_competitions": get_statsbomb_competitions(),
        "attribution": "Data source: StatsBomb Open Data.",
    }
