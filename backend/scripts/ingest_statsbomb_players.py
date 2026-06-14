from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config.statsbomb_competitions import find_statsbomb_competition  # noqa: E402
from app.db.connection import database_path, get_connection  # noqa: E402
from app.db.schema import initialize_schema  # noqa: E402
from app.services.ingestion.statsbomb_players import ingest_statsbomb_player_rows  # noqa: E402
from app.services.metrics.statsbomb_aggregations import aggregate_player_season  # noqa: E402
from app.services.metrics.statsbomb_aggregations import season_quality_summary  # noqa: E402
from app.services.providers.statsbomb_open import StatsBombOpenDataProvider  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest StatsBomb Open Data player seasons.")
    parser.add_argument("--competition-id", type=int, required=True)
    parser.add_argument("--season-id", type=int, required=True)
    parser.add_argument("--limit-matches", type=int)
    parser.add_argument("--full", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = find_statsbomb_competition(args.competition_id, args.season_id)
    if not config:
        raise SystemExit(f"StatsBomb competition is not configured: {args.competition_id}/{args.season_id}")
    if not args.full and args.limit_matches is None:
        args.limit_matches = 5

    started = time.perf_counter()
    provider = StatsBombOpenDataProvider()
    matches = provider.list_matches(args.competition_id, args.season_id)
    selected_matches = matches if args.full else matches[: args.limit_matches]
    events_by_match = {
        int(match["match_id"]): provider.read_events(int(match["match_id"]))
        for match in selected_matches
    }
    rows = aggregate_player_season(
        selected_matches,
        events_by_match,
        config["competition_name"],
        config["season_name"],
    )
    diagnostics = season_quality_summary(selected_matches, events_by_match, rows)
    quality_summary = {
        "competition": config["competition_name"],
        "season": config["season_name"],
        "matches_expected": config["expected_match_count"],
        "matches_processed": len(selected_matches),
        "events_processed": sum(len(events) for events in events_by_match.values()),
        "players_aggregated": len(rows),
        "players_with_minutes": sum(1 for row in rows if row["minutes"] and row["minutes"] > 0),
        "players_with_positions": sum(1 for row in rows if row["position_group"]),
        "players_above_900_minutes": sum(1 for row in rows if row["minutes"] and row["minutes"] >= 900),
        "minute_quality": "estimated",
        "minute_reconciliation": diagnostics,
        "minutes_quality_counts": diagnostics["minutes_quality_counts"],
        "metric_definition_version": "statsbomb_open_v1",
        "historical_demo": True,
        "processing_time_seconds": round(time.perf_counter() - started, 3),
    }
    with get_connection() as connection:
        initialize_schema(connection)
        result = ingest_statsbomb_player_rows(
            connection,
            args.competition_id,
            args.season_id,
            rows,
            quality_summary,
        )
    output = {
        **quality_summary,
        "database": str(database_path()),
        "ingestion": result,
    }
    output_path = ROOT / "data_sources" / "statsbomb_open" / "outputs" / "ingestion_summary.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
