# StatsBomb Open Data Evaluation

Evaluation date: 2026-06-14

## Summary

StatsBomb Open Data is the official primary metrics source for the first ScoutFootball MVP. The MVP is now a historical real-data MVP, not a current-season coverage product. StatsBomb Open Data provides real event-level JSON, lineups, and selected 360 files, but coverage is curated rather than comprehensive.

Product classification: `primary_mvp_metrics_provider`.

MVP classification: `historical_real_data_mvp`.

Strategic classification: `viable_for_selected_league_mvp`.

## Repository Structure And Usage

- Repository: https://github.com/statsbomb/open-data
- `data/competitions.json`: competition and season catalogue.
- `data/matches/{competition_id}/{season_id}.json`: match lists for each listed competition-season.
- `data/events/{match_id}.json`: event stream for each available match.
- `data/lineups/{match_id}.json`: lineup/player metadata for each available match.
- `data/three-sixty/{match_id}.json`: 360 freeze-frame data for selected matches only.
- `doc/`: StatsBomb Open Data PDFs for competitions, matches, events, lineups, 360 frames, and the open data specification.

StatsBomb attribution requirement from the repository README: if publishing, sharing, or distributing research, analysis, or insights based on the data, state StatsBomb as the data source and use the StatsBomb logo from their media pack.

Local data handling: only metadata and a 3-match POC subset were downloaded to ignored `backend/data_sources/statsbomb_open/`. Full event datasets are not committed.

## Selected Proof Of Concept

| Field | Value |
| --- | --- |
| Selected competition | Premier League |
| Selected season | 2015/2016 |
| competition_id | 2 |
| season_id | 27 |
| Repository match count | 380 |
| POC matches processed | 3 |
| POC match IDs | 3754217, 3754117, 3754296 |
| Reason selected | Target domestic league with complete historical 380-match coverage and full events/lineups. |
| Known limitations | Historical only, no 360 files, POC processes a small subset to avoid large local downloads. |

Bundesliga 2023/2024 was not selected because the repository contains 34 matches, not a complete domestic season.

## Target League Availability

| Target league | Available seasons in StatsBomb Open Data | Current season? | Last completed season? | Useful role |
| --- | --- | --- | --- | --- |
| Premier League | 2003/2004 (38 matches), 2015/2016 (380 matches) | No | No | historical complete demo |
| La Liga | 1973/1974 (1 matches), 2004/2005 (7 matches), 2005/2006 (17 matches), 2006/2007 (26 matches), 2007/2008 (27 matches), 2008/2009 (31 matches), 2009/2010 (35 matches), 2010/2011 (33 matches), 2011/2012 (37 matches), 2012/2013 (32 matches), 2013/2014 (31 matches), 2014/2015 (38 matches), 2015/2016 (380 matches), 2016/2017 (34 matches), 2017/2018 (36 matches), 2018/2019 (34 matches), 2019/2020 (33 matches), 2020/2021 (35 matches) | No | No | historical complete demo |
| Bundesliga | 2015/2016 (34 matches), 2023/2024 (34 matches) | No | No | historical partial demo only |
| Serie A Italy | 1986/1987 (1 matches), 2015/2016 (380 matches) | No | No | historical complete demo |
| Ligue 1 | 2015/2016 (377 matches), 2021/2022 (26 matches), 2022/2023 (32 matches) | No | No | historical complete demo |
| Eredivisie | None found | No | No | not available |
| Liga Portugal | None found | No | No | not available |
| Brasileirao Serie A | None found | No | No | not available |
| Argentina Primera Division | 1981 (1 matches), 1997/1998 (1 matches) | No | No | historical partial demo only |
| Colombia Categoria Primera A | None found | No | No | not available |
| Uruguay Primera Division | None found | No | No | not available |
| Chile Primera Division | None found | No | No | not available |

## Complete Coverage Matrix

