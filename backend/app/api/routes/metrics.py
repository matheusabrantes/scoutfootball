from fastapi import APIRouter

from app.db.connection import get_connection
from app.db.schema import initialize_schema
from app.repositories.metrics import MVP_METRIC_FIELDS, list_metrics

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("")
def metrics() -> dict:
    with get_connection() as connection:
        initialize_schema(connection)
        stored_metrics = list_metrics(connection)
    return {
        "data_source": "sqlite",
        "mock": False,
        "supported_metrics": sorted(MVP_METRIC_FIELDS.keys()),
        "stored_metrics": stored_metrics,
        "blocked_metrics": [
            "xg",
            "npxg",
            "xa",
            "psxg",
            "progressive_carries",
            "progressive_passes",
            "touches_in_box",
            "possession_adjusted_metrics",
            "aerial_duel_subtype",
            "offensive_defensive_duel_subtype",
        ],
    }
