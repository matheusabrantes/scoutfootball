from fastapi import APIRouter

from app.core.config import get_settings
from app.services.providers.api_football import latest_validation_report

router = APIRouter(prefix="/api/players", tags=["players"])


@router.get("")
def list_players() -> dict:
    settings = get_settings()
    report = latest_validation_report()
    if report and report.get("status") == "completed":
        return {
            "data_source": "api_football_validation_sample",
            "mock": False,
            "message": "Real provider validation metadata is available. Full player API is not wired yet.",
            "validated_leagues": report.get("validated_leagues", []),
            "player_field_paths": report.get("player_field_paths", []),
        }
    return {
        "data_source": None,
        "mock": False,
        "error": "Real player data is not configured yet.",
        "message": "Set API_FOOTBALL_KEY and run backend/scripts/validate_api_football.py.",
        "api_football_configured": settings.api_football_configured,
    }
