# Provider Field Mapping

This file tracks how API-Football player fields may map to ScoutFootball metrics. The mapping is intentionally conservative until the validation script confirms real fields for the target leagues and seasons.

Status values:

- `supported`
- `partially_supported`
- `not_supported`
- `requires_paid_event_data`
- `unknown_until_provider_validation`

## API-Football MVP Mapping

| ScoutFootball Metric | API-Football Candidate Fields | Status | Notes |
| --- | --- | --- | --- |
| Minutes | `statistics.games.minutes` | `unknown_until_provider_validation` | Required for per-90 calculations. |
| Appearances | `statistics.games.appearences` or equivalent | `unknown_until_provider_validation` | Field spelling must be confirmed from raw provider response. |
| Goals | `statistics.goals.total` | `unknown_until_provider_validation` | Common base attacking metric. |
| Assists | `statistics.goals.assists` | `unknown_until_provider_validation` | Common base attacking metric. |
| Shots | `statistics.shots.total` | `unknown_until_provider_validation` | Needed for conversion. |
| Shots on target | `statistics.shots.on` | `unknown_until_provider_validation` | Useful attacking context. |
| Passes | `statistics.passes.total` | `unknown_until_provider_validation` | Can support passes per 90 if present. |
| Key passes | `statistics.passes.key` | `unknown_until_provider_validation` | Can support key passes per 90 if present. |
| Pass accuracy | `statistics.passes.accuracy` | `unknown_until_provider_validation` | May be a string or percentage-like value. |
| Successful dribbles | `statistics.dribbles.success` | `unknown_until_provider_validation` | Can support successful dribbles per 90 if present. |
| Duels | `statistics.duels.total` | `unknown_until_provider_validation` | Needed for duel win percentage. |
| Duels won | `statistics.duels.won` | `unknown_until_provider_validation` | Needed for duel win percentage. |
| Tackles | `statistics.tackles.total` | `unknown_until_provider_validation` | Basic defensive count. |
| Interceptions | `statistics.tackles.interceptions` | `unknown_until_provider_validation` | Raw interceptions only; not possession-adjusted. |
| Cards | `statistics.cards.yellow`, `statistics.cards.red` | `unknown_until_provider_validation` | Context field, not a core performance metric. |
| Saves | `statistics.goals.saves` | `unknown_until_provider_validation` | Goalkeeper metric if exposed. |
| Goals conceded | `statistics.goals.conceded` | `unknown_until_provider_validation` | Goalkeeper/team context if exposed. |
| Non-penalty goals | Goal and penalty fields if available | `partially_supported` | Requires penalty-goal field; otherwise unsupported. |
| Goal conversion % | Goals and shots | `partially_supported` | Supported only if shots and goals are present. |
| Save percentage % | Saves and shots on target faced | `partially_supported` | API-Football may not expose shots faced at player level. |
| Expected assists | None confirmed | `requires_paid_event_data` | Do not show as real until provider validates xA. |
| Non-penalty xG | None confirmed | `requires_paid_event_data` | Requires xG/npxG feed or add-on. |
| npxG + xA | None confirmed | `requires_paid_event_data` | Requires xG/xA feed or add-on. |
| PSxG - GA | None confirmed | `requires_paid_event_data` | Requires post-shot xG. |
| Progressive carries | None confirmed | `requires_paid_event_data` | Requires event data and stable definition. |
| Progressive passes | None confirmed | `requires_paid_event_data` | Requires event data and stable definition. |
| Possession-adjusted interceptions | Interceptions plus possession context | `requires_paid_event_data` | Needs team/opponent possession context and methodology. |
| Touches in box | None confirmed | `requires_paid_event_data` | Requires zone/touch event data. |
| Offensive duels won | None confirmed | `requires_paid_event_data` | Requires Wyscout-style duel taxonomy or equivalent. |

## Implementation Rule

The application must not present `unknown_until_provider_validation`, `requires_paid_event_data`, or `not_supported` metrics as real values. These metrics can appear in methodology and glossary views with clear unavailable or blocked states.

