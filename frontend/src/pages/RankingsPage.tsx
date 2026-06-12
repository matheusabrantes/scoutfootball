import { useEffect, useState } from "react";

import { StatusPanel } from "../components/StatusPanel";
import { PercentileBar } from "../d3/PercentileBar";
import { getRankingsMetadata } from "../lib/api";
import type { PlayerFieldResponse } from "../types/api";

export function RankingsPage() {
  const [data, setData] = useState<PlayerFieldResponse | null>(null);

  useEffect(() => {
    getRankingsMetadata().then(setData).catch((error: Error) =>
      setData({ mock: false, error: error.message })
    );
  }, []);

  return (
    <section className="page">
      <div className="page__heading">
        <p className="eyebrow">Position tables</p>
        <h2>Rankings</h2>
        <p>Rankings will activate after provider validation and local storage ingestion.</p>
      </div>
      <StatusPanel
        title={data?.error ? "Real rankings unavailable" : "Awaiting ingestion"}
        message={data?.message ?? data?.error ?? "Checking ranking readiness."}
        tone={data?.error ? "warning" : "neutral"}
      />
      {data?.rankings?.length ? (
        <div className="table-surface table-surface--spaced">
          <table>
            <thead>
              <tr>
                <th>Player</th>
                <th>Team</th>
                <th>Metric</th>
                <th>Value</th>
                <th>Percentile</th>
              </tr>
            </thead>
            <tbody>
              {data.rankings.map((row) => (
                <tr key={`${row.id}-${row.metric_key}`}>
                  <td>{row.name}</td>
                  <td>{row.team_name}</td>
                  <td>{row.metric_key}</td>
                  <td>{row.metric_value ?? "-"}</td>
                  <td>
                    {row.percentile === null ? "-" : <PercentileBar value={row.percentile} label={row.name} />}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </section>
  );
}
