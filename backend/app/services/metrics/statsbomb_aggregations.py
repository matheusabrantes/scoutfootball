from __future__ import annotations

import math
from typing import Any


PITCH_LENGTH = 120.0
PITCH_WIDTH = 80.0
GOAL_CENTER = (120.0, 40.0)
PENALTY_AREA_X = 102.0
PENALTY_AREA_Y_MIN = 18.0
PENALTY_AREA_Y_MAX = 62.0
PROGRESSIVE_MIN_DISTANCE_GAIN = 5.0
PROGRESSIVE_MIN_DISTANCE_REDUCTION = 0.25
MINIMUM_CARRY_DISTANCE = 5.0


OUTPUT_FIELDS = [
    "player_id",
    "player_name",
    "team",
    "competition",
    "season",
    "position_group",
    "minutes",
    "appearances",
    "starts",
    "goals",
    "non_penalty_goals",
    "assists",
    "shots",
    "shots_on_target",
    "xg",
    "npxg",
    "key_passes",
    "passes_attempted",
    "passes_completed",
    "pass_completion_pct",
    "progressive_passes",
    "progressive_carries",
    "crosses",
    "accurate_crosses",
    "successful_dribbles",
    "touches_in_box",
    "interceptions",
    "blocks",
    "ball_recoveries",
    "duels",
    "duels_won",
    "aerial_duels",
    "aerial_duels_won",
    "saves",
    "goals_conceded",
    "yellow_cards",
    "red_cards",
]


def position_group(position_name: str | None) -> str | None:
    if not position_name:
        return None
    position = position_name.lower()
    if "goalkeeper" in position:
        return "Goalkeepers"
    if "center back" in position or "centre back" in position:
        return "Centrebacks"
    if "left back" in position or "right back" in position or "wing back" in position:
        return "Fullbacks"
    if "midfield" in position:
        return "Midfielders"
    if (
        "wing" in position
        or "striker" in position
        or "forward" in position
        or "center forward" in position
        or "centre forward" in position
    ):
        return "Attackers"
    return "Midfielders"


def distance_to_goal(location: list[float] | tuple[float, ...] | None) -> float | None:
    if not location or len(location) < 2:
        return None
    return math.dist((float(location[0]), float(location[1])), GOAL_CENTER)


def distance_between(
    start: list[float] | tuple[float, ...] | None,
    end: list[float] | tuple[float, ...] | None,
) -> float | None:
    if not start or not end or len(start) < 2 or len(end) < 2:
        return None
    return math.dist((float(start[0]), float(start[1])), (float(end[0]), float(end[1])))


def in_attacking_penalty_area(location: list[float] | tuple[float, ...] | None) -> bool:
    if not location or len(location) < 2:
        return False
    return (
        float(location[0]) >= PENALTY_AREA_X
        and PENALTY_AREA_Y_MIN <= float(location[1]) <= PENALTY_AREA_Y_MAX
    )


def is_progressive_action(
    start: list[float] | tuple[float, ...] | None,
    end: list[float] | tuple[float, ...] | None,
    minimum_action_distance: float = 0.0,
) -> bool:
    start_distance = distance_to_goal(start)
    end_distance = distance_to_goal(end)
    action_distance = distance_between(start, end)
    if start_distance is None or end_distance is None or action_distance is None:
        return False
    if action_distance < minimum_action_distance or end_distance >= start_distance:
        return False
    distance_gain = start_distance - end_distance
    reduction = distance_gain / start_distance if start_distance else 0.0
    return (
        distance_gain >= PROGRESSIVE_MIN_DISTANCE_GAIN
        and reduction >= PROGRESSIVE_MIN_DISTANCE_REDUCTION
    )


def event_seconds(event: dict[str, Any]) -> int:
    minute = int(event.get("minute") or 0)
    second = int(event.get("second") or 0)
    return minute * 60 + second


def match_duration_minutes(events: list[dict[str, Any]]) -> int:
    if not events:
        return 90
    duration = max(event_seconds(event) for event in events) / 60
    return int(math.ceil(duration))


