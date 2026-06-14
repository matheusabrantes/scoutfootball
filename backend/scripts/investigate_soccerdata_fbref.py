from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.services.providers.fbref_soccerdata import (  # noqa: E402
    FBREF_TABLES,
    dataframe_metadata,
    soccerdata_available,
    soccerdata_install_hint,
)

OUTPUT_DIR = ROOT / "data_samples" / "fbref"
REPORT_PATH = OUTPUT_DIR / "soccerdata_fbref_investigation.json"
SOCCERDATA_CACHE_DIR = ROOT / "data" / "soccerdata_cache"
FBREF_COMPS_URL = "https://fbref.com/en/comps/"

TARGETS = [
    {"label": "Premier League", "league": "ENG-Premier League", "season": "2024-2025"},
    {"label": "Brasileirao Serie A", "league": "BRA-Serie A", "season": "2024"},
    {"label": "La Liga", "league": "ESP-La Liga", "season": "2024-2025"},
    {"label": "Bundesliga", "league": "GER-Bundesliga", "season": "2024-2025"},
    {"label": "Serie A Italy", "league": "ITA-Serie A", "season": "2024-2025"},
    {"label": "Ligue 1", "league": "FRA-Ligue 1", "season": "2024-2025"},
    {"label": "Argentina Primera Division", "league": "ARG-Primera Division", "season": "2024"},
]


def write_report(report: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")


def try_read_table(fbref: Any, table_name: str) -> Any:
    method_candidates = [
        f"read_player_{table_name}_stats",
        f"read_{table_name}",
        "read_player_season_stats",
    ]
    last_error = None
    for method_name in method_candidates:
        method = getattr(fbref, method_name, None)
        if not method:
            continue
        try:
            if method_name == "read_player_season_stats":
                return method(stat_type=table_name)
            return method()
        except TypeError:
            try:
                return method(table_name)
            except Exception as exc:
                last_error = exc
        except Exception as exc:
            last_error = exc
    if last_error:
        raise last_error
    raise AttributeError(f"No soccerdata FBref method found for table {table_name}")


def preflight_fbref_access(fbref: Any) -> dict[str, Any]:
    try:
        response = fbref._session.get(FBREF_COMPS_URL)  # noqa: SLF001
        status_code = getattr(response, "status_code", None)
        return {
            "ok": status_code is not None and 200 <= int(status_code) < 400,
            "status_code": status_code,
            "url": FBREF_COMPS_URL,
            "error": None,
        }
    except Exception as exc:
        return {
            "ok": False,
            "status_code": None,
            "url": FBREF_COMPS_URL,
            "error": f"{type(exc).__name__}: {exc}",
        }


def investigate() -> dict[str, Any]:
    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provider": "fbref_via_soccerdata",
        "soccerdata_available": soccerdata_available(),
        "install_hint": soccerdata_install_hint(),
        "targets": [],
        "fbref_access": None,
        "strategy_classification": "unknown",
        "recommendation": None,
    }
    if not report["soccerdata_available"]:
        report["status"] = "missing_dependency"
        report["recommendation"] = "Install soccerdata before FBref investigation."
        return report

    import soccerdata as sd  # type: ignore

    preflight_reader = sd.FBref(
        leagues=[TARGETS[0]["league"]],
        seasons=[TARGETS[0]["season"]],
        data_dir=SOCCERDATA_CACHE_DIR,
    )
    report["fbref_access"] = preflight_fbref_access(preflight_reader)
    if not report["fbref_access"]["ok"]:
        report["status"] = "blocked_by_fbref_access"
        report["strategy_classification"] = "not_viable_without_paid_provider"
        report["recommendation"] = (
            "FBref refused the soccerdata request before table inspection. "
            "Do not bypass access controls; keep API-Football as metadata fallback "
            "and use a paid/licensed provider or vetted bootstrap dataset for metrics."
        )
        for target in TARGETS:
            report["targets"].append(
                {
                    **target,
                    "status": "not_tested_fbref_access_blocked",
                    "tables": {},
                    "error": (
                        f"FBref access preflight failed for {report['fbref_access']['url']} "
                        f"with status {report['fbref_access']['status_code']}"
                    ),
                }
            )
        return report

    working_targets = []
    for target in TARGETS:
        target_result = {
            **target,
            "status": "not_tested",
            "tables": {},
            "error": None,
        }
        try:
            fbref = sd.FBref(
                leagues=[target["league"]],
                seasons=[target["season"]],
                data_dir=SOCCERDATA_CACHE_DIR,
            )
            for table_name in FBREF_TABLES:
                try:
                    dataframe = try_read_table(fbref, table_name)
                    target_result["tables"][table_name] = dataframe_metadata(dataframe)
                except Exception as exc:
                    target_result["tables"][table_name] = {
                        "error": str(exc),
                        "rows": 0,
                        "columns": [],
                    }
            if any(table.get("rows", 0) > 0 for table in target_result["tables"].values()):
                target_result["status"] = "worked"
                working_targets.append(target["label"])
            else:
                target_result["status"] = "no_tables_returned"
        except Exception as exc:
            target_result["status"] = "failed"
            target_result["error"] = str(exc)
        report["targets"].append(target_result)

        if len(report["targets"]) >= 2 and not working_targets:
            report["recommendation"] = "Stop early: soccerdata API or league naming needs manual adjustment."
            break

    worked = set(working_targets)
    europe_worked = bool(worked & {"Premier League", "La Liga", "Bundesliga", "Serie A Italy", "Ligue 1"})
    south_america_worked = bool(worked & {"Brasileirao Serie A", "Argentina Primera Division"})
    if europe_worked and south_america_worked:
        report["strategy_classification"] = "fbref_first_viable"
    elif europe_worked:
        report["strategy_classification"] = "fbref_europe_only_viable"
    elif not europe_worked and not south_america_worked:
        report["strategy_classification"] = "unknown"
    else:
        report["strategy_classification"] = "fbref_plus_api_football_viable"
    report["status"] = "completed"
    if not report.get("recommendation"):
        report["recommendation"] = (
            "Use FBref via soccerdata where tables work; keep API-Football as metadata fallback."
        )
    return report


def main() -> int:
    report = investigate()
    write_report(report)
    print(json.dumps(
        {
            "soccerdata_available": report["soccerdata_available"],
            "status": report["status"],
            "strategy_classification": report["strategy_classification"],
            "recommendation": report["recommendation"],
            "report_path": str(REPORT_PATH),
        },
        indent=2,
        sort_keys=True,
    ))
    return 0 if report["soccerdata_available"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
