# ScoutFootball Implementation Backlog

## Phase 0 — Data Validation and Scaffold

### Validate API-Football coverage

Priority: P0
Area: Data
Description:
Validate API-Football against all 12 target leagues, current season, last completed season, player-stat endpoints, rate limits, public display rights, and local cache/storage permissions.
Acceptance Criteria:
Every target league has a confirmed API-Football league id or a documented gap; current and last completed season availability are recorded; player-stat endpoint coverage is mapped; legal/cache notes are captured in `docs/DATA_SOURCE_RESEARCH.md`.
Dependencies:
API-Football account or trial key.
Notes:
Complete enough to proceed as of 2026-06-12. Premier League, La Liga, Bundesliga, Brasileirao Serie A, and Argentina Primera Division returned player statistics. Brazil and Argentina work for season 2024, while 2026 and 2025 returned empty player pages.

### Validate Sportmonks coverage

Priority: P2
Area: Data
Description:
Validate Sportmonks against all 12 target leagues, current season, last completed season, player-stat endpoints, plan limits, xG add-on needs, public display rights, and local cache/storage permissions.
Acceptance Criteria:
Every target league is mapped to a Sportmonks league id or documented gap; required plan tier is identified; player-stat and advanced-stat coverage are recorded; legal/cache notes are captured in `docs/DATA_SOURCE_RESEARCH.md`.
Dependencies:
Sportmonks account, trial access, or sales confirmation.
Notes:
Sportmonks is future/backup only for this early MVP because it is too expensive right now.

### Map available provider fields to ScoutFootball metrics

Priority: P0
Area: Data
Description:
Create a provider-field mapping for each ScoutFootball metric using API-Football and Sportmonks validation results.
Acceptance Criteria:
Every metric in `docs/METRICS_SPEC.md` has provider field names, calculation notes, source reliability, and status for each provider.
Dependencies:
Validate API-Football coverage; validate Sportmonks coverage.
Notes:
Initial API-Football mapping is documented in `docs/PROVIDER_FIELD_MAPPING.md` and `docs/MVP_METRICS.md`. Continue with API-Football first; Sportmonks is backup only.

### Define unsupported metrics

Priority: P0
Area: Data
Description:
List metrics that cannot be supported exactly by the selected MVP provider and classify them as approximated or unavailable.
Acceptance Criteria:
Unsupported metrics are documented with user-facing wording, methodology notes, and default UI behavior.
Dependencies:
Provider-field mapping.
Notes:
Unavailable metrics should not appear in default ranking selectors.

### Resolve Brazil and Argentina player-stat blocker

Priority: P0
Area: Data
Description:
Determine why API-Football returned no player statistics for Brasileirao Serie A and Argentina Primera Division despite resolving league ids.
Acceptance Criteria:
Provider plan, endpoint, season-year, competition-id, or data-coverage cause is documented; either both leagues return player-stat samples or a replacement MVP source/league strategy is approved.
Dependencies:
API-Football validation result from 2026-06-12.
Notes:
Resolved for MVP ingestion: both leagues return league-level player statistics for season 2024. Keep a known limitation that API-Football marks 2026 current, but 2026 and 2025 returned empty player pages.

### Resolve API-Football null metric values

Priority: P0
Area: Data
Description:
Determine why API-Football `/players` returns real player rows and statistics object fields but null values for core MVP metrics.
Acceptance Criteria:
At least one active MVP league returns non-null values for minutes, goals, passes, duels, or equivalent MVP metrics; otherwise document provider plan/endpoint limitations and decide whether to upgrade, use another provider, or reduce scope.
Dependencies:
API-Football SQLite ingestion scaffold.
Notes:
Do not treat rows with all-null supported metric values as usable player analytics data.

### Investigate FBref via soccerdata

