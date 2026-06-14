# Historical Demo Release

ScoutFootball MVP scope: historical real-data player analytics powered by StatsBomb Open Data.

## Selected Competitions

P0:

- Premier League 2015/2016, `competition_id=2`, `season_id=27`, 380 matches available.
- Bundesliga 2023/2024, `competition_id=9`, `season_id=281`, 34 matches available, incomplete but recent.

P1:

- La Liga 2015/2016.
- Serie A 2015/2016.
- Ligue 1 2015/2016, close to complete with 377 matches.

## Supported Metrics

The MVP calculates event-derived metrics including minutes, appearances, starts, goals, non-penalty goals, assists, shots, shots on target, xG, npxG, key passes, passing totals, forward passes, progressive passes, progressive carries, crosses, dribbles, touches in box, interceptions, blocks, ball recoveries, duels, saves, cards, and per-90 versions for count metrics.

## Unsupported Metrics

Unavailable or intentionally null in the initial MVP:

- Direct xA.
- PSxG.
- PSxG minus goals allowed.
- Possession-adjusted interceptions, tackles, or possession won.
- Fully validated aerial duel percentages.

## Historical Nature

The MVP does not claim current-season coverage. Every UI and API response should label relevant StatsBomb rows as a historical dataset.

## Current Local Dataset Snapshot

Validation date: 2026-06-14.

| Competition | Matches processed | Player-season rows | Players above 900 minutes | Status |
| --- | ---: | ---: | ---: | --- |
| Premier League 2015/2016 | 380/380 | 549 | 330 | Complete historical season |
| Bundesliga 2023/2024 | 34 open-data matches | 372 | 17 | Incomplete curated open-data sample |

Combined local SQLite snapshot after both ingestions:

- Players: 914.
- Player-season rows: 921.
- Teams: 38.
- Metric rows: 77,364.
- Metric rows with calculated percentiles at the 900-minute threshold: 25,227.

## Attribution

Data source: StatsBomb Open Data.

Before public deployment, verify whether the official StatsBomb logo from the media pack must be displayed on the footer or methodology page. Do not commit third-party logo assets until usage permission is verified.

## Local Setup

```bash
cd backend
source .venv/bin/activate
```

## Download

```bash
python scripts/download_statsbomb_competition.py \
  --competition-id 2 \
  --season-id 27 \
  --full
```

For the incomplete recent Bundesliga sample:

```bash
python scripts/download_statsbomb_competition.py \
  --competition-id 9 \
  --season-id 281 \
  --full
```

## Aggregation

```bash
python scripts/build_statsbomb_player_season.py \
  --competition-id 2 \
  --season-id 27 \
  --full
```

## Ingestion

```bash
python scripts/init_db.py
python scripts/ingest_statsbomb_players.py \
  --competition-id 2 \
  --season-id 27 \
  --full
python scripts/calculate_percentiles.py --minimum-minutes 900
```

Additional percentile thresholds can be recalculated as needed:

```bash
python scripts/calculate_percentiles.py --minimum-minutes 300
python scripts/calculate_percentiles.py --minimum-minutes 500
python scripts/calculate_percentiles.py --minimum-minutes 900
python scripts/calculate_percentiles.py --minimum-minutes 1500
```

## Backend Run

```bash
uvicorn app.main:app --reload
```

## Frontend Run

```bash
cd frontend
npm install
VITE_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

## Known Limitations

- Premier League 2015/2016 is the primary complete historical demo season.
- Bundesliga 2023/2024 is useful as a recent sample, but StatsBomb Open Data only exposes 34 matches locally, so it is not full Bundesliga coverage.
- Minutes are currently `estimated`; reconciliation error is low, but official provider minutes should be added before broader public ranking claims.
- Direct xA and PSxG are not available in the open event schema.
- StatsBomb Open Data coverage is curated and does not cover the full ScoutFootball target list.
- `npm audit --omit=dev` reports Vite/esbuild development-server advisories. The suggested automated fix upgrades to a breaking Vite major version and should be handled separately.

## Future Expansion

- Add P1 complete historical leagues.
- Harden minute reconciliation.
- Add provider-neutral event interfaces for future licensed feeds.
