from __future__ import annotations

import math
from typing import Any

from app.services.metrics.position_mapping import map_statsbomb_position


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
    "provider_team_id",
    "team",
    "competition",
    "season",
    "position_group",
    "minutes_quality",
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
    "forward_passes_attempted",
    "forward_passes_completed",
    "forward_pass_completion_pct",
    "progressive_passes",
    "progressive_carries",
    "crosses",
    "accurate_crosses",
    "dribbles_attempted",
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
    "shots_on_target_faced",
    "save_percentage",
    "goals_conceded",
    "long_passes_attempted",
    "long_passes_completed",
    "long_pass_accuracy",
    "short_passes_attempted",
    "short_passes_completed",
    "short_pass_completion",
    "exits",
    "yellow_cards",
    "red_cards",
]


def position_group(position_name: str | None) -> str | None:
    return map_statsbomb_position(position_name)


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
        player_id: {
            "minutes": duration,
            "start": True,
            "position": position_name,
            "quality": "estimated",
        }
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
                {
                    "minutes": duration,
                    "start": player_id in starters,
                    "position": position_name,
                    "quality": "estimated" if player_id in starters else "incomplete",
                },
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
                "quality": "estimated",
            }
    for event in events:
        card = event.get("bad_behaviour", {}).get("card", {}).get("name") or event.get(
            "foul_committed", {}
        ).get("card", {}).get("name")
        if card != "Red Card" or not event.get("player", {}).get("id"):
            continue
        player_id = int(event["player"]["id"])
        minute = min(duration, int(math.floor(event_seconds(event) / 60)))
        player_minutes.setdefault(
            player_id,
            {"minutes": duration, "start": False, "position": None, "quality": "incomplete"},
        )
        player_minutes[player_id]["minutes"] = min(player_minutes[player_id]["minutes"], minute)
    for player_id, item in player_minutes.items():
        if item["minutes"] < 0 or item["minutes"] > duration:
            item["minutes"] = max(0, min(item["minutes"], duration))
            item["quality"] = "invalid"
        elif not item.get("position"):
            item["quality"] = "incomplete"
    return player_minutes


def season_quality_summary(
    matches: list[dict[str, Any]],
    events_by_match: dict[int, list[dict[str, Any]]],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    diagnostics = {
        "expected_team_player_minutes": 0,
        "calculated_team_player_minutes": 0,
        "absolute_difference": 0,
        "relative_difference": 0.0,
        "players_with_negative_minutes": 0,
        "players_above_match_duration": 0,
        "players_with_events_but_zero_minutes": 0,
        "players_with_minutes_but_no_position": 0,
        "duplicate_player_match_rows": 0,
        "duplicate_player_team_season_rows": len(rows)
        - len({(row.get("player_id"), row.get("provider_team_id")) for row in rows}),
        "minutes_quality_counts": {"reliable": 0, "estimated": 0, "incomplete": 0, "invalid": 0},
    }
    event_player_ids = set()
    for match in matches:
        events = events_by_match.get(int(match["match_id"]), [])
        duration = match_duration_minutes(events)
        diagnostics["expected_team_player_minutes"] += duration * 22
        minute_rows = calculate_match_minutes(events)
        diagnostics["calculated_team_player_minutes"] += sum(item["minutes"] for item in minute_rows.values())
        diagnostics["duplicate_player_match_rows"] += len(minute_rows) - len(set(minute_rows))
        for event in events:
            if event.get("player", {}).get("id"):
                event_player_ids.add(int(event["player"]["id"]))
        for item in minute_rows.values():
            if item["minutes"] < 0:
                diagnostics["players_with_negative_minutes"] += 1
            if item["minutes"] > duration:
                diagnostics["players_above_match_duration"] += 1
    row_by_player = {int(row["player_id"]): row for row in rows if row.get("player_id")}
    for player_id in event_player_ids:
        if row_by_player.get(player_id, {}).get("minutes", 0) == 0:
            diagnostics["players_with_events_but_zero_minutes"] += 1
    for row in rows:
        if row.get("minutes", 0) > 0 and not row.get("position_group"):
            diagnostics["players_with_minutes_but_no_position"] += 1
        quality = row.get("minutes_quality") or "incomplete"
        diagnostics["minutes_quality_counts"][quality] = diagnostics["minutes_quality_counts"].get(quality, 0) + 1
    diagnostics["absolute_difference"] = abs(
        diagnostics["expected_team_player_minutes"] - diagnostics["calculated_team_player_minutes"]
    )
    if diagnostics["expected_team_player_minutes"]:
        diagnostics["relative_difference"] = round(
            diagnostics["absolute_difference"] / diagnostics["expected_team_player_minutes"],
            4,
        )
    return diagnostics


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
            sanitized_minutes = max(0, min(minute_info["minutes"], match_duration_minutes(events)))
            row["minutes"] += sanitized_minutes
            row["appearances"] += 1 if minute_info["minutes"] > 0 else 0
            row["starts"] += 1 if minute_info["start"] else 0
            minute_quality = minute_info.get("quality", "estimated")
            if row["minutes_quality"] in {None, "incomplete"} or minute_quality == "invalid":
                row["minutes_quality"] = minute_quality
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
                row["provider_team_id"] = team_id
                row["team"] = team_by_match.get(match_id, {}).get(team_id, event.get("team", {}).get("name"))
            if event.get("position", {}).get("name") and not row["position_group"]:
                row["position_group"] = position_group(event["position"]["name"])
            _apply_event(row, event)

    rows = []
    for row in players.values():
        row["pass_completion_pct"] = _pct(row["passes_completed"], row["passes_attempted"])
        row["forward_pass_completion_pct"] = _pct(
            row["forward_passes_completed"],
            row["forward_passes_attempted"],
        )
        row["save_percentage"] = _pct(row["saves"], row["shots_on_target_faced"])
        row["long_pass_accuracy"] = _pct(row["long_passes_completed"], row["long_passes_attempted"])
        row["short_pass_completion"] = _pct(
            row["short_passes_completed"],
            row["short_passes_attempted"],
        )
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
            "provider_team_id": None,
            "team": None,
            "competition": competition,
            "season": season,
            "position_group": None,
            "minutes_quality": "incomplete",
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
        pass_length = float(pass_data.get("length") or 0.0)
        row["passes_attempted"] += 1
        if outcome is None:
            row["passes_completed"] += 1
        if pass_data.get("end_location") and location:
            if float(pass_data["end_location"][0]) > float(location[0]):
                row["forward_passes_attempted"] += 1
                if outcome is None:
                    row["forward_passes_completed"] += 1
        if pass_length >= 30.0:
            row["long_passes_attempted"] += 1
            if outcome is None:
                row["long_passes_completed"] += 1
        elif pass_length > 0:
            row["short_passes_attempted"] += 1
            if outcome is None:
                row["short_passes_completed"] += 1
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
        row["dribbles_attempted"] += 1
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
        goalkeeper_type = goalkeeper.get("type", {}).get("name")
        if goalkeeper_type in {"Shot Faced", "Save"}:
            row["shots_on_target_faced"] += 1
        if outcome in {"Saved", "Saved Twice", "Success", "In Play Safe"}:
            row["saves"] += 1
        if goalkeeper_type == "Shot Faced" and outcome == "Goal Conceded":
            row["goals_conceded"] += 1
        if goalkeeper_type in {"Collected", "Keeper Sweeper", "Punch"}:
            row["exits"] += 1

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
