import json

from app.services.metrics.statsbomb_aggregations import (
    aggregate_player_season,
    calculate_match_minutes,
    in_attacking_penalty_area,
    is_progressive_action,
    match_duration_minutes,
    position_group,
)
from app.services.providers.statsbomb_open import StatsBombOpenDataProvider


def test_provider_reads_cached_competitions(tmp_path):
    data_dir = tmp_path / "statsbomb"
    data_dir.mkdir()
    (data_dir / "competitions.json").write_text(
        json.dumps(
            [
                {
                    "competition_id": 2,
                    "season_id": 27,
                    "competition_name": "Premier League",
                }
            ]
        ),
        encoding="utf-8",
    )

    provider = StatsBombOpenDataProvider(data_dir)

    assert provider.list_competitions()[0]["competition_name"] == "Premier League"


def test_normalize_event_exposes_nested_fields(tmp_path):
    provider = StatsBombOpenDataProvider(tmp_path)
    event = {
        "id": "abc",
        "index": 1,
        "period": 1,
        "minute": 12,
        "second": 3,
        "type": {"name": "Pass"},
        "player": {"id": 10, "name": "Player"},
        "team": {"id": 20, "name": "Team"},
        "position": {"name": "Right Wing"},
        "location": [40, 50],
        "pass": {"end_location": [80, 50]},
    }

    normalized = provider.normalize_event(event)

    assert normalized["type"] == "Pass"
    assert normalized["player_id"] == 10
    assert normalized["pass"]["end_location"] == [80, 50]


def test_position_group_mapping():
    assert position_group("Goalkeeper") == "Goalkeepers"
    assert position_group("Left Center Back") == "Centrebacks"
    assert position_group("Right Back") == "Fullbacks"
    assert position_group("Center Midfield") == "Midfielders"
    assert position_group("Left Wing") == "Attackers"


def test_progressive_action_logic():
    assert is_progressive_action([60, 40], [90, 40])
    assert not is_progressive_action([60, 40], [61, 40])
    assert not is_progressive_action([90, 40], [60, 40])


def test_attacking_penalty_area_logic():
    assert in_attacking_penalty_area([110, 40])
    assert not in_attacking_penalty_area([100, 40])
    assert not in_attacking_penalty_area([110, 70])


def test_minutes_use_absolute_statsbomb_match_minutes():
    events = [
        starting_xi_event(
            [
                (1, "Starter", "Center Forward"),
                (2, "Subbed Off", "Center Midfield"),
            ]
        ),
        {
            "type": {"name": "Substitution"},
            "minute": 60,
            "second": 0,
            "period": 2,
            "player": {"id": 2, "name": "Subbed Off"},
            "position": {"name": "Center Midfield"},
            "substitution": {"replacement": {"id": 3, "name": "Subbed On"}},
        },
        {"type": {"name": "Half End"}, "minute": 94, "second": 10, "period": 2},
    ]

    assert match_duration_minutes(events) == 95
    minutes = calculate_match_minutes(events)

    assert minutes[1]["minutes"] == 95
    assert minutes[2]["minutes"] == 60
    assert minutes[3]["minutes"] == 35
    assert minutes[3]["start"] is False


def test_aggregate_player_season_handles_null_aerial_fields():
    matches = [
        {
            "match_id": 1,
            "home_team": {"home_team_id": 10, "home_team_name": "Home"},
            "away_team": {"away_team_id": 20, "away_team_name": "Away"},
        }
    ]
    events = [
        starting_xi_event([(1, "Forward", "Center Forward")]),
        player_event("Pass", 1, "Forward", 10, "Home", [40, 40], {"end_location": [90, 40]}),
        player_event(
            "Shot",
            1,
            "Forward",
            10,
            "Home",
            [110, 40],
            {"statsbomb_xg": 0.4, "outcome": {"name": "Goal"}, "type": {"name": "Open Play"}},
        ),
        {"type": {"name": "Half End"}, "minute": 90, "second": 0, "period": 2},
    ]

    rows = aggregate_player_season(matches, {1: events}, "Premier League", "2015/2016")

    assert rows[0]["player_name"] == "Forward"
    assert rows[0]["minutes"] == 90
    assert rows[0]["goals"] == 1
    assert rows[0]["progressive_passes"] == 1
    assert rows[0]["aerial_duels"] is None


def starting_xi_event(players):
    return {
        "type": {"name": "Starting XI"},
        "minute": 0,
        "second": 0,
        "period": 1,
        "tactics": {
            "lineup": [
                {
                    "player": {"id": player_id, "name": player_name},
                    "position": {"name": position},
                }
                for player_id, player_name, position in players
            ]
        },
    }


def player_event(event_type, player_id, player_name, team_id, team_name, location, payload):
    event = {
        "type": {"name": event_type},
        "minute": 10,
        "second": 0,
        "period": 1,
        "player": {"id": player_id, "name": player_name},
        "team": {"id": team_id, "name": team_name},
        "position": {"name": "Center Forward"},
        "location": location,
    }
    event[event_type.lower().replace(" ", "_")] = payload
    return event
