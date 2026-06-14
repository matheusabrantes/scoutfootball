from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from app.core.config import get_settings


REPO_RAW_BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master"
REPO_TREE_URL = "https://api.github.com/repos/statsbomb/open-data/git/trees/master?recursive=1"
DEFAULT_DATA_DIR = "backend/data_sources/statsbomb_open"


class StatsBombOpenDataProvider:
    def __init__(self, data_dir: Path | str | None = None) -> None:
        self.data_dir = _resolve_data_dir(data_dir or get_settings().statsbomb_data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def list_competitions(self) -> list[dict[str, Any]]:
        return self._read_or_download_json("competitions.json", "data/competitions.json")

    def list_matches(self, competition_id: int, season_id: int) -> list[dict[str, Any]]:
        cache_name = f"matches/{competition_id}_{season_id}.json"
        repo_path = f"data/matches/{competition_id}/{season_id}.json"
        return self._read_or_download_json(cache_name, repo_path)

    def read_events(self, match_id: int) -> list[dict[str, Any]]:
        return self._read_or_download_json(f"events/{match_id}.json", f"data/events/{match_id}.json")

    def read_lineups(self, match_id: int) -> list[dict[str, Any]]:
        return self._read_or_download_json(f"lineups/{match_id}.json", f"data/lineups/{match_id}.json")

    def read_three_sixty(self, match_id: int) -> list[dict[str, Any]]:
        return self._read_or_download_json(
            f"three-sixty/{match_id}.json",
            f"data/three-sixty/{match_id}.json",
        )

    def repository_paths(self) -> set[str]:
        tree = self._read_or_download_url("tree.json", REPO_TREE_URL)
        return {item["path"] for item in tree.get("tree", []) if item.get("type") == "blob"}

    def normalize_event(self, event: dict[str, Any]) -> dict[str, Any]:
        event_type = event.get("type", {}).get("name")
        normalized = {
            "id": event.get("id"),
            "index": event.get("index"),
            "period": event.get("period"),
            "minute": event.get("minute"),
            "second": event.get("second"),
            "type": event_type,
            "player_id": event.get("player", {}).get("id"),
            "player_name": event.get("player", {}).get("name"),
            "team_id": event.get("team", {}).get("id"),
            "team_name": event.get("team", {}).get("name"),
            "position": event.get("position", {}).get("name"),
            "location": event.get("location"),
            "duration": event.get("duration"),
            "under_pressure": event.get("under_pressure", False),
            "possession": event.get("possession"),
        }
        for nested_key in (
            "pass",
            "carry",
            "shot",
            "duel",
            "dribble",
            "goalkeeper",
            "interception",
            "foul_committed",
            "foul_won",
            "bad_behaviour",
            "ball_recovery",
            "block",
            "clearance",
            "substitution",
            "tactics",
        ):
            if nested_key in event:
                normalized[nested_key] = event[nested_key]
        return normalized

    def _read_or_download_json(self, cache_name: str, repo_path: str) -> Any:
        return self._read_or_download_url(cache_name, f"{REPO_RAW_BASE_URL}/{repo_path}")

    def _read_or_download_url(self, cache_name: str, url: str) -> Any:
        cache_path = self.data_dir / cache_name
        if cache_path.exists():
            return json.loads(cache_path.read_text(encoding="utf-8"))
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        request = Request(url, headers={"User-Agent": "ScoutFootball StatsBomb Open Data POC"})
        with urlopen(request, timeout=60) as response:
            payload = response.read().decode("utf-8")
        cache_path.write_text(payload, encoding="utf-8")
        return json.loads(payload)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _resolve_data_dir(data_dir: Path | str) -> Path:
    path = Path(data_dir)
    if path.is_absolute():
        return path
    return _project_root() / path
