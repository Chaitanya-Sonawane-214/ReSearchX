import { Check, Loader2 } from "lucide-react";
import { cn } from "../../lib/utils";
import type { TimelineStep } from "../../types";

export function Stepper({ steps, orientation = "horizontal" }: { steps: TimelineStep[]; orientation?: "horizontal" | "vertical" }) {
  if (orientation === "vertical") {
    return (
      <ol className="space-y-0">
        {steps.map((step, i) => (
          <li key={step.key} className="relative flex gap-3 pb-7 last:pb-0">
            {i < steps.length - 1 && (
              <span
                className={cn(
                  "absolute left-[11px] top-6 h-full w-0.5",
                  step.status === "done" ? "bg-success-300" : "bg-ink-200",
                )}
              />
            )}
            <StepDot status={step.status} />
            <div className="pt-0.5">
              <p className={cn("text-sm font-semibold", step.status === "pending" ? "text-ink-400" : "text-ink-800")}>
                {step.label}
              </p>
              <p className="text-xs text-ink-400">
                {step.status === "done" ? "Complete" : step.status === "current" ? "In progress" : "Pending"}
              </p>
            </div>
          </li>
        ))}
      </ol>
    );
  }

  return (
    <div className="flex items-center overflow-x-auto pb-1">
      {steps.map((step, i) => (
        <div key={step.key} className="flex shrink-0 items-center">
          <div className="flex flex-col items-center gap-1.5">
            <StepDot status={step.status} />
            <span className={cn("max-w-[84px] text-center text-[11px] font-medium leading-tight", step.status === "pending" ? "text-ink-400" : "text-ink-700")}>
              {step.label}
            </span>
          </div>
          {i < steps.length - 1 && (
            <span className={cn("mx-1.5 mb-4 h-0.5 w-8 shrink-0", step.status === "done" ? "bg-success-300" : "bg-ink-200")} />
          )}
        </div>
      ))}
    </div>
  );
}

function StepDot({ status }: { status: TimelineStep["status"] }) {
  return (
    <span
      className={cn(
        "flex h-6 w-6 shrink-0 items-center justify-center rounded-full ring-4",
        status === "done" && "bg-success-500 text-white ring-success-100",
        status === "current" && "bg-info-500 text-white ring-info-100",
        status === "pending" && "bg-ink-200 text-ink-400 ring-transparent",
      )}
    >
      {status === "done" && <Check size={13} strokeWidth={3} />}
      {status === "current" && <Loader2 size={12} className="animate-spin" />}
    </span>
  );
}