| competition_id | season_id | country | competition | gender | season | match_count | events_available | lineups_available | 360_available | target_league_match | scoutfootball_relevance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1267 | 107 | Africa | African Cup of Nations | male | 2023 | 52 | True | True | True |  | non_target_reference |
| 81 | 275 | Argentina | Liga Profesional | male | 1981 | 1 | True | True | False | Argentina Primera Division | target_historical_partial_demo |
| 81 | 48 | Argentina | Liga Profesional | male | 1997/1998 | 1 | True | True | False | Argentina Primera Division | target_historical_partial_demo |
| 37 | 4 | England | FA Women's Super League | female | 2018/2019 | 107 | True | True | False |  | non_target_reference |
| 37 | 42 | England | FA Women's Super League | female | 2019/2020 | 87 | True | True | False |  | non_target_reference |
| 37 | 90 | England | FA Women's Super League | female | 2020/2021 | 131 | True | True | False |  | non_target_reference |
| 37 | 281 | England | FA Women's Super League | female | 2023/2024 | 132 | True | True | False |  | non_target_reference |
| 2 | 44 | England | Premier League | male | 2003/2004 | 38 | True | True | False | Premier League | target_historical_partial_demo |
| 2 | 27 | England | Premier League | male | 2015/2016 | 380 | True | True | False | Premier League | target_historical_complete_demo |
| 16 | 276 | Europe | Champions League | male | 1970/1971 | 1 | True | True | False |  | non_target_reference |
| 16 | 71 | Europe | Champions League | male | 1971/1972 | 1 | True | True | False |  | non_target_reference |
| 16 | 277 | Europe | Champions League | male | 1972/1973 | 1 | True | True | False |  | non_target_reference |
| 16 | 76 | Europe | Champions League | male | 1999/2000 | 1 | True | True | False |  | non_target_reference |
| 16 | 44 | Europe | Champions League | male | 2003/2004 | 1 | True | True | False |  | non_target_reference |
| 16 | 37 | Europe | Champions League | male | 2004/2005 | 1 | True | True | False |  | non_target_reference |
| 16 | 39 | Europe | Champions League | male | 2006/2007 | 1 | True | True | False |  | non_target_reference |
| 16 | 41 | Europe | Champions League | male | 2008/2009 | 1 | True | True | False |  | non_target_reference |
| 16 | 21 | Europe | Champions League | male | 2009/2010 | 1 | True | True | False |  | non_target_reference |
| 16 | 22 | Europe | Champions League | male | 2010/2011 | 1 | True | True | False |  | non_target_reference |
| 16 | 23 | Europe | Champions League | male | 2011/2012 | 1 | True | True | False |  | non_target_reference |
| 16 | 24 | Europe | Champions League | male | 2012/2013 | 1 | True | True | False |  | non_target_reference |
| 16 | 25 | Europe | Champions League | male | 2013/2014 | 1 | True | True | False |  | non_target_reference |
| 16 | 26 | Europe | Champions League | male | 2014/2015 | 1 | True | True | False |  | non_target_reference |
| 16 | 27 | Europe | Champions League | male | 2015/2016 | 1 | True | True | False |  | non_target_reference |
| 16 | 2 | Europe | Champions League | male | 2016/2017 | 1 | True | True | False |  | non_target_reference |
| 16 | 1 | Europe | Champions League | male | 2017/2018 | 1 | True | True | False |  | non_target_reference |
| 16 | 4 | Europe | Champions League | male | 2018/2019 | 1 | True | True | False |  | non_target_reference |
| 55 | 43 | Europe | UEFA Euro | male | 2020 | 51 | True | True | True |  | non_target_reference |
| 55 | 282 | Europe | UEFA Euro | male | 2024 | 51 | True | True | True |  | non_target_reference |
| 35 | 75 | Europe | UEFA Europa League | male | 1988/1989 | 3 | True | True | False |  | non_target_reference |
| 53 | 106 | Europe | UEFA Women's Euro | female | 2022 | 31 | True | True | True |  | non_target_reference |
| 53 | 315 | Europe | UEFA Women's Euro | female | 2025 | 31 | True | True | True |  | non_target_reference |
| 7 | 27 | France | Ligue 1 | male | 2015/2016 | 377 | True | True | False | Ligue 1 | target_historical_complete_demo |
| 7 | 108 | France | Ligue 1 | male | 2021/2022 | 26 | True | True | True | Ligue 1 | target_historical_partial_demo |
| 7 | 235 | France | Ligue 1 | male | 2022/2023 | 32 | True | True | True | Ligue 1 | target_historical_partial_demo |
| 9 | 27 | Germany | 1. Bundesliga | male | 2015/2016 | 34 | True | True | False | Bundesliga | target_historical_partial_demo |
| 9 | 281 | Germany | 1. Bundesliga | male | 2023/2024 | 34 | True | True | True | Bundesliga | target_recent_partial |
| 135 | 281 | Germany | Frauen Bundesliga | female | 2023/2024 | 132 | True | True | False |  | non_target_reference |
| 1238 | 108 | India | Indian Super league | male | 2021/2022 | 115 | True | True | False |  | non_target_reference |
| 1470 | 274 | International | FIFA U20 World Cup | male | 1979 | 1 | True | True | False |  | non_target_reference |
| 43 | 269 | International | FIFA World Cup | male | 1958 | 2 | True | True | False |  | non_target_reference |
| 43 | 270 | International | FIFA World Cup | male | 1962 | 1 | True | True | False |  | non_target_reference |
| 43 | 272 | International | FIFA World Cup | male | 1970 | 6 | True | True | False |  | non_target_reference |
| 43 | 51 | International | FIFA World Cup | male | 1974 | 6 | True | True | False |  | non_target_reference |
| 43 | 54 | International | FIFA World Cup | male | 1986 | 3 | True | True | False |  | non_target_reference |
| 43 | 55 | International | FIFA World Cup | male | 1990 | 1 | True | True | False |  | non_target_reference |
| 43 | 3 | International | FIFA World Cup | male | 2018 | 64 | True | True | False |  | non_target_reference |
| 43 | 106 | International | FIFA World Cup | male | 2022 | 64 | True | True | True |  | non_target_reference |
| 72 | 30 | International | Women's World Cup | female | 2019 | 52 | True | True | False |  | non_target_reference |
| 72 | 107 | International | Women's World Cup | female | 2023 | 64 | True | True | True |  | non_target_reference |
| 12 | 86 | Italy | Serie A | male | 1986/1987 | 1 | True | True | False | Serie A Italy | target_historical_partial_demo |
| 12 | 27 | Italy | Serie A | male | 2015/2016 | 380 | True | True | False | Serie A Italy | target_historical_complete_demo |
| 131 | 281 | Italy | Serie A Women | female | 2023/2024 | 130 | True | True | False |  | non_target_reference |
| 116 | 68 | North and Central America | North American League | male | 1977 | 1 | True | True | False |  | non_target_reference |
| 223 | 282 | South America | Copa America | male | 2024 | 32 | True | True | False |  | non_target_reference |
| 87 | 279 | Spain | Copa del Rey | male | 1977/1978 | 1 | True | True | False |  | non_target_reference |
| 87 | 268 | Spain | Copa del Rey | male | 1982/1983 | 1 | True | True | False |  | non_target_reference |
| 87 | 84 | Spain | Copa del Rey | male | 1983/1984 | 1 | True | True | False |  | non_target_reference |
| 11 | 278 | Spain | La Liga | male | 1973/1974 | 1 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 37 | Spain | La Liga | male | 2004/2005 | 7 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 38 | Spain | La Liga | male | 2005/2006 | 17 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 39 | Spain | La Liga | male | 2006/2007 | 26 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 40 | Spain | La Liga | male | 2007/2008 | 27 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 41 | Spain | La Liga | male | 2008/2009 | 31 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 21 | Spain | La Liga | male | 2009/2010 | 35 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 22 | Spain | La Liga | male | 2010/2011 | 33 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 23 | Spain | La Liga | male | 2011/2012 | 37 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 24 | Spain | La Liga | male | 2012/2013 | 32 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 25 | Spain | La Liga | male | 2013/2014 | 31 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 26 | Spain | La Liga | male | 2014/2015 | 38 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 27 | Spain | La Liga | male | 2015/2016 | 380 | True | True | False | La Liga | target_historical_complete_demo |
| 11 | 2 | Spain | La Liga | male | 2016/2017 | 34 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 1 | Spain | La Liga | male | 2017/2018 | 36 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 4 | Spain | La Liga | male | 2018/2019 | 34 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 42 | Spain | La Liga | male | 2019/2020 | 33 | True | True | False | La Liga | target_historical_partial_demo |
| 11 | 90 | Spain | La Liga | male | 2020/2021 | 35 | True | True | True | La Liga | target_historical_partial_demo |
| 182 | 281 | Spain | Liga F | female | 2023/2024 | 240 | True | True | False |  | non_target_reference |
| 44 | 107 | United States of America | Major League Soccer | male | 2023 | 6 | True | True | True |  | non_target_reference |
| 49 | 3 | United States of America | NWSL | female | 2018 | 36 | True | True | False |  | non_target_reference |
| 49 | 107 | United States of America | NWSL | female | 2023 | 137 | True | True | False |  | non_target_reference |

