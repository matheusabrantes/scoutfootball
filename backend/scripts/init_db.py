from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.db.connection import database_path, get_connection  # noqa: E402
from app.db.schema import initialize_schema  # noqa: E402
from app.repositories.leagues import upsert_configured_leagues  # noqa: E402


def main() -> int:
    with get_connection() as connection:
        initialize_schema(connection)
        upsert_configured_leagues(connection)
    print(f"Initialized SQLite database at {database_path()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
