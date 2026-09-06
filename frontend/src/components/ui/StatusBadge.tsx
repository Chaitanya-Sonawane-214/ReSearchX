import { Badge } from "./Badge";
import { AGENT_STATUS_META, PAPER_STATUS_META, SEVERITY_META } from "../../lib/status";
import type { AgentStatus, IssueSeverity, PaperStatus } from "../../types";

export function PaperStatusBadge({ status }: { status: PaperStatus }) {
  const meta = PAPER_STATUS_META[status];
  return (
    <Badge tone={meta.tone} animated={meta.animated}>
      {meta.label}
    </Badge>
  );
}

export function AgentStatusBadge({ status }: { status: AgentStatus }) {
  const meta = AGENT_STATUS_META[status];
  return (
    <Badge tone={meta.tone} animated={meta.animated}>
      {meta.label}
    </Badge>
  );
}

export function SeverityBadge({ severity }: { severity: IssueSeverity }) {
  const meta = SEVERITY_META[severity];
  return <Badge tone={meta.tone}>{meta.label}</Badge>;
}
