from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.core.config import Settings


class ProviderConfigurationError(RuntimeError):
    pass


class ApiFootballClient:
    def __init__(self, settings: Settings) -> None:
        if not settings.api_football_key:
            raise ProviderConfigurationError("API_FOOTBALL_KEY is not configured.")
        self.base_url = settings.api_football_base_url.rstrip("/")
        self.api_key = settings.api_football_key

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        query = f"?{urlencode(params)}" if params else ""
        request = Request(
            f"{self.base_url}/{path.lstrip('/')}{query}",
            headers={"x-apisports-key": self.api_key},
        )
        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"API-Football HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"API-Football request failed: {exc.reason}") from exc

    def status(self) -> dict[str, Any]:
        return self.get("status")

    def leagues(self, **params: Any) -> dict[str, Any]:
        return self.get("leagues", params)

    def players(self, league_id: int, season: int, page: int = 1) -> dict[str, Any]:
        return self.get("players", {"league": league_id, "season": season, "page": page})


def sample_metadata_path() -> Path:
    return Path(__file__).resolve().parents[3] / "data_samples" / "api_football"


def latest_validation_report() -> dict[str, Any] | None:
    report_path = sample_metadata_path() / "validation_report.json"
    if not report_path.exists():
        return None
    return json.loads(report_path.read_text(encoding="utf-8"))

