from __future__ import annotations

import json
from sqlite3 import Connection
from typing import Any

from app.repositories.leagues import find_league_by_internal_key


def normalize_position_group(position: str | None) -> str:
    if not position:
        return "unknown"
    lowered = position.lower()
    if "goalkeeper" in lowered:
        return "goalkeepers"
    if "defender" in lowered:
        return "centrebacks"
    if "midfielder" in lowered:
        return "midfielders"
    if "attacker" in lowered:
        return "attackers"
    return "unknown"


def upsert_season(connection: Connection, year: int) -> int:
    connection.execute(
        "INSERT INTO seasons (year, label) VALUES (?, ?) ON CONFLICT(year) DO NOTHING",
        (year, str(year)),
    )
    row = connection.execute("SELECT id FROM seasons WHERE year = ?", (year,)).fetchone()
    return int(row["id"])


def upsert_team(connection: Connection, team: dict[str, Any], league_id: int, season_id: int) -> int:
    connection.execute(
        """
        INSERT INTO teams (provider, provider_team_id, name, logo_url, league_id, season_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(provider, provider_team_id, league_id, season_id) DO UPDATE SET
            name=excluded.name,
            logo_url=excluded.logo_url
        """,
        ("api_football", team["id"], team["name"], team.get("logo"), league_id, season_id),
    )
    row = connection.execute(
        """
        SELECT id FROM teams
        WHERE provider = ? AND provider_team_id = ? AND league_id = ? AND season_id = ?
        """,
        ("api_football", team["id"], league_id, season_id),
    ).fetchone()
    return int(row["id"])


def upsert_player(connection: Connection, player: dict[str, Any]) -> int:
    birth = player.get("birth") or {}
    connection.execute(
        """
        INSERT INTO players (
            provider, provider_player_id, name, firstname, lastname, age, birth_date,
            birth_place, birth_country, nationality, height, weight, photo_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(provider, provider_player_id) DO UPDATE SET
            name=excluded.name,
            firstname=excluded.firstname,
            lastname=excluded.lastname,
            age=excluded.age,
            birth_date=excluded.birth_date,
            birth_place=excluded.birth_place,
            birth_country=excluded.birth_country,
            nationality=excluded.nationality,
            height=excluded.height,
            weight=excluded.weight,
            photo_url=excluded.photo_url
        """,
        (
            "api_football",
            player["id"],
            player["name"],
            player.get("firstname"),
            player.get("lastname"),
            player.get("age"),
            birth.get("date"),
            birth.get("place"),
            birth.get("country"),
            player.get("nationality"),
            player.get("height"),
            player.get("weight"),
            player.get("photo"),
        ),
    )
    row = connection.execute(
        "SELECT id FROM players WHERE provider = ? AND provider_player_id = ?",
        ("api_football", player["id"]),
    ).fetchone()
    return int(row["id"])


def upsert_player_season_stats(
    connection: Connection,
    league_internal_key: str,
    season_year: int,
    player_row: dict[str, Any],
) -> int:
    league = find_league_by_internal_key(connection, league_internal_key)
    if not league:
        raise ValueError(f"League not initialized: {league_internal_key}")
    player = player_row["player"]
    statistics = player_row["statistics"][0]
    games = statistics.get("games") or {}
    team_id = upsert_team(connection, statistics["team"], league["id"], upsert_season(connection, season_year))
    season_id = upsert_season(connection, season_year)
    player_id = upsert_player(connection, player)
    position = games.get("position")
    connection.execute(
        """
        INSERT INTO player_season_stats (
            player_id, league_id, season_id, team_id, provider, position, position_group,
            appearances, starts, minutes, rating, raw_field_metadata
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(player_id, league_id, season_id, team_id) DO UPDATE SET
            position=excluded.position,
            position_group=excluded.position_group,
            appearances=excluded.appearances,
            starts=excluded.starts,
            minutes=excluded.minutes,
            rating=excluded.rating,
            raw_field_metadata=excluded.raw_field_metadata
        """,
        (
            player_id,
            league["id"],
            season_id,
            team_id,
            "api_football",
            position,
            normalize_position_group(position),
            games.get("appearences"),
            games.get("lineups"),
            games.get("minutes"),
            _to_float(games.get("rating")),
            json.dumps(sorted(_flatten_field_paths(player_row))),
        ),
    )
    row = connection.execute(
        """
        SELECT id FROM player_season_stats
        WHERE player_id = ? AND league_id = ? AND season_id = ? AND team_id = ?
        """,
        (player_id, league["id"], season_id, team_id),
    ).fetchone()
    return int(row["id"])


def list_players(
    connection: Connection,
    league_key: str | None = None,
    season: int | None = None,
    team: str | None = None,
    position_group: str | None = None,
    nationality: str | None = None,
    minimum_minutes: int = 0,
    limit: int = 100,
    offset: int = 0,
) -> list[dict[str, Any]]:
    filters = ["COALESCE(player_season_stats.minutes, 0) >= ?"]
    params: list[Any] = [minimum_minutes]
    if league_key:
        filters.append("leagues.internal_key = ?")
        params.append(league_key)
    if season:
        filters.append("seasons.year = ?")
        params.append(season)
    if team:
        filters.append("teams.name LIKE ?")
        params.append(f"%{team}%")
    if position_group:
        filters.append("player_season_stats.position_group = ?")
        params.append(position_group)
    if nationality:
        filters.append("players.nationality = ?")
        params.append(nationality)
    params.extend([limit, offset])
    rows = connection.execute(
        f"""
        SELECT
            players.id,
            players.provider_player_id,
            players.name,
            players.age,
            players.nationality,
            teams.name AS team_name,
            leagues.internal_key AS league_key,
            leagues.display_name AS league_name,
            seasons.year AS season,
            player_season_stats.id AS player_season_stats_id,
            player_season_stats.position,
            player_season_stats.position_group,
            player_season_stats.appearances,
            player_season_stats.starts,
            player_season_stats.minutes,
            player_season_stats.rating
        FROM player_season_stats
        JOIN players ON players.id = player_season_stats.player_id
        JOIN teams ON teams.id = player_season_stats.team_id
        JOIN leagues ON leagues.id = player_season_stats.league_id
        JOIN seasons ON seasons.id = player_season_stats.season_id
        WHERE {" AND ".join(filters)}
        ORDER BY player_season_stats.minutes DESC, players.name
        LIMIT ? OFFSET ?
        """,
        params,
    ).fetchall()
    return [dict(row) for row in rows]


def get_player_profile(connection: Connection, player_id: int) -> dict[str, Any] | None:
    players = list_players(connection, limit=5000)
    profile = next((player for player in players if player["id"] == player_id), None)
    if not profile:
        return None
    metrics = connection.execute(
        """
        SELECT metric_key, metric_value, percentile, peer_count
        FROM player_metric_values
        WHERE player_season_stats_id = ?
        ORDER BY metric_key
        """,
        (profile["player_season_stats_id"],),
    ).fetchall()
    profile["metrics"] = [dict(row) for row in metrics]
    return profile


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _flatten_field_paths(value: Any, prefix: str = "") -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            paths.add(child_prefix)
            paths.update(_flatten_field_paths(child, child_prefix))
    elif isinstance(value, list) and value:
        paths.update(_flatten_field_paths(value[0], prefix))
    return paths

