from __future__ import annotations

def percentile_rank(value: float, peer_values: list[float]) -> float | None:
    if not peer_values:
        return None
    eligible_values = [peer_value for peer_value in peer_values if peer_value is not None]
    if not eligible_values:
        return None
    count_less_or_equal = sum(1 for peer_value in eligible_values if peer_value <= value)
    return round((count_less_or_equal / len(eligible_values)) * 100, 2)
