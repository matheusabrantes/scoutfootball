# Provider Field Mapping

This file tracks how API-Football player fields map to ScoutFootball metrics. The mapping is based on the real validation run from 2026-06-12.

Validation summary:

- Provider: API-Football / API-SPORTS.
- Initial P0 validation requests used: 24.
- South America follow-up investigation requests used: 9.
- Validated P0 player-stat leagues: Brasileirao Serie A, Argentina Primera Division, Premier League, La Liga, Bundesliga.
- Blocked P0 player-stat leagues from the first pass: Serie A Italy, Ligue 1.
- South America validation detail: Brazil and Argentina player stats work at league level for season 2024; seasons 2026 and 2025 returned empty player pages.
- MVP decision: API-Football is usable for MVP ingestion if the first South America implementation accepts the latest available player-stat season found by provider metadata, currently 2024 for both Brazil and Argentina.
- Sportmonks remains future/backup only because it is too expensive for this early MVP.

Status values:

- `supported`
- `partially_supported`
- `not_supported`
- `requires_paid_event_data`
- `unknown_until_provider_validation`

## API-Football MVP Mapping

| ScoutFootball Metric | API-Football Candidate Fields | Status | Notes |
| --- | --- | --- | --- |
| Minutes | `statistics.games.minutes` | `supported` | Returned by validated player samples. Required for per-90 calculations. |
| Appearances | `statistics.games.appearences` | `supported` | Returned by validated player samples with provider spelling `appearences`. |
| Goals | `statistics.goals.total` | `supported` | Returned by validated player samples. |
| Assists | `statistics.goals.assists` | `supported` | Returned by validated player samples. |
| Shots | `statistics.shots.total` | `supported` | Returned by validated player samples. |
| Shots on target | `statistics.shots.on` | `supported` | Returned by validated player samples. |
| Passes | `statistics.passes.total` | `supported` | Returned by validated player samples. |
| Key passes | `statistics.passes.key` | `supported` | Returned by validated player samples. |
| Pass accuracy | `statistics.passes.accuracy` | `supported` | Returned by validated player samples. Must normalize string/number shape during ingestion. |
| Successful dribbles | `statistics.dribbles.success` | `supported` | Returned by validated player samples. |
| Dribble attempts | `statistics.dribbles.attempts` | `supported` | Returned by validated player samples. |
| Duels | `statistics.duels.total` | `supported` | Returned by validated player samples. |
| Duels won | `statistics.duels.won` | `supported` | Returned by validated player samples. |
| Tackles | `statistics.tackles.total` | `supported` | Returned by validated player samples. |
| Interceptions | `statistics.tackles.interceptions` | `supported` | Raw interceptions only; not possession-adjusted. |
| Blocks | `statistics.tackles.blocks` | `supported` | Returned by validated player samples. |
| Fouls committed/drawn | `statistics.fouls.committed`, `statistics.fouls.drawn` | `supported` | Returned by validated player samples. |
| Cards | `statistics.cards.yellow`, `statistics.cards.yellowred`, `statistics.cards.red` | `supported` | Context field, not a core performance metric. |
| Saves | `statistics.goals.saves` | `supported` | Returned by validated player samples; only meaningful for goalkeepers. |
| Goals conceded | `statistics.goals.conceded` | `supported` | Returned by validated player samples; only meaningful for goalkeepers/defensive context. |
| Non-penalty goals | Goal and penalty fields if available | `partially_supported` | Requires penalty-goal field; otherwise unsupported. |
| Goal conversion % | Goals and shots | `partially_supported` | Supported only if shots and goals are present. |
| Save percentage % | Saves and shots on target faced | `partially_supported` | API-Football may not expose shots faced at player level. |
| Expected assists | None confirmed | `requires_paid_event_data` | Do not show as real until provider validates xA. |
| Non-penalty xG | None confirmed | `requires_paid_event_data` | Requires xG/npxG feed or add-on. |
| npxG + xA | None confirmed | `requires_paid_event_data` | Requires xG/xA feed or add-on. |
| PSxG - GA | None confirmed | `requires_paid_event_data` | Requires post-shot xG. |
| Progressive carries | None confirmed | `requires_paid_event_data` | Requires event data and stable definition. |
| Progressive passes | None confirmed | `requires_paid_event_data` | Requires event data and stable definition. |
| Possession-adjusted interceptions | Interceptions plus possession context | `requires_paid_event_data` | Needs team/opponent possession context and methodology. |
| Touches in box | None confirmed | `requires_paid_event_data` | Requires zone/touch event data. |
| Offensive duels won | None confirmed | `requires_paid_event_data` | Requires Wyscout-style duel taxonomy or equivalent. |

## Implementation Rule

The application must not present `unknown`, `requires_paid_event_data`, or `not_supported` metrics as real values. These metrics can appear in methodology and glossary views with clear unavailable or blocked states.

## Available Player Field Groups

The same player field groups were confirmed for Premier League, La Liga, Bundesliga, Brasileirao Serie A, and Argentina Primera Division.

Identity:

- `player.id`
- `player.name`
- `player.firstname`
- `player.lastname`
- `player.age`
- `player.birth.date`
- `player.birth.place`
- `player.birth.country`
- `player.nationality`
- `player.height`
- `player.weight`
- `player.injured`
- `player.photo`

Team/club:

- `statistics.team.id`
- `statistics.team.name`
- `statistics.team.logo`

League/season:

- `statistics.league.id`
- `statistics.league.name`
- `statistics.league.country`
- `statistics.league.season`
- `statistics.league.logo`
- `statistics.league.flag`

Position:

- `statistics.games.position`
- `statistics.games.rating`

Minutes/appearances:

- `statistics.games.appearences`
- `statistics.games.lineups`
- `statistics.games.minutes`
- `statistics.games.number`
- `statistics.games.captain`

Attacking:

- `statistics.goals.total`
- `statistics.goals.assists`
- `statistics.shots.total`
- `statistics.shots.on`

Passing:

- `statistics.passes.total`
- `statistics.passes.key`
- `statistics.passes.accuracy`

Defensive:

- `statistics.tackles.total`
- `statistics.tackles.blocks`
- `statistics.tackles.interceptions`

Duels:

- `statistics.duels.total`
- `statistics.duels.won`

Dribbling:

- `statistics.dribbles.attempts`
- `statistics.dribbles.success`
- `statistics.dribbles.past`

Goalkeeper:

- `statistics.goals.saves`
- `statistics.goals.conceded`

Discipline:

- `statistics.cards.yellow`
- `statistics.cards.yellowred`
- `statistics.cards.red`
- `statistics.penalty.won`
- `statistics.penalty.commited`
- `statistics.penalty.scored`
- `statistics.penalty.missed`
- `statistics.penalty.saved`
