# ScoutFootball Product Plan

## Product Vision

ScoutFootball is a free web-only football player analytics platform that helps users find better players through clearer football data. The product focuses on selected leagues, current-season data, and last completed season data, with a premium, fast, minimal interface.

The product is inspired by the public category of football analytics tools, but it must be original in code, data, visual identity, copy, and methodology.

GitHub repository: [https://github.com/matheusabrantes/scoutfootball.git](https://github.com/matheusabrantes/scoutfootball.git)

Tagline: "Find better players through clearer football data."

## Target Users

- Recruitment analysts who need quick player shortlists.
- Coaches and scouts who want clean position-specific comparisons.
- Football analysts and writers who need explainable player metrics.
- Fans who want deeper player context without dense dashboard clutter.

## MVP Scope

### In Scope

- Player-only analytics.
- Current season and last completed season.
- Selected leagues in Europe and South America.
- Player search.
- Player database with filters.
- Player profile pages.
- Player ranking pages by position group and metric.
- Player comparison table for 2 to 5 players.
- Position-specific metric templates.
- League, season, club, position, age, minutes, and nationality filters.
- Percentile rankings by season, league or league group, position group, and minutes threshold.
- Metric glossary.
- Data source and methodology page.
- Responsive web design.
- Clear unavailable/approximated metric states.

### Out of Scope

- Club/team analysis.
- AI chat.
- Radar charts.
- Scatter plots.
- Native mobile app.
- Paid subscription.
- User accounts.
- Saved shortlists.
- Transfer valuation.
- Tactical reports.
- Video scouting.
- Admin CMS unless later needed for ingestion operations.

## Supported Leagues

Europe:

- Premier League.
- La Liga.
- Bundesliga.
- Serie A Italy.
- Ligue 1.
- Eredivisie.
- Liga Portugal.

South America:

- Brasileirao Serie A.
- Argentina Primera Division.
- Colombia Categoria Primera A.
- Uruguay Primera Division.
- Chile Primera Division.

## Position Groups

- Goalkeepers.
- Centrebacks.
- Fullbacks.
- Midfielders.
- Attackers.

Attackers combines wingers and strikers and includes the union of winger-style and striker-style metrics.

## Page Structure

| Route | Purpose | Primary UX |
| --- | --- | --- |
| `/` | Landing and product entry | Premium first screen, search, league coverage, "Explore Players" CTA |
| `/players` | Player database | Sticky filters, search, sortable TanStack Table, percentile micro-bars |
| `/players/:playerId` | Player profile | Bio, club/league/season context, metric cards, percentile cards |
| `/rankings` | Position and metric rankings | Position tabs, metric selector, raw/percentile sorting |
| `/compare` | Compare 2 to 5 players | Search/add players, clean comparison table, raw values and percentiles |
| `/glossary` | Metric definitions | Plain-language definitions and calculation notes |
| `/methodology` | Data/source transparency | Sources, percentile logic, thresholds, approximations, unavailable metrics |
| `/leagues` | Supported coverage | League and season availability |

## Core User Stories

- As a scout, I can filter players by league, season, position, age, minutes, and club so I can build a focused shortlist.
- As an analyst, I can sort a position ranking by a selected metric or percentile so I can identify top performers.
- As a coach, I can compare up to 5 players side by side so I can evaluate tradeoffs quickly.
- As a user, I can open a player profile and understand raw metrics, percentile context, and data limitations.
- As a user, I can read metric definitions and methodology so I know what each number means.
- As a product owner, I can trace every metric to a source and ingestion run so data issues are auditable.

## MVP Acceptance Criteria

- Landing page is polished and responsive.
- Users can browse player data.
- Users can filter by league, season, club, position, age, minutes, and nationality when available.
- Users can open player profile pages.
- Users can compare 2 to 5 players in a table.
- Users can view rankings by position and metric.
- Users can read metric definitions.
- Data source is legal and documented.
- Unsupported metrics are clearly marked.
- Percentiles are calculated consistently.
- No AI chat, radar chart, scatter plot, club analysis, or subscription flow exists.
- Backend and frontend validation commands pass for configured tooling.
- Planning and methodology documentation are complete.

## Phased Roadmap

### Phase 0: Data Validation and Scaffold

- Complete product, metrics, data source, design, architecture, and backlog docs.
- Validate API-Football and Sportmonks coverage, limits, and legal/cache terms.
- Lock metric availability and unsupported metric behavior.
- Create backend/frontend scaffolds using documented mock contracts.
- Build the first player database, profile, rankings, and comparison UI against mock data.

### Phase 1: Data Foundation

- Create backend project.
- Define database schema.
- Implement provider adapter interface.
- Build reproducible ingestion scripts.
- Add validation and metric calculation tests.
- Seed local SQLite or DuckDB database for MVP development.

### Phase 2: API and Contracts

- Build FastAPI endpoints.
- Document shared response contracts.
- Add filtering, ranking, comparison, and profile APIs.
- Add percentile calculation and minimum-minute thresholds.

### Phase 3: Frontend MVP

- Connect React + Vite + TypeScript frontend screens to API-backed data.
- Add Tailwind and a compact component system.
- Complete player database, profile, rankings, compare, glossary, methodology, and leagues pages.
- Use D3 only for small percentile bars and table mini visuals.

### Phase 4: Polish and Release

- Improve performance for table filters and search.
- Add loading, empty, error, unavailable, and approximation states.
- Run validation.
- Prepare simple deployment.
- Publish methodology and data source notes.

### Phase 5: Licensed Event Data

- Add licensed event data provider.
- Expand metric coverage.
- Replace approximations with exact calculations where possible.
- Add advanced visuals only when the underlying data supports them.
