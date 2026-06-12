import { useEffect, useState } from "react";

import { Shell } from "./components/Shell";
import { StatusPanel } from "./components/StatusPanel";
import { ComparePage } from "./pages/ComparePage";
import { HomePage } from "./pages/HomePage";
import { LeaguesPage } from "./pages/LeaguesPage";
import { MethodologyPage } from "./pages/MethodologyPage";
import { PlayersPage } from "./pages/PlayersPage";
import { RankingsPage } from "./pages/RankingsPage";
import { getProviderStatus } from "./lib/api";
import type { ProviderStatusResponse } from "./types/api";

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
  const [providerStatus, setProviderStatus] = useState<ProviderStatusResponse | null>(null);

  useEffect(() => {
    getProviderStatus().then(setProviderStatus).catch(() => setProviderStatus(null));
  }, []);

  return (
    <Shell currentPage={page} onNavigate={setPage}>
      <div className="provider-strip">
        <StatusPanel
          title="Provider status"
          message={
            providerStatus?.providers?.api_football_configured
              ? "API-Football key is configured."
              : "API-Football key is not configured. Real data validation is required."
          }
          tone={providerStatus?.providers?.api_football_configured ? "success" : "warning"}
        />
      </div>
      {renderPage(page, setPage)}
    </Shell>
  );
}

