from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from app.config.leagues import TARGET_LEAGUES  # noqa: E402

OUTPUT_DIR = ROOT / "data_samples" / "api_football"
REPORT_PATH = OUTPUT_DIR / "validation_report.json"
REQUEST_COUNT = 0


def load_dotenv_if_present() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def api_get(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    global REQUEST_COUNT
    api_key = os.environ.get("API_FOOTBALL_KEY")
    if not api_key:
        raise RuntimeError("API_FOOTBALL_KEY is not configured.")
    base_url = os.environ.get("API_FOOTBALL_BASE_URL", "https://v3.football.api-sports.io")
    query = f"?{urlencode(params)}" if params else ""
    request = Request(
        f"{base_url.rstrip('/')}/{path.lstrip('/')}{query}",
        headers={"x-apisports-key": api_key},
    )
    try:
        REQUEST_COUNT += 1
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
            delay_seconds = float(os.environ.get("API_FOOTBALL_REQUEST_DELAY_SECONDS", "7"))
            if delay_seconds > 0:
                time.sleep(delay_seconds)
            return payload
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API-Football HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"API-Football request failed: {exc.reason}") from exc


def flatten_field_paths(value: Any, prefix: str = "") -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            paths.add(child_prefix)
            paths.update(flatten_field_paths(child, child_prefix))
    elif isinstance(value, list):
        if value:
            paths.update(flatten_field_paths(value[0], prefix))
    return paths


def group_player_field_paths(field_paths: list[str]) -> dict[str, list[str]]:
    groups = {
        "identity": [],
        "team_club": [],
        "league_season": [],
        "position": [],
        "minutes_appearances": [],
        "attacking": [],
        "passing": [],
        "defensive": [],
        "duels": [],
        "dribbling": [],
        "goalkeeper": [],
        "discipline": [],
        "other": [],
    }
    for path in field_paths:
        if path.startswith("player."):
            groups["identity"].append(path)
        elif path.startswith("statistics.team"):
            groups["team_club"].append(path)
        elif path.startswith("statistics.league"):
            groups["league_season"].append(path)
        elif path in {"statistics.games.position", "statistics.games.rating"}:
            groups["position"].append(path)
        elif path.startswith("statistics.games"):
            groups["minutes_appearances"].append(path)
        elif path.startswith("statistics.goals") or path.startswith("statistics.shots"):
            if path.endswith(".saves") or path.endswith(".conceded"):
                groups["goalkeeper"].append(path)
            else:
                groups["attacking"].append(path)
        elif path.startswith("statistics.passes"):
            groups["passing"].append(path)
        elif path.startswith("statistics.tackles"):
            groups["defensive"].append(path)
        elif path.startswith("statistics.duels"):
            groups["duels"].append(path)
        elif path.startswith("statistics.dribbles"):
            groups["dribbling"].append(path)
        elif path.startswith("statistics.cards") or path.startswith("statistics.penalty"):
            groups["discipline"].append(path)
        else:
            groups["other"].append(path)
    return {group: sorted(paths) for group, paths in groups.items() if paths}


def select_recent_seasons(seasons: list[int]) -> list[int]:
    ordered = sorted({season for season in seasons if isinstance(season, int)}, reverse=True)
    return ordered[:2]


def resolve_league_id(league: dict[str, Any]) -> int | None:
    configured_id = league.get("api_football_league_id")
    if isinstance(configured_id, int):
        return configured_id
    country = league["country"]
    for term in league.get("api_football_search_terms", []):
        response = api_get("leagues", {"search": term})
        for item in response.get("response", []):
            provider_league = item.get("league", {})
            provider_country = item.get("country", {})
            if provider_country.get("name") == country:
                return provider_league.get("id")
    return None