Priority: P0
Area: Data
Description:
Install and validate `soccerdata` against FBref player stat tables for Premier League, one South American league, and then the remaining target leagues if the API is clear.
Acceptance Criteria:
Safe metadata is captured for available FBref tables, columns, row counts, seasons, and competitions; `docs/FBREF_FIELD_MAPPING.md` is updated from observed columns; the data strategy is classified as `fbref_first_viable`, `fbref_europe_only_viable`, `fbref_plus_api_football_viable`, `kaggle_bootstrap_required`, or `not_viable_without_paid_provider`.
Dependencies:
Optional `soccerdata` provider dependency.
Notes:
Completed as far as allowed by access controls on 2026-06-12. `soccerdata 1.8.8` installed in local `backend/.venv`, but FBref returned `403 Forbidden` for `https://fbref.com/en/comps/` before table inspection. The script now fails fast on blocked access and records safe metadata only. Do not bypass access controls. API-Football remains metadata/basic fallback only; advanced metrics need a licensed provider or vetted bootstrap dataset.

### Validate static CSV data sources

Priority: P0
Area: Data
Description:
Evaluate vetted Kaggle/FBref-style static CSV datasets for top-five European player metrics and define a safe manual upload workflow with source provenance.
Acceptance Criteria:
At least one candidate dataset has documented URL, license, seasons, leagues, row count, column list, metric mapping, and allowed local use; unsupported metrics are marked unavailable; no live scraping or private endpoint ingestion is implemented.
Dependencies:
`docs/FOOTBALL_DATA_SOURCE_DEEP_RESEARCH.md`.
Notes:
Recommended next data task from 2026-06-14 deep research. Start with Kaggle top-five Europe 2024-2025 and FBref 2017-2024 datasets. Keep API-Football as metadata/basic fallback for Brazil and Argentina.

### Create backend scaffold

Priority: P0
Area: Backend
Description:
Create the FastAPI backend structure with Pydantic contracts, settings, basic routes, test setup, and mock-data service boundaries.
Acceptance Criteria:
Backend starts locally, exposes a health route, can serve mock contract responses, and has a documented validation command.
Dependencies:
`docs/DATA_CONTRACT.md`.
Notes:
No real provider ingestion in this phase.

### Create frontend scaffold

Priority: P0
Area: Frontend
Description:
Create the React + Vite + TypeScript frontend with routing, Tailwind, API client boundaries, and base layout.
Acceptance Criteria:
Frontend dev server runs, routes render, TypeScript check is configured, and mock API/client types align with `docs/DATA_CONTRACT.md`.
Dependencies:
`docs/DATA_CONTRACT.md`.
Notes:
Do not use Next.js.

### Create mock player dataset

Priority: P0
Area: Data
Description:
Create a small original mock dataset covering all supported response shapes, all five position groups, available/approximated/unavailable metric states, and at least one European and one South American league.
Acceptance Criteria:
Mock data supports player database, profile, rankings, and comparison screens without using real provider or DataMB data.
Dependencies:
Data contract; metric spec.
Notes:
Mock values must be synthetic and clearly marked.

### Build player database UI with mock data

Priority: P0
Area: Frontend
Description:
Build `/players` against mock responses with search, filters, sorting, pagination-ready table state, and percentile mini bars.
Acceptance Criteria:
Users can filter by league, season, club, position, age, minutes, and nationality; users can sort metrics and navigate to mock player profiles.
Dependencies:
Frontend scaffold; mock player dataset.
Notes:
Use D3 only for small inline percentile visuals.

### Build player profile UI with mock data

Priority: P0
Area: Frontend
Description:
Build `/players/:playerId` against mock responses with player context, metric cards, percentiles, and source/availability states.
Acceptance Criteria:
Profile renders available, approximated, and unavailable metrics clearly and remains responsive.
Dependencies:
Frontend scaffold; mock player dataset.
Notes:
Do not add similar-player logic unless represented as a non-functional placeholder.

### Build rankings UI with mock data

Priority: P0
Area: Frontend
Description:
Build `/rankings` against mock responses with position tabs, metric selector, league/season filters, minutes threshold, and raw/percentile sorting.
Acceptance Criteria:
Users can rank mock players by position and metric; unavailable metrics are hidden or disabled by default.
Dependencies:
Frontend scaffold; mock player dataset.
Notes:
No radar chart or scatter plot.

### Build comparison UI with mock data

