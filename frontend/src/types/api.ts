export type LeagueStatus =
  | "active"
  | "validated"
  | "incomplete"
  | "not_selected"
  | "needs_validation"
  | "provider_not_available"
  | "blocked";

export type LeaguePriority = "P0" | "P1" | "P2";

export interface League {
  internal_league_key: string;
  display_name: string;
  country: string;
  priority: LeaguePriority;
  provider_name: string;
  api_football_league_id: number | null;
  sportmonks_league_id: number | null;
  status: LeagueStatus;
  notes: string;
}

export interface LeagueResponse {
  data_source: string;
  primary_mvp_metrics_provider?: string;
  mvp_mode?: string;
  real_data_configured: boolean;
  leagues?: League[];
  statsbomb_competitions?: StatsBombCompetition[];
  api_football_fallback_leagues?: League[];
}

export interface StatsBombCompetition {
  internal_key: string;
  competition_id: number;
  season_id: number;
  country: string;
  competition_name: string;
  season_name: string;
  expected_match_count: number;
  actual_match_count: number;
  status: LeagueStatus;
  historical_demo: boolean;
  notes: string;
}

export interface ProviderStatusResponse {
  status?: string;
  service?: string;
  providers?: {
    api_football_configured: boolean;
    sportmonks_configured: boolean;
  };
}

export interface PlayerFieldResponse {
  mock: boolean;
  message?: string;
  error?: string;
  api_football_configured?: boolean;
  validated_leagues?: string[];
  player_field_paths?: string[];
  players?: PlayerRow[];
  count?: number;
  rankings?: RankingRow[];
  metric?: string;
  metadata?: ResponseMetadata;
}

export interface PlayerProfileResponse {
  data_source: string;
  mock: boolean;
  player: PlayerRow & {
    metrics: Array<{
      metric_key: string;
      metric_value: number | null;
      percentile: number | null;
      peer_count: number | null;
    }>;
  };
}

export interface PlayerRow {
  id: number;
  provider_player_id: number;
  name: string;
  age: number | null;
  nationality: string | null;
  team_name: string;
  league_key: string;
  league_name: string;
  season: number;
  player_season_stats_id: number;
  position: string | null;
  position_group: string;
  appearances: number | null;
  starts: number | null;
  minutes: number | null;
  rating: number | null;
  provider?: string;
  historical_demo?: number;
  metric_definition_version?: string | null;
  last_updated_at?: string | null;
}

export interface RankingRow extends PlayerRow {
  metric_key: string;
  metric_value: number | null;
  percentile: number | null;
  peer_count: number | null;
  population_size?: number | null;
  minutes_threshold?: number | null;
}

export interface CompareResponse {
  data_source?: string;
  mock: boolean;
  message?: string;
  players: Array<{
    id: number;
    name: string;
    team_name: string;
    league_name: string;
    season: number;
    position_group: string;
    metrics: Record<string, { value: number | null; percentile: number | null }>;
  }>;
}

export interface MetricsResponse {
  data_source: string;
  mock: boolean;
  supported_metrics: string[];
  stored_metrics: Array<{ metric_key: string; row_count: number; value_count: number }>;
  blocked_metrics: string[];
  metric_definition_version?: string;
}

export interface ResponseMetadata {
  source: string;
  historical_demo: boolean;
  metric_definition_version: string | null;
  last_updated_at: string | null;
}

export interface DataSourcesResponse {
  mock: boolean;
  primary_mvp_metrics_provider: string;
  mvp_mode: string;
  sources: Array<{ provider: string; player_rows: number; last_updated_at: string | null }>;
  statsbomb_competitions: StatsBombCompetition[];
  attribution: string;
}