def validate_league(league: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "internal_league_key": league["internal_league_key"],
        "display_name": league["display_name"],
        "priority": league["priority"],
        "country": league["country"],
        "league_id": None,
        "seasons_checked": [],
        "player_sample_count": 0,
        "player_field_paths": [],
        "status": "needs_validation",
        "error": None,
    }
    league_id = resolve_league_id(league)
    result["league_id"] = league_id
    if not league_id:
        result["status"] = "provider_not_available"
        result["error"] = "Could not resolve API-Football league id."
        return result

    league_response = api_get("leagues", {"id": league_id})
    if not league_response.get("response"):
        result["status"] = "provider_not_available"
        result["error"] = "API-Football returned no league coverage response."
        return result

    seasons = []
    for item in league_response.get("response", []):
        seasons.extend(season.get("year") for season in item.get("seasons", []))
    result["seasons_checked"] = select_recent_seasons(seasons)
    for season in result["seasons_checked"]:
        players_response = api_get("players", {"league": league_id, "season": season, "page": 1})
        players = players_response.get("response", [])
        if players:
            result["player_sample_count"] = len(players)
            result["player_field_paths"] = sorted(flatten_field_paths(players[0]))
            result["status"] = "validated"
            break
    if result["status"] != "validated":
        result["status"] = "blocked"
        result["error"] = "League exists, but no player statistics sample was returned."
    return result


def write_report(report: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")


def summarize_acceptance(report: dict[str, Any]) -> dict[str, Any]:
    validated = set(report["validated_leagues"])
    euro_p0 = {
        "premier_league",
        "la_liga",
        "bundesliga",
        "serie_a_italy",
        "ligue_1",
    }
    return {
        "brasileirao_validated": "bra_serie_a" in validated,
        "argentina_validated": "argentina_primera" in validated,
        "major_european_validated_count": len(validated & euro_p0),
        "validated_major_european_leagues": sorted(validated & euro_p0),
        "enough_to_proceed": (
            "bra_serie_a" in validated
            and "argentina_primera" in validated
            and len(validated & euro_p0) >= 3
        ),
    }


def refresh_report_summary(report: dict[str, Any]) -> None:
    report["acceptance"] = summarize_acceptance(report)
    report["player_field_groups"] = group_player_field_paths(report["player_field_paths"])
    report["requests_used_by_script"] = REQUEST_COUNT


def main() -> int:
    load_dotenv_if_present()
    started_at = datetime.now(timezone.utc).isoformat()
    report: dict[str, Any] = {
        "generated_at": started_at,
        "provider": "api_football",
        "configured": bool(os.environ.get("API_FOOTBALL_KEY")),
        "status": None,
        "account": None,
        "requests_used_by_script": 0,
        "validated_leagues": [],
        "league_results": [],
        "player_field_paths": [],
        "player_field_groups": {},
        "acceptance": {
            "brasileirao_validated": False,
            "argentina_validated": False,
            "major_european_validated_count": 0,
            "enough_to_proceed": False,
        },
    }

    if not report["configured"]:
        report["status"] = "missing_api_key"
        write_report(report)
        print("API_FOOTBALL_KEY is not configured.")
        print(f"Wrote metadata-only report to {REPORT_PATH}")
        return 1

    try:
        report["account"] = api_get("status")
        for priority in ("P0", "P1", "P2"):
            for league in [item for item in TARGET_LEAGUES if item["priority"] == priority]:
                print(f"Validating {league['display_name']} ({priority})...")
                result = validate_league(league)
                report["league_results"].append(result)
                if result["status"] == "validated":
                    report["validated_leagues"].append(result["internal_league_key"])
                    report["player_field_paths"] = sorted(
                        set(report["player_field_paths"]) | set(result["player_field_paths"])
                    )
            refresh_report_summary(report)
            if priority == "P0":
                write_report(report)
            if priority == "P0" and league["internal_league_key"] == "ligue_1":
                if not report["acceptance"]["enough_to_proceed"]:
                    report["status"] = "completed_p0_acceptance_failed"
                    refresh_report_summary(report)
                    write_report(report)
                    print(json.dumps(report["acceptance"], indent=2, sort_keys=True))
                    print("P0 validation completed, but MVP acceptance did not pass.")
                    print(f"Wrote validation report to {REPORT_PATH}")
                    return 1
        report["status"] = "completed"
        refresh_report_summary(report)
        write_report(report)
        print(json.dumps(report["acceptance"], indent=2, sort_keys=True))
        print("Available player field paths:")
        for field_path in report["player_field_paths"]:
            print(f"- {field_path}")
        print(f"Wrote validation report to {REPORT_PATH}")
        return 0
    except Exception as exc:
        report["status"] = "failed"
        report["error"] = str(exc)
        refresh_report_summary(report)
        write_report(report)
        print(f"Validation failed: {exc}")
        print(f"Wrote failure report to {REPORT_PATH}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
