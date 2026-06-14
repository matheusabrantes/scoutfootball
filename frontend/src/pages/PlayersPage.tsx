import { useEffect, useState } from "react";

import { StatusPanel } from "../components/StatusPanel";
import { getPlayersMetadata } from "../lib/api";
import type { PlayerFieldResponse } from "../types/api";

export function PlayersPage() {
  const [data, setData] = useState<PlayerFieldResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [positionGroup, setPositionGroup] = useState("");
  const [minimumMinutes, setMinimumMinutes] = useState("0");

  useEffect(() => {
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (positionGroup) params.set("position_group", positionGroup);
    if (minimumMinutes) params.set("minimum_minutes", minimumMinutes);
    getPlayersMetadata(params.toString())
      .then(setData)
      .catch((requestError: Error) => setError(requestError.message));
  }, [minimumMinutes, positionGroup, search]);

  if (error) {
    return <StatusPanel title="Backend unavailable" message={error} tone="warning" />;
  }

  return (
    <section className="page">
      <div className="page__heading">
        <p className="eyebrow">Historical dataset</p>
        <h2>Players</h2>
        <p>
          Real player-season rows calculated from StatsBomb Open Data events. Historical data is not
          presented as current-season coverage.
        </p>
      </div>
      <div className="filter-bar">
        <input placeholder="Search player" value={search} onChange={(event) => setSearch(event.target.value)} />
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
      </div>
      {!data ? (
        <StatusPanel title="Loading provider state" message="Checking backend data status." />
      ) : data.error ? (
        <StatusPanel title="Real data not configured" message={data.message ?? data.error} tone="warning" />
      ) : data.players?.length ? (
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
              {data.players.map((player) => (
                <tr key={player.player_season_stats_id}>
                  <td>{player.id}</td>
                  <td>{player.name}</td>
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
