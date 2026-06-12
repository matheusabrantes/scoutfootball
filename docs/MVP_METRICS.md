# ScoutFootball MVP Metrics

Status values:

- `supported`: directly available from validated API-Football player samples.
- `partially_supported`: can be derived from validated fields, but does not match the full ScoutFootball target definition.
- `not_supported`: unavailable from the validated fields.
- `requires_paid_event_data`: requires event, tracking, xG, PSxG, or provider-specific advanced data not present in validation.
- `unknown`: not validated yet for the relevant target leagues.

Validation basis:

- Provider: API-Football / API-SPORTS.
- Validation date: 2026-06-12.
- Initial validation requests used by script: 24.
- South America follow-up requests used by script: 9.
- Validated player-stat leagues: Brasileirao Serie A, Argentina Primera Division, Premier League, La Liga, Bundesliga.
- South America season detail: Brasileirao Serie A and Argentina Primera Division returned player-stat samples for season 2024; seasons 2026 and 2025 returned no players.
- MVP acceptance: passes if the MVP accepts latest provider-available South America player-stat seasons instead of requiring the provider current season for those leagues.
- Sportmonks: future/backup only.

## Supported MVP Metric Set

These are safe candidates for the first real-data UI where validated league data exists:

| Metric | Source Fields | Status | Notes |
| --- | --- | --- | --- |
| Minutes | `statistics.games.minutes` | `supported` | Required for per-90 calculations. |
| Appearances | `statistics.games.appearences` | `supported` | Provider field uses `appearences`. |
| Starts | `statistics.games.lineups` | `supported` | Can show starts/lineups. |
| Goals | `statistics.goals.total` | `supported` | Base attacking count. |
| Assists | `statistics.goals.assists` | `supported` | Base attacking count. |
| Shots | `statistics.shots.total` | `supported` | Base attacking count. |
| Shots on target | `statistics.shots.on` | `supported` | Base attacking count. |
| Passes | `statistics.passes.total` | `supported` | Can derive passes per 90. |
| Key passes | `statistics.passes.key` | `supported` | Can derive key passes per 90. |
| Pass accuracy | `statistics.passes.accuracy` | `supported` | Normalize provider shape before display. |
| Successful dribbles | `statistics.dribbles.success` | `supported` | Can derive successful dribbles per 90. |
| Dribble attempts | `statistics.dribbles.attempts` | `supported` | Can support dribble success percentage. |
| Duels | `statistics.duels.total` | `supported` | Can support duels per 90. |
| Duels won | `statistics.duels.won` | `supported` | Can support duels won percentage. |
| Tackles | `statistics.tackles.total` | `supported` | Basic defensive metric. |
| Interceptions | `statistics.tackles.interceptions` | `supported` | Raw interceptions only. |
| Blocks | `statistics.tackles.blocks` | `supported` | Basic defensive metric. |
| Saves | `statistics.goals.saves` | `supported` | Goalkeeper metric if player is a goalkeeper. |
| Goals conceded | `statistics.goals.conceded` | `supported` | Goalkeeper/defensive context. |
| Cards | `statistics.cards.yellow`, `statistics.cards.yellowred`, `statistics.cards.red` | `supported` | Context field. |

## Target Metric Classification

### Goalkeepers

| Target Metric | Status | Reason |
| --- | --- | --- |
| Save percentage % | `partially_supported` | Saves are available, but shots on target faced are not confirmed at player level. |
| Aerial duels won per 90 | `not_supported` | API-Football sample has total duels, not aerial duel subtype. |
| Interceptions, possession adjusted | `requires_paid_event_data` | Raw interceptions exist, but possession adjustment requires possession/event context. |
| Passes completed per 90 | `partially_supported` | Total passes and pass accuracy exist; completed passes can be estimated only if accuracy is reliable. |
| Long pass accuracy % | `not_supported` | No long-pass subtype found. |
| Short pass completion % | `not_supported` | No short-pass subtype found. |
| Prevented goals, PSxG - GA per 90 | `requires_paid_event_data` | No PSxG field found. |

