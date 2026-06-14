# StatsBomb Metric Definitions

These definitions are ScoutFootball-specific rules for StatsBomb Open Data. They are not claimed to match DataMB, Wyscout, Opta, FBref, or StatsBomb commercial definitions.

## Coordinate Model

StatsBomb event locations use a 120 x 80 pitch:

- Attacking goal center: `(120, 40)`
- Attacking penalty area approximation: `x >= 102` and `18 <= y <= 62`
- Distance to goal: Euclidean distance from the event location to `(120, 40)`

## Progressive Pass

A completed pass is counted as progressive when all conditions are true:

- The event type is `Pass`.
- The pass has no `pass.outcome`, which StatsBomb uses for completed passes.
- Both `location` and `pass.end_location` are available.
- The end location is closer to the opponent goal than the start location.
- The absolute distance-to-goal reduction is at least `5.0` StatsBomb coordinate units.
- The relative distance-to-goal reduction is at least `25%`.

Formula:

```text
start_distance = distance(start_location, opponent_goal_center)
end_distance = distance(end_location, opponent_goal_center)
distance_gain = start_distance - end_distance
progressive = end_distance < start_distance
  and distance_gain >= 5.0
  and distance_gain / start_distance >= 0.25
```

## Progressive Carry

A carry is counted as progressive when all conditions are true:

- The event type is `Carry`.
- Both `location` and `carry.end_location` are available.
- The carry path length is at least `5.0` StatsBomb coordinate units.
- The end location is closer to the opponent goal than the start location.
- The absolute distance-to-goal reduction is at least `5.0` StatsBomb coordinate units.
- The relative distance-to-goal reduction is at least `25%`.

Formula:

```text
carry_distance = distance(start_location, end_location)
start_distance = distance(start_location, opponent_goal_center)
end_distance = distance(end_location, opponent_goal_center)
distance_gain = start_distance - end_distance
progressive = carry_distance >= 5.0
  and end_distance < start_distance
  and distance_gain >= 5.0
  and distance_gain / start_distance >= 0.25
```

## Touches In Box

A player receives one attacking penalty-area touch for any event with a player and a `location` inside:

```text
x >= 102 and 18 <= y <= 62
```

This is an event-touch approximation, not an Opta or FBref touches-in-box definition.

## Minutes

The proof-of-concept minutes algorithm uses:

- `Starting XI` events to identify starters and starting positions.
- `Substitution` events to reduce the outgoing player minutes and assign replacement minutes.
- `Bad Behaviour` or `Foul Committed` red cards to cap the dismissed player's minutes.
- Match duration as the maximum event timestamp in absolute StatsBomb match minutes.

Known limitations:

- Stoppage time is included only as far as the event feed timestamp reaches.
- Red-card and substitution logic is event-feed dependent.
- Players with missing Starting XI/substitution data may have incomplete minutes.
- The algorithm is suitable for a proof of concept, but should be reconciled against official minutes before public rankings.

## Derived Metric Inventory

