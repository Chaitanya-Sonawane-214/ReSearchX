import { useNavigate, useParams } from "react-router-dom";
import { AlertTriangle, ArrowRight, Copyleft, ShieldCheck, Flag, RotateCcw } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardHeader, CardBody } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { SimilarityGauge } from "../components/similarity/SimilarityGauge";
import { SourcesTable } from "../components/similarity/SourcesTable";
import { ResponsibleAINotice } from "../components/ui/ResponsibleAINotice";
import { usePaper, useRunSimilarity, useResolveSimilarity, useSystemStatus } from "../hooks/useApi";
import { useToast } from "../components/ui/Toast";
import { formatDateTime } from "../lib/utils";

export default function SimilarityReport() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { push } = useToast();
  const { data: paper, isLoading } = usePaper(id, { poll: true });
  const { data: status } = useSystemStatus();
  const runSimilarity = useRunSimilarity();
  const resolve = useResolveSimilarity();

  if (isLoading || !paper) return <p className="py-10 text-center text-sm text-ink-400">Loading similarity check…</p>;

  if (!paper.report) {
    return (
      <Card>
        <CardBody className="py-10 text-center">
          <p className="text-sm text-ink-500">Complete the AI review before running a similarity check.</p>
          <Button className="mt-4" onClick={() => navigate(`/papers/${paper.id}/pipeline`)}>Go to Analysis Pipeline</Button>
        </CardBody>
      </Card>
    );
  }

  const similarity = paper.similarity;
  const threshold = status?.similarity_threshold ?? 30;

  return (
    <div className="space-y-5">
      <PageHeading title="Similarity Analysis" description={paper.title} />

      {!similarity ? (
        <Card>
          <CardBody className="flex flex-col items-center gap-3 py-10 text-center">
            <Copyleft size={28} className="text-ink-300" />
            <p className="text-sm font-semibold text-ink-800">Run plagiarism / similarity detection</p>
            <p className="max-w-sm text-xs text-ink-500">
              Checks this paper against reference sources for overlapping or matched content requiring inspection.
            </p>
            <Button
              className="mt-2"
              loading={runSimilarity.isPending}
              onClick={() =>
                runSimilarity.mutate(paper.id, {
                  onError: (err: Error) => push({ kind: "error", title: "Similarity check failed", description: err.message }),
                })
              }
            >
              Run Similarity Analysis
            </Button>
          </CardBody>
        </Card>
      ) : (
        <>
          <Card className={similarity.status === "high" ? "border-critical-100 bg-critical-50/40" : "border-success-100 bg-success-50/40"}>
            <CardBody className="flex flex-col items-center gap-6 pt-6 sm:flex-row">
              <SimilarityGauge percentage={similarity.overall_similarity} threshold={threshold} />
              <div className="flex-1 text-center sm:text-left">
                {similarity.status === "high" ? (
                  <p className="flex items-center justify-center gap-2 text-lg font-bold text-critical-700 sm:justify-start">
                    <AlertTriangle size={19} /> HIGH SIMILARITY DETECTED
                  </p>
                ) : (
                  <p className="flex items-center justify-center gap-2 text-lg font-bold text-success-700 sm:justify-start">
                    <ShieldCheck size={19} /> ACCEPTABLE SIMILARITY
                  </p>
                )}
                <p className="mt-1 text-sm text-ink-600">
                  {similarity.status === "high"
                    ? "The paper requires further inspection before reviewer assignment."
                    : `Similarity is within the configured ${threshold}% threshold.`}
                </p>
                <p className="mt-1 text-xs text-ink-400">Checked {formatDateTime(similarity.checked_at)}</p>
              </div>
              <div className="grid grid-cols-2 gap-3 text-center">
                <div className="rounded-xl bg-white/70 px-4 py-2.5 ring-1 ring-ink-100">
                  <p className="text-xl font-bold text-ink-900">{similarity.direct_matches}</p>
                  <p className="text-[11px] uppercase tracking-wide text-ink-400">Direct Matches</p>
                </div>
                <div className="rounded-xl bg-white/70 px-4 py-2.5 ring-1 ring-ink-100">
                  <p className="text-xl font-bold text-ink-900">{similarity.potential_sources.length}</p>
                  <p className="text-[11px] uppercase tracking-wide text-ink-400">Potential Sources</p>
                </div>
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Potentially Similar Sources" subtitle="Sources requiring inspection — not a plagiarism verdict" />
            <CardBody>
              <SourcesTable sources={similarity.potential_sources} />
            </CardBody>
          </Card>

          {similarity.status === "high" && paper.status === "similarity_flagged" && (
            <Card>
              <CardHeader title="Editor Decision" subtitle="A human editor reviews flagged similarity before proceeding" />
              <CardBody className="flex flex-wrap gap-3 pt-2">
                <Button
                  variant="outline"
                  icon={<RotateCcw size={15} />}
                  loading={resolve.isPending}
                  onClick={() => resolve.mutate({ id: paper.id, action: "return_to_author" })}
                >
                  Return to Author for Revision
                </Button>
                <Button
                  icon={<Flag size={15} />}
                  loading={resolve.isPending}
                  onClick={() => resolve.mutate({ id: paper.id, action: "proceed" })}
                >
                  Editor Override — Proceed to Reviewer Assignment
                </Button>
              </CardBody>
            </Card>
          )}

          {paper.status === "reviewer_assignment" && (
            <div className="flex justify-end">
              <Button icon={<ArrowRight size={15} />} onClick={() => navigate(`/papers/${paper.id}/reviewers`)}>
                Continue to Reviewer Assignment
              </Button>
            </div>
          )}
        </>
      )}

      <ResponsibleAINotice compact />
    </div>
  );
}