### Centrebacks

| Target Metric | Status | Reason |
| --- | --- | --- |
| Passes completed per 90 | `partially_supported` | Total passes and pass accuracy exist; completed passes can be estimated only if accuracy is reliable. |
| Forward pass completion % | `requires_paid_event_data` | No pass direction field found. |
| Progressive passes completed per 90 | `requires_paid_event_data` | No progressive pass field found. |
| Possession won per 90 | `partially_supported` | Tackles and interceptions exist, but exact possession wins do not. |
| Defensive duels won % | `partially_supported` | Total duels and duels won exist, but defensive duel subtype does not. |
| Aerial duels won % | `not_supported` | No aerial duel subtype found. |
| Progressive carries per 90 | `requires_paid_event_data` | No progressive carry field found. |

### Fullbacks

| Target Metric | Status | Reason |
| --- | --- | --- |
| Accurate crosses per 90 | `not_supported` | No cross field found in validation. |
| Expected assists per 90 | `requires_paid_event_data` | No xA field found. |
| Progressive passes completed per 90 | `requires_paid_event_data` | No progressive pass field found. |
| Possession won per 90 | `partially_supported` | Tackles and interceptions exist, but exact possession wins do not. |
| Defensive duels won % | `partially_supported` | Total duels and duels won exist, but defensive duel subtype does not. |
| Aerial duels won % | `not_supported` | No aerial duel subtype found. |
| Progressive carries per 90 | `requires_paid_event_data` | No progressive carry field found. |

### Midfielders

| Target Metric | Status | Reason |
| --- | --- | --- |
| Duels won % | `supported` | `statistics.duels.won` and `statistics.duels.total` are available. |
| Possession won per 90 | `partially_supported` | Tackles and interceptions exist, but exact possession wins do not. |
| Progressive carries per 90 | `requires_paid_event_data` | No progressive carry field found. |
| Forward passes completed per 90 | `requires_paid_event_data` | No pass direction field found. |
| Forward pass completion % | `requires_paid_event_data` | No pass direction field found. |
| Key passes per 90 | `supported` | `statistics.passes.key` and minutes are available. |
| Progressive passes completed per 90 | `requires_paid_event_data` | No progressive pass field found. |

### Attackers

| Target Metric | Status | Reason |
| --- | --- | --- |
| Progressive carries per 90 | `requires_paid_event_data` | No progressive carry field found. |
| Successful dribbles per 90 | `supported` | `statistics.dribbles.success` and minutes are available. |
| Non-penalty goals per 90 | `partially_supported` | Goals exist and penalty scored exists, but provider semantics must be verified before subtracting. |
| Non-penalty xG per 90 | `requires_paid_event_data` | No npxG field found. |
| npxG + xA per 90 | `requires_paid_event_data` | No npxG or xA fields found. |
| Assists per 90 | `supported` | `statistics.goals.assists` and minutes are available. |
| Expected assists per 90 | `requires_paid_event_data` | No xA field found. |
| Key passes per 90 | `supported` | `statistics.passes.key` and minutes are available. |
| Accurate crosses per 90 | `not_supported` | No cross field found. |
| Goal conversion % | `supported` | Goals and shots are available. |
| Touches in box per 90 | `requires_paid_event_data` | No touch-zone field found. |
| Aerial duels won % | `not_supported` | No aerial duel subtype found. |
| Offensive duels won per 90 | `requires_paid_event_data` | No offensive duel subtype found. |

## MVP Decision

API-Football can support MVP ingestion with a provider-aware season policy:

- Use league-level `/players?league={league_id}&season=2024` for Brasileirao Serie A and Argentina Primera Division.
- Use league-level player-stat seasons validated for European leagues from the API-Football metadata.
- Store the exact provider season per player-season row and make season availability visible in the UI.

Next validation task:

1. Build controlled SQLite ingestion for validated P0 leagues only.
2. Keep request volume low and ingest one page per league first before expanding pagination.
3. Re-test Serie A Italy and Ligue 1 with metadata-selected seasons before marking them active.
