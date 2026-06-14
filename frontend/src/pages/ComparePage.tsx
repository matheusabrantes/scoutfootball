import { useEffect, useState } from "react";

import { StatusPanel } from "../components/StatusPanel";
import { getCompareMetadata } from "../lib/api";
import type { CompareResponse } from "../types/api";

export function ComparePage() {
  const [data, setData] = useState<CompareResponse | null>(null);

  useEffect(() => {
    getCompareMetadata().then(setData).catch((error: Error) =>
      setData({ mock: false, message: error.message, players: [] })
    );
  }, []);

  return (
    <section className="page">
      <div className="page__heading">
        <p className="eyebrow">Historical dataset</p>
        <h2>Compare</h2>
        <p>Compare two to five real StatsBomb player rows in a table-first view.</p>
      </div>
      <StatusPanel
        title={data?.players.length ? "Comparison ready" : "Choose players after ingestion"}
        message={data?.message ?? "Use ?player_ids=1,2 once real players are ingested."}
        tone={data?.players.length ? "success" : "neutral"}
      />
      {data?.players.length ? (
        <div className="table-surface table-surface--spaced">
          <table>
            <thead>
              <tr>
                <th>Player</th>
                <th>Team</th>
                <th>Competition</th>
                <th>Season</th>
                <th>Goals</th>
                <th>xG</th>
                <th>Progressive passes</th>
              </tr>
            </thead>
            <tbody>
              {data.players.map((player) => (
                <tr key={player.id}>
                  <td>{player.name}</td>
                  <td>{player.team_name}</td>
                  <td>{player.league_name}</td>
                  <td>{player.season}</td>
                  <td>{player.metrics.goals?.value ?? "-"}</td>
                  <td>{player.metrics.xg?.value ?? "-"}</td>
                  <td>{player.metrics.progressive_passes?.value ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </section>
  );
}
