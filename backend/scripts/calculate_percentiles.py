from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.db.connection import database_path, get_connection  # noqa: E402
from app.services.metrics.percentiles import calculate_percentiles  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate ScoutFootball MVP percentiles.")
    parser.add_argument("--minimum-minutes", type=int, default=900)
    parser.add_argument("--minimum-peer-count", type=int, default=5)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    with get_connection() as connection:
        result = calculate_percentiles(
            connection,
            minimum_minutes=args.minimum_minutes,
            minimum_peer_count=args.minimum_peer_count,
        )
    print(f"Database: {database_path()}")
    print(f"Percentiles updated: {result['updated']}")
    print(f"Metrics skipped: {result['skipped']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
