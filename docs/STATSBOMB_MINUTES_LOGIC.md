# StatsBomb Minutes Logic

ScoutFootball calculates player minutes from StatsBomb Open Data events for the historical MVP.

## Inputs

- `Starting XI` events identify starters and starting positions.
- `Substitution` events identify outgoing players and replacements.
- `Bad Behaviour` and `Foul Committed` red-card fields cap dismissed-player minutes.
- Match duration is estimated from the maximum absolute StatsBomb event timestamp.

## Algorithm

1. Set match duration to the maximum event timestamp, rounded up to the next minute.
2. Assign every starter the full match duration.
3. For each substitution:
   - outgoing player minutes become the substitution minute;
   - replacement player minutes become `match_duration - substitution_minute`;
   - replacement player starts are set to false.
4. For red cards:
   - dismissed player minutes are capped at the dismissal minute.
5. Players with events but no lineup/substitution record are retained through event aggregation, but their minutes quality should be considered incomplete unless reconciled.

## Reconciliation Checks

The ingestion summary tracks:

- `expected_team_minutes`
- `calculated_team_minutes`
- `minute_difference`
- `players_with_negative_minutes`
- `players_above_match_duration`
- `players_with_events_but_zero_minutes`

Current MVP status:

- Premier League 2015/2016 development ingestion uses `estimated` minute quality.
- Full public rankings should use reliable or estimated minutes only.
- Official minutes reconciliation should be added before broader public release.

## Quality Flags

- `reliable`: lineup, substitution, red-card, and team-minute reconciliation pass.
- `estimated`: event-derived minutes are usable but not fully reconciled.
- `incomplete`: missing lineup/substitution data prevents safe ranking use.
