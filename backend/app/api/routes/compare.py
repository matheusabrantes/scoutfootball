from fastapi import APIRouter, Query

from app.db.connection import get_connection
from app.db.schema import initialize_schema

router = APIRouter(prefix="/api/compare", tags=["compare"])


@router.get("")
def compare(player_ids: str = Query(default="")) -> dict:
    ids = [int(value) for value in player_ids.split(",") if value.strip().isdigit()]
    if not 2 <= len(ids) <= 5:
        return {
            "mock": False,
            "players": [],
            "message": "Provide 2 to 5 player ids with ?player_ids=1,2.",
        }
    placeholders = ",".join("?" for _ in ids)
    with get_connection() as connection:
        initialize_schema(connection)
        rows = connection.execute(
            f"""
            SELECT
                players.id,
                players.name,
                teams.name AS team_name,
                leagues.display_name AS league_name,
                seasons.year AS season,
                player_season_stats.position_group,
                player_metric_values.metric_key,
                player_metric_values.metric_value,
                player_metric_values.percentile
            FROM players
            JOIN player_season_stats ON player_season_stats.player_id = players.id
            JOIN teams ON teams.id = player_season_stats.team_id
            JOIN leagues ON leagues.id = player_season_stats.league_id
            JOIN seasons ON seasons.id = player_season_stats.season_id
            LEFT JOIN player_metric_values ON player_metric_values.player_season_stats_id = player_season_stats.id
            WHERE players.id IN ({placeholders})
            ORDER BY players.name, player_metric_values.metric_key
            """,
            ids,
        ).fetchall()
    if not rows:
        return {"mock": False, "players": [], "message": "Real data has not been ingested yet."}
    players: dict[int, dict] = {}
    for row in rows:
        item = dict(row)
        player = players.setdefault(
            item["id"],
            {
                "id": item["id"],
                "name": item["name"],
                "team_name": item["team_name"],
                "league_name": item["league_name"],
                "season": item["season"],
                "position_group": item["position_group"],
                "metrics": {},
            },
        )
        if item["metric_key"]:
            player["metrics"][item["metric_key"]] = {
                "value": item["metric_value"],
                "percentile": item["percentile"],
            }
    return {"data_source": "sqlite", "mock": False, "players": list(players.values())}
