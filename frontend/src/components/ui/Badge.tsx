import type { ReactNode } from "react";
import { cn } from "../../lib/utils";
import { TONE_CLASSES, type Tone } from "../../lib/status";

export function Badge({
  tone = "neutral",
  animated,
  children,
  className,
}: {
  tone?: Tone;
  animated?: boolean;
  children: ReactNode;
  className?: string;
}) {
  const t = TONE_CLASSES[tone];
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset",
        t.bg,
        t.text,
        t.ring,
        className,
      )}
    >
      <span className={cn("h-1.5 w-1.5 rounded-full", t.dot, animated && "animate-pulse")} />
      {children}
    </span>
  );
}
