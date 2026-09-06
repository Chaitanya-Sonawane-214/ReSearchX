import { ExternalLink } from "lucide-react";
import type { SimilaritySource } from "../../types";
import { scoreToneInverted } from "../../lib/status";
import { Badge } from "../ui/Badge";

export function SourcesTable({ sources }: { sources: SimilaritySource[] }) {
  if (sources.length === 0) {
    return <p className="text-sm text-ink-400">No overlapping sources were flagged for this paper.</p>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="text-xs uppercase tracking-wide text-ink-400">
            <th className="pb-2 font-medium">Potentially Similar Source</th>
            <th className="pb-2 font-medium">Matched Content</th>
            <th className="pb-2 pl-4 text-right font-medium">Similarity</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-ink-100">
          {sources.map((s, i) => (
            <tr key={i}>
              <td className="py-3 pr-4">
                <p className="font-medium text-ink-800">{s.title}</p>
                <p className="flex items-center gap-1 text-xs text-ink-400">
                  <ExternalLink size={11} /> {s.source}
                </p>
              </td>
              <td className="py-3 pr-4 text-xs text-ink-500">{s.matched_excerpt}</td>
              <td className="py-3 pl-4 text-right">
                <Badge tone={scoreToneInverted(s.similarity)}>{s.similarity}%</Badge>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
