import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FileText, Search, UploadCloud } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardBody } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { EmptyState } from "../components/ui/EmptyState";
import { PapersTable } from "../components/dashboard/PapersTable";
import { PAPER_STATUS_META } from "../lib/status";
import { usePapers } from "../hooks/useApi";
import type { PaperStatus } from "../types";
import { cn } from "../lib/utils";

const FILTERS: { key: PaperStatus | "all"; label: string }[] = [
  { key: "all", label: "All" },
  { key: "uploaded", label: "Ready for Analysis" },
  { key: "ready_for_review", label: "Ready for Review" },
  { key: "revision_required", label: "Revision Required" },
  { key: "similarity_flagged", label: "Similarity Flagged" },
  { key: "reviewer_assignment", label: "Reviewer Assignment" },
  { key: "under_human_review", label: "Under Human Review" },
  { key: "not_recommended", label: "Not Recommended" },
];

export default function Papers() {
  const navigate = useNavigate();
  const { data: papers, isLoading } = usePapers();
  const [filter, setFilter] = useState<PaperStatus | "all">("all");
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    if (!papers) return [];
    return papers.filter((p) => {
      const matchesFilter = filter === "all" || p.status === filter;
      const matchesQuery =
        !query || p.title.toLowerCase().includes(query.toLowerCase()) ||
        p.authors.some((a) => a.toLowerCase().includes(query.toLowerCase()));
      return matchesFilter && matchesQuery;
    });
  }, [papers, filter, query]);

  return (
    <div className="space-y-5">
      <PageHeading
        title="Papers"
        description="Every research paper submitted for AI-assisted editorial screening."
        action={
          <Button icon={<UploadCloud size={15} />} onClick={() => navigate("/upload")}>
            Upload Paper
          </Button>
        }
      />

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-wrap gap-1.5">
          {FILTERS.map((f) => (
            <button
              key={f.key}
              onClick={() => setFilter(f.key)}
              className={cn(
                "rounded-full px-3 py-1.5 text-xs font-medium transition-colors",
                filter === f.key ? "bg-brand-600 text-white" : "bg-white text-ink-600 ring-1 ring-ink-200 hover:bg-ink-50",
              )}
            >
              {f.key === "all" ? f.label : PAPER_STATUS_META[f.key].label}
            </button>
          ))}
        </div>
        <div className="relative w-full sm:w-64">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-300" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search title or author…"
            className="w-full rounded-lg border border-ink-200 bg-white py-2 pl-8 pr-3 text-sm text-ink-700 placeholder:text-ink-300 focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-100"
          />
        </div>
      </div>

      <Card>
        <CardBody className="pt-5">
          {isLoading ? (
            <p className="py-8 text-center text-sm text-ink-400">Loading papers…</p>
          ) : filtered.length > 0 ? (
            <PapersTable papers={filtered} />
          ) : (
            <EmptyState icon={FileText} title="No papers match" description="Try a different filter or search term." />
          )}
        </CardBody>
      </Card>
    </div>
  );
}
