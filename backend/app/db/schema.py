from __future__ import annotations

from sqlite3 import Connection


SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS leagues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        internal_key TEXT NOT NULL UNIQUE,
        provider TEXT NOT NULL,
        provider_league_id INTEGER NOT NULL,
        display_name TEXT NOT NULL,
        country TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL,
        active_season INTEGER,
        last_validated_season INTEGER,
        validation_notes TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS seasons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL UNIQUE,
        label TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider TEXT NOT NULL,
        provider_team_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        logo_url TEXT,
        league_id INTEGER NOT NULL,
        season_id INTEGER NOT NULL,
        UNIQUE(provider, provider_team_id, league_id, season_id),
        FOREIGN KEY (league_id) REFERENCES leagues(id),
        FOREIGN KEY (season_id) REFERENCES seasons(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider TEXT NOT NULL,
        provider_player_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        firstname TEXT,
        lastname TEXT,
        age INTEGER,
        birth_date TEXT,
        birth_place TEXT,
        birth_country TEXT,
        nationality TEXT,
        height TEXT,
        weight TEXT,
        photo_url TEXT,
        UNIQUE(provider, provider_player_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS player_season_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL,
        league_id INTEGER NOT NULL,
        season_id INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        provider TEXT NOT NULL,
        position TEXT,
        position_group TEXT,
        appearances INTEGER,
        starts INTEGER,
        minutes INTEGER,
        rating REAL,
        raw_field_metadata TEXT,
        UNIQUE(player_id, league_id, season_id, team_id),
        FOREIGN KEY (player_id) REFERENCES players(id),
        FOREIGN KEY (league_id) REFERENCES leagues(id),
        FOREIGN KEY (season_id) REFERENCES seasons(id),
        FOREIGN KEY (team_id) REFERENCES teams(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS player_metric_values (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_season_stats_id INTEGER NOT NULL,
        metric_key TEXT NOT NULL,
        metric_value REAL,
        percentile REAL,
        peer_count INTEGER,
        calculation_version TEXT NOT NULL DEFAULT 'mvp_v1',
        UNIQUE(player_season_stats_id, metric_key),
        FOREIGN KEY (player_season_stats_id) REFERENCES player_season_stats(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ingestion_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider TEXT NOT NULL,
        league_internal_key TEXT,
        league_id INTEGER,
        season INTEGER,
        started_at TEXT NOT NULL,
        finished_at TEXT,
        status TEXT NOT NULL,
        requests_used INTEGER NOT NULL DEFAULT 0,
        players_ingested INTEGER NOT NULL DEFAULT 0,
        error_message TEXT
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_player_stats_league_season ON player_season_stats(league_id, season_id)",
    "CREATE INDEX IF NOT EXISTS idx_metric_key_value ON player_metric_values(metric_key, metric_value)",
]


def initialize_schema(connection: Connection) -> None:
    for statement in SCHEMA_STATEMENTS:
        connection.execute(statement)
    connection.commit()

