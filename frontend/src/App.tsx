import { useEffect, useState } from "react";

import { Shell } from "./components/Shell";
import { StatusPanel } from "./components/StatusPanel";
import { ComparePage } from "./pages/ComparePage";
import { HomePage } from "./pages/HomePage";
import { LeaguesPage } from "./pages/LeaguesPage";
import { MethodologyPage } from "./pages/MethodologyPage";
import { PlayersPage } from "./pages/PlayersPage";
import { RankingsPage } from "./pages/RankingsPage";
import { getDataSources } from "./lib/api";
import type { DataSourcesResponse } from "./types/api";

function renderPage(page: string, onNavigate: (page: string) => void) {
  if (page === "players") return <PlayersPage />;
  if (page === "rankings") return <RankingsPage />;
  if (page === "compare") return <ComparePage />;
  if (page === "leagues") return <LeaguesPage />;
  if (page === "methodology") return <MethodologyPage />;
  return <HomePage onNavigate={onNavigate} />;
}

export default function App() {
  const [page, setPage] = useState("home");
  const [dataSources, setDataSources] = useState<DataSourcesResponse | null>(null);

  useEffect(() => {
    getDataSources().then(setDataSources).catch(() => setDataSources(null));
  }, []);

  return (
    <Shell currentPage={page} onNavigate={setPage}>
      <div className="provider-strip">
        <StatusPanel
          title="Provider status"
          message={
            dataSources
              ? "Historical real-data MVP powered by StatsBomb Open Data."
              : "StatsBomb data source not loaded yet."
          }
          tone={dataSources ? "success" : "warning"}
        />
      </div>
      {renderPage(page, setPage)}
    </Shell>
  );
}
