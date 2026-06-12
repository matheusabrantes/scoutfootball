export type LeagueStatus =
  | "active"
  | "validated"
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
  real_data_configured: boolean;
  leagues: League[];
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
}

