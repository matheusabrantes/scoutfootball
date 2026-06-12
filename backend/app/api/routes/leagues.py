from fastapi import APIRouter

from app.db.connection import get_connection
from app.db.schema import initialize_schema
from app.repositories.leagues import list_leagues as list_db_leagues
from app.repositories.leagues import upsert_configured_leagues
from app.config.leagues import get_target_leagues
from app.services.providers.api_football import latest_validation_report

router = APIRouter(prefix="/api/leagues", tags=["leagues"])


@router.get("")
def list_leagues() -> dict:
    with get_connection() as connection:
        initialize_schema(connection)
        upsert_configured_leagues(connection)
        db_leagues = list_db_leagues(connection)
    return {
        "data_source": "api_football",
        "real_data_configured": latest_validation_report() is not None,
        "leagues": get_target_leagues(),
        "database_leagues": db_leagues,
    }
