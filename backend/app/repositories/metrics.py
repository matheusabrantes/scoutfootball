from __future__ import annotations

from sqlite3 import Connection
from typing import Any


MVP_METRIC_FIELDS = {
    "minutes": ("games", "minutes"),
    "appearances": ("games", "appearences"),
    "starts": ("games", "lineups"),
    "rating": ("games", "rating"),
    "goals": ("goals", "total"),
    "assists": ("goals", "assists"),
    "shots": ("shots", "total"),
    "shots_on_target": ("shots", "on"),
    "passes": ("passes", "total"),
    "key_passes": ("passes", "key"),
    "pass_accuracy": ("passes", "accuracy"),
    "dribbles_attempted": ("dribbles", "attempts"),
    "successful_dribbles": ("dribbles", "success"),
    "duels": ("duels", "total"),
    "duels_won": ("duels", "won"),
    "tackles": ("tackles", "total"),
    "blocks": ("tackles", "blocks"),
    "interceptions": ("tackles", "interceptions"),
    "saves": ("goals", "saves"),
    "goals_conceded": ("goals", "conceded"),
    "yellow_cards": ("cards", "yellow"),
    "red_cards": ("cards", "red"),
    "penalties_scored": ("penalty", "scored"),
    "penalties_missed": ("penalty", "missed"),
}


def extract_metric_values(statistics: dict[str, Any]) -> dict[str, float | None]:
    values = {}
    for metric_key, path in MVP_METRIC_FIELDS.items():
        values[metric_key] = _to_float(_nested_get(statistics, path))
    return values


def upsert_metric_values(
    connection: Connection,
    player_season_stats_id: int,
    metric_values: dict[str, float | None],
) -> None:
    for metric_key, metric_value in metric_values.items():
        connection.execute(
            """
            INSERT INTO player_metric_values (player_season_stats_id, metric_key, metric_value)
            VALUES (?, ?, ?)
            ON CONFLICT(player_season_stats_id, metric_key) DO UPDATE SET
                metric_value=excluded.metric_value,
                percentile=NULL,
                peer_count=NULL
            """,
            (player_season_stats_id, metric_key, metric_value),
        )


def list_metrics(connection: Connection) -> list[dict[str, Any]]:
    rows = connection.execute(
        """
        SELECT
            metric_key,
            COUNT(*) AS row_count,
            COUNT(metric_value) AS value_count
        FROM player_metric_values
        GROUP BY metric_key
        ORDER BY metric_key
        """
    ).fetchall()
    return [dict(row) for row in rows]


def _nested_get(value: dict[str, Any], path: tuple[str, str]) -> Any:
    parent = value.get(path[0]) or {}
    return parent.get(path[1])


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

