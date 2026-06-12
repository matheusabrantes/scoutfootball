import { useEffect, useState } from "react";

import { getLeagues } from "../lib/api";
import type { League, LeagueResponse } from "../types/api";

const priorityOrder = ["P0", "P1", "P2"];

function groupLeagues(leagues: League[]) {
  return priorityOrder.map((priority) => ({
    priority,
    leagues: leagues.filter((league) => league.priority === priority)
  }));
}

export function LeaguesPage() {
  const [data, setData] = useState<LeagueResponse | null>(null);

  useEffect(() => {
    getLeagues().then(setData).catch(() => setData(null));
  }, []);

  return (
    <section className="page">
      <div className="page__heading">
        <p className="eyebrow">Coverage</p>
        <h2>League validation</h2>
        <p>Inactive leagues stay mapped but hidden from production UI until real player data is validated.</p>
      </div>
      <div className="league-list">
        {groupLeagues(data?.leagues ?? []).map((group) => (
          <section className="league-group" key={group.priority}>
            <h3>{group.priority}</h3>
            {group.leagues.map((league) => (
              <article className="league-row" key={league.internal_league_key}>
                <div>
                  <strong>{league.display_name}</strong>
                  <span>{league.country}</span>
                </div>
                <span className={`status-pill status-pill--${league.status}`}>{league.status}</span>
              </article>
            ))}
          </section>
        ))}
      </div>
    </section>
  );
}

