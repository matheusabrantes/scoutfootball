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

OUTPUT_DIR = ROOT / "data_samples" / "api_football"
REPORT_PATH = OUTPUT_DIR / "south_america_investigation.json"
REQUEST_COUNT = 0

TARGETS = [
    {
        "internal_league_key": "bra_serie_a",
        "display_name": "Brasileirao Serie A",
        "candidate_league_id": 71,
        "country": "Brazil",
        "fallback_team_names": ["Flamengo", "Palmeiras", "Corinthians"],
    },
    {
        "internal_league_key": "argentina_primera",
        "display_name": "Argentina Primera Division",
        "candidate_league_id": 128,
        "country": "Argentina",
        "fallback_team_names": ["River Plate", "Boca Juniors", "Racing Club"],
    },
]


def load_dotenv_if_present() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
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
    elif isinstance(value, list) and value:
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


def extract_status_payload(status_response: dict[str, Any]) -> dict[str, Any]:
    response = status_response.get("response") or {}
    requests = response.get("requests") or {}
    account = response.get("account") or {}
    subscription = response.get("subscription") or {}
    return {
        "account": {
            "firstname_present": bool(account.get("firstname")),
            "lastname_present": bool(account.get("lastname")),
            "email_present": bool(account.get("email")),
        },
        "subscription": {
            "plan": subscription.get("plan"),
            "active": subscription.get("active"),
            "end": subscription.get("end"),
        },
        "requests": {
            "current": requests.get("current"),
            "limit_day": requests.get("limit_day"),
        },
    }


def season_years_from_metadata(league_response: dict[str, Any]) -> list[int]:
    seasons = []
    for item in league_response.get("response", []):
        for season in item.get("seasons", []):
            year = season.get("year")
            if isinstance(year, int):
                seasons.append(year)
    return sorted(set(seasons), reverse=True)


def select_seasons(league_response: dict[str, Any]) -> list[int]:
    metadata_seasons = []
    current_seasons = []
    for item in league_response.get("response", []):
        for season in item.get("seasons", []):
            year = season.get("year")
            if not isinstance(year, int):
                continue
            metadata_seasons.append(year)
            if season.get("current"):
                current_seasons.append(year)

    selected: list[int] = []
    for year in current_seasons + sorted(set(metadata_seasons), reverse=True)[:2] + [2025, 2024, 2023]:
        if year not in selected:
            selected.append(year)
    return selected[:4]


def league_metadata_summary(league_response: dict[str, Any]) -> dict[str, Any]:
    if not league_response.get("response"):
        return {"available": False}
    item = league_response["response"][0]
    league = item.get("league", {})
    country = item.get("country", {})
    seasons = item.get("seasons", [])
    return {
        "available": True,
        "provider_league_id": league.get("id"),
        "provider_league_name": league.get("name"),
        "country": country.get("name"),
        "available_seasons": [season.get("year") for season in seasons],
        "current_seasons": [season.get("year") for season in seasons if season.get("current")],
        "coverage_by_season": [
            {
                "year": season.get("year"),
                "current": season.get("current"),
                "coverage": season.get("coverage"),
            }
            for season in seasons
        ],
    }


def players_probe(params: dict[str, Any]) -> dict[str, Any]:
    response = api_get("players", params)
    rows = response.get("response", [])
    first_row = rows[0] if rows else {}
    field_paths = sorted(flatten_field_paths(first_row)) if rows else []
    return {
        "endpoint": "/players",
        "params": params,
        "results_on_page_1": response.get("results", len(rows)),
        "paging": response.get("paging", {}),
        "has_players": bool(rows),
        "has_statistics": bool(rows and rows[0].get("statistics")),
        "player_field_paths": field_paths,
        "player_field_groups": group_player_field_paths(field_paths),
    }


def find_fallback_teams(teams_response: dict[str, Any], wanted_names: list[str]) -> list[dict[str, Any]]:
    teams = []
    response_rows = teams_response.get("response", [])
    for wanted_name in wanted_names:
        for row in response_rows:
            team = row.get("team", {})
            if wanted_name.lower() in str(team.get("name", "")).lower():
                teams.append({"id": team.get("id"), "name": team.get("name")})
                break
        if len(teams) >= 2:
            break
    if teams:
        return teams
    for row in response_rows[:2]:
        team = row.get("team", {})
        teams.append({"id": team.get("id"), "name": team.get("name")})
    return [team for team in teams if team.get("id")]


