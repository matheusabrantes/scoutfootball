from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/health")
def health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "scoutfootball-backend",
        "mvp_mode": "historical_real_data_mvp",
        "primary_mvp_metrics_provider": "statsbomb_open",
        "providers": {
            "statsbomb_open_configured": True,
            "api_football_configured": settings.api_football_configured,
            "sportmonks_configured": settings.sportmonks_configured,
        },
    }
