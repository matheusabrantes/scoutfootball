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
