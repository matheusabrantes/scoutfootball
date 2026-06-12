import type { LeagueResponse, PlayerFieldResponse, ProviderStatusResponse } from "../types/api";

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

export function getLeagues(): Promise<LeagueResponse> {
  return request<LeagueResponse>("/api/leagues");
}

export function getPlayersMetadata(): Promise<PlayerFieldResponse> {
  return request<PlayerFieldResponse>("/api/players");
}

export function getRankingsMetadata(): Promise<PlayerFieldResponse> {
  return request<PlayerFieldResponse>("/api/rankings");
}

export function getCompareMetadata(): Promise<PlayerFieldResponse> {
  return request<PlayerFieldResponse>("/api/compare");
}

