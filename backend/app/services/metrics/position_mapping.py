from __future__ import annotations


STATSBOMB_POSITION_GROUPS = {
    "Goalkeeper": "Goalkeepers",
    "Left Center Back": "Centrebacks",
    "Center Back": "Centrebacks",
    "Right Center Back": "Centrebacks",
    "Left Back": "Fullbacks",
    "Right Back": "Fullbacks",
    "Left Wing Back": "Fullbacks",
    "Right Wing Back": "Fullbacks",
    "Left Defensive Midfield": "Midfielders",
    "Center Defensive Midfield": "Midfielders",
    "Right Defensive Midfield": "Midfielders",
    "Left Center Midfield": "Midfielders",
    "Center Midfield": "Midfielders",
    "Right Center Midfield": "Midfielders",
    "Left Attacking Midfield": "Midfielders",
    "Center Attacking Midfield": "Midfielders",
    "Right Attacking Midfield": "Midfielders",
    "Left Midfield": "Midfielders",
    "Right Midfield": "Midfielders",
    "Left Wing": "Attackers",
    "Right Wing": "Attackers",
    "Left Center Forward": "Attackers",
    "Center Forward": "Attackers",
    "Right Center Forward": "Attackers",
    "Secondary Striker": "Attackers",
}


def map_statsbomb_position(position_name: str | None) -> str | None:
    if not position_name:
        return None
    if position_name in STATSBOMB_POSITION_GROUPS:
        return STATSBOMB_POSITION_GROUPS[position_name]
    lowered = position_name.lower()
    if "goalkeeper" in lowered:
        return "Goalkeepers"
    if "center back" in lowered or "centre back" in lowered:
        return "Centrebacks"
    if "back" in lowered:
        return "Fullbacks"
    if "midfield" in lowered:
        return "Midfielders"
    if "wing" in lowered or "forward" in lowered or "striker" in lowered:
        return "Attackers"
    return None
