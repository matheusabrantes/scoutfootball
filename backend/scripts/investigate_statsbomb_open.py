from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.services.providers.statsbomb_open import StatsBombOpenDataProvider  # noqa: E402


TARGET_LEAGUES = {
    "Premier League": ["Premier League"],
    "La Liga": ["La Liga"],
    "Bundesliga": ["1. Bundesliga"],
    "Serie A Italy": ["Serie A"],
    "Ligue 1": ["Ligue 1"],
    "Eredivisie": ["Eredivisie"],
    "Liga Portugal": ["Liga Portugal", "Primeira Liga"],
    "Brasileirao Serie A": ["Serie A"],
    "Argentina Primera Division": ["Liga Profesional", "Primera División"],
    "Colombia Categoria Primera A": ["Categoría Primera A", "Primera A"],
    "Uruguay Primera Division": ["Primera División"],
    "Chile Primera Division": ["Primera División"],
}


def target_match(competition: dict[str, Any]) -> str | None:
    country = competition["country_name"]
    name = competition["competition_name"]
    for target, aliases in TARGET_LEAGUES.items():
        if any(alias == name for alias in aliases):
            if target == "Bundesliga" and country == "Germany":
                return target
            if target == "Serie A Italy" and country == "Italy":
                return target
            if target == "Brasileirao Serie A" and country == "Brazil":
                return target
            if target == "Argentina Primera Division" and country == "Argentina":
                return target
            if target == "Colombia Categoria Primera A" and country == "Colombia":
                return target
            if target == "Uruguay Primera Division" and country == "Uruguay":
                return target
            if target == "Chile Primera Division" and country == "Chile":
                return target
            if target in {"Premier League", "La Liga", "Ligue 1", "Eredivisie", "Liga Portugal"}:
                return target
    return None


def build_coverage(provider: StatsBombOpenDataProvider) -> list[dict[str, Any]]:
    paths = provider.repository_paths()
    coverage = []
    for competition in provider.list_competitions():
        competition_id = int(competition["competition_id"])
        season_id = int(competition["season_id"])
        matches = provider.list_matches(competition_id, season_id)
        match_ids = [int(match["match_id"]) for match in matches]
        events_count = sum(1 for match_id in match_ids if f"data/events/{match_id}.json" in paths)
        lineups_count = sum(1 for match_id in match_ids if f"data/lineups/{match_id}.json" in paths)
        three_sixty_count = sum(
            1 for match_id in match_ids if f"data/three-sixty/{match_id}.json" in paths
        )
        target = target_match(competition)
        coverage.append(
            {
                "competition_id": competition_id,
                "season_id": season_id,
                "country": competition["country_name"],
                "competition": competition["competition_name"],
                "gender": competition["competition_gender"],
                "season": competition["season_name"],
                "match_count": len(matches),
                "events_available": events_count == len(matches),
                "lineups_available": lineups_count == len(matches),
                "360_available": three_sixty_count > 0,
                "360_match_count": three_sixty_count,
                "target_league_match": target,
                "scoutfootball_relevance": relevance(target, len(matches), competition["season_name"]),
            }
        )
    return sorted(
        coverage,
        key=lambda row: (row["country"], row["competition"], row["season"]),
    )


def relevance(target: str | None, match_count: int, season: str) -> str:
    if not target:
        return "non_target_reference"
    if season in {"2023/2024", "2024/2025", "2025/2026"}:
        return "target_recent_partial" if match_count < 300 else "target_recent_complete"
    if match_count >= 300:
        return "target_historical_complete_demo"
    return "target_historical_partial_demo"


def inspect_schema(provider: StatsBombOpenDataProvider, match_ids: list[int]) -> dict[str, Any]:
    type_counts: Counter[str] = Counter()
    fields_by_type: dict[str, set[str]] = {}
    nested_fields: dict[str, set[str]] = {}
    event_count = 0
    for match_id in match_ids:
        events = provider.read_events(match_id)
        event_count += len(events)
        for event in events:
            event_type = event.get("type", {}).get("name", "Unknown")
            type_counts[event_type] += 1
            fields_by_type.setdefault(event_type, set()).update(event.keys())
            for key, value in event.items():
                if isinstance(value, dict):
                    nested_fields.setdefault(key, set()).update(value.keys())
    return {
        "matches_inspected": match_ids,
        "event_count": event_count,
        "event_type_counts": dict(type_counts.most_common()),
        "fields_by_type": {
            event_type: sorted(fields)
            for event_type, fields in sorted(fields_by_type.items())
        },
        "nested_fields": {key: sorted(fields) for key, fields in sorted(nested_fields.items())},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--competition-id", type=int, default=2)
    parser.add_argument("--season-id", type=int, default=27)
    parser.add_argument("--sample-matches", type=int, default=3)
    args = parser.parse_args()

    provider = StatsBombOpenDataProvider()
    coverage = build_coverage(provider)
    selected_matches = provider.list_matches(args.competition_id, args.season_id)
    sample_match_ids = [int(match["match_id"]) for match in selected_matches[: args.sample_matches]]
    schema = inspect_schema(provider, sample_match_ids)
    output = {
        "coverage": coverage,
        "selected_competition": {
            "competition_id": args.competition_id,
            "season_id": args.season_id,
            "match_count": len(selected_matches),
            "sample_match_ids": sample_match_ids,
        },
        "schema": schema,
    }
    output_path = ROOT / "data_sources" / "statsbomb_open" / "investigation_summary.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(
        json.dumps(
            {
                "coverage_rows": len(coverage),
                "selected_match_count": len(selected_matches),
                "sample_match_ids": sample_match_ids,
                "event_count": schema["event_count"],
                "output_path": str(output_path),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
