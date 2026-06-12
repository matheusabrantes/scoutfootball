import { useEffect, useState } from "react";

import { StatusPanel } from "../components/StatusPanel";
import { getCompareMetadata } from "../lib/api";
import type { PlayerFieldResponse } from "../types/api";

export function ComparePage() {
  const [data, setData] = useState<PlayerFieldResponse | null>(null);

  useEffect(() => {
    getCompareMetadata().then(setData).catch((error: Error) =>
      setData({ mock: false, error: error.message })
    );
  }, []);

  return (
    <section className="page">
      <div className="page__heading">
        <p className="eyebrow">Two to five players</p>
        <h2>Compare</h2>
        <p>Comparison stays table-first. No radar charts, scatter plots, or club analysis.</p>
      </div>
      <StatusPanel
        title={data?.error ? "Real comparison unavailable" : "Awaiting player ingestion"}
        message={data?.message ?? data?.error ?? "Checking comparison readiness."}
        tone={data?.error ? "warning" : "neutral"}
      />
    </section>
  );
}

