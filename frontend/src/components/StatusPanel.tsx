interface StatusPanelProps {
  title: string;
  message: string;
  tone?: "neutral" | "warning" | "success";
}

export function StatusPanel({ title, message, tone = "neutral" }: StatusPanelProps) {
  return (
    <section className={`status-panel status-panel--${tone}`}>
      <p>{title}</p>
      <span>{message}</span>
    </section>
  );
}

