from fastapi import APIRouter

from app.db.connection import get_connection
from app.db.schema import initialize_schema
from app.config.statsbomb_competitions import get_statsbomb_competitions
from app.config.leagues import get_target_leagues
from app.services.providers.api_football import latest_validation_report
from app.repositories.leagues import list_leagues as list_db_leagues
from app.repositories.leagues import upsert_configured_leagues

router = APIRouter(prefix="/api/leagues", tags=["leagues"])


@router.get("")
def list_leagues() -> dict:
    with get_connection() as connection:
        initialize_schema(connection)
        upsert_configured_leagues(connection)
        db_leagues = list_db_leagues(connection)
    return {
        "data_source": "statsbomb_open",
        "primary_mvp_metrics_provider": "statsbomb_open",
        "mvp_mode": "historical_real_data_mvp",
        "real_data_configured": latest_validation_report() is not None,
        "statsbomb_competitions": get_statsbomb_competitions(),
        "api_football_fallback_leagues": get_target_leagues(),
        "database_leagues": db_leagues,
    }
