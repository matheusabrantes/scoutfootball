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
- Active MVP ingestion season for all five validated leagues: 2024.
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
- Use league-level `/players?league={league_id}&season=2024` for Premier League, La Liga, and Bundesliga. A later ingestion check found that 2025 returned empty player pages for those leagues.
- Store the exact provider season per player-season row and make season availability visible in the UI.

Next validation task:

1. Resolve why API-Football returns player rows with null metric values for the current free-plan `/players` responses.
2. Confirm whether non-null player statistics require a paid plan, different endpoint, different query shape, or another validated season.
3. Keep the SQLite ingestion scaffold, but do not treat player rows with all-null metrics as usable analytic data.
4. Re-test Serie A Italy and Ligue 1 with metadata-selected seasons before marking them active.

## FBref Pivot Status

API-Football remains useful for metadata, but its tested `/players` responses returned null values for supported MVP metric fields. FBref was tested through `soccerdata` in a local backend virtual environment.

Current state:

- `soccerdata 1.8.8` installs and imports successfully in `backend/.venv`.
- FBref returned `403 Forbidden` for `https://fbref.com/en/comps/` before table inspection.
- FBref field mapping has been drafted in `docs/FBREF_FIELD_MAPPING.md`.
- Expected FBref support remains unverified for all target leagues and tables.
- Brazil and Argentina did not reach table inspection.
- Current strategy classification is `not_viable_without_paid_provider`.
- API-Football should remain as metadata/basic fallback.
- Advanced MVP metrics still require a licensed provider, a different acceptable source, or a vetted bootstrap dataset.

## Deep Research Update

Deep source research on 2026-06-14 is documented in `docs/FOOTBALL_DATA_SOURCE_DEEP_RESEARCH.md`.

MVP metric strategy:

- Top-five Europe: use vetted FBref-style Kaggle/static CSVs first, with metric support determined by actual columns.
- Brazil and Argentina: keep API-Football metadata/basic context only until a legitimate advanced dataset or paid provider is validated.
- Do not show unsupported advanced metrics as real values.
- Do not implement live scraping or private/unofficial endpoint ingestion.

## StatsBomb Open Data Status

StatsBomb Open Data was evaluated on 2026-06-14 in `docs/STATSBOMB_OPEN_DATA_EVALUATION.md`.

Metric implications:

- Strong for event-derived metric engine development: goals, shots, xG, npxG, passes, key passes, crosses, dribbles, interceptions, blocks, ball recoveries, duels, cards, and transparent progressive pass/carry rules.
- Useful for a historical demo using complete target seasons such as Premier League 2015/2016.
- Not sufficient for current-season ScoutFootball, full target-league coverage, or Brazil/Argentina advanced league metrics.
- Does not provide PSxG or a direct xA field in the inspected open event schema.
- Aerial duel metrics remain only partially derivable because a complete aerial-duel denominator was not proven.
