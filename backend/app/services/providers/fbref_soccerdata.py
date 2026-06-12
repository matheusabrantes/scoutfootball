from __future__ import annotations

from importlib.util import find_spec
from typing import Any


FBREF_TABLES = [
    "standard",
    "shooting",
    "passing",
    "passing_types",
    "goal_shot_creation",
    "defense",
    "possession",
    "playing_time",
    "misc",
    "keeper",
    "keeper_adv",
]


def soccerdata_available() -> bool:
    return find_spec("soccerdata") is not None


def soccerdata_install_hint() -> str:
    return 'cd backend && . .venv/bin/activate && python -m pip install -e ".[providers]"'


def dataframe_metadata(dataframe: Any) -> dict[str, Any]:
    columns = []
    for column in getattr(dataframe, "columns", []):
        if isinstance(column, tuple):
            columns.append(".".join(str(part) for part in column if str(part)))
        else:
            columns.append(str(column))
    sample_players: list[str] = []
    try:
        if "player" in dataframe.columns:
            sample_players = [str(value) for value in dataframe["player"].head(5).tolist()]
        elif "Player" in dataframe.columns:
            sample_players = [str(value) for value in dataframe["Player"].head(5).tolist()]
    except Exception:
        sample_players = []
    return {
        "rows": int(len(dataframe)),
        "columns": columns,
        "sample_player_names": sample_players,
    }
