import { ShieldCheck } from "lucide-react";
import { cn } from "../../lib/utils";

export function ResponsibleAINotice({ className, compact }: { className?: string; compact?: boolean }) {
  return (
    <div
      className={cn(
        "flex items-start gap-2.5 rounded-xl border border-brand-100 bg-brand-50/60 px-4 py-3 text-brand-800",
        className,
      )}
    >
      <ShieldCheck size={16} className="mt-0.5 shrink-0 text-brand-500" />
      <p className="text-xs leading-relaxed">
        <span className="font-semibold">AI-assisted screening:</span>{" "}
        {compact
          ? "Results assist editors and should be independently verified by qualified human reviewers."
          : "Results are generated to assist editors and reviewers. AI scores and recommendations should be independently verified by qualified human reviewers. Final publication and peer-review decisions are made by qualified human reviewers/editors."}
      </p>
    </div>
  );
}
