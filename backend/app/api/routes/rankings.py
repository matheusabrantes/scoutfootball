from fastapi import APIRouter

from app.services.providers.api_football import latest_validation_report

router = APIRouter(prefix="/api/rankings", tags=["rankings"])


@router.get("")
def rankings() -> dict:
    report = latest_validation_report()
    if not report or report.get("status") != "completed":
        return {
            "mock": False,
            "error": "Rankings require real player data validation first.",
            "message": "Set API_FOOTBALL_KEY and run the API-Football validation script.",
        }
    return {
        "mock": False,
        "message": "Ranking calculation is pending database ingestion.",
        "validated_player_fields": report.get("player_field_paths", []),
    }