def investigate_target(target: dict[str, Any]) -> dict[str, Any]:
    league_id = target["candidate_league_id"]
    league_response = api_get("leagues", {"id": league_id})
    league_summary = league_metadata_summary(league_response)
    selected_seasons = select_seasons(league_response)
    result = {
        "internal_league_key": target["internal_league_key"],
        "display_name": target["display_name"],
        "candidate_league_id": league_id,
        "league_metadata": league_summary,
        "selected_seasons": selected_seasons,
        "league_level_player_tests": [],
        "team_level_fallback_tests": [],
        "works": False,
        "working_pattern": None,
        "working_season": None,
        "available_player_fields": [],
        "available_player_field_groups": {},
        "blocker": None,
    }

    for season in selected_seasons:
        probe = players_probe({"league": league_id, "season": season, "page": 1})
        result["league_level_player_tests"].append(probe)
        if probe["has_players"] and probe["has_statistics"]:
            result["works"] = True
            result["working_pattern"] = "league_level"
            result["working_season"] = season
            result["available_player_fields"] = probe["player_field_paths"]
            result["available_player_field_groups"] = probe["player_field_groups"]
            return result

    for season in selected_seasons[:2]:
        teams_response = api_get("teams", {"league": league_id, "season": season})
        teams = find_fallback_teams(teams_response, target["fallback_team_names"])
        season_fallback = {
            "season": season,
            "teams_endpoint": "/teams",
            "teams_results": teams_response.get("results", 0),
            "tested_teams": teams,
            "player_tests": [],
        }
        for team in teams[:2]:
            probe = players_probe({"team": team["id"], "season": season, "page": 1})
            probe["team"] = team
            season_fallback["player_tests"].append(probe)
            if probe["has_players"] and probe["has_statistics"]:
                result["works"] = True
                result["working_pattern"] = "team_level_fallback"
                result["working_season"] = season
                result["available_player_fields"] = probe["player_field_paths"]
                result["available_player_field_groups"] = probe["player_field_groups"]
                result["team_level_fallback_tests"].append(season_fallback)
                return result
        result["team_level_fallback_tests"].append(season_fallback)

    result["blocker"] = "No player statistics returned from league-level or limited team-level probes."
    return result


def classify(report: dict[str, Any]) -> str:
    target_results = report.get("target_results", [])
    if all(result.get("works") for result in target_results):
        if any(result.get("working_pattern") == "team_level_fallback" for result in target_results):
            return "usable_with_team_level_fallback"
        return "usable_for_full_mvp"
    if any(result.get("works") for result in target_results):
        return "usable_for_europe_only_mvp"
    return "not_viable_for_south_america"


def write_report(report: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    load_dotenv_if_present()
    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provider": "api_football",
        "configured": bool(os.environ.get("API_FOOTBALL_KEY")),
        "status": "started",
        "requests_used_by_script": 0,
        "provider_status": None,
        "target_results": [],
        "classification": None,
        "recommendation": None,
    }
    if not report["configured"]:
        report["status"] = "missing_api_key"
        write_report(report)
        print("API_FOOTBALL_KEY is not configured.")
        return 1

    try:
        report["provider_status"] = extract_status_payload(api_get("status"))
        for target in TARGETS:
            print(f"Investigating {target['display_name']}...")
            report["target_results"].append(investigate_target(target))
            report["requests_used_by_script"] = REQUEST_COUNT
            write_report(report)
        report["classification"] = classify(report)
        if report["classification"] in {"usable_for_full_mvp", "usable_with_team_level_fallback"}:
            report["recommendation"] = "Proceed with API-Football MVP ingestion."
            exit_code = 0
        else:
            report["recommendation"] = (
                "Do not build ingestion yet. Validate another low-cost provider or reduce MVP to "
                "Europe-only."
            )
            exit_code = 1
        report["status"] = "completed"
        report["requests_used_by_script"] = REQUEST_COUNT
        write_report(report)
        print(json.dumps(
            {
                "requests_used_by_script": report["requests_used_by_script"],
                "classification": report["classification"],
                "recommendation": report["recommendation"],
                "targets": [
                    {
                        "league": result["display_name"],
                        "works": result["works"],
                        "working_pattern": result["working_pattern"],
                        "working_season": result["working_season"],
                    }
                    for result in report["target_results"]
                ],
            },
            indent=2,
            sort_keys=True,
        ))
        print(f"Wrote safe metadata report to {REPORT_PATH}")
        return exit_code
    except Exception as exc:
        report["status"] = "failed"
        report["error"] = str(exc)
        report["requests_used_by_script"] = REQUEST_COUNT
        write_report(report)
        print(f"Investigation failed: {exc}")
        print(f"Wrote failure report to {REPORT_PATH}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

