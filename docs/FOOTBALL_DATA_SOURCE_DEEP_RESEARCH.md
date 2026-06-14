# Football Data Source Deep Research

Research date: 2026-06-14

Product decision update: ScoutFootball will proceed with StatsBomb Open Data as the official `primary_mvp_metrics_provider` for a `historical_real_data_mvp`. Kaggle/static CSV remains a supplement, not the main implementation priority.

## Executive Summary

The most realistic low-cost ScoutFootball path is a static/hybrid MVP: use vetted FBref-style Kaggle CSVs for top-five European league advanced metrics, API-Football only for identity/league/team metadata and South America basic context, and manually uploaded CSVs for Brazil/Argentina advanced metrics until a licensed data provider is affordable.

Live FBref scraping is not viable right now because local `soccerdata` access returned `403 Forbidden`, and public community reports indicate FBref blocking has become common. Do not bypass access controls.

Best findings:

- Best source found for immediate ScoutFootball metric depth: [Football Players Stats 2024-2025 on Kaggle](https://www.kaggle.com/datasets/hubertsidorowicz/football-players-stats-2024-2025), sourced from FBref and described as top-five European leagues with weekly updates.
- Best free historical dataset: [FBref 2017-2024 for Europe's Top 5 leagues](https://www.kaggle.com/datasets/akshankrithick/fbref-2017-2024-for-europes-top-5-leagues), CSV, seven files, about 2 MB, player-level top-five league stats from 2017-18 through 2023-24.
- Best low-cost API candidate if paying now: [TheStatsAPI Football Player Stats API](https://www.thestatsapi.com/football/player-stats), claiming player season stats, xG, 10 years of history, 150 default competitions, 100,000 requests/month, and plans from $50/month.
- Best cheap supplemental xG source: [Understat](https://understat.com/) or an Apify Understat actor for top-five Europe plus RFPL only; useful for xG/npxG/xA but not full scouting metrics.
- Best South America reality: free/cheap advanced player metrics for Brazil and Argentina are not reliably available. API-Football can provide metadata/basic rows, while DataMB-level Brazil/Argentina metrics likely require DataMB Pro, manual CSVs, or a paid provider.
- StatsBomb Open Data role: evaluated separately in `docs/STATSBOMB_OPEN_DATA_EVALUATION.md`; useful for event-level metric-engine development and historical demos, not full/current ScoutFootball coverage.

## Source Comparison Matrix

Scores are ScoutFootball MVP fit from 1 to 5, where 5 means low-cost, legally usable, and close to DataMB metric depth.

| Source | Type | Cost | Free tier | Coverage | Top 5 Europe support | Brazil support | Argentina support | Other South America support | Player season stats | Advanced metrics | xG/npxG | xA/xAG | Progressive passes | Progressive carries | Touches in box | Aerial duels | GK advanced | Ease | Legal/ToS risk | Technical risk | Update frequency | Best use case | Score | Notes | Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kaggle FBref 2024-2025 | Static dataset | Free | Yes | Top 5 Europe | Yes | No | No | No | Yes | Strong if columns match FBref | Likely | Likely xAG | Likely | Likely | Likely | Likely misc | Possibly separate keeper files | Easy CSV | Medium: dataset provenance/license must be checked | Low | Weekly per listing | Europe MVP metrics bootstrap | 5 | Best immediate top-five Europe path. Confirm license before redistribution. | [Kaggle](https://www.kaggle.com/datasets/hubertsidorowicz/football-players-stats-2024-2025) |
| Kaggle FBref 2017-2024 | Static dataset | Free | Yes | Top 5 Europe historical | Yes | No | No | No | Yes | Strong historical FBref-style | Likely | Likely | Likely | Likely | Likely | Likely | Unknown | Easy CSV | Medium | Low | Static/updated recently | Backfill, testing, percentile baselines | 5 | Strongest historical free dataset found. | [Kaggle](https://www.kaggle.com/datasets/akshankrithick/fbref-2017-2024-for-europes-top-5-leagues) |
| API-Football / API-SPORTS | Paid API | Free, from $19/mo | 100 requests/day | 1,200+ leagues/cups | Metadata yes; player metrics null in local free-plan test | Metadata/basic rows yes for 2024 | Metadata/basic rows yes for 2024 | Likely metadata | Rows yes | Weak in current validation | Not confirmed | Not confirmed | No | No | No | Basic duels if non-null | Saves/goals conceded if non-null | Easy REST | Low-medium | Low | Live/current | Metadata, IDs, fixtures, fallback | 3 | Keep, but do not rely on advanced player metrics until non-null fields are confirmed. | [API-Football](https://www.api-football.com/), [pricing](https://www.api-football.com/pricing) |
| TheStatsAPI | Paid API | From $50/mo | 7-day trial | 150 competitions default, up to 1,196 | Claims yes | Unknown; likely request | Unknown; likely request | Unknown | Claims yes | Claims player stats + xG | Yes claimed | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Easy REST | Medium: must verify terms | Medium: unvalidated | Live and historical | Best low-cost API candidate | 4 | Needs a schema/trial validation before adoption. | [Player stats](https://www.thestatsapi.com/football/player-stats), [xG](https://www.thestatsapi.com/football/xg) |
| Understat | Public stat site / unofficial APIs | Free | Public site | EPL, La Liga, Bundesliga, Serie A, Ligue 1, RFPL | Yes | No | No | No | Yes for xG-specific player stats | Narrow | Yes | xA-like | No | No | No | No | No | Medium | Medium-high: unofficial access | Medium | Current/historical | xG/npxG/xA supplement for Europe | 3 | Good xG supplement, not a full ScoutFootball source. | [Understat](https://understat.com/), [understatAPI](https://github.com/collinb9/understatAPI) |
| Apify Understat actors | Paid hosted scraper | Pay per run | Trial/free credits vary | Understat leagues | Yes | No | No | No | Yes for xG rows | Narrow | Yes | Yes | No | No | No | No | No | Easy API/export | Medium | Medium | On demand | Cheap Europe xG extraction | 3 | Cost examples are low for all six Understat leagues, but still depends on scraped source. | [Apify actor](https://apify.com/mirthful_radish/understat-xg-football-scraper), [pricing example](https://apify.com/constructive_calm/understat-football-analytics) |
| FBref live via soccerdata/worldfootballR | Public site scraper | Free | Public pages | Broad but changing | Historically yes | Possible but unverified | Possible but unverified | Mixed | Yes if accessible | Strong aggregates | Yes historically | Yes historically | Yes historically | Yes historically | Yes historically | Yes historically | PSxG historically | Medium | High | High due to 403/Cloudflare | Current/historical but fragile | Not recommended for live ingestion | 2 | Local test returned `403`; use static exports instead. | [soccerdata](https://github.com/probberechts/soccerdata), [worldfootballR FBref](https://jaseziv.github.io/worldfootballR/articles/extract-fbref-data.html) |
| Manual FBref CSV/export | Manual dataset | Free | Yes | User-selected | Yes if manually obtained | Possible | Possible | Possible | Yes | Strong aggregates where pages expose them | Yes where available | Yes where available | Yes where available | Yes where available | Yes where available | Yes | PSxG where available | Medium manual | Medium | Low once file is local | Manual | Safer static prototype than scraping | 4 | Use only with documented provenance and no automated bypass. | [FBref](https://fbref.com/en/) |
| FootyStats API | Paid API | From £29.99/mo | API docs public; paid tiers | 50 leagues at Hobby | Likely | Likely | Likely | Likely | Unclear player depth | Betting/team heavy; player depth uncertain | Team xG visible; player unclear | Unclear | No evidence | No evidence | No evidence | Unclear | No evidence | Easy REST | Medium | Medium | Live | Betting/team stats, possible fallback | 2 | Affordable, but not proven for DataMB-style player metrics. | [FootyStats API](https://footystats.org/api), [Brazil xG page](https://footystats.org/brazil/serie-a/xg) |
| football-data.org | Paid/free API | Free, paid tiers | Yes | Fixtures/standings/squads | Yes for competitions | Yes | Listed | Listed | Weak | Weak | No meaningful player xG | No | No | No | No | No | No | Easy REST | Low-medium | Low | Live | Fixtures, standings, squads | 2 | Useful metadata fallback, not advanced player analytics. | [Docs](https://www.football-data.org/documentation/api) |
| TheSportsDB | Public API | Free, premium $9/mo | Yes | Broad sports | Basic | Basic | Basic | Basic | Basic | Weak | No | No | No | No | No | No | No | Easy REST | Low-medium | Low | Live/community | Metadata/prototyping | 2 | Cheap but not deep enough for ScoutFootball metrics. | [TheSportsDB](https://www.thesportsdb.com/), [free API](https://www.thesportsdb.com/free_sports_api) |
| StatsBomb Open Data | Open event dataset | Free | Yes | Curated competitions/seasons | Historical complete seasons for selected target leagues only | No Brazil league season found | Argentina has one-match historical samples | No target full South America league seasons found | Match/event level | Strong event model | Yes | No direct xA observed | Derivable from events | Derivable from events | Partially derivable | Partial aerial indicators, no proven denominator | Shot-stopping partially derivable; no PSxG | Medium | Low if attribution followed | Medium transformation | Static releases | Metric-engine prototype and historical demo | 3 | Separate POC processed Premier League 2015/2016 sample: 3 matches, 11,041 events, 60 players. Not current or full target coverage. | [Open data](https://github.com/statsbomb/open-data), [Evaluation](STATSBOMB_OPEN_DATA_EVALUATION.md) |
| FotMob public/unofficial | Public app/site | Free public app | No official public API | 500+ leagues on site | Yes | Likely | Likely | Likely | Yes in app | Good app metrics | Yes | Yes | Some | Some | Some | Some | xGOT on app | Medium | High: unofficial API | High | Live | Research only unless licensed | 2 | Public sources say API access is difficult and unofficial. | [FotMob](https://www.fotmob.com/), [fotmob-api PyPI](https://pypi.org/project/fotmob-api/) |
| SofaScore public/unofficial | Public app/site | Free widgets | Widgets free | 500+ competitions claimed by community pages | Yes | Likely | Likely | Likely | Yes in app | Good app metrics | Yes via Opta in some contexts | Yes | Some | Some | Some | Some | Some | Medium | High: unofficial/private endpoints | High | Live | Manual reference only | 2 | Do not build on hidden endpoints. Widgets may help display, not ingest. | [SofaScore compare](https://www.sofascore.com/football/player/compare), [widgets](https://corporate.sofascore.com/widgets) |
| StatBunker | Public stat site | Free/paid unknown | Public pages | Many leagues | Yes | Unknown | Unknown | Unknown | Yes basic | Mostly traditional | Unclear | Unclear | No evidence | No evidence | No evidence | Some | Some | Medium | Medium | Medium | Current | Basic public reference | 2 | Could be inspected manually but unlikely DataMB-depth. | [StatBunker](https://www.statbunker.com/) |
| Transfermarkt / transfermarkt-datasets | Public/GitHub/Kaggle | Free | Yes | Global | Yes | Yes | Yes | Yes | Appearances/goals/transfers, not advanced | Weak | No | No | No | No | No | No | No | Easy static | Medium | Low | Updated datasets exist | Identity, market value, transfers | 2 | Pair with metrics source for enrichment only. | [GitHub dataset](https://github.com/salimt/football-datasets), [Kaggle Transfermarkt](https://www.kaggle.com/datasets/davidcariboo/player-scores) |
| DataHub football collection | Static datasets | Free/open | Yes | Mixed | Some | Some | Some | Some | Mostly match/metadata | Weak | Limited | Limited | No | No | No | No | No | Easy | Low-medium | Low | Static | Reference datasets | 2 | Useful for non-player advanced context. | [DataHub blog](https://datahub.io/blog/football-data-our-open-source-collection-of-worldwide-statistics) |
| Sportmonks | Paid API | Too high for now | Trial/free plan | 2,500+ leagues claimed | Yes | Likely | Likely | Likely | Yes | Better than API-Football, xG add-on | Yes add-on from 2024 | Unknown | Unknown | Unknown | Unknown | Some | Some | Easy REST | Low after contract | Medium | Live | Future paid fallback | 3 | Stronger product, but current cost is outside weekend MVP. | [Sportmonks](https://www.sportmonks.com/football-api/), [xG](https://www.sportmonks.com/football-api/xg-data/) |
| Wyscout / Hudl | Licensed provider | Contact sales | No | 600+ leagues claimed | Yes | Yes | Yes | Yes | Yes | Very strong event/scouting | Yes likely | Yes likely | Yes | Yes | Yes | Yes | Yes | Harder contract | Low after license | Medium | Live/historical | Long-term DataMB-like source | 4 technical, 1 cost | Likely too expensive, but metric taxonomy fit is strong. | [Wyscout API](https://apidocs.wyscout.com/), [Hudl data API](https://www.hudl.com/products/wyscout/data-api) |
| Opta / Stats Perform | Licensed provider | Enterprise | No | Global | Yes | Yes | Yes | Yes | Yes | Very strong | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Contract/API | Low after license | Medium | Live | Professional product | 4 technical, 1 cost | Best quality, not weekend-budget. | [Stats Perform](https://www.statsperform.com/products/dynamic-stats-api/) |
| SkillCorner | Licensed/open sample | Enterprise; open sample | Small open data | Tracking products across 120+ comps | Yes likely paid | Unknown | Unknown | Unknown | Physical/tracking, not base stat source | Tracking/physical | No base xG focus | No | Derived | Carries possible | Tracking zones possible | No | No | Hard | Low after license | High modeling | Live/paid | Future tracking augmentation | 2 MVP | Open data is tiny sample; paid product is not cheap. | [SkillCorner](https://skillcorner.com/us), [open data](https://github.com/SkillCorner/opendata) |

## DataMB Public Clues

Public clues found:

- DataMB public guide says Pro tools cover all 55 leagues, current and past season, and 100+ metrics per 90 and total.
- Free tools focus on Top 7 leagues: Premier League, La Liga, Bundesliga, Serie A, Ligue 1, Eredivisie, Liga Portugal.
- Public guide lists supported Pro leagues including Brazil Serie A, Argentina Primera Division, Uruguay Primera Division, Colombia Primera A, and Chile Primera Division.
- Public player/team pages and articles show metrics such as xG, xA, non-penalty xG+xA, progressive carries, successful dribbling, touches in the opponent box, duels, forward pass percentage, possession won, and performance indexes.
- I found no public source attribution proving DataMB uses FBref, Wyscout, Opta, Understat, StatsBomb, or another provider.

Inference:

- DataMB likely uses either licensed event data, a batch/precomputed third-party feed, or a hybrid of public/static scraped tables plus proprietary calculations.
- The breadth of 55 leagues and metrics such as forward pass percentage, possession won, duels, accelerations, and performance indexes looks closer to Wyscout-style event/scouting data than to plain FBref or Understat alone.
- DataMB could also normalize multiple sources, but this cannot be confirmed publicly.

Do not infer permission to copy DataMB data or inspect private endpoints.

Sources: [DataMB homepage](https://datamb.football/), [DataMB guide](https://datamb.football/guide/), [DataMB midfielders page](https://datamb.football/midfielders/), [DataMB Florian Wirtz analysis](https://datamb.football/florian-wirtz-analysis/), [DataMB Franco Mastantuono analysis](https://datamb.football/franco-mastantuono-analysis/).

## Concrete Downloadable Dataset Candidates

Do not download until license and file size are checked.

| Dataset | URL | Platform | Seasons | Leagues | Rows | Columns | Metrics | License | Last updated | Download method | Problems | ScoutFootball fit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Football Players Stats 2024-2025 | https://www.kaggle.com/datasets/hubertsidorowicz/football-players-stats-2024-2025 | Kaggle | 2024-2025 | Top 5 Europe | Not visible from search result | Not visible from search result | FBref-style player stats; likely standard/shooting/passing/possession/defense/misc | Must inspect Kaggle license | Search says auto-updated weekly | Kaggle CLI/browser after accepting terms | Europe only; FBref provenance; license must allow use | Best free Europe MVP dataset |
| FBref 2017-2024 for Europe's Top 5 leagues | https://www.kaggle.com/datasets/akshankrithick/fbref-2017-2024-for-europes-top-5-leagues | Kaggle | 2017-18 to 2023-24 | Top 5 Europe | Not visible from search result | 7 CSV files; about 2 MB per search result | Player-level FBref statistics | Must inspect Kaggle license | Search says updated recently | Kaggle CLI/browser | Historical only to 2023-24 | Best free historical backfill |
| All Football Players Stats in Top 5 Leagues 24/25 | https://www.kaggle.com/datasets/orkunaktas/all-football-players-stats-in-top-5-leagues-2425/data | Kaggle | 2024-2025 | Top 5 Europe | Not visible | Not visible | xG and top-five league player analysis; exact advanced fields need inspection | Must inspect | Search says updated about a year ago | Kaggle | Unknown license/columns | Good backup Europe CSV |
| Understat-data | https://www.kaggle.com/datasets/codytipton/understat-data | Kaggle | Historical Understat seasons | EPL, La Liga, Bundesliga, Serie A, Ligue 1, RFPL | Not visible | Not visible | Player/game xG stats | Must inspect | Not visible | Kaggle | Narrow xG source only | Good Europe xG supplement |
| Football Data: Expected Goals and Other Metrics | https://www.kaggle.com/datasets/slehkyi/extended-football-stats-for-european-leagues-xg | Kaggle | Historical European league matches | European leagues | Not visible | Not visible | xG/xGA/team metrics | Must inspect | Not visible | Kaggle | Mostly team/match, not player scouting | Low for player MVP |
| Brazilian League - Players Statistics 2020 | https://www.kaggle.com/datasets/phillippycardelly/players-statistics-brazilian-league-2020 | Kaggle | 2020 | Brazil Serie A | 738 per search result | Not visible | Player statistics | Must inspect | Static | Kaggle | Old season, likely basic only | Brazil prototype only |
| Football Data from Transfermarkt | https://www.kaggle.com/datasets/davidcariboo/player-scores | Kaggle | Many seasons | Broad | 80,000+ games per listing | Many files | Transfermarkt games, appearances, market values, transfers | Must inspect | Automatically updated per listing | Kaggle | Not advanced performance metrics | Identity/enrichment source |
| StatsBomb Open Data | https://github.com/statsbomb/open-data | GitHub | Curated seasons | Curated competitions | Many match JSON files | Event schema | Event data, lineups, 360 for selected matches | StatsBomb open-data terms | Periodic | Git clone/HTTP small subsets | Not broad current player seasons | Event prototype/calculation tests |
| SkillCorner Open Data | https://github.com/SkillCorner/opendata | GitHub | 2024-2025 sample | Australian A-League sample | 10 matches | Tracking/events/physical data | Broadcast tracking, dynamic events, physical season aggregation | Repo license/terms | Static sample | Git clone small subset | Not target leagues | Tracking demo only |

## GitHub and Library Findings

| Repo / library | URL | Stars / activity from search | Data source | Files available | Dataset committed | License | Reuse potential |
| --- | --- | --- | --- | --- | --- | --- | --- |
| soccerdata | https://github.com/probberechts/soccerdata | Search shows about 1.8k stars and updated 2026-06-14 | Club Elo, ESPN, FBref, Football-Data.co.uk, SofaScore, SoFIFA, Understat, WhoScored | Python library | No large data | Check repo | Useful wrapper, but FBref blocked locally |
| worldfootballR | https://github.com/JaseZiv/worldfootballR | Active R package | FBref, Transfermarkt, Understat | R package/docs | No | Check repo | Good reference, but FBref 403 risk remains |
| ScraperFC | https://github.com/oseymour/ScraperFC | Python package | Capology, ClubELO, FBref, SofaScore, Transfermarkt, Understat | Python package | No | Check repo | Research only; scraping risk |
| understatAPI | https://github.com/collinb9/understatAPI | Python API | Understat | Python package | No | MIT shown on PyPI | Europe xG supplement |
| UnderData | https://github.com/osvaldomx/UnderData | Python client | Understat | Python package | No | MIT shown in search snippet | Europe xG supplement |
| StatsBomb open-data | https://github.com/statsbomb/open-data | Search shows 3.3k stars | StatsBomb | JSON competitions/matches/events/lineups/360 | Yes | StatsBomb open terms | Strong event prototype |
| statsbombpy | https://github.com/statsbomb/statsbombpy | Official Python package | StatsBomb API/open data | Python package | No | Check repo | Easy open-data loader |
| socceraction | https://github.com/ML-KULeuven/socceraction | Research package | Event streams from providers | Python package | No | Check repo | Calculate VAEP/SPADL if event data exists |
| kloppy | https://kloppy.pysport.org/ | Active docs | Event/tracking providers | Python package | No | Check project | Standardize event/tracking data once licensed |
| mplsoccer | https://mplsoccer.readthedocs.io/ | Active docs | StatsBomb open data helpers | Python package | No | Check project | Visualization and data examples |
| player-recommender | https://github.com/alexgasconn/player-recommender | Public app | FBref stats | Streamlit app | May include derived/sample data | Check repo | Reference for FBref-style embeddings/radars |
| fbref-comparison-radar | https://github.com/marcusrprojects/fbref-comparison-radar | 0 stars in snippet | Saved FBref HTML | Python script | No | Check repo | Useful manual-export pattern, not ingestion |
| Edd Webster football_analytics | https://github.com/eddwebster/football_analytics | Curated resources | Public football analytics resources | Code/resources | Mixed | Check repo | Discovery/reference hub |
| salimt football-datasets | https://github.com/salimt/football-datasets | Public Transfermarkt datalake | Transfermarkt | Dataset/code | Yes | Check repo | Identity/market-value enrichment |

## Brazil and Argentina Findings

Brazil and Argentina are the hardest part of a free advanced-metrics MVP.

- API-Football returned league/player rows for Brazil Serie A and Argentina Primera Division season 2024 in this repo, but tested metric values were null.
- DataMB publicly lists Brazil Serie A and Argentina Primera Division among 55 Pro leagues, but no public source attribution was found.
- Kaggle has an older Brazilian League 2020 player stats dataset, but it is too stale and likely too basic for the MVP.
- FootyStats has Brazil xG pages at team level, but I did not find evidence of comprehensive player-level DataMB-style advanced metrics.
- Understat does not cover Brazil or Argentina.
- StatsBomb Open Data can include South American tournaments or national-team competitions, but not broad current Brazil/Argentina league seasons.

Practical conclusion: free/cheap South America advanced player metrics are not realistically solved. The MVP should either:

- launch Europe advanced metrics first and mark South America as metadata/basic only;
- support manual CSV upload for Brazil/Argentina when a legitimate dataset is available;
- pay for a provider that explicitly covers these leagues and fields;
- or use DataMB Pro manually for personal research without ingesting or redistributing DataMB data.

## Candidate MVP Paths

| Path | Cost | Data quality | Metric coverage | Legal risk | Technical complexity | Maintenance | DataMB closeness | Recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A: API-Football only | $0-$19/mo+ | Good metadata; metrics blocked locally | Basic only if non-null fields become available | Low-medium | Low | Low | Low | Keep for metadata, not analytics MVP |
| B: FBref/Kaggle static dataset | $0 | Strong Europe aggregates | Strong top-five Europe advanced fields if columns match | Medium, license/provenance dependent | Low | Medium manual refresh | Medium for Europe | Best immediate MVP route |
| C: FBref static export/manual CSV | $0 | Strong if files are clean | Strong where exported tables exist | Medium | Medium manual | Medium manual | Medium | Good fallback if Kaggle license is unclear |
| D: Understat + API-Football | $0 or low Apify cost | Good xG Europe, good metadata | xG/npxG/xA only plus basic metadata | Medium | Medium matching IDs | Medium | Low-medium | Useful supplement, not full scouting |
| E: Dataset hybrid | $0-$20/mo | Best pragmatic mix | Europe advanced, South America metadata/manual | Medium | Medium | Medium | Medium | Recommended ScoutFootball MVP path |
| F: Low-cost provider | $50/mo+ for TheStatsAPI, £29.99/mo FootyStats, $19/mo API-Football | Unknown until trial | Potentially broader but unverified | Low after terms | Medium | Low | Medium if schema is rich | Validate TheStatsAPI trial before paying |

## Recommended ScoutFootball Data Strategy

Primary source: vetted Kaggle/CSV FBref-style datasets for top-five European advanced player metrics.

Secondary source: Understat for Europe xG/npxG/xA cross-checks if needed.

Metadata source: API-Football for league/team/player identity, countries, seasons, fixtures, and South America context.

Europe strategy: build the first real analytics MVP on static top-five Europe 2024-2025 CSVs, plus 2017-2024 historical CSVs for percentile testing and backfill.

Brazil strategy: API-Football metadata/basic context only; advanced metrics blocked unless a legitimate CSV/provider is found.

Argentina strategy: API-Football metadata/basic context only; advanced metrics blocked unless a legitimate CSV/provider is found.

Advanced metrics strategy: show only metrics present in the CSV schema. Do not silently approximate forward pass %, possession won, touches in box, PSxG-GA, or duels without source definitions.

Fallback strategy: manual CSV upload with provenance fields: source name, source URL, license, downloaded_at, season, league, table type, column mapping version.

Estimated monthly cost: $0 for static CSV MVP; $19/mo if API-Football paid tier is needed for metadata volume; $50/mo if TheStatsAPI trial proves it covers required player metrics.

Implementation difficulty: medium. The hard parts are source licensing, stable player identity matching, and metric-definition transparency, not ingestion mechanics.

Legal/ToS risk: medium for Kaggle/FBref-derived CSVs until license/provenance is confirmed; low for API-Football metadata if terms allow the intended use; high for live scraping/unofficial hidden endpoints.

Next implementation task: build a CSV dataset intake spec and validator, not a scraper. The validator should inspect files locally, list columns, classify ScoutFootball metrics, record source/license metadata, and reject unknown provenance.
