# ScoutFootball

ScoutFootball is a free web-only football player analytics platform focused on selected leagues, real provider data, and clear player-level metrics.

## Stack

- Backend: Python, FastAPI, SQLite for MVP development.
- Data provider: API-Football / API-SPORTS as primary.
- Future backup provider: Sportmonks.
- Frontend: React, Vite, TypeScript, D3 for small percentile visuals.

## Environment

Create a local `.env` file from `.env.example`.

Required:

```bash
API_FOOTBALL_KEY=
API_FOOTBALL_BASE_URL=https://v3.football.api-sports.io
SCOUTFOOTBALL_DB_PATH=backend/data/scoutfootball.db
```

Never commit `.env`.

## Backend Setup

Use a project-local backend virtual environment. Do not install backend dependencies into
the global macOS Python environment.

From the project root:

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python scripts/init_db.py
```

Run the API:

```bash
cd backend
. .venv/bin/activate
python -m uvicorn app.main:app --reload
```

## API-Football Validation

Focused South America validation:

```bash
cd backend
python3 scripts/investigate_api_football_south_america.py
```

General validation:

```bash
cd backend
python3 scripts/validate_api_football.py
```

## FBref / soccerdata Investigation

`soccerdata` is optional during the provider investigation phase and must be installed
inside `backend/.venv`.

Install when ready:

```bash
cd backend
. .venv/bin/activate
python -m pip install -e ".[providers]"
```

Then run:

```bash
python scripts/investigate_soccerdata_fbref.py
```

Investigation result from 2026-06-12: `soccerdata 1.8.8` installed successfully in
`backend/.venv`, but FBref returned `403 Forbidden` for `https://fbref.com/en/comps/`
before table inspection. The script now records this as a safe metadata result and does
not continue into table retries. API-Football remains the metadata/basic fallback while
advanced metrics require a licensed provider or vetted bootstrap dataset.

## Ingestion

Safe first run, one provider page per active league:

```bash
cd backend
python3 scripts/ingest_api_football_players.py --limit-pages 1
```

Full pagination, only after request budget is acceptable:

```bash
cd backend
python3 scripts/ingest_api_football_players.py --full
```

Current known limitation: API-Football returns player rows for the active MVP leagues, but the tested free-plan responses returned null values for supported metric fields. The ingestion skips rows where every supported MVP metric is null.

## Percentiles

```bash
cd backend
python3 scripts/calculate_percentiles.py --minimum-minutes 500
```

Percentiles are grouped by league, season, position group, and metric. They are skipped when there are too few valid peers or no non-null metric values.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Validation:

```bash
npm run lint
npm run typecheck
npm run build
```

## MVP Routes

Backend:

- `GET /health`
- `GET /api/leagues`
- `GET /api/players`
- `GET /api/players/{player_id}`
- `GET /api/rankings`
- `GET /api/compare`
- `GET /api/metrics`

Frontend:

- Landing
- Players
- Rankings
- Compare
- League coverage
- Methodology

## Active MVP Leagues

All active MVP leagues currently use API-Football season `2024`:

- Brasileirao Serie A
- Argentina Primera Division
- Premier League
- La Liga
- Bundesliga

Serie A Italy and Ligue 1 remain blocked until a season/endpoint returns usable player metric values.
