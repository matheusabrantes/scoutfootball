# StatsBomb MVP Data Quality

Report date: 2026-06-14

This report reflects the current local ScoutFootball historical real-data MVP after full Premier League 2015/2016 ingestion and the available Bundesliga 2023/2024 open-data sample ingestion.

## Dataset Summary

| Field | Premier League 2015/2016 | Bundesliga 2023/2024 |
| --- | ---: | ---: |
| competition_id | 2 | 9 |
| season_id | 27 | 281 |
| expected/open matches | 380 | 34 open-data matches |
| matches_processed | 380 | 34 |
| events_processed | 1,313,773 | 137,765 |
| teams | 20 | 18 |
| player rows found before ingestion | 550 | 373 |
| player-season rows ingested | 549 | 372 |
| skipped rows | 1 | 1 |
| players_with_minutes | 550 | 373 |
| players_with_positions | 550 | 373 |
| players_above_900_minutes | 330 | 17 |
| duplicate_player_season_rows | 0 | 0 |
| aggregation_time_seconds | 34.626 | 2.543 |

Bundesliga 2023/2024 is not full-league coverage. StatsBomb Open Data currently exposes 34 matches locally for this competition/season, so the UI and docs must label it as incomplete historical coverage.

## Combined SQLite Snapshot

After both ingestions and recalculating 900-minute percentiles:

- Players: 914.
- Player-season rows: 921.
- Teams: 38.
- Metric rows: 77,364.
- Metric rows with percentile values: 25,227.
- Percentile groups are league, season, position group, metric, and minimum-minute threshold.

Players above 900 minutes by position group:

| Position group | Count |
| --- | ---: |
| Attackers | 85 |
| Centrebacks | 61 |
| Fullbacks | 59 |
| Goalkeepers | 28 |
| Midfielders | 114 |

## Minute Reconciliation

| Field | Premier League 2015/2016 | Bundesliga 2023/2024 |
| --- | ---: | ---: |
| expected_team_player_minutes | 794,508 | 71,214 |
| calculated_team_player_minutes | 793,603 | 71,076 |
| absolute_difference | 905 | 138 |
| relative_difference | 0.0011 | 0.0019 |
| players_with_negative_minutes | 0 | 0 |
| players_above_match_duration | 0 | 0 |
| players_with_events_but_zero_minutes | 0 | 0 |
| players_with_minutes_but_no_position | 0 | 0 |
| duplicate_player_match_rows | 0 | 0 |

Minute quality counts:

| Quality | Premier League 2015/2016 | Bundesliga 2023/2024 |
| --- | ---: | ---: |
| reliable | 0 | 0 |
| estimated | 550 | 373 |
| incomplete | 0 | 0 |
| invalid | 0 | 0 |

Current interpretation: event-derived minutes are usable for the historical MVP, but remain `estimated` until official minutes or a stronger team-minute reconciliation rule is added.

## Metric Missingness

- Count metrics are stored as `0` when no qualifying event occurred.
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

Premier League 2015/2016 is suitable for historical demo rankings at the 900-minute threshold.

Bundesliga 2023/2024 should be treated as an incomplete recent historical sample. It can validate multi-competition UI behavior, but it should not be presented as complete Bundesliga rankings.
