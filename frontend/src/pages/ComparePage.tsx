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
        <p className="eyebrow">Two to five players</p>
        <h2>Compare</h2>
        <p>Comparison stays table-first. No radar charts, scatter plots, or club analysis.</p>
      </div>
      <StatusPanel
        title={data?.players.length ? "Comparison ready" : "Choose players after ingestion"}
        message={data?.message ?? "Use ?player_ids=1,2 once real players are ingested."}
        tone={data?.players.length ? "success" : "neutral"}
      />
    </section>
  );
}