Priority: P0
Area: Frontend
Description:
Build `/compare` against mock responses for comparing 2 to 5 players in a clean metric table.
Acceptance Criteria:
Users can add/remove mock players, compare raw values and percentiles, and see warnings for mixed position groups or missing metrics.
Dependencies:
Frontend scaffold; mock player dataset.
Notes:
Keep comparison table-first and chart-free.

## Phase 1: Backend Foundation

### Harden FastAPI backend scaffold

Priority: P0
Area: Backend
Description:
Extend the Phase 0 backend scaffold with SQLAlchemy, database settings, pytest, ruff, and typed service boundaries.
Acceptance Criteria:
`backend/app` imports cleanly, health endpoint works, and backend test command runs.
Dependencies:
Phase 0 backend scaffold.
Notes:
Use SQLite locally unless DuckDB is clearly better for batch analytics.

### Define database schema

Priority: P0
Area: Backend
Description:
Create models for leagues, seasons, clubs, players, player season stats, metrics, metric values, data sources, and ingestion runs.
Acceptance Criteria:
Schema supports all required fields and can be migrated/created locally.
Dependencies:
Backend scaffold.
Notes:
Prefer explicit constraints for uniqueness and required ids.

### Build provider ingestion adapter

Priority: P0
Area: Data
Description:
Create a provider-neutral ingestion interface and one MVP provider implementation.
Acceptance Criteria:
Ingestion can fetch or load league, club, player, and stat records into canonical models.
Dependencies:
Confirmed provider and schema.
Notes:
Keep provider-specific fields out of API response contracts.

### Implement data validation checks

Priority: P0
Area: Data
Description:
Add validation for required fields, row uniqueness, minutes, percentages, metric availability, and source metadata.
Acceptance Criteria:
Invalid sample data fails with clear errors and valid sample data passes.
Dependencies:
Database schema and ingestion adapter.
Notes:
Validation should run before metric publication.

## Phase 2: Metrics and API

### Implement per-90 calculations

Priority: P0
Area: Backend
Description:
Create reusable per-90 calculation functions for count metrics.
Acceptance Criteria:
Zero-minute, null-minute, and normal cases are covered by unit tests.
Dependencies:
Backend scaffold.
Notes:
Use decimal-safe handling and let frontend format display precision.

### Implement percentile logic

Priority: P0
Area: Backend
Description:
Calculate percentiles by season, league or league group, position group, metric, and configurable minutes threshold.
Acceptance Criteria:
Tests cover ties, nulls, unavailable metrics, small peer groups, and threshold filtering.
Dependencies:
Metric value model.
Notes:
Store threshold and calculation version.

### Build player database API

Priority: P0
Area: Backend
Description:
Implement `GET /api/players` with search, filters, sorting, and pagination.
Acceptance Criteria:
API supports season, league, club, position, age, minutes, nationality, search, and metric sorting.
Dependencies:
Schema and sample data.
Notes:
Return enough metric summary data for table rows without overfetching.

### Build player profile API

Priority: P0
Area: Backend
Description:
Implement `GET /api/players/{player_id}` with bio, context, metrics, percentiles, and availability states.
Acceptance Criteria:
Profile response contains player identity, season stats, metric cards, and source metadata.
Dependencies:
Metrics layer.
Notes:
Handle players with multiple clubs in a season explicitly.

### Build rankings and comparison APIs

Priority: P0
Area: Backend
Description:
Implement `GET /api/rankings` and `GET /api/compare`.
Acceptance Criteria:
Rankings sort by raw value or percentile; compare accepts 2 to 5 players and returns aligned metrics.
Dependencies:
Percentile logic.
Notes:
Reject more than 5 players with a clear validation error.

## Phase 3: Frontend MVP

### Connect frontend scaffold to backend API

Priority: P0
Area: Frontend
Description:
Connect the Phase 0 React, TypeScript, Vite, Tailwind frontend scaffold to real backend API responses while preserving the mock-data fallback for local development.
Acceptance Criteria:
Frontend dev server runs, TypeScript check works, base routes render, and API client types align with backend response contracts.
Dependencies:
Phase 0 frontend scaffold; player database API; profile API; rankings API; comparison API.
Notes:
Do not use Next.js.

### Connect player database page

