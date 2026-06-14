from __future__ import annotations

import sqlite3
from pathlib import Path

from app.core.config import get_settings


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def database_path() -> Path:
    database_url = get_settings().database_url
    if database_url:
        sqlite_prefix = "sqlite:///"
        if database_url.startswith(sqlite_prefix):
            path = Path(database_url.removeprefix(sqlite_prefix))
        else:
            path = Path(database_url)
        if path.is_absolute():
            return path
        return project_root() / path
    configured_path = Path(get_settings().scoutfootball_db_path)
    if configured_path.is_absolute():
        return configured_path
    return project_root() / configured_path


def get_connection() -> sqlite3.Connection:
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
