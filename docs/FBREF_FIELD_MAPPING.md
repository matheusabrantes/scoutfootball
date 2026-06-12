# FBref Field Mapping

Status values:

- `supported`: expected direct FBref column mapping, pending local `soccerdata` verification.
- `partially_supported`: can be derived or approximated from FBref columns, but not identical to the ScoutFootball target definition.
- `not_supported`: no known FBref public table mapping.
- `requires_different_source`: requires Understat, event data, tracking, or another provider.
- `unknown`: must be confirmed after `soccerdata` is installed and FBref tables are inspected.

Investigation status:

- `soccerdata` was not installed in the current environment.
- The POC script exists at `backend/scripts/investigate_soccerdata_fbref.py`.
- Safe metadata output path is `backend/data_samples/fbref/`.
- Run `python3 -m pip install soccerdata` or install the `providers` extra before re-running.

## Expected FBref Tables

Prioritized tables:

- `standard`
- `shooting`
- `passing`
- `passing_types`
- `goal_shot_creation`
- `defense`
- `possession`
- `playing_time`
- `misc`
- `keeper`
- `keeper_adv`

## Target Metric Mapping

### Goalkeepers

| Target Metric | Expected FBref Columns | Status | Notes |
| --- | --- | --- | --- |
| Save percentage % | `Save%` from `keeper` | `unknown` | Likely direct if keeper table is available. |
| Aerial duels won per 90 | Aerial won columns from `misc` if available | `unknown` | Requires table inspection. |
| Interceptions, possession adjusted | `Int` plus possession context | `requires_different_source` | FBref can provide raw interceptions, not possession-adjusted values directly. |
| Passes completed per 90 | `Cmp` from passing/keeper passing fields | `unknown` | Keeper passing table availability must be verified. |
| Long pass accuracy % | Launch/long pass fields from `keeper_adv` | `unknown` | Likely available for top leagues if advanced keeper table exists. |
| Short pass completion % | Keeper pass fields from `keeper_adv` | `unknown` | Requires column inspection. |
| Prevented goals, PSxG - GA per 90 | `PSxG+/-` or `PSxG-GA` from `keeper_adv` | `unknown` | Likely strong FBref fit for top leagues. |

### Centrebacks / Fullbacks / Midfielders

| Target Metric | Expected FBref Columns | Status | Notes |
| --- | --- | --- | --- |
| Passes completed per 90 | `Cmp`, `90s` from `passing` | `unknown` | Likely direct. |
| Forward pass completion % | No simple public FBref direction column | `requires_different_source` | Requires event/vector data. |
| Progressive passes completed per 90 | `PrgP`, `90s` from `passing` | `unknown` | Likely direct. |
| Possession won per 90 | `Tkl`, `Int`, recoveries if available | `partially_supported` | Exact possession won is not direct. |
| Defensive duels won % | Tackles/challenges fields from `defense` | `partially_supported` | FBref taxonomy differs from Wyscout defensive duels. |
| Aerial duels won % | `Won`, `Lost`, `Won%` from `misc` | `unknown` | Likely direct if aerial columns are present. |
| Progressive carries per 90 | `PrgC`, `90s` from `possession` | `unknown` | Likely direct. |
| Accurate crosses per 90 | `Crs` or cross-related passing type fields | `partially_supported` | Accurate crosses may not be direct. |
| Expected assists per 90 | `xAG` or `xA`, `90s` from `passing`/`standard` | `unknown` | Depends on table/season. |
| Duels won % | Aerial and tackle challenge fields | `partially_supported` | Overall duels won may not be direct. |
| Forward passes completed per 90 | No simple public FBref direction column | `requires_different_source` | Requires event/vector data. |
| Key passes per 90 | `KP`, `90s` from `passing` | `unknown` | Likely direct. |

### Attackers

| Target Metric | Expected FBref Columns | Status | Notes |
| --- | --- | --- | --- |
| Progressive carries per 90 | `PrgC`, `90s` from `possession` | `unknown` | Likely direct. |
| Successful dribbles per 90 | Take-ons successful fields from `possession` | `unknown` | Column names changed in recent FBref tables; inspect first. |
| Non-penalty goals per 90 | `Gls`, `PK`, `90s` or `G-PK` | `unknown` | Likely direct/derived. |
| Non-penalty xG per 90 | `npxG`, `90s` from `shooting`/`standard` | `unknown` | Likely direct in top leagues. |
| npxG + xA per 90 | `npxG+xAG` or `npxG+xA`, `90s` | `unknown` | Depends on column naming. |
| Assists per 90 | `Ast`, `90s` | `unknown` | Likely direct. |
| Expected assists per 90 | `xAG` or `xA`, `90s` | `unknown` | Likely direct for top leagues. |
| Key passes per 90 | `KP`, `90s` from `passing` | `unknown` | Likely direct. |
| Accurate crosses per 90 | Cross fields from `passing_types` | `partially_supported` | Accuracy may require attempted/completed distinction not always available. |
| Goal conversion % | `Gls`, `Sh` | `unknown` | Direct derived metric if shooting table exists. |
| Touches in box per 90 | `Att Pen`/penalty-area touches from `possession` | `unknown` | Likely available in possession table for top leagues. |
| Aerial duels won % | `Won%` from `misc` | `unknown` | Likely direct if misc table exists. |
| Offensive duels won per 90 | No direct FBref Wyscout-style taxonomy | `requires_different_source` | Requires event-provider duel taxonomy. |

## Expected Coverage Strength

- xG/xA/npxG: likely available for top European FBref leagues, pending `soccerdata` verification.
- Progressive passes/carries: likely available via `PrgP` and `PrgC`, pending verification.
- Goalkeeper PSxG: likely available through `keeper_adv`, pending verification.
- South America: unknown until `soccerdata` and FBref league identifiers are confirmed.

