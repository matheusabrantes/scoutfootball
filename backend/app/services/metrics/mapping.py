from typing import Literal, TypedDict


MetricSupportStatus = Literal[
    "supported",
    "partially_supported",
    "not_supported",
    "requires_paid_event_data",
    "unknown_until_provider_validation",
]


class ProviderMetricMapping(TypedDict):
    metric_key: str
    scoutfootball_label: str
    api_football_fields: list[str]
    status: MetricSupportStatus
    notes: str


API_FOOTBALL_METRIC_MAPPING: list[ProviderMetricMapping] = [
    {
        "metric_key": "minutes_played",
        "scoutfootball_label": "Minutes",
        "api_football_fields": ["statistics.games.minutes"],
        "status": "unknown_until_provider_validation",
        "notes": "Commonly expected from player statistics; validate per league and season.",
    },
    {
        "metric_key": "goals",
        "scoutfootball_label": "Goals",
        "api_football_fields": ["statistics.goals.total"],
        "status": "unknown_until_provider_validation",
        "notes": "Use as a base attacking count if present.",
    },
    {
        "metric_key": "assists",
        "scoutfootball_label": "Assists",
        "api_football_fields": ["statistics.goals.assists"],
        "status": "unknown_until_provider_validation",
        "notes": "Use as a base attacking count if present.",
    },
    {
        "metric_key": "shots_total",
        "scoutfootball_label": "Shots",
        "api_football_fields": ["statistics.shots.total"],
        "status": "unknown_until_provider_validation",
        "notes": "Can support goal conversion when combined with goals.",
    },
    {
        "metric_key": "shots_on_target",
        "scoutfootball_label": "Shots on target",
        "api_football_fields": ["statistics.shots.on"],
        "status": "unknown_until_provider_validation",
        "notes": "Useful for attacking summaries if available.",
    },
    {
        "metric_key": "passes_total",
        "scoutfootball_label": "Passes",
        "api_football_fields": ["statistics.passes.total"],
        "status": "unknown_until_provider_validation",
        "notes": "Can support passes per 90 if minutes are available.",
    },
    {
        "metric_key": "key_passes",
        "scoutfootball_label": "Key passes",
        "api_football_fields": ["statistics.passes.key"],
        "status": "unknown_until_provider_validation",
        "notes": "Can support key passes per 90 if present.",
    },
    {
        "metric_key": "pass_accuracy",
        "scoutfootball_label": "Pass accuracy",
        "api_football_fields": ["statistics.passes.accuracy"],
        "status": "unknown_until_provider_validation",
        "notes": "May be a percentage string or number depending on provider response.",
    },
    {
        "metric_key": "dribbles_success",
        "scoutfootball_label": "Successful dribbles",
        "api_football_fields": ["statistics.dribbles.success"],
        "status": "unknown_until_provider_validation",
        "notes": "Can support successful dribbles per 90 if present.",
    },
    {
        "metric_key": "duels_total",
        "scoutfootball_label": "Duels",
        "api_football_fields": ["statistics.duels.total"],
        "status": "unknown_until_provider_validation",
        "notes": "Can support broad duel volume.",
    },
    {
        "metric_key": "duels_won",
        "scoutfootball_label": "Duels won",
        "api_football_fields": ["statistics.duels.won"],
        "status": "unknown_until_provider_validation",
        "notes": "Can support duels won percentage with total duels.",
    },
    {
        "metric_key": "tackles",
        "scoutfootball_label": "Tackles",
        "api_football_fields": ["statistics.tackles.total"],
        "status": "unknown_until_provider_validation",
        "notes": "Useful for defensive summaries.",
    },
    {
        "metric_key": "interceptions",
        "scoutfootball_label": "Interceptions",
        "api_football_fields": ["statistics.tackles.interceptions"],
        "status": "unknown_until_provider_validation",
        "notes": "Raw interceptions can be supported if present; possession-adjusted version needs more data.",
    },
    {
        "metric_key": "cards",
        "scoutfootball_label": "Cards",
        "api_football_fields": ["statistics.cards.yellow", "statistics.cards.red"],
        "status": "unknown_until_provider_validation",
        "notes": "Useful context metric; not a primary ScoutFootball performance metric.",
    },
    {
        "metric_key": "saves",
        "scoutfootball_label": "Saves",
        "api_football_fields": ["statistics.goals.saves"],
        "status": "unknown_until_provider_validation",
        "notes": "Can support goalkeeper summaries if present.",
    },
    {
        "metric_key": "xg_xa_family",
        "scoutfootball_label": "xG, npxG, xA",
        "api_football_fields": [],
        "status": "requires_paid_event_data",
        "notes": "Do not show as real unless provider validation proves these fields exist in the selected plan.",
    },
    {
        "metric_key": "progressive_actions",
        "scoutfootball_label": "Progressive carries and passes",
        "api_football_fields": [],
        "status": "requires_paid_event_data",
        "notes": "Requires event data and a stable definition.",
    },
    {
        "metric_key": "psxg_prevented_goals",
        "scoutfootball_label": "PSxG minus goals against",
        "api_football_fields": [],
        "status": "requires_paid_event_data",
        "notes": "Requires post-shot xG or an equivalent paid advanced goalkeeper feed.",
    },
]

