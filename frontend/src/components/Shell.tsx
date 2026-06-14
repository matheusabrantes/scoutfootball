import { BarChart3, GitCompare, ListFilter, Search } from "lucide-react";
import type { ReactNode } from "react";

interface ShellProps {
  currentPage: string;
  onNavigate: (page: string) => void;
  children: ReactNode;
}

const navItems = [
  { key: "home", label: "ScoutFootball", icon: Search },
  { key: "players", label: "Players", icon: ListFilter },
  { key: "rankings", label: "Rankings", icon: BarChart3 },
  { key: "compare", label: "Compare", icon: GitCompare },
  { key: "leagues", label: "Leagues", icon: ListFilter },
  { key: "methodology", label: "Methodology", icon: Search }
];

export function Shell({ currentPage, onNavigate, children }: ShellProps) {
  return (
    <div className="app-shell">
      <header className="topbar">
        <button className="brand" onClick={() => onNavigate("home")}>
          ScoutFootball
        </button>
        <nav className="nav">
          {navItems.slice(1).map((item) => {
            const Icon = item.icon;
            return (
              <button
                className={currentPage === item.key ? "nav__item nav__item--active" : "nav__item"}
                key={item.key}
                onClick={() => onNavigate(item.key)}
              >
                <Icon size={16} />
                {item.label}
              </button>
            );
          })}
        </nav>
      </header>
      <main>{children}</main>
    </div>
  );
}

