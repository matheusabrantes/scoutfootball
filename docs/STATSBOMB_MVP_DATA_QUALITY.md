# StatsBomb MVP Data Quality

Report date: 2026-06-14

This report reflects the current local development slice, not the full Premier League 2015/2016 season.

| Field | Value |
| --- | --- |
| competition | Premier League |
| season | 2015/2016 |
| competition_id | 2 |
| season_id | 27 |
| matches_expected | 380 |
| matches_processed | 5 |
| events_processed | 18,245 |
| teams | 6 |
| players | 89 |
| players_with_minutes | 89 |
| players_with_positions | 89 |
| players_above_900_minutes | 0 |
| minute_reconciliation_error | Not fully reconciled yet |
| duplicate_rows | 0 |
| processing_time | 0.163 seconds for aggregation/ingestion after files were cached |
| disk_usage | 22.37 MB in ignored `backend/data_sources/statsbomb_open/` |

## Metric Missingness

- Most count metrics are stored as `0` when no event occurred.
- Percentage metrics are null when the denominator is zero.
- `aerial_duels` and `aerial_duels_won` remain null because a complete aerial-duel denominator has not been validated.
- `direct_xa`, `psxg`, `psxg_minus_goals_allowed`, and possession-adjusted placeholders are intentionally null.

## Unsupported Metrics

- `direct_xa`
- `psxg`
- `psxg_minus_goals_allowed`
- `interceptions_padj`
- `tackles_padj`
- `possession_won_padj`

## Ranking Readiness

The 5-match slice is suitable for endpoint validation, UI wiring, and ingestion tests.

It is not sufficient for public player rankings. Full Premier League 2015/2016 ingestion should be run before enabling serious rankings, with a default minimum-minutes threshold of 900.
