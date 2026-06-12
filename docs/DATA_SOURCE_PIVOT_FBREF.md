# Data Source Pivot: FBref and Low-Cost Public Data

## Why We Are Pivoting

API-Football is useful for league, team, player identity, and metadata validation, but the tested `/players` responses returned real player objects with null values for the main player metrics. That makes it unsafe to build ScoutFootball's analytic MVP on API-Football alone right now.

Sportmonks remains a plausible backup, but it is too expensive for this early personal weekend project.

The new data strategy prioritizes low-cost and free public sources for a non-commercial project:

- FBref via `soccerdata`.
- Understat via `soccerdata` for xG/xA in top European leagues.
- Kaggle FBref-style datasets as optional bootstrap data.
- API-Football as metadata fallback only.

Rules:

- Do not bypass login, paywalls, captchas, Cloudflare, private APIs, or authentication.
- Do not overload websites.
- Use polite scraping, caching, and rate limits.
- Prefer maintained open-source libraries instead of fragile custom scrapers.
- Store only safe metadata during investigation: table names, columns, row counts, seasons, competitions, and small non-sensitive samples.

## Source Comparison

| Source | Cost | Coverage | Player metrics depth | xG/xA | South America | Risk | MVP fit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| API-Football | Free tier plus paid plans | Broad league metadata and player objects | Tested responses returned null metric values | Not confirmed in current plan | League/player objects exist, metrics null in tests | Low API integration risk, metric-depth blocker | Metadata fallback only for now |
| FBref via soccerdata | Free public site access through open-source library | Strong top European coverage; South America depends on FBref availability/library support | Strong standard, shooting, passing, defense, possession, playing time, misc, keeper tables | Often available as xG, npxG, xAG depending on table/league | Needs investigation | Moderate terms/rate-limit risk; must be polite and cache | Primary candidate |
| Understat via soccerdata | Free public site access through open-source library | Mainly top European leagues | Good xG/xA shot/player data, weaker all-around scouting profile | Strong for xG/xA | Not enough for target South America | Moderate scraping/terms risk | Complement for European xG/xA |
| Kaggle FBref datasets | Free, dataset-dependent | Usually top European historical seasons | Can be rich if dataset is well-formed | Dataset-dependent | Usually limited | License/provenance risk per dataset | Optional bootstrap only |
| worldfootballR | Free R package | Strong football web data workflows | Good if R workflow is acceptable | Depends on source | Depends on source | Adds R dependency and similar scraping risks | Research/reference, not first Python MVP |
| ScraperFC | Free Python library | Multiple football sources | Depends on source and maintained modules | Depends on source | Unknown until tested | Scraper maintenance risk | Backup investigation candidate |
| football-data.org | Free/paid API | Strong competitions, fixtures, standings | Weak for player analytics | No meaningful player xG/xA | Some metadata coverage | Low API risk, weak metric depth | Metadata/reference only |
| StatsBomb Open Data | Free open data | Curated competitions/seasons | Very strong event data where available | Event-derived xG available in data | Not broad/current enough for target MVP | Low if attribution/license followed | Prototyping and tests, not main MVP |

## Preferred Investigation Order

1. Test `soccerdata` with FBref for Premier League and one South American league.
2. If FBref works, inspect table availability and columns.
3. Map FBref columns to ScoutFootball metrics.
4. Use Understat via `soccerdata` only as a complement for European xG/xA.
5. Keep API-Football for metadata fallback, league ids, teams, and identity where useful.

## Decision Framework

Classify the data strategy as one of:

- `fbref_first_viable`
- `fbref_europe_only_viable`
- `fbref_plus_api_football_viable`
- `kaggle_bootstrap_required`
- `not_viable_without_paid_provider`

Decision rules:

- If FBref/soccerdata gives rich player metrics for top European leagues, use it for Europe.
- If FBref/soccerdata gives Brazil and Argentina, use it for South America too.
- If South America is missing, use API-Football for basic South America metadata only and mark advanced South America metrics as unavailable.
- If Kaggle gives a faster top-five European bootstrap, use it only as optional seed data and document dataset source and license risk.

