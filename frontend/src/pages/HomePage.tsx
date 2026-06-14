import { ArrowRight } from "lucide-react";

interface HomePageProps {
  onNavigate: (page: string) => void;
}

export function HomePage({ onNavigate }: HomePageProps) {
  return (
    <section className="hero">
      <div className="hero__content">
        <p className="eyebrow">Historical dataset powered by StatsBomb Open Data</p>
        <h1>ScoutFootball</h1>
        <p className="hero__copy">
          Explore real event-derived player metrics from historical StatsBomb Open Data
          competitions. The first release starts with Premier League 2015/2016 and clearly labels
          historical coverage.
        </p>
        <div className="hero__actions">
          <button className="primary-action" onClick={() => onNavigate("players")}>
            Explore Players
            <ArrowRight size={18} />
          </button>
          <button className="secondary-action" onClick={() => onNavigate("leagues")}>
            Check Coverage
          </button>
        </div>
      </div>
    </section>
  );
}
