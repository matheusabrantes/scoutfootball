import { useEffect, useState } from "react";

import { StatusPanel } from "../components/StatusPanel";
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
    </section>
  );
}

