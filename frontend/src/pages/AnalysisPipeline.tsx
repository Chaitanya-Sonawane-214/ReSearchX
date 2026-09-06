import { useNavigate, useParams } from "react-router-dom";
import { AlertOctagon, ArrowRight, Loader2, PlayCircle, Sparkles } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardBody, CardHeader } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { ScoreRing } from "../components/ui/ScoreRing";
import { ParsingChecklist } from "../components/pipeline/ParsingChecklist";
import { AgentGrid } from "../components/pipeline/AgentGrid";
import { Stepper } from "../components/paper/Stepper";
import { PaperStatusBadge } from "../components/ui/StatusBadge";
import { useAnalyzePaper, usePaper } from "../hooks/useApi";
import { useToast } from "../components/ui/Toast";

export default function AnalysisPipeline() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { push } = useToast();
  const { data: paper, isLoading } = usePaper(id, { poll: true });
  const analyze = useAnalyzePaper();

  if (isLoading || !paper) {
    return <p className="py-10 text-center text-sm text-ink-400">Loading pipeline…</p>;
  }

  const isRunning = ["parsing", "analyzing", "aggregating"].includes(paper.status);
  const isDone = !!paper.report;
  const failed = paper.status === "analysis_failed";

  return (
    <div className="space-y-5">
      <PageHeading
        title="Analysis Pipeline"
        description={paper.title}
        action={<PaperStatusBadge status={paper.status} />}
      />

      <Card>
        <CardBody className="pt-5">
          <Stepper steps={paper.timeline} />
        </CardBody>
      </Card>

      {paper.status === "uploaded" && (
        <Card className="border-brand-100 bg-brand-50/40">
          <CardBody className="flex items-center justify-between pt-5">
            <div>
              <p className="text-sm font-semibold text-ink-900">Ready to begin AI review</p>
              <p className="text-xs text-ink-500">This will run PDF parsing, all 7 review agents, and report aggregation.</p>
            </div>
            <Button
              icon={<PlayCircle size={16} />}
              loading={analyze.isPending}
              onClick={() =>
                analyze.mutate(paper.id, {
                  onError: (err: Error) => push({ kind: "error", title: "Could not start analysis", description: err.message }),
                })
              }
            >
              Start AI Review
            </Button>
          </CardBody>
        </Card>
      )}

      {failed && (
        <Card className="border-critical-100 bg-critical-50/50">
          <CardBody className="flex items-center justify-between pt-5">
            <div className="flex items-start gap-3">
              <AlertOctagon size={20} className="mt-0.5 shrink-0 text-critical-600" />
              <div>
                <p className="text-sm font-semibold text-critical-800">Analysis Failed</p>
                <p className="text-xs text-critical-600">
                  {paper.error || "Something went wrong while processing the paper."}
                </p>
              </div>
            </div>
            <Button variant="danger" loading={analyze.isPending} onClick={() => analyze.mutate(paper.id)}>
              Retry Analysis
            </Button>
          </CardBody>
        </Card>
      )}

      <ParsingChecklist items={paper.parsing_checklist} />

      <Card>
        <CardHeader
          title="Multi-Agent Review Layer"
          subtitle="Seven specialized AI agents evaluate different aspects of the paper"
          action={isRunning && paper.status === "analyzing" && <Loader2 size={16} className="animate-spin text-info-500" />}
        />
        <CardBody>
          <AgentGrid agents={paper.agents} />
        </CardBody>
      </Card>

      {paper.status === "aggregating" && (
        <Card className="border-info-100 bg-info-50/50">
          <CardBody className="flex items-center gap-3 pt-5">
            <Loader2 size={18} className="animate-spin text-info-600" />
            <div>
              <p className="text-sm font-semibold text-info-800">Report Aggregation Agent running</p>
              <p className="text-xs text-info-600">Aggregating findings… generating unified review…</p>
            </div>
          </CardBody>
        </Card>
      )}

      {isDone && paper.report && paper.editorial && (
        <Card className="border-brand-100 bg-gradient-to-br from-brand-50 to-white">
          <CardBody className="flex flex-col items-center gap-4 pt-6 text-center sm:flex-row sm:items-center sm:text-left">
            <ScoreRing score={paper.report.overall_score} label="Overall" />
            <div className="flex-1">
              <p className="flex items-center justify-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-brand-600 sm:justify-start">
                <Sparkles size={13} /> AI Editorial Recommendation
              </p>
              <p className="mt-1 text-lg font-bold text-ink-900">{paper.editorial.headline}</p>
              <p className="mt-1 text-sm text-ink-500">{paper.editorial.message}</p>
            </div>
            <Button icon={<ArrowRight size={15} />} onClick={() => navigate(`/papers/${paper.id}/report`)}>
              View Full Report
            </Button>
          </CardBody>
        </Card>
      )}
    </div>
  );
}
