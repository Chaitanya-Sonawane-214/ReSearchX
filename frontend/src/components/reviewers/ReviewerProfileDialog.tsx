import { BookOpen, ShieldCheck, ShieldAlert, Layers } from "lucide-react";
import { Dialog } from "../ui/Dialog";
import { Badge } from "../ui/Badge";
import { initials } from "../../lib/utils";
import type { Reviewer } from "../../types";

export function ReviewerProfileDialog({ reviewer, onClose }: { reviewer: Reviewer | null; onClose: () => void }) {
  if (!reviewer) return null;
  return (
    <Dialog open={!!reviewer} onClose={onClose} title="Reviewer Profile">
      <div className="flex items-center gap-4">
        <div className="flex h-14 w-14 items-center justify-center rounded-full bg-brand-100 text-lg font-bold text-brand-700">
          {initials(reviewer.name)}
        </div>
        <div>
          <p className="text-base font-semibold text-ink-900">{reviewer.name}</p>
          <p className="text-xs text-ink-500">{reviewer.domains.join(" • ")}</p>
        </div>
      </div>

      <p className="mt-4 text-sm leading-relaxed text-ink-600">{reviewer.bio}</p>

      <div className="mt-5 grid grid-cols-2 gap-3">
        <div className="rounded-xl bg-ink-50 p-3">
          <p className="text-[11px] uppercase tracking-wide text-ink-400">Expertise Match</p>
          <p className="mt-1 text-lg font-bold text-brand-600">{reviewer.match_score || "—"}%</p>
        </div>
        <div className="rounded-xl bg-ink-50 p-3">
          <p className="text-[11px] uppercase tracking-wide text-ink-400">Recommendation Score</p>
          <p className="mt-1 text-lg font-bold text-ink-800">{reviewer.recommendation_score || "—"}%</p>
        </div>
      </div>

      <div className="mt-4 space-y-2 text-sm text-ink-600">
        <p className="flex items-center gap-2">
          <Layers size={14} className="text-ink-400" /> Expertise: {reviewer.expertise.join(", ")}
        </p>
        <p className="flex items-center gap-2">
          <BookOpen size={14} className="text-ink-400" /> {reviewer.publications} publications on record
        </p>
        <p className="flex items-center gap-2">
          {reviewer.conflict_of_interest ? (
            <ShieldAlert size={14} className="text-critical-500" />
          ) : (
            <ShieldCheck size={14} className="text-success-500" />
          )}
          Conflict of interest: {reviewer.conflict_of_interest ? "Flagged for review" : "Clear"}
        </p>
      </div>

      <div className="mt-4">
        <Badge tone={reviewer.workload === "low" ? "success" : reviewer.workload === "medium" ? "warning" : "critical"}>
          Current workload: {reviewer.workload}
        </Badge>
      </div>
    </Dialog>
  );
}