def extract_starting_positions(events: list[dict[str, Any]]) -> dict[int, str]:
    positions = {}
    for event in events:
        if event.get("type", {}).get("name") != "Starting XI":
            continue
        for item in event.get("tactics", {}).get("lineup", []):
            player = item.get("player", {})
            position = item.get("position", {})
            if player.get("id") and position.get("name"):
                positions[int(player["id"])] = position["name"]
    return positions


def calculate_match_minutes(events: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    duration = match_duration_minutes(events)
    starters = extract_starting_positions(events)
    player_minutes: dict[int, dict[str, Any]] = {
        player_id: {"minutes": duration, "start": True, "position": position_name}
        for player_id, position_name in starters.items()
    }
    for event in events:
        if event.get("type", {}).get("name") != "Substitution":
            continue
        second = event_seconds(event)
        minute = min(duration, int(math.floor(second / 60)))
        leaving_player = event.get("player", {})
        replacement = event.get("substitution", {}).get("replacement", {})
        position_name = event.get("position", {}).get("name")
        if leaving_player.get("id"):
            player_id = int(leaving_player["id"])
            player_minutes.setdefault(
                player_id,
                {"minutes": duration, "start": player_id in starters, "position": position_name},
            )
            player_minutes[player_id]["minutes"] = min(
                player_minutes[player_id]["minutes"],
                minute,
            )
        if replacement.get("id"):
            player_id = int(replacement["id"])
            player_minutes[player_id] = {
                "minutes": max(duration - minute, 0),
                "start": False,
                "position": position_name,
            }
    for event in events:
        card = event.get("bad_behaviour", {}).get("card", {}).get("name") or event.get(
            "foul_committed", {}
        ).get("card", {}).get("name")
        if card != "Red Card" or not event.get("player", {}).get("id"):
            continue
        player_id = int(event["player"]["id"])
        minute = min(duration, int(math.floor(event_seconds(event) / 60)))
        player_minutes.setdefault(player_id, {"minutes": duration, "start": False, "position": None})
        player_minutes[player_id]["minutes"] = min(player_minutes[player_id]["minutes"], minute)
    return player_minutes


def aggregate_player_season(
    matches: list[dict[str, Any]],
    events_by_match: dict[int, list[dict[str, Any]]],
    competition: str,
    season: str,
) -> list[dict[str, Any]]:
    players: dict[int, dict[str, Any]] = {}
    team_by_match = {}
    for match in matches:
        team_by_match[int(match["match_id"])] = {
            match["home_team"]["home_team_id"]: match["home_team"]["home_team_name"],
            match["away_team"]["away_team_id"]: match["away_team"]["away_team_name"],
        }

    for match in matches:
        match_id = int(match["match_id"])
        events = events_by_match.get(match_id, [])
        minutes = calculate_match_minutes(events)
        for player_id, minute_info in minutes.items():
            row = players.setdefault(player_id, _empty_player_row(player_id, competition, season))
            row["minutes"] += minute_info["minutes"]
            row["appearances"] += 1 if minute_info["minutes"] > 0 else 0
            row["starts"] += 1 if minute_info["start"] else 0
            if minute_info.get("position") and not row["position_group"]:
                row["position_group"] = position_group(minute_info["position"])

        for event in events:
            player = event.get("player", {})
            if not player.get("id"):
                continue
            player_id = int(player["id"])
            row = players.setdefault(player_id, _empty_player_row(player_id, competition, season))
            row["player_name"] = player.get("name") or row["player_name"]
            team_id = event.get("team", {}).get("id")
            if team_id:
                row["team"] = team_by_match.get(match_id, {}).get(team_id, event.get("team", {}).get("name"))
            if event.get("position", {}).get("name") and not row["position_group"]:
                row["position_group"] = position_group(event["position"]["name"])
            _apply_event(row, event)

    rows = []
    for row in players.values():
        row["pass_completion_pct"] = _pct(row["passes_completed"], row["passes_attempted"])
        for field in ("xg", "npxg"):
            row[field] = round(row[field], 4)
        for unavailable in ("aerial_duels", "aerial_duels_won"):
            row[unavailable] = None
        rows.append({field: row.get(field) for field in OUTPUT_FIELDS})
    return sorted(rows, key=lambda item: (item.get("team") or "", item.get("player_name") or ""))


def _empty_player_row(player_id: int, competition: str, season: str) -> dict[str, Any]:
    row: dict[str, Any] = {field: 0 for field in OUTPUT_FIELDS}
    row.update(
        {
            "player_id": player_id,
            "player_name": None,
            "team": None,
            "competition": competition,
            "season": season,
            "position_group": None,
            "pass_completion_pct": None,
            "aerial_duels": None,
            "aerial_duels_won": None,
        }
    )
    return row


def _apply_event(row: dict[str, Any], event: dict[str, Any]) -> None:
    event_type = event.get("type", {}).get("name")
    location = event.get("location")
    if in_attacking_penalty_area(location):
        row["touches_in_box"] += 1
    if event_type == "Pass":
        pass_data = event.get("pass", {})
        outcome = pass_data.get("outcome", {}).get("name")
        row["passes_attempted"] += 1
        if outcome is None:
            row["passes_completed"] += 1
        if pass_data.get("shot_assist"):
            row["key_passes"] += 1
        if pass_data.get("goal_assist"):
            row["assists"] += 1
        if pass_data.get("cross"):
            row["crosses"] += 1
            if outcome is None:
                row["accurate_crosses"] += 1
        if outcome is None and is_progressive_action(location, pass_data.get("end_location")):
            row["progressive_passes"] += 1
    elif event_type == "Carry":
        if is_progressive_action(
            location,
            event.get("carry", {}).get("end_location"),
            minimum_action_distance=MINIMUM_CARRY_DISTANCE,
        ):
            row["progressive_carries"] += 1
    elif event_type == "Shot":
        shot = event.get("shot", {})
        row["shots"] += 1
        row["xg"] += float(shot.get("statsbomb_xg") or 0.0)
        if shot.get("type", {}).get("name") != "Penalty":
            row["npxg"] += float(shot.get("statsbomb_xg") or 0.0)
        outcome = shot.get("outcome", {}).get("name")
        if outcome in {"Goal", "Saved", "Saved to Post", "Saved Off Target", "Post"}:
            row["shots_on_target"] += 1
        if outcome == "Goal":
            row["goals"] += 1
            if shot.get("type", {}).get("name") != "Penalty":
                row["non_penalty_goals"] += 1
    elif event_type == "Dribble":
        if event.get("dribble", {}).get("outcome", {}).get("name") == "Complete":
            row["successful_dribbles"] += 1
    elif event_type == "Interception":
        row["interceptions"] += 1
        if event.get("interception", {}).get("outcome", {}).get("name") not in {
            "Lost",
            "Lost In Play",
            "Lost Out",
        }:
            row["possession_won"] = row.get("possession_won", 0) + 1
    elif event_type == "Block":
        row["blocks"] += 1
    elif event_type == "Ball Recovery":
        row["ball_recoveries"] += 1
        row["possession_won"] = row.get("possession_won", 0) + 1
    elif event_type == "Duel":
        row["duels"] += 1
        outcome = event.get("duel", {}).get("outcome", {}).get("name")
        if outcome in {"Won", "Success", "Success In Play", "Success Out"}:
            row["duels_won"] += 1
            row["possession_won"] = row.get("possession_won", 0) + 1
    elif event_type == "Goal Keeper":
        goalkeeper = event.get("goalkeeper", {})
        outcome = goalkeeper.get("outcome", {}).get("name")
        if outcome in {"Saved", "Saved Twice", "Success", "In Play Safe"}:
            row["saves"] += 1
        if goalkeeper.get("type", {}).get("name") == "Shot Faced" and outcome == "Goal Conceded":
            row["goals_conceded"] += 1

    card = event.get("bad_behaviour", {}).get("card", {}).get("name") or event.get(
        "foul_committed", {}
    ).get("card", {}).get("name")
    if card == "Yellow Card":
        row["yellow_cards"] += 1
    elif card in {"Red Card", "Second Yellow"}:
        row["red_cards"] += 1


def _pct(numerator: int | float, denominator: int | float) -> float | None:
    if not denominator:
        return None
    return round(float(numerator) / float(denominator) * 100, 2)
