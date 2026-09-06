import { cn } from "../../lib/utils";
import { TONE_CLASSES, type Tone } from "../../lib/status";

export function ProgressBar({
  value,
  tone = "brand",
  className,
  height = "h-2",
}: {
  value: number;
  tone?: Tone;
  className?: string;
  height?: string;
}) {
  const clamped = Math.max(0, Math.min(100, value));
  return (
    <div className={cn("w-full overflow-hidden rounded-full bg-ink-100", height, className)}>
      <div
        className={cn("h-full rounded-full transition-all duration-500 ease-out", TONE_CLASSES[tone].dot)}
        style={{ width: `${clamped}%` }}
      />
    </div>
  );
}
