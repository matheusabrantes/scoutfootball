from app.services.metrics.percentiles import percentile_rank


def test_percentile_rank_handles_ordered_values() -> None:
    assert percentile_rank(20, [10, 20, 30, 40]) == 50.0


def test_percentile_rank_returns_none_without_peers() -> None:
    assert percentile_rank(20, []) is None

