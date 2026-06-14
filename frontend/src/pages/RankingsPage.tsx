import { useEffect, useState } from "react";

import { StatusPanel } from "../components/StatusPanel";
import { PercentileBar } from "../d3/PercentileBar";
import { getRankingsMetadata } from "../lib/api";
import type { PlayerFieldResponse } from "../types/api";

export function RankingsPage() {
  const [data, setData] = useState<PlayerFieldResponse | null>(null);
  const [metric, setMetric] = useState("goals");
  const [competition, setCompetition] = useState("");
  const [season, setSeason] = useState("");
  const [team, setTeam] = useState("");
  const [positionGroup, setPositionGroup] = useState("");
  const [minimumMinutes, setMinimumMinutes] = useState("0");
  const [sort, setSort] = useState("metric_value");

  useEffect(() => {
    const params = new URLSearchParams({ metric, minimum_minutes: minimumMinutes, sort });
    if (competition) params.set("competition", competition);
    if (season) params.set("season", season);
    if (team) params.set("team", team);
    if (positionGroup) params.set("position_group", positionGroup);
    getRankingsMetadata(params.toString()).then(setData).catch((error: Error) =>
      setData({ mock: false, error: error.message })
    );
  }, [competition, metric, minimumMinutes, positionGroup, season, sort, team]);

  return (
    <section className="page">
      <div className="page__heading">
        <p className="eyebrow">Historical dataset · Data source: StatsBomb Open Data</p>
        <h2>Rankings</h2>
        <p>Rank players within the available historical StatsBomb Open Data sample.</p>
      </div>
      <div className="filter-bar">
        <select value={metric} onChange={(event) => setMetric(event.target.value)}>
          <option value="goals">Goals</option>
          <option value="xg">xG</option>
          <option value="npxg">npxG</option>
          <option value="progressive_passes">Progressive passes</option>
          <option value="progressive_carries">Progressive carries</option>
          <option value="passes_completed">Passes completed</option>
          <option value="successful_dribbles">Successful dribbles</option>
        </select>
        <select value={competition} onChange={(event) => setCompetition(event.target.value)}>
          <option value="">All competitions</option>
          <option value="statsbomb_premier_league_2015_2016">Premier League 2015/2016</option>
          <option value="statsbomb_bundesliga_2023_2024">Bundesliga 2023/2024 partial</option>
        </select>
        <select value={season} onChange={(event) => setSeason(event.target.value)}>
          <option value="">All seasons</option>
          <option value="2016">2016</option>
          <option value="2024">2024</option>
        </select>
        <input placeholder="Team" value={team} onChange={(event) => setTeam(event.target.value)} />
        <select value={positionGroup} onChange={(event) => setPositionGroup(event.target.value)}>
          <option value="">All positions</option>
          <option value="Goalkeepers">Goalkeepers</option>
          <option value="Centrebacks">Centrebacks</option>
          <option value="Fullbacks">Fullbacks</option>
          <option value="Midfielders">Midfielders</option>
          <option value="Attackers">Attackers</option>
        </select>
        <select value={minimumMinutes} onChange={(event) => setMinimumMinutes(event.target.value)}>
          <option value="0">0+ minutes</option>
          <option value="300">300+ minutes</option>
          <option value="500">500+ minutes</option>
          <option value="900">900+ minutes</option>
        </select>
        <select value={sort} onChange={(event) => setSort(event.target.value)}>
          <option value="metric_value">Sort by raw value</option>
          <option value="percentile">Sort by percentile</option>
        </select>
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
                <th>Population</th>
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
                  <td>{row.population_size ?? row.peer_count ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </section>
  );
}
