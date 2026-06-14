import { useEffect, useState } from "react";

import { Shell } from "./components/Shell";
import { StatusPanel } from "./components/StatusPanel";
import { ComparePage } from "./pages/ComparePage";
import { HomePage } from "./pages/HomePage";
import { LeaguesPage } from "./pages/LeaguesPage";
import { MethodologyPage } from "./pages/MethodologyPage";
import { PlayerProfilePage } from "./pages/PlayerProfilePage";
import { PlayersPage } from "./pages/PlayersPage";
import { RankingsPage } from "./pages/RankingsPage";
import { getDataSources } from "./lib/api";
import type { DataSourcesResponse } from "./types/api";

function routeFromPath(pathname: string): string {
  if (pathname === "/players") return "players";
  if (pathname.startsWith("/players/")) return pathname;
  if (pathname === "/rankings") return "rankings";
  if (pathname === "/compare") return "compare";
  if (pathname === "/leagues") return "leagues";
  if (pathname === "/methodology") return "methodology";
  return "home";
}

function pathFromPage(page: string): string {
  if (page === "home") return "/";
  if (page.startsWith("/players/")) return page;
  return `/${page}`;
}

function renderPage(page: string, onNavigate: (page: string) => void) {
  if (page === "players") return <PlayersPage onNavigate={onNavigate} />;
  if (page.startsWith("/players/")) {
    const playerId = Number(page.replace("/players/", ""));
    return Number.isFinite(playerId) ? (
      <PlayerProfilePage playerId={playerId} />
    ) : (
      <StatusPanel title="Invalid player" message="The player URL does not contain a valid ID." tone="warning" />
    );
  }
  if (page === "rankings") return <RankingsPage />;
  if (page === "compare") return <ComparePage />;
  if (page === "leagues") return <LeaguesPage />;
  if (page === "methodology") return <MethodologyPage />;
  return <HomePage onNavigate={onNavigate} />;
}

export default function App() {
  const [page, setPage] = useState(routeFromPath(window.location.pathname));
  const [dataSources, setDataSources] = useState<DataSourcesResponse | null>(null);

  useEffect(() => {
    getDataSources().then(setDataSources).catch(() => setDataSources(null));
  }, []);

  useEffect(() => {
    const handlePopState = () => setPage(routeFromPath(window.location.pathname));
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  function handleNavigate(nextPage: string) {
    const nextPath = pathFromPage(nextPage);
    if (window.location.pathname !== nextPath) {
      window.history.pushState({}, "", nextPath);
    }
    setPage(nextPage);
  }

  return (
    <Shell currentPage={page} onNavigate={handleNavigate}>
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
      {renderPage(page, handleNavigate)}
    </Shell>
  );
}
