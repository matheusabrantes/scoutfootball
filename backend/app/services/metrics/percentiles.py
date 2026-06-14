from __future__ import annotations

from sqlite3 import Connection


def percentile_rank(value: float, peer_values: list[float]) -> float | None:
    if not peer_values:
        return None
    eligible_values = [peer_value for peer_value in peer_values if peer_value is not None]
    if not eligible_values:
        return None
    count_less_or_equal = sum(1 for peer_value in eligible_values if peer_value <= value)
    return round((count_less_or_equal / len(eligible_values)) * 100, 2)


def calculate_percentiles(
    connection: Connection,
    minimum_minutes: int = 500,
    minimum_peer_count: int = 5,
) -> dict[str, int]:
    connection.execute(
        """
        UPDATE player_metric_values
        SET percentile = NULL, peer_count = NULL, population_size = NULL, minutes_threshold = NULL
        """
    )
    rows = connection.execute(
        """
        SELECT
            player_metric_values.id,
            player_metric_values.metric_key,
            player_metric_values.metric_value,
            player_season_stats.league_id,
            player_season_stats.season_id,
            player_season_stats.position_group
        FROM player_metric_values
        JOIN player_season_stats ON player_season_stats.id = player_metric_values.player_season_stats_id
        WHERE
            player_metric_values.metric_value IS NOT NULL
            AND COALESCE(player_season_stats.minutes, 0) >= ?
            AND player_season_stats.position_group != 'unknown'
        """,
        (minimum_minutes,),
    ).fetchall()
    grouped_values: dict[tuple[int, int, str, str], list[float]] = {}
    for row in rows:
        key = (row["league_id"], row["season_id"], row["position_group"], row["metric_key"])
        grouped_values.setdefault(key, []).append(float(row["metric_value"]))

    updated = 0
    skipped = 0
    for row in rows:
        key = (row["league_id"], row["season_id"], row["position_group"], row["metric_key"])
        peer_values = grouped_values[key]
        if len(peer_values) < minimum_peer_count:
            skipped += 1
            continue
        percentile = percentile_rank(float(row["metric_value"]), peer_values)
        connection.execute(
            """
            UPDATE player_metric_values
            SET percentile = ?, peer_count = ?, population_size = ?, minutes_threshold = ?,
                calculation_version = ?
            WHERE id = ?
            """,
            (
                percentile,
                len(peer_values),
                len(peer_values),
                minimum_minutes,
                f"mvp_v1_min_{minimum_minutes}",
                row["id"],
            ),
        )
        updated += 1
    connection.commit()
    return {"updated": updated, "skipped": skipped}
