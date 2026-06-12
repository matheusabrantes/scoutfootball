# ScoutFootball Metrics Specification

## Principles

- Metrics must be reproducible from stored source data.
- Every metric value must store source, season, league, club, player, position group, calculation version, and ingestion run.
- Unsupported metrics must be explicitly marked unavailable.
- Approximated metrics must be labeled and explained in methodology.
- Percentiles must compare players only within a meaningful peer group.

## Position Groups

| Key | Label | Notes |
| --- | --- | --- |
| `goalkeepers` | Goalkeepers | Keeper-specific shot-stopping and distribution metrics |
| `centrebacks` | Centrebacks | Central defenders |
| `fullbacks` | Fullbacks | Fullbacks and wingbacks |
| `midfielders` | Midfielders | Defensive, central, and attacking midfielders |
| `attackers` | Attackers | Wingers and strikers combined |

## Metric Data Contract

Each player metric row should contain:

- `player_id`
- `season_id`
- `league_id`
- `club_id`
- `position_group`
- `metric_key`
- `metric_value`
- `per_90_value` when applicable
- `percentile`
- `availability_status`: `available`, `approximated`, or `unavailable`
- `source_metric_keys`
- `data_source_id`
- `calculation_version`
- `last_updated_at`

## Position Metric Templates

### Goalkeepers

| Metric Key | Label | Calculation / Source Requirement |
| --- | --- | --- |
| `save_percentage` | Save percentage % | Saves / shots on target faced |
| `aerial_duels_won_per90` | Aerial duels won per 90 | Aerial duels won / minutes * 90 |
| `interceptions_padj` | Interceptions, possession adjusted | Interceptions adjusted by team/opponent possession; requires possession context |
| `passes_completed_per90` | Passes completed per 90 | Completed passes / minutes * 90 |
| `long_pass_accuracy_pct` | Long pass accuracy % | Accurate long passes / attempted long passes |
| `short_pass_completion_pct` | Short pass completion % | Completed short passes / attempted short passes |
| `prevented_goals_per90` | Prevented goals, PSxG - GA per 90 | (Post-shot xG faced - goals against) / minutes * 90 |

### Centrebacks

| Metric Key | Label | Calculation / Source Requirement |
| --- | --- | --- |
| `passes_completed_per90` | Passes completed per 90 | Completed passes / minutes * 90 |
| `forward_pass_completion_pct` | Forward pass completion % | Completed forward passes / attempted forward passes |
| `progressive_passes_completed_per90` | Progressive passes completed per 90 | Completed progressive passes / minutes * 90 |
| `possession_won_per90` | Possession won per 90 | Possession regains / minutes * 90 |
| `defensive_duels_won_pct` | Defensive duels won % | Defensive duels won / defensive duels attempted |
| `aerial_duels_won_pct` | Aerial duels won % | Aerial duels won / aerial duels attempted |
| `progressive_carries_per90` | Progressive carries per 90 | Progressive carries / minutes * 90 |

### Fullbacks

| Metric Key | Label | Calculation / Source Requirement |
| --- | --- | --- |
| `accurate_crosses_per90` | Accurate crosses per 90 | Accurate crosses / minutes * 90 |
| `xa_per90` | Expected assists per 90 | xA / minutes * 90 |
| `progressive_passes_completed_per90` | Progressive passes completed per 90 | Completed progressive passes / minutes * 90 |
| `possession_won_per90` | Possession won per 90 | Possession regains / minutes * 90 |
| `defensive_duels_won_pct` | Defensive duels won % | Defensive duels won / defensive duels attempted |
| `aerial_duels_won_pct` | Aerial duels won % | Aerial duels won / aerial duels attempted |
| `progressive_carries_per90` | Progressive carries per 90 | Progressive carries / minutes * 90 |

### Midfielders