## Event Schema Sample

Sample inspected matches: 3754217, 3754117, 3754296.
Sample event count: 11041.

| Event type | Count |
| --- | --- |
| 50/50 | 2 |
| Bad Behaviour | 3 |
| Ball Receipt* | 2936 |
| Ball Recovery | 310 |
| Block | 123 |
| Carry | 2408 |
| Clearance | 124 |
| Dispossessed | 75 |
| Dribble | 126 |
| Dribbled Past | 82 |
| Duel | 219 |
| Error | 4 |
| Foul Committed | 79 |
| Foul Won | 75 |
| Goal Keeper | 100 |
| Half End | 12 |
| Half Start | 12 |
| Injury Stoppage | 10 |
| Interception | 39 |
| Miscontrol | 85 |
| Own Goal Against | 1 |
| Own Goal For | 1 |
| Pass | 3205 |
| Player Off | 2 |
| Player On | 2 |
| Pressure | 879 |
| Referee Ball-Drop | 2 |
| Shield | 4 |
| Shot | 88 |
| Starting XI | 6 |
| Substitution | 18 |
| Tactical Shift | 9 |

Relevant nested fields observed:

- `pass`: aerial_won, angle, assisted_shot_id, body_part, cross, cut_back, deflected, end_location, goal_assist, height, inswinging, length, miscommunication, no_touch, outcome, outswinging, recipient, shot_assist, switch, technique, through_ball, type
- `carry`: end_location
- `shot`: aerial_won, body_part, end_location, first_time, freeze_frame, key_pass_id, one_on_one, outcome, statsbomb_xg, technique, type
- `duel`: outcome, type
- `interception`: outcome
- `ball_recovery`: offensive, recovery_failure
- `block`: deflection, save_block
- `clearance`: aerial_won, body_part, head, left_foot, other, right_foot
- `dribble`: nutmeg, outcome, overrun
- `goalkeeper`: body_part, end_location, outcome, position, technique, type
- `foul_committed`: advantage, card, penalty, type
- `foul_won`: advantage, defensive, penalty
- `substitution`: outcome, replacement
- `tactics`: formation, lineup

