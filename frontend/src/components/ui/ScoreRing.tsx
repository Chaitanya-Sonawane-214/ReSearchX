import { cn } from "../../lib/utils";
import { scoreTone, TONE_HEX } from "../../lib/status";

export function ScoreRing({
  score,
  size = 96,
  strokeWidth = 9,
  label,
  className,
}: {
  score: number;
  size?: number;
  strokeWidth?: number;
  label?: string;
  className?: string;
}) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - Math.max(0, Math.min(100, score)) / 100);
  const tone = scoreTone(score);

  return (
    <div className={cn("relative inline-flex items-center justify-center", className)} style={{ width: size, height: size }}>
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
      <div className="absolute flex flex-col items-center justify-center">
        <span className="text-2xl font-bold text-ink-900">{score}</span>
        {label && <span className="text-[10px] font-medium uppercase tracking-wide text-ink-400">{label}</span>}
      </div>
    </div>
  );
}
