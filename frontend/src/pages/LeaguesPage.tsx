import { useEffect, useState } from "react";

import { getLeagues } from "../lib/api";
import type { LeagueResponse } from "../types/api";

export function LeaguesPage() {
  const [data, setData] = useState<LeagueResponse | null>(null);

  useEffect(() => {
    getLeagues().then(setData).catch(() => setData(null));
  }, []);

  return (
    <section className="page">
      <div className="page__heading">
        <p className="eyebrow">Historical dataset · Data source: StatsBomb Open Data</p>
        <h2>Historical datasets</h2>
        <p>Available competitions depend on StatsBomb Open Data and are clearly labeled as historical.</p>
      </div>
      <div className="league-list">
        {(data?.statsbomb_competitions ?? []).map((competition) => (
          <article className="league-row" key={competition.internal_key}>
            <div>
              <strong>
                {competition.competition_name} {competition.season_name}
              </strong>
              <span>
                {competition.country} · {competition.actual_match_count}/{competition.expected_match_count} matches
              </span>
            </div>
            <span className={`status-pill status-pill--${competition.status}`}>{competition.status}</span>
          </article>
        ))}
      </div>
    </section>
  );
}
