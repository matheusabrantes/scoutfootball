import { useEffect, useState } from "react";

import { StatusPanel } from "../components/StatusPanel";
import { PercentileBar } from "../d3/PercentileBar";
import { getPlayerProfile } from "../lib/api";
import type { PlayerProfileResponse } from "../types/api";

interface PlayerProfilePageProps {
  playerId: number;
}

const FEATURED_METRICS = [
  "goals",
  "xg",
  "assists",
  "progressive_passes",
  "progressive_carries",
  "passes_completed",
  "successful_dribbles",
  "ball_recoveries"
];

export function PlayerProfilePage({ playerId }: PlayerProfilePageProps) {
  const [data, setData] = useState<PlayerProfileResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPlayerProfile(playerId)
      .then((profile) => {
        setData(profile);
        setError(null);
      })
      .catch((requestError: Error) => {
        setData(null);
        setError(requestError.message);
      });
  }, [playerId]);

  if (error) {
    return <StatusPanel title="Player unavailable" message={error} tone="warning" />;
  }

  if (!data) {
    return <StatusPanel title="Loading player" message="Checking StatsBomb player profile." />;
  }

  const metricsByKey = new Map(data.player.metrics.map((metric) => [metric.metric_key, metric]));

  return (
    <section className="page">
      <div className="page__heading">
        <p className="eyebrow">Historical dataset · Data source: StatsBomb Open Data</p>
        <h2>{data.player.name}</h2>
        <p>
          {data.player.team_name} · {data.player.league_name} · {data.player.season} ·{" "}
          {data.player.position_group} · {data.player.minutes ?? "-"} minutes
        </p>
      </div>
      <div className="metric-grid">
        {FEATURED_METRICS.map((metricKey) => {
          const metric = metricsByKey.get(metricKey);
          return (
            <article className="metric-card" key={metricKey}>
              <h3>{metricKey.replace(/_/g, " ")}</h3>
              <strong>{metric?.metric_value ?? "-"}</strong>
              {metric?.percentile == null ? (
                <span>Percentile unavailable</span>
              ) : (
                <PercentileBar value={metric.percentile} label={metricKey} />
              )}
            </article>
          );
        })}
      </div>
    </section>
  );
}
