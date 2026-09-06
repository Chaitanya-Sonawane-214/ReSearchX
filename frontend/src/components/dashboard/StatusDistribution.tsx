import { PAPER_STATUS_META, TONE_CLASSES } from "../../lib/status";
import type { PaperStatus } from "../../types";
import { cn } from "../../lib/utils";

const DISPLAY_ORDER: PaperStatus[] = [
  "ready_for_review",
  "under_human_review",
  "reviewer_assignment",
  "revision_required",
  "similarity_flagged",
  "not_recommended",
  "uploaded",
  "parsing",
  "analyzing",
  "aggregating",
];

export function StatusDistribution({ breakdown }: { breakdown: Record<string, number> }) {
  const total = Object.values(breakdown).reduce((a, b) => a + b, 0) || 1;
  const rows = DISPLAY_ORDER.map((status) => ({
    status,
    count: breakdown[status] ?? 0,
    meta: PAPER_STATUS_META[status],
  })).filter((r) => r.count > 0);

  if (rows.length === 0) {
    return <p className="text-sm text-ink-400">No papers yet — upload one to see the pipeline distribution.</p>;
  }

  return (
    <div>
      <div className="flex h-3 w-full overflow-hidden rounded-full bg-ink-100">
        {rows.map((r, i) => (
          <div
            key={r.status}
            className={cn(TONE_CLASSES[r.meta.tone].dot, i > 0 && "ml-[2px]")}
            style={{ width: `${(r.count / total) * 100}%` }}
            title={`${r.meta.label}: ${r.count}`}
          />
        ))}
      </div>
      <div className="mt-4 flex flex-col gap-2">
        {rows.map((r) => (
          <div key={r.status} className="flex items-center gap-2 text-xs">
            <span className={cn("h-2 w-2 shrink-0 rounded-full", TONE_CLASSES[r.meta.tone].dot)} />
            <span className="text-ink-500">{r.meta.label}</span>
            <span className="ml-auto font-semibold text-ink-800">{r.count}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
