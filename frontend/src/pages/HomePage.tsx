import { ArrowRight } from "lucide-react";

interface HomePageProps {
  onNavigate: (page: string) => void;
}

export function HomePage({ onNavigate }: HomePageProps) {
  return (
    <section className="hero">
      <div className="hero__content">
        <p className="eyebrow">Player analytics for selected leagues</p>
        <h1>ScoutFootball</h1>
        <p className="hero__copy">
          Find better players through clearer football data, starting with a real provider
          validation path for API-Football and Sportmonks.
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

