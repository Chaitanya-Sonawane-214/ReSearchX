import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowRight, CheckCircle2, Download, RotateCcw, AlertTriangle, XCircle } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardHeader, CardBody } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { ScoreRing } from "../components/ui/ScoreRing";
import { AgentScoreChart } from "../components/report/AgentScoreChart";
import { PriorityIssuesTable } from "../components/report/PriorityIssuesTable";
import { ResponsibleAINotice } from "../components/ui/ResponsibleAINotice";
import { ResubmitDialog } from "../components/paper/ResubmitDialog";
import { usePaper } from "../hooks/useApi";
import { api } from "../services/api";

export default function ReviewReport() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: paper, isLoading } = usePaper(id);
  const [resubmitOpen, setResubmitOpen] = useState(false);

  if (isLoading || !paper) return <p className="py-10 text-center text-sm text-ink-400">Loading review report…</p>;

  if (!paper.report || !paper.editorial) {
    return (
      <Card>
        <CardBody className="py-10 text-center">
          <p className="text-sm text-ink-500">
            The unified review report isn't available yet — run the AI analysis first.
          </p>
          <Button className="mt-4" onClick={() => navigate(`/papers/${paper.id}/pipeline`)}>
            Go to Analysis Pipeline
          </Button>
        </CardBody>
      </Card>
    );
  }

  const { report, editorial } = paper;
  const decision = editorial.decision;

  return (
    <div className="space-y-5">
      <PageHeading
        title="Unified Review Report"
        description={`${paper.title}${paper.revision > 1 ? ` · Revision ${paper.revision}` : ""}`}
      />

      <Card className="border-brand-100 bg-gradient-to-br from-brand-50 to-white">
        <CardBody className="flex flex-col items-center gap-5 pt-6 sm:flex-row sm:items-center">
          <ScoreRing score={report.overall_score} size={110} label="Overall" />
          <div className="flex-1 text-center sm:text-left">
            <DecisionHeadline decision={decision} headline={editorial.headline} />
            <p className="mt-1 text-sm text-ink-600">{editorial.message}</p>
            <p className="mt-1 text-xs font-medium text-ink-400">Next: {editorial.next_step}</p>
          </div>
        </CardBody>
      </Card>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Agent Scores" subtitle="Weighted contribution of each specialized agent" />
          <CardBody>
            <AgentScoreChart agentScores={report.agent_scores} />
          </CardBody>
        </Card>

        <Card>
          <CardHeader title="Strengths" subtitle="What the paper does well" />
          <CardBody>
            <ul className="space-y-2">
              {report.strengths.map((s, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-ink-700">
                  <CheckCircle2 size={15} className="mt-0.5 shrink-0 text-success-500" /> {s}
                </li>
              ))}
            </ul>
          </CardBody>
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader title="Major Concerns" />
          <CardBody>
            {report.major_concerns.length > 0 ? (
              <ul className="space-y-2">
                {report.major_concerns.map((c, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-ink-700">
                    <AlertTriangle size={15} className="mt-0.5 shrink-0 text-critical-500" /> {c}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-ink-400">No major concerns identified.</p>
            )}
          </CardBody>
        </Card>
        <Card>
          <CardHeader title="Minor Concerns" />
          <CardBody>
            {report.minor_concerns.length > 0 ? (
              <ul className="space-y-2">
                {report.minor_concerns.map((c, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-ink-700">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-ink-300" /> {c}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-ink-400">No minor concerns identified.</p>
            )}
          </CardBody>
        </Card>
      </div>

      <Card>
        <CardHeader title="Priority Issues" subtitle="Ranked by severity across all agents" />
        <CardBody>
          <PriorityIssuesTable issues={report.priority_issues} />
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="Recommended Actions" />
        <CardBody>
          <ul className="grid grid-cols-1 gap-2 sm:grid-cols-2">
            {report.recommended_actions.map((a, i) => (
              <li key={i} className="rounded-lg bg-ink-50 px-3 py-2 text-xs text-ink-600">{a}</li>
            ))}
          </ul>
        </CardBody>
      </Card>

      <Card>
        <CardBody className="flex flex-wrap items-center justify-between gap-3 pt-5">
          <a href={api.downloadReportUrl(paper.id)} download>
            <Button variant="outline" icon={<Download size={15} />}>Download Review Report</Button>
          </a>

          {decision === "ready_for_review" && (
            <Button icon={<ArrowRight size={15} />} onClick={() => navigate(`/papers/${paper.id}/similarity`)}>
              Continue to Similarity Detection
            </Button>
          )}

          {(decision === "revision_required" || decision === "not_recommended") && (
            <Button icon={<RotateCcw size={15} />} onClick={() => setResubmitOpen(true)}>
              Resubmit Revised Paper
            </Button>
          )}
        </CardBody>
      </Card>

      <ResponsibleAINotice />

      <ResubmitDialog
        paperId={paper.id}
        open={resubmitOpen}
        onClose={() => setResubmitOpen(false)}
        onResubmitted={(newId) => navigate(`/papers/${newId}/pipeline`)}
      />
    </div>
  );
}

function DecisionHeadline({ decision, headline }: { decision: string | null; headline: string }) {
  const Icon = decision === "ready_for_review" ? CheckCircle2 : decision === "revision_required" ? AlertTriangle : XCircle;
  const color =
    decision === "ready_for_review" ? "text-success-600" : decision === "revision_required" ? "text-warning-600" : "text-critical-600";
  return (
    <p className={`flex items-center justify-center gap-2 text-xl font-bold sm:justify-start ${color}`}>
      <Icon size={20} /> {headline}
    </p>
  );
}
