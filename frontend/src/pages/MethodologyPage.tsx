import { useEffect, useState } from "react";

import { getMetrics } from "../lib/api";
import type { MetricsResponse } from "../types/api";

export function MethodologyPage() {
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);

  useEffect(() => {
    getMetrics().then(setMetrics).catch(() => setMetrics(null));
  }, []);

  return (
    <section className="page">
      <div className="page__heading">
        <p className="eyebrow">Methodology</p>
        <h2>Data rules</h2>
        <p>
          ScoutFootball calculates metrics from StatsBomb Open Data events. Historical seasons are
          clearly labeled, and custom definitions may differ from DataMB, FBref, Opta, Wyscout, or
          StatsBomb commercial products.
        </p>
      </div>
      <div className="method-grid">
        <article>
          <h3>Primary source</h3>
          <p>Data source: StatsBomb Open Data. API-Football remains an optional metadata fallback.</p>
        </article>
        <article>
          <h3>Storage</h3>
          <p>SQLite stores normalized player-season rows, metric values, and percentile metadata.</p>
        </article>
        <article>
          <h3>Visuals</h3>
          <p>D3 is limited to compact percentile bars and inline metric indicators for this phase.</p>
        </article>
      </div>
      {metrics ? (
        <div className="method-grid method-grid--spaced">
          <article>
            <h3>Supported MVP metrics</h3>
            <p>{metrics.supported_metrics.join(", ")}</p>
          </article>
          <article>
            <h3>Blocked metrics</h3>
            <p>{metrics.blocked_metrics.join(", ")}</p>
          </article>
        </div>
      ) : null}
    </section>
  );
}
