from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/health")
def health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "scoutfootball-backend",
        "providers": {
            "api_football_configured": settings.api_football_configured,
            "sportmonks_configured": settings.sportmonks_configured,
        },
    }

