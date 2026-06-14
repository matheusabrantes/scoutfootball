from __future__ import annotations

from typing import Any


STATSBOMB_MVP_COMPETITIONS: list[dict[str, Any]] = [
    {
        "internal_key": "statsbomb_premier_league_2015_2016",
        "competition_id": 2,
        "season_id": 27,
        "country": "England",
        "competition_name": "Premier League",
        "season_name": "2015/2016",
        "expected_match_count": 380,
        "actual_match_count": 380,
        "status": "active",
        "historical_demo": True,
        "notes": "P0 full historical target league season for the first StatsBomb MVP slice.",
    },
    {
        "internal_key": "statsbomb_bundesliga_2023_2024",
        "competition_id": 9,
        "season_id": 281,
        "country": "Germany",
        "competition_name": "1. Bundesliga",
        "season_name": "2023/2024",
        "expected_match_count": 306,
        "actual_match_count": 34,
        "status": "incomplete",
        "historical_demo": True,
        "notes": "P0 relevant recent sample, but only 34 matches are available in open data.",
    },
    {
        "internal_key": "statsbomb_la_liga_2015_2016",
        "competition_id": 11,
        "season_id": 27,
        "country": "Spain",
        "competition_name": "La Liga",
        "season_name": "2015/2016",
        "expected_match_count": 380,
        "actual_match_count": 380,
        "status": "not_selected",
        "historical_demo": True,
        "notes": "P1 complete historical target league, add after P0 ingestion is stable.",
    },
    {
        "internal_key": "statsbomb_serie_a_2015_2016",
        "competition_id": 12,
        "season_id": 27,
        "country": "Italy",
        "competition_name": "Serie A",
        "season_name": "2015/2016",
        "expected_match_count": 380,
        "actual_match_count": 380,
        "status": "not_selected",
        "historical_demo": True,
        "notes": "P1 complete historical target league, add after P0 ingestion is stable.",
    },
    {
        "internal_key": "statsbomb_ligue_1_2015_2016",
        "competition_id": 7,
        "season_id": 27,
        "country": "France",
        "competition_name": "Ligue 1",
        "season_name": "2015/2016",
        "expected_match_count": 380,
        "actual_match_count": 377,
        "status": "validated",
        "historical_demo": True,
        "notes": "P1 close-to-complete historical target league; three matches fewer than expected.",
    },
]


def get_statsbomb_competitions() -> list[dict[str, Any]]:
    return STATSBOMB_MVP_COMPETITIONS


def find_statsbomb_competition(competition_id: int, season_id: int) -> dict[str, Any] | None:
    return next(
        (
            competition
            for competition in STATSBOMB_MVP_COMPETITIONS
            if competition["competition_id"] == competition_id
            and competition["season_id"] == season_id
        ),
        None,
    )
