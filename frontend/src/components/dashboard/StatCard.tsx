import type { LucideIcon } from "lucide-react";
import { Card } from "../ui/Card";
import { TONE_CLASSES, type Tone } from "../../lib/status";
import { cn } from "../../lib/utils";

export function StatCard({
  label,
  value,
  icon: Icon,
  tone = "brand",
  hint,
}: {
  label: string;
  value: number | string;
  icon: LucideIcon;
  tone?: Tone;
  hint?: string;
}) {
  const t = TONE_CLASSES[tone];
  return (
    <Card className="p-5">
      <div className="flex items-center justify-between">
        <p className="text-xs font-medium uppercase tracking-wide text-ink-400">{label}</p>
        <div className={cn("flex h-8 w-8 items-center justify-center rounded-lg", t.bg, t.text)}>
          <Icon size={16} />
        </div>
      </div>
      <p className="mt-3 text-2xl font-bold text-ink-900">{value}</p>
      {hint && <p className="mt-1 text-xs text-ink-400">{hint}</p>}
    </Card>
  );
}
