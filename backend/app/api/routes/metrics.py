from fastapi import APIRouter

from app.db.connection import get_connection
from app.db.schema import initialize_schema
from app.repositories.metrics import MVP_METRIC_FIELDS, list_metrics


STATSBOMB_SUPPORTED_METRICS = [
    "minutes",
    "appearances",
    "starts",
    "goals",
    "non_penalty_goals",
    "assists",
    "shots",
    "shots_on_target",
    "xg",
    "npxg",
    "key_passes",
    "passes_attempted",
    "passes_completed",
    "pass_completion_pct",
    "forward_passes_attempted",
    "forward_passes_completed",
    "forward_pass_completion_pct",
    "progressive_passes",
    "progressive_carries",
    "crosses",
    "accurate_crosses",
    "dribbles_attempted",
    "successful_dribbles",
    "touches_in_box",
    "interceptions",
    "blocks",
    "ball_recoveries",
    "duels",
    "duels_won",
    "saves",
    "save_percentage",
    "goals_conceded",
    "yellow_cards",
    "red_cards",
]

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("")
def metrics() -> dict:
    with get_connection() as connection:
        initialize_schema(connection)
        stored_metrics = list_metrics(connection)
    return {
        "data_source": "statsbomb_open",
        "mock": False,
        "supported_metrics": sorted(set(MVP_METRIC_FIELDS.keys()) | set(STATSBOMB_SUPPORTED_METRICS)),
        "stored_metrics": stored_metrics,
        "blocked_metrics": [
            "direct_xa",
            "psxg",
            "psxg_minus_goals_allowed",
            "interceptions_padj",
            "tackles_padj",
            "possession_won_padj",
        ],
        "metric_definition_version": "statsbomb_open_v1",
    }
