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
  --limit-matches 5
```

For the full selected season:

```bash
python scripts/download_statsbomb_competition.py \
  --competition-id 2 \
  --season-id 27 \
  --full
```

## Aggregation

```bash
python scripts/build_statsbomb_player_season.py \
  --competition-id 2 \
  --season-id 27 \
  --limit-matches 5
```

## Ingestion

```bash
python scripts/init_db.py
python scripts/ingest_statsbomb_players.py \
  --competition-id 2 \
  --season-id 27 \
  --limit-matches 5
python scripts/calculate_percentiles.py --minimum-minutes 300
```

For public-like rankings, use full ingestion and:

```bash
python scripts/calculate_percentiles.py --minimum-minutes 900
```

## Backend Run

```bash
uvicorn app.main:app --reload
```

## Frontend Run

```bash
cd frontend
npm install
npm run dev
```

## Known Limitations

- Current data slice processes 5 Premier League 2015/2016 matches locally.
- Full rankings require full-season download and ingestion.
- Minutes are currently `estimated` until team-minute reconciliation is hardened.
- Direct xA and PSxG are not available in the open event schema.
- StatsBomb Open Data coverage is curated and does not cover the full ScoutFootball target list.

## Future Expansion

- Run full Premier League 2015/2016 ingestion.
- Add Bundesliga 2023/2024 as an incomplete recent historical dataset.
- Add P1 complete historical leagues.
- Harden minute reconciliation.
- Add provider-neutral event interfaces for future licensed feeds.
