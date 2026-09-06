import { ShieldCheck, ShieldAlert, BookOpen } from "lucide-react";
import { Card } from "../ui/Card";
import { Badge } from "../ui/Badge";
import { Button } from "../ui/Button";
import { initials } from "../../lib/utils";
import type { Reviewer } from "../../types";

const WORKLOAD_TONE = { low: "success", medium: "warning", high: "critical" } as const;

export function ReviewerCard({
  reviewer,
  assigned,
  onAssign,
  onViewProfile,
  assigning,
}: {
  reviewer: Reviewer;
  assigned?: boolean;
  onAssign?: () => void;
  onViewProfile?: () => void;
  assigning?: boolean;
}) {
  return (
    <Card className="flex flex-col p-5">
      <div className="flex items-start gap-3">
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-brand-100 text-sm font-bold text-brand-700">
          {initials(reviewer.name)}
        </div>
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold text-ink-900">{reviewer.name}</p>
          <p className="truncate text-xs text-ink-500">{reviewer.expertise.join(" • ")}</p>
        </div>
        {reviewer.match_score > 0 && (
          <span className="ml-auto shrink-0 text-right">
            <span className="block text-lg font-bold text-brand-600">{reviewer.match_score}%</span>
            <span className="block text-[10px] uppercase tracking-wide text-ink-400">Match</span>
          </span>
        )}
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        <Badge tone={WORKLOAD_TONE[reviewer.workload]}>Workload: {reviewer.workload}</Badge>
        <Badge tone={reviewer.conflict_of_interest ? "critical" : "success"}>
          {reviewer.conflict_of_interest ? <ShieldAlert size={11} /> : <ShieldCheck size={11} />}
          COI: {reviewer.conflict_of_interest ? "Flagged" : "Clear"}
        </Badge>
        <span className="flex items-center gap-1 text-xs text-ink-400">
          <BookOpen size={12} /> {reviewer.publications} publications
        </span>
      </div>

      <div className="mt-4 flex gap-2">
        <Button variant="outline" size="sm" className="flex-1" onClick={onViewProfile}>
          View Profile
        </Button>
        {onAssign && (
          <Button size="sm" className="flex-1" onClick={onAssign} disabled={assigned} loading={assigning}>
            {assigned ? "Assigned" : "Assign Reviewer"}
          </Button>
        )}
      </div>
    </Card>
  );
}