## ScoutFootball Metric Coverage

| Metric | Classification | Formula / event logic |
| --- | --- | --- |
| Minutes played | derivable | Starting XI, substitutions, red cards, max event timestamp. |
| Appearances | derivable | One appearance when calculated match minutes > 0. |
| Starts | directly_available | Starting XI event/tactics lineup. |
| Goals | directly_available | Shot outcome Goal. |
| Non-penalty goals | derivable | Shot outcome Goal where shot.type is not Penalty. |
| Assists | directly_available | Pass goal_assist flag. |
| Shots | directly_available | Shot events. |
| Shots on target | derivable | Shot outcomes Goal/Saved/Saved to Post/Saved Off Target/Post approximation. |
| xG | directly_available | shot.statsbomb_xg. |
| Non-penalty xG | derivable | Sum shot.statsbomb_xg excluding penalties. |
| Key passes | directly_available | pass.shot_assist flag. |
| Expected assists / xA | not_available | No xA field observed in open event schema sample. |
| Passes completed | derivable | Pass events with no pass.outcome. |
| Pass completion percentage | derivable | Completed passes / attempted passes. |
| Forward passes | derivable | Can be computed by positive x movement, but definition must be ScoutFootball-specific. |
| Forward pass completion percentage | derivable | Completed forward passes / attempted forward passes under ScoutFootball rule. |
| Progressive passes | derivable | ScoutFootball distance-to-goal rule in STATSBOMB_METRIC_DEFINITIONS.md. |
| Progressive carries | derivable | ScoutFootball distance-to-goal rule in STATSBOMB_METRIC_DEFINITIONS.md. |
| Crosses | directly_available | pass.cross flag. |
| Accurate crosses | derivable | pass.cross with no pass.outcome. |
| Successful dribbles | directly_available | Dribble outcome Complete. |
| Touches in attacking penalty area | partially_derivable | Any player event location in approximated penalty area. |
| Tackles | partially_derivable | StatsBomb Duel taxonomy includes tackle-like duels but no simple tackle total in sample. |
| Interceptions | directly_available | Interception events. |
| Blocks | directly_available | Block events. |
| Possession won | partially_derivable | Approximate from successful duels, ball recoveries, and non-lost interceptions. |
| Duels won | derivable | Duel outcomes indicating success. |
| Aerial duels won | partially_derivable | pass.aerial_won/shot.aerial_won/clearance.aerial_won exist, but no full aerial duel denominator was proven. |
| Cards | directly_available | bad_behaviour.card or foul_committed.card. |
| Saves | partially_derivable | Goal Keeper outcome/type can identify saves, but validate against official keeper logs. |
| Save percentage | partially_derivable | Saves / shots on target faced requires robust shot-faced event logic. |
| Goals conceded | partially_derivable | Goal Keeper Shot Faced/Goal Conceded or team goals against; needs validation. |
| Post-shot xG | not_available | No PSxG field observed. |
| PSxG minus goals allowed | not_available | Requires PSxG. |
| Long pass accuracy | derivable | Can derive by pass.length threshold; threshold is ScoutFootball-specific. |
| Short pass completion | derivable | Can derive by pass.length threshold; threshold is ScoutFootball-specific. |
| Goalkeeper exits | partially_derivable | Goal Keeper type fields may support some exits; needs deeper validation. |
| Goalkeeper interceptions | partially_derivable | Interception events by goalkeeper position. |

