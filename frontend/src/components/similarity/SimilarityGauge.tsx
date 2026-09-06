import { TONE_HEX, type Tone } from "../../lib/status";

function similarityTone(pct: number, threshold: number): Tone {
  if (pct > threshold) return "critical";
  if (pct > threshold * 0.6) return "warning";
  return "success";
}

export function SimilarityGauge({
  percentage,
  threshold = 30,
  size = 140,
}: {
  percentage: number;
  threshold?: number;
  size?: number;
}) {
  const strokeWidth = 12;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - Math.min(100, percentage) / 100);
  const tone = similarityTone(percentage, threshold);

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} stroke="var(--color-ink-100)" strokeWidth={strokeWidth} fill="none" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={TONE_HEX[tone]}
          strokeWidth={strokeWidth}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 0.7s ease-out" }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="text-3xl font-bold text-ink-900">{percentage}%</span>
        <span className="text-[11px] font-medium uppercase tracking-wide text-ink-400">Similarity</span>
      </div>
    </div>
  );
}
