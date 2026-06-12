import { useEffect, useState } from "react";

import { StatusPanel } from "../components/StatusPanel";
import { getPlayersMetadata } from "../lib/api";
import type { PlayerFieldResponse } from "../types/api";

export function PlayersPage() {
  const [data, setData] = useState<PlayerFieldResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPlayersMetadata().then(setData).catch((requestError: Error) => setError(requestError.message));
  }, []);

  if (error) {
    return <StatusPanel title="Backend unavailable" message={error} tone="warning" />;
  }

  return (
    <section className="page">
      <div className="page__heading">
        <p className="eyebrow">Real data first</p>
        <h2>Players</h2>
        <p>
          This page reads provider validation metadata. It will not silently show fake players when
          real data is not configured.
        </p>
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
                <th>Player</th>
                <th>Team</th>
                <th>League</th>
                <th>Position</th>
                <th>Minutes</th>
                <th>Rating</th>
              </tr>
            </thead>
            <tbody>
              {data.players.map((player) => (
                <tr key={player.player_season_stats_id}>
                  <td>{player.name}</td>
                  <td>{player.team_name}</td>
                  <td>{player.league_name}</td>
                  <td>{player.position_group}</td>
                  <td>{player.minutes ?? "-"}</td>
                  <td>{player.rating ?? "-"}</td>
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
