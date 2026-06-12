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
          ScoutFootball shows only metrics backed by validated provider fields. Unsupported advanced
          metrics remain blocked until paid event data or an equivalent licensed feed is available.
        </p>
      </div>
      <div className="method-grid">
        <article>
          <h3>Primary source</h3>
          <p>API-Football / API-SPORTS is validated first. Sportmonks remains the backup provider.</p>
        </article>
        <article>
          <h3>Storage</h3>
          <p>SQLite is the local MVP target, with PostgreSQL planned after the data model is proven.</p>
        </article>
        <article>
          <h3>Visuals</h3>
          <p>D3 is limited to small interface elements such as percentile bars for this phase.</p>
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
