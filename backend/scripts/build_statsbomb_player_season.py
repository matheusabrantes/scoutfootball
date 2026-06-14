from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.services.metrics.statsbomb_aggregations import (  # noqa: E402
    OUTPUT_FIELDS,
    aggregate_player_season,
)
from app.services.providers.statsbomb_open import StatsBombOpenDataProvider  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--competition-id", type=int, default=2)
    parser.add_argument("--season-id", type=int, default=27)
    parser.add_argument("--limit-matches", type=int, default=3)
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()

    started = time.perf_counter()
    provider = StatsBombOpenDataProvider()
    competitions = provider.list_competitions()
    competition = next(
        item
        for item in competitions
        if item["competition_id"] == args.competition_id and item["season_id"] == args.season_id
    )
    all_matches = provider.list_matches(args.competition_id, args.season_id)
    selected_matches = all_matches if args.full else all_matches[: args.limit_matches]
    events_by_match = {
        int(match["match_id"]): provider.read_events(int(match["match_id"]))
        for match in selected_matches
    }
    rows = aggregate_player_season(
        selected_matches,
        events_by_match,
        competition["competition_name"],
        competition["season_name"],
    )
    output_dir = ROOT / "data_sources" / "statsbomb_open" / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "player_season_sample.json"
    csv_path = output_dir / "player_season_sample.csv"
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    event_count = sum(len(events) for events in events_by_match.values())
    players_with_minutes = sum(1 for row in rows if row["minutes"])
    players_with_positions = sum(1 for row in rows if row["position_group"])
    missing_rates = {
        field: round(
            sum(1 for row in rows if row.get(field) is None) / len(rows) * 100,
            2,
        )
        for field in OUTPUT_FIELDS
        if rows
    }
    summary = {
        "competition": competition["competition_name"],
        "season": competition["season_name"],
        "competition_id": args.competition_id,
        "season_id": args.season_id,
        "total_competition_matches": len(all_matches),
        "matches_processed": len(selected_matches),
        "match_ids": [int(match["match_id"]) for match in selected_matches],
        "players_found": len(rows),
        "teams_found": len({row["team"] for row in rows if row["team"]}),
        "event_count": event_count,
        "players_with_minutes": players_with_minutes,
        "players_with_valid_positions": players_with_positions,
        "duplicate_player_season_rows": len(rows) - len({row["player_id"] for row in rows}),
        "missing_value_rates_pct": missing_rates,
        "unsupported_metrics": [
            "expected_assists",
            "post_shot_xg",
            "psxg_minus_goals_allowed",
            "long_pass_accuracy",
            "short_pass_completion",
            "aerial_duels",
            "aerial_duels_won",
        ],
        "processing_time_seconds": round(time.perf_counter() - started, 3),
        "output_json": str(json_path),
        "output_csv": str(csv_path),
    }
    summary_path = output_dir / "player_season_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
