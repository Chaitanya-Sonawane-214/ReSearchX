import { useState } from "react";
import { Loader2 } from "lucide-react";
import { Card } from "../ui/Card";
import { AgentStatusBadge } from "../ui/StatusBadge";
import { agentIcon } from "../../lib/agentIcons";
import { cn } from "../../lib/utils";
import { scoreTone, TONE_CLASSES } from "../../lib/status";
import type { AgentReview } from "../../types";
import { AgentDetailDialog } from "./AgentDetailDialog";

export function AgentGrid({ agents }: { agents: AgentReview[] }) {
  const [selected, setSelected] = useState<AgentReview | null>(null);

  return (
    <>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {agents.map((agent) => {
          const Icon = agentIcon(agent.agent_name);
          const clickable = agent.status === "completed";
          const tone = agent.status === "completed" ? scoreTone(agent.score) : "neutral";
          return (
            <Card
              key={agent.agent_name}
              onClick={() => clickable && setSelected(agent)}
              className={cn(
                "p-4 transition-all",
                clickable && "cursor-pointer hover:-translate-y-0.5 hover:shadow-md",
                agent.status === "running" && "ring-1 ring-info-200",
              )}
            >
              <div className="flex items-center justify-between">
                <div className={cn("flex h-9 w-9 items-center justify-center rounded-lg", TONE_CLASSES[tone].bg, TONE_CLASSES[tone].text)}>
                  {agent.status === "running" ? <Loader2 size={16} className="animate-spin" /> : <Icon size={16} />}
                </div>
                {agent.status === "completed" && (
                  <span className="text-xl font-bold text-ink-900">{agent.score}</span>
                )}
              </div>
              <p className="mt-3 text-sm font-semibold text-ink-800">{agent.agent_name}</p>
              <div className="mt-2">
                <AgentStatusBadge status={agent.status} />
              </div>
            </Card>
          );
        })}
      </div>
      <AgentDetailDialog agent={selected} onClose={() => setSelected(null)} />
    </>
  );
}
