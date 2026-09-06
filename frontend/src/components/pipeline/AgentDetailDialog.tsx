import { CheckCircle2, Lightbulb, Sparkles } from "lucide-react";
import { Dialog } from "../ui/Dialog";
import { ScoreRing } from "../ui/ScoreRing";
import { SeverityBadge } from "../ui/StatusBadge";
import { agentIcon } from "../../lib/agentIcons";
import type { AgentReview } from "../../types";

export function AgentDetailDialog({ agent, onClose }: { agent: AgentReview | null; onClose: () => void }) {
  if (!agent) return null;
  const Icon = agentIcon(agent.agent_name);

  return (
    <Dialog open={!!agent} onClose={onClose} title={agent.agent_name}>
      <div className="flex items-center gap-4">
        <ScoreRing score={agent.score} size={80} strokeWidth={7} />
        <div>
          <p className="flex items-center gap-1.5 text-xs font-medium text-ink-400">
            <Icon size={13} /> AI-generated review finding
            {agent.ai_generated && (
              <span className="ml-1 inline-flex items-center gap-1 rounded-full bg-brand-50 px-1.5 py-0.5 text-[10px] font-semibold text-brand-600">
                <Sparkles size={9} /> Live AI
              </span>
            )}
          </p>
          <p className="mt-1 text-sm text-ink-600">{agent.summary}</p>
        </div>
      </div>

      {agent.strengths.length > 0 && (
        <div className="mt-5">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink-400">Strengths</p>
          <ul className="space-y-1.5">
            {agent.strengths.map((s, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-ink-700">
                <CheckCircle2 size={15} className="mt-0.5 shrink-0 text-success-500" />
                {s}
              </li>
            ))}
          </ul>
        </div>
      )}

      {agent.issues.length > 0 && (
        <div className="mt-5">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink-400">Issues Found</p>
          <ul className="space-y-2.5">
            {agent.issues.map((issue, i) => (
              <li key={i} className="rounded-xl border border-ink-100 bg-ink-50/60 p-3">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-sm font-semibold text-ink-800">{issue.title}</p>
                  <SeverityBadge severity={issue.severity} />
                </div>
                <p className="mt-1 text-xs leading-relaxed text-ink-500">{issue.description}</p>
              </li>
            ))}
          </ul>
        </div>
      )}

      {agent.recommendations.length > 0 && (
        <div className="mt-5">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink-400">Recommendations</p>
          <ul className="space-y-1.5">
            {agent.recommendations.map((r, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-ink-700">
                <Lightbulb size={15} className="mt-0.5 shrink-0 text-warning-500" />
                {r}
              </li>
            ))}
          </ul>
        </div>
      )}
    </Dialog>
  );
}
