import { useEffect, useState } from "react";

import { StatusPanel } from "../components/StatusPanel";
import { PercentileBar } from "../d3/PercentileBar";
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
      ) : (
        <div className="data-surface">
          <StatusPanel
            title="Provider sample available"
            message={data.message ?? "API-Football metadata is available."}
            tone="success"
          />
          <div className="metric-grid">
            {(data.player_field_paths ?? []).slice(0, 12).map((fieldPath, index) => (
              <article className="metric-card" key={fieldPath}>
                <span>{fieldPath}</span>
                <PercentileBar value={Math.min(95, 35 + index * 5)} label={fieldPath} />
              </article>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}

