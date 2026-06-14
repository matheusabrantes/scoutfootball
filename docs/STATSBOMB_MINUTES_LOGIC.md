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

- `expected_team_player_minutes`
- `calculated_team_player_minutes`
- `absolute_difference`
- `relative_difference`
- `players_with_negative_minutes`
- `players_above_match_duration`
- `players_with_events_but_zero_minutes`
- `players_with_minutes_but_no_position`
- duplicate player-match and player-team-season rows
- `minutes_quality_counts`

Current MVP status:

- Premier League 2015/2016 full ingestion uses `estimated` minute quality for 550 rows with 0 invalid/incomplete rows.
- Bundesliga 2023/2024 open-data sample uses `estimated` minute quality for 373 rows with 0 invalid/incomplete rows.
- Full public rankings should use reliable or estimated minutes only and should disclose that current open-data minutes are event-derived estimates.
- Official minutes reconciliation should be added before broader public release.

## Quality Flags

- `reliable`: lineup, substitution, red-card, and team-minute reconciliation pass.
- `estimated`: event-derived minutes are usable but not fully reconciled.
- `incomplete`: missing lineup/substitution data prevents safe ranking use.
- `invalid`: minutes exceeded the match duration or fell below zero before sanitization.
