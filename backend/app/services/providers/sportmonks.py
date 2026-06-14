from app.core.config import Settings


class SportmonksClient:
    def __init__(self, settings: Settings) -> None:
        self.configured = settings.sportmonks_configured
        self.base_url = settings.sportmonks_base_url

    def configuration_status(self) -> dict:
        if not self.configured:
            return {
                "provider": "sportmonks",
                "configured": False,
                "message": "SPORTMONKS_API_KEY and SPORTMONKS_BASE_URL are not configured.",
            }
        return {
            "provider": "sportmonks",
            "configured": True,
            "message": "Sportmonks backup provider is configured but not implemented yet.",
        }

