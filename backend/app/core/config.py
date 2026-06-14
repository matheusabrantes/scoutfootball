from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from os import getenv


@dataclass(frozen=True)
class Settings:
    api_football_key: str | None = None
    api_football_base_url: str = "https://v3.football.api-sports.io"
    database_url: str | None = None
    scoutfootball_db_path: str = "backend/data/scoutfootball.db"
    cors_allowed_origins: tuple[str, ...] = (
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    )
    statsbomb_data_dir: str = "backend/data_sources/statsbomb_open"
    scoutfootball_env: str = "development"
    sportmonks_api_key: str | None = None
    sportmonks_base_url: str | None = None

    @property
    def api_football_configured(self) -> bool:
        return bool(self.api_football_key)

    @property
    def sportmonks_configured(self) -> bool:
        return bool(self.sportmonks_api_key and self.sportmonks_base_url)


@lru_cache
def get_settings() -> Settings:
    return Settings(
        api_football_key=getenv("API_FOOTBALL_KEY") or None,
        api_football_base_url=getenv(
            "API_FOOTBALL_BASE_URL", "https://v3.football.api-sports.io"
        ),
        database_url=getenv("DATABASE_URL") or None,
        scoutfootball_db_path=getenv("SCOUTFOOTBALL_DB_PATH", "backend/data/scoutfootball.db"),
        cors_allowed_origins=tuple(
            origin.strip()
            for origin in getenv(
                "CORS_ALLOWED_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173",
            ).split(",")
            if origin.strip()
        ),
        statsbomb_data_dir=getenv("STATSBOMB_DATA_DIR", "backend/data_sources/statsbomb_open"),
        scoutfootball_env=getenv("SCOUTFOOTBALL_ENV", "development"),
        sportmonks_api_key=getenv("SPORTMONKS_API_KEY") or None,
        sportmonks_base_url=getenv("SPORTMONKS_BASE_URL") or None,
    )
