# ScoutFootball Technical Architecture

## Architecture Summary

ScoutFootball should use a Python backend/API with a React + Vite frontend. The system should prioritize legal data ingestion, reproducible metric calculations, documented data contracts, and a fast table-first user experience.

GitHub repository: [https://github.com/matheusabrantes/scoutfootball.git](https://github.com/matheusabrantes/scoutfootball.git)

Recommended MVP architecture:

- Backend: Python, FastAPI, Pydantic, Pandas or Polars, SQLAlchemy.
- Local database: SQLite or DuckDB for MVP development.
- Production database: PostgreSQL.
- Frontend: React, TypeScript, Vite, Tailwind CSS.
- UI system: shadcn/ui or a similarly small component layer if it fits.
- Tables: TanStack Table.
- Visual utilities: D3.js for percentile bars and small inline distribution visuals.
- Testing: pytest for backend, frontend typecheck/lint/build, component tests if configured.

## Proposed Repository Structure

```text
scoutfootball/
  backend/
    app/
      api/
      core/
      db/
      models/
      services/
      metrics/
      ingestion/
      validation/
    tests/
    pyproject.toml

  frontend/
    src/
      components/
      pages/
      features/
      hooks/
      lib/
      styles/
      d3/
      types/
    package.json
    vite.config.ts

  docs/
    PRODUCT_PLAN.md
    DATA_SOURCE_RESEARCH.md
    DATA_CONTRACT.md
    METRICS_SPEC.md
    DESIGN_DIRECTION.md
    TECHNICAL_ARCHITECTURE.md
    IMPLEMENTATION_BACKLOG.md
```

## Backend Responsibilities

- Provider ingestion.
- Data cleaning and normalization.
- Data source tracking.
- Data validation checks.
- Metric calculation.
- Percentile calculation.
- Player filtering API.
- Player profile API.
- Ranking API.
- Comparison API.
- Methodology and metric metadata API.

## Frontend Responsibilities

- Premium responsive UI.
- Player database.
- Player profile pages.
- Player ranking pages.
- Comparison tables.
- Filters and search.
- Glossary page.
- Methodology page.
- D3 mini visuals where useful.

## Data Model

### Core Tables

| Table | Purpose |
| --- | --- |
| `leagues` | Supported competition metadata |
| `seasons` | Current and historical season metadata |
| `clubs` | Club identity and league-season membership |
| `players` | Stable player identity |
| `position_groups` | Canonical ScoutFootball position groups |
| `player_season_stats` | Normalized player season context |
| `metrics` | Metric definitions and display metadata |
| `player_metric_values` | Calculated metric values and percentiles |
| `data_sources` | Provider identity, terms notes, and attribution |
| `ingestion_runs` | Reproducible import audit trail |

### Important Fields

- `player_id`
- `player_name`
- `date_of_birth`
- `age`
- `nationality`
- `club_id`
- `league_id`
- `season_id`
- `position_group`
- `minutes_played`
- `metric_key`
- `metric_value`
- `percentile`
- `availability_status`
- `data_source_id`
- `ingestion_run_id`
- `calculation_version`
- `last_updated_at`

## API Design

Base path: `/api`

| Endpoint | Purpose |
| --- | --- |
| `GET /api/leagues` | List supported leagues and availability |
| `GET /api/seasons` | List supported seasons |
| `GET /api/clubs` | List clubs, filterable by league and season |
| `GET /api/players` | Search and filter player database |
| `GET /api/players/{player_id}` | Player profile, season context, metrics, percentiles |
| `GET /api/rankings` | Ranked players by position, metric, league, season, threshold |
| `GET /api/compare` | Compare 2 to 5 player ids |
| `GET /api/metrics` | Metric definitions, availability, position mapping |
| `GET /api/methodology` | Source, percentile, threshold, and approximation metadata |

Current implementation note: `/api/leagues`, `/api/players`, `/api/players/{player_id}`, `/api/rankings`, `/api/compare`, and `/api/metrics` are wired to SQLite. If no usable data has been ingested, the API returns a clear "Real data has not been ingested yet" style message instead of fake data.

## Query Contract Examples

### `GET /api/players`

Parameters:

- `q`
- `league_id`
- `season_id`
- `club_id`
- `position_group`
- `age_min`
- `age_max`
- `minutes_min`
- `nationality`
- `sort`
- `direction`
- `limit`
- `offset`

### `GET /api/rankings`

Parameters:

- `season_id`
- `league_id`
- `position_group`
- `metric_key`
- `minutes_min`
- `sort_by`: `raw_value` or `percentile`
- `direction`

### `GET /api/compare`

Parameters:

- `player_ids`: comma-separated list of 2 to 5 ids.
- `season_id`
- `league_id` optional, used for percentile context.

## Ingestion Approach

1. Fetch raw provider data into `backend/app/ingestion/raw/` or provider-specific object storage in production.
2. Normalize provider records into canonical database tables.
3. Store ingestion run metadata: provider, timestamp, source season, source league ids, code version, and row counts.
4. Run validation checks before publishing data.
5. Calculate metrics using versioned functions.
6. Calculate percentiles after all metric values are loaded.
7. Mark each metric as available, approximated, or unavailable.

## Metric Calculation Layer

Recommended modules:

- `backend/app/metrics/per90.py`
- `backend/app/metrics/percentiles.py`
- `backend/app/metrics/position_templates.py`
- `backend/app/metrics/availability.py`
- `backend/app/metrics/calculation_versions.py`

This layer needs focused unit tests because the product depends on correct football data.

## Validation Checks

Backend data checks:

- Required ids are present.
- Minutes are non-negative.
- Percentages are between 0 and 100.
- Per-90 values are null when minutes are zero.
- Player-season rows are unique by player, club, league, season, and provider.
- Percentiles are between 0 and 100.
- Unavailable metrics have null values.
- Approximated metrics include approximation notes.

Backend commands once configured:

```bash
cd backend
python -m pytest
python -m ruff check .
python -m mypy app
```

Frontend commands once configured:

```bash
cd frontend
npm run lint
npm run typecheck
npm run build
```

## Deployment Options

### Option A: Split Deployment

- Frontend on Vercel.
- Python API on Cloud Run, Render, Fly.io, or Railway.
- PostgreSQL hosted separately.

This is the recommended production shape when the API and ingestion jobs mature.

### Option B: Single Container

- One container serves FastAPI and the static React build.
- PostgreSQL remains external.

This is simpler for a small MVP and can reduce deployment overhead.

## Recommended MVP Deployment

Start with Option B if deployment speed matters most. Move to Option A when frontend release cadence, API scaling, or ingestion scheduling need independent operations.

Do not over-engineer infrastructure before the data source and metric coverage are proven.
