# ScoutFootball Data Source Research

Research snapshot: 2026-06-12

## Executive Summary

ScoutFootball should not ingest, scrape, mirror, or infer data from DataMB. Public inspection of DataMB shows league, club, player, radar, plot, and guide functionality, but I did not find a public statement that identifies its underlying provider. The available metric mix resembles event-data products such as Wyscout, Opta/Stats Perform, StatsBomb-style feeds, or derived FBref-style tables, but that is an inference, not a confirmed source.

The MVP should use a legally documented provider and show only supported metrics. The most practical path is:

1. Use a paid API with explicit product terms for current-season operational data, likely API-Football or Sportmonks.
2. Keep an ingestion adapter interface so a future Wyscout, Opta, or StatsBomb licensed feed can replace or augment the MVP source.
3. Mark unavailable event metrics clearly until the project has licensed event data.

## Reference Site Investigation

Observed public DataMB properties:

- DataMB publicly lists players, teams, Pro, supported leagues, mobile app links, and a guide page.
- Public homepage coverage includes Premier League, La Liga, Bundesliga, Serie A, Ligue 1, Eredivisie, and Liga Portugal.
- The public guide exposes player visual/stat concepts, but no obvious source attribution was found during this research pass.
- No private endpoint, authenticated page, hidden API, or protected asset should be inspected or scraped for ScoutFootball.

Sources:

