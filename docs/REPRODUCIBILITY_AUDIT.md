# Reproducibility Audit

Audit date: 2026-06-14
Branch: `feature/local-release-validation`
Base: merged `main` after PR #1, `Add StatsBomb historical real-data MVP`

## Summary

A clean clone can reproduce ScoutFootball if the developer installs backend and frontend dependencies, downloads StatsBomb Open Data, initializes SQLite, ingests the selected season, and calculates percentiles. Raw StatsBomb files and SQLite databases are intentionally excluded from Git.

## Findings

| Area | Classification | Finding | Resolution |
| --- | --- | --- | --- |
| Git-tracked generated data | acceptable | `.env`, local DBs, downloaded StatsBomb JSON, generated CSV/Parquet, `node_modules`, caches, and frontend build output are ignored. | Verified with `git ls-files` safety check. |
| Python environment | important | Backend setup requires `backend/.venv`; global Python installs are unsafe. | README documents project-local venv. Validation used `/backend/.venv/bin/python`. |
| Node version | important | Frontend previously did not pin the validated Node version. | Added `.nvmrc` and `engines` for Node `24.16.0`, npm `11.13.0`. |
| Backend env examples | blocking | Clean deployment needed safe examples for DB, CORS, StatsBomb data directory, and environment name. | Added `backend/.env.example` and expanded root `.env.example`. |
| Frontend env examples | blocking | Vite API base URL was configurable but undocumented as a frontend env file. | Added `frontend/.env.example` with `VITE_API_BASE_URL`. |
| CORS | blocking | Backend CORS allowed only hardcoded local origins. | Added `CORS_ALLOWED_ORIGINS` setting with local defaults. |
| SQLite path | important | Backend used `SCOUTFOOTBALL_DB_PATH`; deployment requested `DATABASE_URL`. | Added `DATABASE_URL` support for SQLite paths. |
| StatsBomb cache path | important | StatsBomb provider default path needed deployment configurability. | Added `STATSBOMB_DATA_DIR` support and tests. |
| Existing SQLite dependency | acceptable | API can start with an empty DB, but real data is unavailable until ingestion runs. | Release checklist documents initialization and ingestion. |
| Downloaded StatsBomb dependency | acceptable | Clean clone has no raw JSON. Full real-data setup must download StatsBomb Open Data. | README and checklist document the pipeline. |
| Frontend routing | blocking | State-only navigation did not validate direct `/players`, `/rankings`, `/players/:id` URLs. | Added URL-aware SPA navigation and profile page. |
| Player profile UI | blocking | Backend had `/api/players/{id}` but frontend had no profile page. | Added minimal player profile page using real metrics. |
| Filters/sorting | important | Release validation required competition, season, team, position, minutes, and sortable player tables. | Added competition/season/team filters and simple player sorting. |
| Browser tooling | minor | In-app browser plugin was unavailable in this session. | Used HTTP/API/Vite route validation; no screenshots committed. |
| Vite/esbuild audit | important | `npm audit --omit=dev` reports Vite/esbuild dev-server advisories; suggested fix is breaking Vite major upgrade. | Documented as technical debt; no breaking upgrade performed. |
| Docker | important | No container setup existed for local release validation. | Added backend/frontend Dockerfiles, `docker-compose.yml`, `.dockerignore`, and docs. |

## Clean Clone Reproduction Commands

```bash
git clone https://github.com/matheusabrantes/scoutfootball.git
cd scoutfootball
```

Backend:

```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Frontend:

```bash
cd frontend
nvm use
npm ci
```

Data:

```bash
cd backend
. .venv/bin/activate
python scripts/download_statsbomb_competition.py --competition-id 2 --season-id 27 --full
python scripts/build_statsbomb_player_season.py --competition-id 2 --season-id 27 --full
python scripts/init_db.py
python scripts/ingest_statsbomb_players.py --competition-id 2 --season-id 27 --full
python scripts/calculate_percentiles.py --minimum-minutes 900
```

Run locally:

```bash
cd backend
. .venv/bin/activate
python -m uvicorn app.main:app --reload
```

```bash
cd frontend
VITE_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```
