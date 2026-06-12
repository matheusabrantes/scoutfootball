import { scaleLinear } from "d3";

interface PercentileBarProps {
  value: number;
  label: string;
}

export function PercentileBar({ value, label }: PercentileBarProps) {
  const widthScale = scaleLinear().domain([0, 100]).range([0, 100]).clamp(true);
  const width = widthScale(value);

  return (
    <div className="percentile" aria-label={`${label}: ${value} percentile`}>
      <div className="percentile__track">
        <div className="percentile__fill" style={{ width: `${width}%` }} />
      </div>
      <span>{value}</span>
    </div>
  );
}

