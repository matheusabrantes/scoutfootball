from fastapi import APIRouter

from app.services.providers.api_football import latest_validation_report

router = APIRouter(prefix="/api/compare", tags=["compare"])


@router.get("")
def compare() -> dict:
    report = latest_validation_report()
    if not report or report.get("status") != "completed":
        return {
            "mock": False,
            "error": "Comparison requires real player data validation first.",
            "message": "Set API_FOOTBALL_KEY and run the API-Football validation script.",
        }
    return {
        "mock": False,
        "message": "Comparison API is pending database ingestion.",
        "validated_player_fields": report.get("player_field_paths", []),
    }
