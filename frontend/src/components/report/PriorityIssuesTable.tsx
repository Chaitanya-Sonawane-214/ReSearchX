import type { ReviewIssue } from "../../types";
import { SEVERITY_META } from "../../lib/status";
import { SeverityBadge } from "../ui/StatusBadge";

export function PriorityIssuesTable({ issues }: { issues: ReviewIssue[] }) {
  if (issues.length === 0) {
    return <p className="text-sm text-ink-400">No priority issues were flagged. Great work.</p>;
  }
  const sorted = [...issues].sort((a, b) => SEVERITY_META[a.severity].rank - SEVERITY_META[b.severity].rank);

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="text-xs uppercase tracking-wide text-ink-400">
            <th className="pb-2 font-medium">Priority</th>
            <th className="pb-2 font-medium">Issue</th>
            <th className="pb-2 font-medium">Source Agent</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-ink-100">
          {sorted.map((issue, i) => (
            <tr key={i}>
              <td className="whitespace-nowrap py-3 pr-4 align-top">
                <SeverityBadge severity={issue.severity} />
              </td>
              <td className="py-3 pr-4 align-top">
                <p className="font-medium text-ink-800">{issue.title}</p>
                <p className="mt-0.5 text-xs text-ink-500">{issue.description}</p>
              </td>
              <td className="whitespace-nowrap py-3 align-top text-xs text-ink-500">{issue.source_agent}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