- [DataMB homepage](https://datamb.football/)
- [DataMB guide](https://datamb.football/guide/)

## Practical MVP Decision Matrix

| Source | League Coverage For Target Leagues | Current Season Support | Last Completed Season Support | Player-Level Statistics | Advanced Metrics | API Limits | Free Tier Limitations | Paid Plan Likely Needed | Legal / Commercial Usage Risk | Storage / Cache Restrictions | Fit For MVP | Main Blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| API-Football | Public coverage list includes England Premier League, Spain La Liga, Germany Bundesliga, France Ligue 1, Brazil Serie A, Argentina Liga Profesional, Colombia Primera A, Chile Primera Division, and Uruguay Primera Division variants. Italy Serie A, Eredivisie, and Liga Portugal should be verified by league id before selection. | Yes, provider positions itself around live/current football API data. | Yes for paid plans; free plans are limited by available seasons. | Lists players/coaches, statistics, events, lineups, top scorers, teams, and fixtures. | Some advanced fields may exist, but exact ScoutFootball metrics need endpoint validation. xG/xA, progressive actions, PSxG, possession-adjusted values, touches in box, and duel taxonomy are not guaranteed. | Free: 100 requests/day. Pro: 7,500/day. Ultra: 75,000/day. Mega: 150,000/day. | Low request volume and limited seasons. | Yes for a useful MVP and repeatable validation. | Medium until account terms confirm public/free web display, commercial usage, and caching rights. | Must confirm terms for local database storage, retention, redistribution, and public display. | Best practical first validation candidate because it has broad target-league coverage and low-cost paid tiers. | Need a real API key/schema test to confirm player-stat depth and cache/display permissions. |
| Sportmonks | Claims 2,500+ leagues and includes major global competitions; target leagues likely fit, but the 12 exact leagues must be selected and validated. Starter allows only 5 leagues, Growth 30 leagues, Pro 120 leagues. | Yes, live data and current-season API are core product features. | Yes depending on plan; Enterprise mentions historical data included and other plans may require add-ons or plan-specific access. | Explicitly includes teams, player data, rankings, player and coach statistics, season statistics, lineups, and events. | Advanced statistics are listed; xG is a separate recommended bundle/add-on with player xG, team xG, xGOT, xPTS, npxG, and more. Event-style ScoutFootball metrics still require schema validation. | Starter: 2,000 API calls per entity/hour. Growth: 2,500/entity/hour. Pro: 3,000/entity/hour. Enterprise: 5,000/entity/hour. | Free plan/trial is useful for validation, not full MVP operations. | Yes. Growth is the first obviously comfortable plan for 12 target leagues; xG bundle may be needed. | Medium until terms confirm public/free web display and caching. | Must confirm retention and derived-stat storage rights. | Strong MVP candidate, especially if player-stat schema is richer than API-Football. | Higher monthly cost and need to confirm whether historical/current target leagues plus advanced metrics fit one plan. |
| football-data.org | Free tier covers Premier League, La Liga, Bundesliga, Serie A, Ligue 1, Eredivisie, Primeira Liga, and Brazil Serie A. All-competition list includes Argentina, Chile, Colombia, Uruguay, and more. | Yes for fixture/standing style data. | Paid/history support varies by tier; ML Pack Light lists 10 seasons of history. | Weak for ScoutFootball's player analytics. Paid tiers include squads, lineups, substitutions, goal scorers, bookings/cards; statistics add-on is mostly match/team events like corners, fouls, saves, shots. | Not enough for position-specific player metrics. | Free tier lists 10 calls/minute. Higher tiers list 20-120 calls/minute. | Free competition coverage is useful, but data depth is not enough for player analytics. | Yes if used beyond free fixtures/standings, but not sufficient as primary player source. | Medium; API terms still need review for public display and storage. | Must confirm storage/display rights. | Good backup/reference source for leagues, clubs, fixtures, and standings. Weak primary MVP fit. | Does not provide enough player-level advanced statistics for ScoutFootball's MVP. |
| StatsBomb Open Data | Curated open competitions/seasons only; not a full current-season product across the 12 target leagues. | No reliable current-season support. | Some historical competitions/seasons only. | High-quality event and lineup data for included matches. | Strong event data for prototyping many calculations; selected 360 data exists for some matches. | GitHub/raw file access, not a production API. | Free data is limited by competition/season availability. | No for open-data prototyping; paid commercial StatsBomb would be separate. | Low if license/attribution terms are followed, but not suitable for live public current-season coverage. | Must follow StatsBomb attribution and logo requirements for published analysis. | Excellent for tests, prototypes, calculation examples, and validation fixtures. Not enough as MVP source. | Coverage does not match current + last completed season across target leagues. |
| FBref / public scraping | Broad public tables for many major leagues. South American and lower-coverage fields may vary. | Often current. | Often historical. | Strong public aggregate tables in many competitions, but no official API. | Some advanced tables exist; definitions and availability vary. Event-level needs are not fully covered. | Website access, no official API limits for a product integration. | Free public pages, but use at scale is not equivalent to licensed data. | No paid official API path for this use case; a compliant licensed route would need confirmation. | High. Scraping and redistribution risk; must respect terms, robots, rate limits, and source attribution. | Cache/storage rights are unclear without explicit permission. | Not recommended as primary MVP source. Could be used only if legal review confirms safe access and public reuse. | Legal/commercial reuse and automated extraction risk. |
| TheSportsDB | Broad sports API, but not clearly aligned with deep player football analytics for the target metrics. | Yes for some sports data. | Unknown for target depth. | Basic sports/player/team data; not enough evidence for ScoutFootball metric coverage. | Not sufficient for advanced football metrics. | Free API plus premium key for more features. | Free access exists but with limited features. | Probably yes for production, but still not enough metric depth. | Medium until terms and data provenance are reviewed. | Must confirm display/cache terms. | Useful for lightweight metadata experiments only. | Insufficient player-stat depth for ScoutFootball. |
| Opta / Stats Perform | Enterprise global coverage, likely strongest professional fit. | Yes by contract. | Yes by contract. | Deep live, historical, player, event, tracking, and advanced products. | Strong; includes xG, tracking/vision, predictions, player props, and proprietary advanced metrics depending on product. | Contract-specific. | None for MVP. | Yes, enterprise contract. | Low after contract, high before contract. | Contract-specific. | Best long-term premium provider. Not practical for low-cost MVP unless budget is available. | Cost and sales/legal process. |
| Wyscout / Hudl | Enterprise scouting data category with broad football coverage. | Likely by contract. | Likely by contract. | Strong player scouting and event data likely available under commercial products. | Strong fit for duels, progressive actions, scouting taxonomies, and event-derived metrics if licensed. | Contract-specific. | None for MVP. | Yes, commercial contract. | Low after contract, high before contract. | Contract-specific. | Strong Phase 2 provider for DataMB-like metric depth without copying DataMB. | Cost, contract, and API/data export terms. |

Sources:

- [API-Football pricing](https://www.api-football.com/pricing)
- [API-Football coverage](https://www.api-football.com/coverage)
- [Sportmonks Football API](https://www.sportmonks.com/football-api/)
- [football-data.org coverage](https://www.football-data.org/coverage)
- [football-data.org pricing](https://www.football-data.org/pricing)
- [StatsBomb Open Data](https://github.com/statsbomb/open-data)
- [worldfootballR documentation](https://worldfootballr.sportsdataverse.org/)
- [TheSportsDB free sports API](https://www.thesportsdb.com/free_sports_api)
- [Opta Data by Stats Perform](https://www.statsperform.com/products/opta-data/)

## Requested League Coverage

| League | API-Football | Sportmonks | football-data.org | StatsBomb Open Data | FBref/Public Tables | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Premier League | Listed | Likely | Free tier | Not current/full | Likely | Strong coverage across paid APIs |
| La Liga | Listed | Likely | Free tier | Not current/full | Likely | Strong coverage across paid APIs |
| Bundesliga | Listed | Likely | Free tier | Historical open samples | Likely | StatsBomb Open Data includes Bundesliga historical samples |
| Serie A Italy | Verify exact listing/league id | Likely | Free tier | Not current/full | Likely | Strong paid API fit, but API-Football exact league id must be verified |
| Ligue 1 | Listed | Likely | Free tier | Not current/full | Likely | Strong paid API fit |
| Eredivisie | Verify exact listing/league id | Likely | Free tier | Not current/full | Likely | Verify paid provider player-stat granularity |
| Liga Portugal | Verify exact listing/league id | Likely | Free tier as Primeira Liga | Not current/full | Likely | Verify naming and league id |
| Brasileirao Serie A | Listed as Brazil Serie A | Likely | Free tier | Not current/full | Mixed | Verify player-stat granularity |
| Argentina Primera Division | Listed as Liga Profesional Argentina | Likely | Listed in all-competitions table | Not current/full | Mixed | Verify season calendar handling |
| Colombia Categoria Primera A | Listed as Primera A | Likely | Listed in all-competitions table | No | Mixed | Paid provider likely needed |
| Uruguay Primera Division | Listed as Apertura/Clausura | Likely | Listed in all-competitions table | No | Mixed | Paid provider likely needed |
| Chile Primera Division | Listed | Likely | Listed in all-competitions table | No | Mixed | Paid provider likely needed |

Coverage must be verified through provider-specific league ids before implementation. "Likely" means public provider material claims broad competition coverage, not that a legal ScoutFootball subscription has been purchased or confirmed.

## Metric Availability Assessment

### Metrics We Can Calculate Directly From Common Player Stat APIs

These are likely possible if the provider includes player season totals and minutes:

- Per-90 rates: goals, non-penalty goals if penalty goals are available, assists, passes, completed passes, saves, interceptions, crosses, key passes.
- Percentages: save percentage, pass completion, long pass accuracy, short pass completion, aerial duel win percentage, defensive duel win percentage if won/attempted counts exist.
- Derived percentiles by league, season, position group, and minimum minutes threshold.
- Goal conversion percentage if shots and goals are available.

### Metrics That Require Approximation

These may need provider-specific mapping:

- Possession won per 90: can be approximated from tackles won, interceptions, recoveries, and duels won if exact possession-regain events are absent.
- Forward passes completed per 90: may be approximated from progressive/long/final-third passes if pass direction is missing.
- Forward pass completion percentage: requires event-level pass vectors; aggregate APIs may not support it.
- Accurate crosses per 90: direct if accurate cross totals exist; otherwise approximate from successful crosses.
- Touches in box per 90: direct only if provider exposes touches by zone; otherwise unavailable.
- Offensive duels won per 90: direct only in Wyscout-style event vocabularies; may be approximated from dribbles and attacking duels if exposed.

### Metrics Not Available Without Paid Event or Tracking Data

These should be marked unavailable in Phase 1 unless licensed:

- Progressive carries per 90 with exact carry progression.
- Progressive passes completed per 90 if aggregate progressive pass fields are absent.
- Defensive duels won percentage in a Wyscout-compatible definition.
- Offensive duels won per 90 in a Wyscout-compatible definition.
- Possession-adjusted interceptions.
- Prevented goals / PSxG minus goals against per 90 unless post-shot xG is licensed.
- Advanced off-ball metrics, pressure, and tracking-derived movement metrics.

## Final Recommendation

Recommended MVP path:

1. Primary source: API-Football for the first validation pass because it appears to cover most target leagues publicly, has low-cost paid tiers, and exposes player/statistics/events endpoints. Initial validation on 2026-06-12 found usable player-stat samples for Premier League, La Liga, and Bundesliga. A focused South America follow-up found usable league-level player-stat samples for Brasileirao Serie A and Argentina Primera Division when testing season 2024.
2. Backup source: Sportmonks because it has strong football API positioning, player statistics, advanced statistics, and league-selection plans. Keep it future/backup only for now because it is too expensive for this early MVP.
3. Metrics fully supported: basic identity, league/club/season context, minutes, goals, assists, cards, appearances, goalkeeper saves if exposed, basic shots, basic passes, basic duels, crosses, and per-90/percentage/percentile calculations derived from available totals.
4. Metrics partially supported: xG/xA/npxG depending on paid plan/add-on, successful dribbles, key passes, long/short pass completion, aerial/defensive duel rates, possession won, forward passes, accurate crosses, and goal conversion. These require provider field mapping before committing UI labels.
5. Metrics unavailable without paid event data: exact progressive carries, exact progressive passes under a stable definition, possession-adjusted interceptions, PSxG minus goals against, touches in box, offensive duels in a Wyscout-style taxonomy, tracking/off-ball metrics, and any provider-proprietary performance index.
6. Recommended next validation task: create a source-validation spreadsheet or script checklist that tests API-Football and Sportmonks against the 12 target leagues, current season, last completed season, player season stats, xG/xA availability, event fields, API limits, storage/cache permissions, and public display rights. Use only mock data for frontend/backend scaffold until this is complete.

Show unsupported metrics as "Unavailable" rather than approximating silently.

## API-Football Validation Result: 2026-06-12

Validation run:

- Requests used by validation script: 24.
- P0 leagues checked: Brasileirao Serie A, Argentina Primera Division, Premier League, La Liga, Bundesliga, Serie A Italy, Ligue 1.
- P1/P2 leagues were not checked after P0 failed the MVP acceptance rule.
- Safe metadata only was saved locally; no large raw provider dump is committed.

| League | Priority | API-Football League ID | Seasons Checked | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| Brasileirao Serie A | P0 | 71 | 2026, 2025 | Blocked | League exists, but no player statistics sample was returned. |
| Argentina Primera Division | P0 | 128 | 2026, 2025 | Blocked | League exists, but no player statistics sample was returned. |
| Premier League | P0 | 39 | 2025, 2024 | Validated | Player statistics sample returned. |
| La Liga | P0 | 140 | 2025, 2024 | Validated | Player statistics sample returned. |
| Bundesliga | P0 | 78 | 2025, 2024 | Validated | Player statistics sample returned. |
| Serie A Italy | P0 | 135 | 2026, 2025 | Blocked | League exists, but no player statistics sample was returned. |
| Ligue 1 | P0 | 61 | 2026, 2025 | Blocked | League exists, but no player statistics sample was returned. |

Initial MVP acceptance result: failed before South America season investigation because Brasileirao Serie A and Argentina Primera Division did not return 2026 or 2025 player-stat samples.

Confirmed player-stat field groups from validated leagues:

- Identity: player id, name, first name, last name, age, birth date/place/country, nationality, height, weight, injury status, photo.
- Team/club: team id, name, logo.
- League/season: league id, name, country, season, logo, flag.
- Position: games position, rating.
- Minutes/appearances: appearances, lineups, minutes, shirt number, captain flag.
- Attacking: goals, assists, total shots, shots on target.
- Passing: total passes, key passes, pass accuracy.
- Defensive: tackles, blocks, interceptions.
- Duels: total duels, duels won.
- Dribbling: dribble attempts, successful dribbles, dribbled past.
- Goalkeeper: saves, goals conceded.
- Discipline: yellow cards, second yellow cards, red cards, penalties won/committed/scored/missed/saved.

## South America API-Football Validation

Follow-up investigation date: 2026-06-12.

Requests used by investigation script: 9.

Provider status from `/status`:

- Plan: Free.
- Subscription active: true.
- Daily request limit: 100.
- Requests current at status call: 24.

| League | Candidate ID | Provider Name | Country | API Seasons Listed | Current Season Marked By API | Seasons Tested | League-Level Player Stats | Team-Level Fallback | Correct Working Season | Page 1 Results | Total Pages | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Brasileirao Serie A | 71 | Serie A | Brazil | 2010-2026 | 2026 | 2026, 2025, 2024 | Works | Not needed | 2024 | 20 | 58 | Usable |
| Argentina Primera Division | 128 | Liga Profesional Argentina | Argentina | 2015-2026 | 2026 | 2026, 2025, 2024 | Works | Not needed | 2024 | 20 | 85 | Usable |

Finding:

- The league metadata is valid for both countries.
- API-Football marks 2026 as current for both leagues.
- `/players?league={league_id}&season=2026` and `/players?league={league_id}&season=2025` returned no players for both leagues.
- `/players?league={league_id}&season=2024` returned player statistics for both leagues.
- Team-level fallback was not required because the league-level endpoint works for 2024.
- The same player field groups were available as in validated European leagues: identity, team/club, league/season, position, minutes/appearances, attacking, passing, defensive, duels, dribbling, goalkeeper, and discipline.

API-Football viability classification: `usable_for_full_mvp`.

Recommendation: Proceed with API-Football MVP ingestion, but record the actual provider season used per league and do not imply that Brazil/Argentina current-season player stats are available until API-Football returns them.

### Phase 2: Paid Event-Data Integration

Add a licensed provider such as Wyscout, Opta/Stats Perform, or a StatsBomb commercial feed when budget and terms are clear. This unlocks event-derived metrics, more stable definitions, and premium scouting-grade depth.

### Phase 3: ScoutFootball Proprietary Metrics

Create original metrics only after source licensing is solved:

- Weighted position percentile score.
- Minutes-adjusted confidence factor.
- Similar-player embeddings.
- Role-adjusted player profiles.

Any proprietary index must be named and documented as ScoutFootball's own model and must not copy DataMB's Performance Index.

## Legal Rules For Implementation

- Do not scrape DataMB.
- Do not copy DataMB content, layout, CSS, logo, wording, or private data.
- Do not use paid provider data without an active license.
- Do not bypass authentication, paywalls, rate limits, bot protections, or robots policies.
- Do not present approximations as official provider metrics.
- Store source, license, ingestion run, and last-updated metadata for every metric row.
