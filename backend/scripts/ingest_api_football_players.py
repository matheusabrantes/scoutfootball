from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from app.core.config import get_settings  # noqa: E402
from app.db.connection import database_path, get_connection  # noqa: E402
from app.db.schema import initialize_schema  # noqa: E402
from app.repositories.leagues import upsert_configured_leagues  # noqa: E402
from app.services.ingestion.api_football_players import (  # noqa: E402
    active_api_football_leagues,
    ingest_league_players,
)
from app.services.providers.api_football import ApiFootballClient  # noqa: E402


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest API-Football player statistics.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--full", action="store_true", help="Follow all provider pages.")
    mode.add_argument(
        "--limit-pages",
        type=int,
        default=1,
        help="Limit pages per league. Defaults to 1 for safe MVP ingestion.",
    )
    parser.add_argument(
        "--league",
        action="append",
        help="Optional internal league key. Can be provided multiple times.",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv_if_present()
    args = parse_args()
    if not get_settings().api_football_key:
        print("API_FOOTBALL_KEY is not configured.")
        return 1
    limit_pages = None if args.full else args.limit_pages
    selected_leagues = active_api_football_leagues()
    if args.league:
        selected = set(args.league)
        selected_leagues = [
            league for league in selected_leagues if league["internal_league_key"] in selected
        ]
    if not selected_leagues:
        print("No active API-Football leagues configured for ingestion.")
        return 1
    with get_connection() as connection:
        initialize_schema(connection)
        upsert_configured_leagues(connection)
        client = ApiFootballClient(get_settings())
        results = [
            ingest_league_players(connection, client, league, limit_pages)
            for league in selected_leagues
        ]
    print(f"Database: {database_path()}")
    for result in results:
        print(
            "{league} {season}: {status}, players={players_ingested}, requests={requests_used}".format(
                **result
            )
        )
    if any(result["status"] == "failed" for result in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