| Metric Key | Label | Calculation / Source Requirement |
| --- | --- | --- |
| `duels_won_pct` | Duels won % | Duels won / duels attempted |
| `possession_won_per90` | Possession won per 90 | Possession regains / minutes * 90 |
| `progressive_carries_per90` | Progressive carries per 90 | Progressive carries / minutes * 90 |
| `forward_passes_completed_per90` | Forward passes completed per 90 | Completed forward passes / minutes * 90 |
| `forward_pass_completion_pct` | Forward pass completion % | Completed forward passes / attempted forward passes |
| `key_passes_per90` | Key passes per 90 | Key passes / minutes * 90 |
| `progressive_passes_completed_per90` | Progressive passes completed per 90 | Completed progressive passes / minutes * 90 |

### Attackers

| Metric Key | Label | Calculation / Source Requirement |
| --- | --- | --- |
| `progressive_carries_per90` | Progressive carries per 90 | Progressive carries / minutes * 90 |
| `successful_dribbles_per90` | Successful dribbles per 90 | Successful dribbles / minutes * 90 |
| `non_penalty_goals_per90` | Non-penalty goals per 90 | Non-penalty goals / minutes * 90 |
| `npxg_per90` | Non-penalty xG per 90 | Non-penalty xG / minutes * 90 |
| `npxg_xa_per90` | npxG + xA per 90 | (Non-penalty xG + xA) / minutes * 90 |
| `assists_per90` | Assists per 90 | Assists / minutes * 90 |
| `xa_per90` | Expected assists per 90 | xA / minutes * 90 |
| `key_passes_per90` | Key passes per 90 | Key passes / minutes * 90 |
| `accurate_crosses_per90` | Accurate crosses per 90 | Accurate crosses / minutes * 90 |
| `goal_conversion_pct` | Goal conversion % | Goals / shots |
| `touches_in_box_per90` | Touches in box per 90 | Touches in penalty area / minutes * 90 |
| `aerial_duels_won_pct` | Aerial duels won % | Aerial duels won / aerial duels attempted |
| `offensive_duels_won_per90` | Offensive duels won per 90 | Offensive duels won / minutes * 90 |

## Per-90 Calculation

For count metrics:

```text
per_90 = metric_total / minutes_played * 90
```

Rules:

- Return `null` when `minutes_played` is missing or zero.
- Keep raw totals and per-90 values when both are useful.
- Use decimal values internally; format in the frontend.

## Percentage Calculation

For percentage metrics:

```text
percentage = numerator / denominator * 100
```

Rules:

- Return `null` when denominator is missing or zero.
- Keep numerator and denominator in source audit metadata if available.
- Do not rank players with null percentages.

## Percentile Logic

Default peer group:

- Same season.
- Same league, or selected league group when the UI is explicitly in grouped mode.
- Same position group.
- Player minutes at or above configured threshold.

Recommended thresholds:

- Current season: `400` minutes by default.
- Last completed season: `900` minutes by default.
- Thresholds must be configurable in backend settings.

Percentile calculation:

```text
percentile = 100 * count(peer_values <= player_value) / count(peer_values)
```

Rules:

- Higher is better by default.
- For any future lower-is-better metric, invert before storing or mark `higher_is_better = false`.
- Null and unavailable values are excluded from percentile peer sets.
- Store the calculation version and threshold used.
- If fewer than 20 eligible peers exist, show a low-sample warning.

## Missing Metric Handling

| Status | Meaning | UI Behavior |
| --- | --- | --- |
| `available` | Metric is directly available or directly calculated from source fields | Show value and percentile |
| `approximated` | Metric is estimated from imperfect source fields | Show value with approximation label and methodology note |
| `unavailable` | Source does not support the metric | Show unavailable state; exclude from rankings by default |

## Future Performance Index

Do not build this in the first implementation. A later ScoutFootball index may use:

- Weighted percentiles by position group.
- Metric availability confidence.
- Minutes-adjusted confidence factor.
- Source quality score.

The index must be documented as ScoutFootball's original model and must not copy DataMB's Performance Index.

