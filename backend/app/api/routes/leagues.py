from fastapi import APIRouter

from app.config.leagues import get_target_leagues
from app.services.providers.api_football import latest_validation_report

router = APIRouter(prefix="/api/leagues", tags=["leagues"])


@router.get("")
def list_leagues() -> dict:
    return {
        "data_source": "api_football",
        "real_data_configured": latest_validation_report() is not None,
        "leagues": get_target_leagues(),
    }