Priority: P0
Area: Frontend
Description:
Connect `/players` to the backend player database API with sticky filters, search, sortable TanStack Table, and percentile mini bars.
Acceptance Criteria:
Users can filter and sort players by all MVP filter dimensions and open player profiles.
Dependencies:
Player database API.
Notes:
Use D3 only for small inline visuals.

### Connect player profile page

Priority: P0
Area: Frontend
Description:
Connect `/players/:playerId` to the backend profile API with player context, metric cards, percentile cards, and source status.
Acceptance Criteria:
Available, approximated, and unavailable metrics are visually distinct and understandable.
Dependencies:
Player profile API.
Notes:
Similar players can remain a placeholder for later.

### Connect rankings page

Priority: P0
Area: Frontend
Description:
Connect `/rankings` to the backend rankings API with position tabs, metric selector, filters, and raw/percentile sorting.
Acceptance Criteria:
Users can rank players by any available metric for the selected position group.
Dependencies:
Rankings API.
Notes:
Hide unavailable metrics by default.

### Connect comparison page

Priority: P0
Area: Frontend
Description:
Connect `/compare` to the backend comparison API for 2 to 5 players with aligned raw values and percentiles.
Acceptance Criteria:
Users can search/add/remove players and compare selected metrics in a clean table.
Dependencies:
Comparison API.
Notes:
No radar chart or scatter plot.

### Build glossary and methodology pages

Priority: P1
Area: Frontend
Description:
Create `/glossary` and `/methodology` from API or static content.
Acceptance Criteria:
Every metric has a plain-language definition and methodology explains sources, thresholds, percentiles, approximations, and unavailable metrics.
Dependencies:
Metrics and methodology content.
Notes:
These pages are part of MVP trust.

### Build landing and leagues pages

Priority: P1
Area: Frontend
Description:
Create `/` and `/leagues` with premium product entry, search, CTA, and coverage status.
Acceptance Criteria:
Landing page feels polished and users can enter the player database quickly.
Dependencies:
Frontend scaffold and league API.
Notes:
Keep the first screen product-focused.

## Phase 4: Quality and Release

### Add backend validation suite

Priority: P0
Area: Testing
Description:
Add unit tests for metrics, percentiles, and data validation.
Acceptance Criteria:
Tests cover edge cases and run in CI or local validation.
Dependencies:
Metrics and validation modules.
Notes:
This is higher priority than broad UI tests because metric correctness drives trust.

### Add frontend validation

Priority: P1
Area: Testing
Description:
Configure TypeScript, lint, build, and basic component tests if the selected setup includes test tooling.
Acceptance Criteria:
Validation commands are documented and passing.
Dependencies:
Frontend scaffold.
Notes:
Do not add heavy test infrastructure before core pages exist.

### Prepare MVP deployment

Priority: P1
Area: Backend
Description:
Choose split deployment or single-container deployment and document environment variables and release steps.
Acceptance Criteria:
MVP can be deployed with PostgreSQL and a documented ingestion process.
Dependencies:
Backend, frontend, and provider credentials.
Notes:
Keep infrastructure simple until usage demands more.

## Phase 5: Future Enhancements

### Add licensed event-data provider

Priority: P2
Area: Data
Description:
Integrate Wyscout, Opta/Stats Perform, StatsBomb commercial, or another licensed event provider.
Acceptance Criteria:
Unavailable event metrics become directly available with documented source fields.
Dependencies:
Commercial license.
Notes:
This is the unlock for premium scouting-grade depth.

### Add ScoutFootball performance score

Priority: P2
Area: Metrics
Description:
Create an original weighted percentile score by position group with a minutes-adjusted confidence factor.
Acceptance Criteria:
Formula is documented, tested, and clearly branded as ScoutFootball's own index.
Dependencies:
Stable metric coverage.
Notes:
Do not copy DataMB's index.

### Add advanced visualizations

Priority: P2
Area: Frontend
Description:
Add richer D3 visuals once data coverage supports them.
Acceptance Criteria:
Visuals answer a clear analysis question and remain responsive.
Dependencies:
Licensed event data and stable metrics.
Notes:
Radar charts and scatter plots remain out of MVP.