| Metric | Event Types Used | Fields Used | Formula | Exclusions | Known Limitations |
| --- | --- | --- | --- | --- | --- |
| goals | `Shot` | `shot.outcome.name` | Count shots where outcome is `Goal` | Own goals are not included as player goals | Depends on event tagging |
| non_penalty_goals | `Shot` | `shot.outcome.name`, `shot.type.name` | Goals where shot type is not `Penalty` | Penalties | None for tagged shots |
| assists | `Pass` | `pass.goal_assist` | Count passes with goal-assist flag | Does not include fantasy assists | StatsBomb definition only |
| shots | `Shot` | event type | Count shot events | None | Includes penalties unless filtered elsewhere |
| shots_on_target | `Shot` | `shot.outcome.name` | Count `Goal`, `Saved`, `Saved to Post`, `Saved Off Target`, `Post` | Blocked/off-target outcomes | Approximation of on-target taxonomy |
| xg | `Shot` | `shot.statsbomb_xg` | Sum shot xG | None | StatsBomb model, not FBref/DataMB |
| npxg | `Shot` | `shot.statsbomb_xg`, `shot.type.name` | Sum xG excluding penalties | Penalties | StatsBomb model |
| key_passes | `Pass` | `pass.shot_assist` | Count shot-assist passes | Goal assists also counted only if shot-assist flag exists | Direct xA not available |
| passes_attempted | `Pass` | event type | Count pass events | None | Includes all tagged pass types |
| passes_completed | `Pass` | `pass.outcome` | Count passes with no outcome | Incomplete/out/unknown outcomes | StatsBomb uses missing outcome for completed passes |
| pass_completion_pct | `Pass` | pass totals | `passes_completed / passes_attempted * 100` | None | Not per 90 |
| forward_passes_attempted | `Pass` | `location`, `pass.end_location` | Count passes where end x is greater than start x | Missing locations | Simple x-axis rule |
| forward_passes_completed | `Pass` | `location`, `pass.end_location`, `pass.outcome` | Forward passes with no outcome | Missing locations, incomplete passes | Simple x-axis rule |
| forward_pass_completion_pct | `Pass` | forward pass totals | `forward_passes_completed / forward_passes_attempted * 100` | None | Not per 90 |
| crosses | `Pass` | `pass.cross` | Count passes marked as crosses | None | StatsBomb cross flag |
| accurate_crosses | `Pass` | `pass.cross`, `pass.outcome` | Crosses with no outcome | Incomplete crosses | StatsBomb completion semantics |
| dribbles_attempted | `Dribble` | event type | Count dribble events | None | Does not include carries |
| successful_dribbles | `Dribble` | `dribble.outcome.name` | Count outcome `Complete` | Incomplete dribbles | StatsBomb dribble taxonomy |
| touches_in_box | Any player event | `location` | Count player events in `x >= 102` and `18 <= y <= 62` | Events without location | Event-touch approximation |
| interceptions | `Interception` | event type | Count interception events | None | None |
| blocks | `Block` | event type | Count block events | None | None |
| ball_recoveries | `Ball Recovery` | event type | Count ball recovery events | None | None |
| duels | `Duel` | event type | Count duel events | None | Does not include every aerial contest |
| duels_won | `Duel` | `duel.outcome.name` | Count success/won outcomes | Lost/unknown outcomes | Outcome mapping should be audited per season |
| aerial_duels | Mixed | `pass.aerial_won`, `shot.aerial_won`, `clearance.aerial_won` | Initial MVP stores null | None | Complete denominator not validated |
| saves | `Goal Keeper` | `goalkeeper.type.name`, `goalkeeper.outcome.name` | Count saved/success outcomes | Non-shot keeper actions | Requires deeper goalkeeper audit |
| shots_on_target_faced | `Goal Keeper` | `goalkeeper.type.name` | Count shot-faced/save keeper events | Non-shot actions | May need reconciliation against shots |
| save_percentage | `Goal Keeper` | saves, shots on target faced | `saves / shots_on_target_faced * 100` | None | Partially reliable until audited |
| goals_conceded | `Goal Keeper` | `goalkeeper.type.name`, `goalkeeper.outcome.name` | Count shot-faced goal-conceded outcomes | Own goals/team goals not fully handled | Needs reconciliation |
| long_pass_accuracy | `Pass` | `pass.length`, `pass.outcome` | Completed passes with length >= 30 / attempted length >= 30 | Missing length | Custom threshold |
| short_pass_completion | `Pass` | `pass.length`, `pass.outcome` | Completed passes with length < 30 / attempted length < 30 | Missing length | Custom threshold |
| exits | `Goal Keeper` | `goalkeeper.type.name` | Count `Collected`, `Keeper Sweeper`, `Punch` | Other keeper actions | Custom grouping |

## Per-90 Metrics

For count metrics, ScoutFootball stores an additional metric with the suffix `_per_90`:

```text
metric_per_90 = metric_total / minutes * 90
```

Per-90 values are only calculated when `minutes > 0`.

Percentages and completion rates are not converted to per-90 values.

## Not Available In Initial MVP

The following placeholders are stored as null until formulas and required data are validated:

- `direct_xa`
- `psxg`
- `psxg_minus_goals_allowed`
- `interceptions_padj`
- `tackles_padj`
- `possession_won_padj`
