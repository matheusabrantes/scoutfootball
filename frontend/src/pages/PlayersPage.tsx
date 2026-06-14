import { useEffect, useState } from "react";

import { StatusPanel } from "../components/StatusPanel";
import { getPlayersMetadata } from "../lib/api";
import type { PlayerFieldResponse, PlayerRow } from "../types/api";

interface PlayersPageProps {
  onNavigate: (page: string) => void;
}

type PlayerSortKey = "minutes" | "name" | "team_name";

export function PlayersPage({ onNavigate }: PlayersPageProps) {
  const [data, setData] = useState<PlayerFieldResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [competition, setCompetition] = useState("");
  const [season, setSeason] = useState("");
  const [team, setTeam] = useState("");
  const [positionGroup, setPositionGroup] = useState("");
  const [minimumMinutes, setMinimumMinutes] = useState("0");
  const [sortKey, setSortKey] = useState<PlayerSortKey>("minutes");

  useEffect(() => {
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (competition) params.set("competition", competition);
    if (season) params.set("season", season);
    if (team) params.set("team", team);
    if (positionGroup) params.set("position_group", positionGroup);
    if (minimumMinutes) params.set("minimum_minutes", minimumMinutes);
    getPlayersMetadata(params.toString())
      .then(setData)
      .catch((requestError: Error) => setError(requestError.message));
  }, [competition, minimumMinutes, positionGroup, search, season, team]);

  const players = sortPlayers(data?.players ?? [], sortKey);

  if (error) {
    return <StatusPanel title="Backend unavailable" message={error} tone="warning" />;
  }

  return (
    <section className="page">
      <div className="page__heading">
        <p className="eyebrow">Historical dataset · Data source: StatsBomb Open Data</p>
        <h2>Players</h2>
        <p>
          Real player-season rows calculated from StatsBomb Open Data events. Historical data is not
          presented as current-season coverage.
        </p>
      </div>
      <div className="filter-bar">
        <input placeholder="Search player" value={search} onChange={(event) => setSearch(event.target.value)} />
        <select value={competition} onChange={(event) => setCompetition(event.target.value)}>
          <option value="">All competitions</option>
          <option value="statsbomb_premier_league_2015_2016">Premier League 2015/2016</option>
          <option value="statsbomb_bundesliga_2023_2024">Bundesliga 2023/2024 partial</option>
        </select>
        <select value={season} onChange={(event) => setSeason(event.target.value)}>
          <option value="">All seasons</option>
          <option value="2016">2016</option>
          <option value="2024">2024</option>
        </select>
        <input placeholder="Team" value={team} onChange={(event) => setTeam(event.target.value)} />
        <select value={positionGroup} onChange={(event) => setPositionGroup(event.target.value)}>
          <option value="">All positions</option>
          <option value="Goalkeepers">Goalkeepers</option>
          <option value="Centrebacks">Centrebacks</option>
          <option value="Fullbacks">Fullbacks</option>
          <option value="Midfielders">Midfielders</option>
          <option value="Attackers">Attackers</option>
        </select>
        <select value={minimumMinutes} onChange={(event) => setMinimumMinutes(event.target.value)}>
          <option value="0">0+ minutes</option>
          <option value="300">300+ minutes</option>
          <option value="500">500+ minutes</option>
          <option value="900">900+ minutes</option>
        </select>
        <select value={sortKey} onChange={(event) => setSortKey(event.target.value as PlayerSortKey)}>
          <option value="minutes">Sort by minutes</option>
          <option value="name">Sort by player</option>
          <option value="team_name">Sort by team</option>
        </select>
      </div>
      {!data ? (
        <StatusPanel title="Loading provider state" message="Checking backend data status." />
      ) : data.error ? (
        <StatusPanel title="Real data not configured" message={data.message ?? data.error} tone="warning" />
      ) : players.length ? (
        <div className="table-surface">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Player</th>
                <th>Team</th>
                <th>League</th>
                <th>Position</th>
                <th>Minutes</th>
                <th>Source</th>
              </tr>
            </thead>
            <tbody>
              {players.map((player) => (
                <tr key={player.player_season_stats_id}>
                  <td>{player.id}</td>
                  <td>
                    <button className="table-link" onClick={() => onNavigate(`/players/${player.id}`)}>
                      {player.name}
                    </button>
                  </td>
                  <td>{player.team_name}</td>
                  <td>{player.league_name}</td>
                  <td>{player.position_group}</td>
                  <td>{player.minutes ?? "-"}</td>
                  <td>{player.historical_demo ? "Historical StatsBomb" : player.provider ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <StatusPanel
          title="No data ingested"
          message={data.message ?? "Run the SQLite init and API-Football ingestion scripts."}
          tone="warning"
        />
      )}
    </section>
  );
}

function sortPlayers(players: PlayerRow[], sortKey: PlayerSortKey): PlayerRow[] {
  return [...players].sort((first, second) => {
    if (sortKey === "minutes") {
      return (second.minutes ?? 0) - (first.minutes ?? 0);
    }
    return String(first[sortKey] ?? "").localeCompare(String(second[sortKey] ?? ""));
  });
}
