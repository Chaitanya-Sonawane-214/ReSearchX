import { useNavigate } from "react-router-dom";
import { ChevronRight } from "lucide-react";
import type { PaperSummary } from "../../types";
import { PaperStatusBadge } from "../ui/StatusBadge";
import { formatDate } from "../../lib/utils";
import { scoreTone, TONE_CLASSES } from "../../lib/status";

export function PapersTable({
  papers,
  linkTo,
}: {
  papers: PaperSummary[];
  linkTo?: (id: string) => string;
}) {
  const navigate = useNavigate();
  const resolveLink = linkTo ?? ((id: string) => `/papers/${id}`);

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="text-xs uppercase tracking-wide text-ink-400">
            <th className="pb-2 font-medium">Paper</th>
            <th className="pb-2 font-medium">Status</th>
            <th className="pb-2 font-medium">Score</th>
            <th className="pb-2 font-medium">Uploaded</th>
            <th className="pb-2 font-medium" />
          </tr>
        </thead>
        <tbody className="divide-y divide-ink-100">
          {papers.map((p) => (
            <tr
              key={p.id}
              onClick={() => navigate(resolveLink(p.id))}
              className="cursor-pointer hover:bg-ink-50/70"
            >
              <td className="max-w-xs py-3 pr-4">
                <p className="truncate font-medium text-ink-800">
                  {p.title}
                  {p.revision > 1 && (
                    <span className="ml-1.5 text-xs font-normal text-ink-400">Rev. {p.revision}</span>
                  )}
                </p>
                <p className="truncate text-xs text-ink-400">{p.authors.join(", ") || "Unknown authors"}</p>
              </td>
              <td className="py-3 pr-4">
                <PaperStatusBadge status={p.status} />
              </td>
              <td className="py-3 pr-4">
                {p.overall_score != null ? (
                  <span className={`font-semibold ${TONE_CLASSES[scoreTone(p.overall_score)].text}`}>
                    {p.overall_score}/100
                  </span>
                ) : (
                  <span className="text-ink-300">—</span>
                )}
              </td>
              <td className="whitespace-nowrap py-3 pr-4 text-xs text-ink-500">{formatDate(p.uploaded_at)}</td>
              <td className="py-3 text-right">
                <ChevronRight size={16} className="text-ink-300" />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
