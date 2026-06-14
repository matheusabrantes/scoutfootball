import type {
  CompareResponse,
  DataSourcesResponse,
  LeagueResponse,
  MetricsResponse,
  PlayerFieldResponse,
  ProviderStatusResponse
} from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function getProviderStatus(): Promise<ProviderStatusResponse> {
  return request<ProviderStatusResponse>("/health");
}

export function getDataSources(): Promise<DataSourcesResponse> {
  return request<DataSourcesResponse>("/api/data-sources");
}

export function getLeagues(): Promise<LeagueResponse> {
  return request<LeagueResponse>("/api/leagues");
}

export function getPlayersMetadata(query = ""): Promise<PlayerFieldResponse> {
  return request<PlayerFieldResponse>(`/api/players${query ? `?${query}` : ""}`);
}

export function getRankingsMetadata(query = ""): Promise<PlayerFieldResponse> {
  return request<PlayerFieldResponse>(`/api/rankings${query ? `?${query}` : ""}`);
}

export function getCompareMetadata(playerIds = ""): Promise<CompareResponse> {
  return request<CompareResponse>(`/api/compare${playerIds ? `?player_ids=${playerIds}` : ""}`);
}

export function getMetrics(): Promise<MetricsResponse> {
  return request<MetricsResponse>("/api/metrics");
}