## POC Data Quality Report

- matches_processed: 3
- players_found: 60
- teams_found: 4
- event_count: 11041
- players_with_minutes: 60
- players_with_valid_positions: 60
- duplicate_player_season_rows: 0
- processing_time_seconds: 0.095
- local disk usage: 17 MB for metadata plus 3 match event/lineup sample at evaluation time
- unsupported metrics in POC output: expected_assists, post_shot_xg, psxg_minus_goals_allowed, long_pass_accuracy, short_pass_completion, aerial_duels, aerial_duels_won
- missing value rates: all requested output fields were populated except aerial duel fields, which are intentionally null because a complete aerial-duel denominator was not proven.

The selected Premier League 2015/2016 competition appears complete enough for historical rankings and percentiles if all 380 matches are downloaded and processed. The 3-match POC sample is not enough for public rankings.

## SQLite And Backend Compatibility

SQLite ingestion was not performed. The POC succeeded at provider and aggregation level, but production route integration should wait until the project decides whether historical demo data belongs in the same SQLite tables as API-Football/static CSV data. Existing API-Football, SQLite, and provider-neutral code were not removed.

Because SQLite ingestion was skipped, backend endpoints were not verified against real StatsBomb rows in this task.

## Strategic Decision

- Can it power the first public MVP? Yes, if the MVP is explicitly historical.
- Can it support current-season ScoutFootball? No.
- Can it support the full league list? No.
- Can its event schema help build our own metric engine? Yes.
- Should it replace API-Football? It replaces API-Football as the primary metrics provider.
- Should API-Football remain metadata fallback? Yes.
- Should static CSV/Kaggle remain part of the strategy? Yes, but not as the main implementation priority.

Recommended role: use StatsBomb Open Data as the primary historical MVP metrics provider. Keep API-Football as optional metadata fallback and static CSV/Kaggle as a future supplement. Do not claim current-season coverage.
