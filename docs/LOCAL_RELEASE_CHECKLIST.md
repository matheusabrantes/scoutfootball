# Local Release Checklist

Checklist date: 2026-06-14
Branch: `feature/local-release-validation`

| Item | Status | Command | Expected result | Actual result | Notes |
| --- | --- | --- | --- | --- | --- |
| Git state | pass | `git checkout main && git pull --ff-only origin main` | Local `main` includes merged StatsBomb MVP. | `main` fast-forwarded to merge commit `175f661`. | Old feature branch deleted locally and remotely after merge verification. |
| Feature branch | pass | `git checkout -b feature/local-release-validation` | New milestone branch exists. | Branch created. | Work continued off clean `main`. |
| Python environment | pass | `backend/.venv/bin/python --version` | Uses backend-local venv. | Python `3.9.6`, executable under `backend/.venv/bin/python`. | Clean setup command documented. |
| Backend install | pass | `python -m pip install -e ".[dev]"` | Editable backend + dev tools installed in venv. | Installed successfully. | No global Python install used. |
| Node environment | pass | `nvm use && node --version && npm --version` | Uses validated Node LTS. | Node `v24.16.0`, npm `11.13.0`. | Added `.nvmrc` and `engines`. |
| Frontend install | pass | `npm ci` | Lockfile reproducibly installs dependencies. | 141 packages installed. | `npm audit` warnings remain technical debt. |
| Git safety | pass | `git ls-files | grep -E '(\.env|\.sqlite|\.db|node_modules|data_sources/statsbomb_open)' || true` | No generated/private files tracked. | Only `.env.example` matched. | `.env.example` is safe and intentional. |
| StatsBomb download | pass | `python scripts/download_statsbomb_competition.py --competition-id 2 --season-id 27 --full` | 380 PL matches selected, no errors. | 380 events + 380 lineups downloaded from clean cache; 0 failures. | Disk usage `1085.98 MB` after clean download. |
| Aggregation | pass | `python scripts/build_statsbomb_player_season.py --competition-id 2 --season-id 27 --full` | Full PL player-season output generated. | 380 matches, 1,313,773 events, 550 aggregated rows, 20 teams. | Processing time `36.239s`. |
| Database initialization | pass | `python scripts/init_db.py` | SQLite schema created. | Initialized `backend/data/scoutfootball.db`. | DB is ignored by Git. |
| Ingestion | pass | `python scripts/ingest_statsbomb_players.py --competition-id 2 --season-id 27 --full` | Real PL rows ingested. | 549 inserted, 1 skipped, 0 failed. | 330 players above 900 minutes. |
| Idempotency | pass | Repeat ingestion command | No duplicate inserts. | 0 inserted, 549 updated, 1 skipped. | Confirms no duplicate player-season rows. |
| Percentiles | pass | `python scripts/calculate_percentiles.py --minimum-minutes 900` | Percentiles generated for eligible rows. | 24,777 updated, 0 skipped. | PL-only DB has 46,116 metric rows. |
| Bundesliga coverage | pass | Provider `list_matches(9, 281)` | Exact open-data match count known. | 34 matches. | Classified `sample_only`; do not present as complete Bundesliga. |
| Backend validation | pass | `compileall`, `pytest`, `ruff` | All checks pass. | 14 tests passed; ruff clean. | Includes config/CORS tests. |
| Frontend validation | pass | `npm run lint && npm run typecheck && npm run build` | TypeScript and production build pass. | Build passed; bundle generated. | No breaking Vite upgrade performed. |
| Backend run | pass | `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` | API runs locally. | `http://127.0.0.1:8000`. | CORS allows Vite local origins. |
| Frontend run | pass | `VITE_API_BASE_URL=http://127.0.0.1:8000 npm run dev -- --host 127.0.0.1 --port 5173` | UI runs locally. | `http://127.0.0.1:5173`. | Vite serves SPA fallback paths. |
| Browser validation | partial | Browser plugin setup | Browser automation available. | In-app browser reported unavailable: `iab`. | HTTP/API route validation used instead. |
| Route validation | pass | HTTP checks for `/`, `/players`, `/players/182`, `/rankings`, `/compare`, `/leagues`, `/methodology` | Vite returns app for all paths. | All returned 200 and app HTML. | Direct URL routing added. |
| API validation | pass | Local smoke script | Real data visible through API. | Search, filters, profile, rankings, compare 2/5, empty results, invalid player, unavailable metric passed. | No mock fallback used. |
| Attribution | pass | UI/docs review | Data pages identify historical StatsBomb source. | Data pages show historical dataset/source labels. | Logo use still needs permission check before public deployment. |
| Docker config | blocked locally | `docker --version && docker compose config` | Compose file is valid when Docker is installed. | `docker: command not found`. | Docker files were added, but this machine cannot execute Docker validation until Docker Desktop/CLI is installed. |
| Known limitations | pass | Docs update | Release caveats are explicit. | Vite audit, StatsBomb historical scope, Bundesliga sample-only, estimated minutes documented. | No public deployment yet. |

## Docker Initialization Flow

Build and start empty containers:

```bash
docker compose build
docker compose up
```

Initialize real data in the backend container:

```bash
docker compose run --rm backend python scripts/download_statsbomb_competition.py --competition-id 2 --season-id 27 --full
docker compose run --rm backend python scripts/build_statsbomb_player_season.py --competition-id 2 --season-id 27 --full
docker compose run --rm backend python scripts/init_db.py
docker compose run --rm backend python scripts/ingest_statsbomb_players.py --competition-id 2 --season-id 27 --full
docker compose run --rm backend python scripts/calculate_percentiles.py --minimum-minutes 900
```

The compose setup stores SQLite and StatsBomb cache in named volumes and does not bake raw data into images.
