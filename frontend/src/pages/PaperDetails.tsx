import { useNavigate, useParams } from "react-router-dom";
import {
  Bot, ClipboardList, Copyleft, Users, ArrowRight, FileText, Calendar, Target, Layers,
} from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardHeader, CardBody } from "../components/ui/Card";
import { PaperStatusBadge } from "../components/ui/StatusBadge";
import { Stepper } from "../components/paper/Stepper";
import { ScoreRing } from "../components/ui/ScoreRing";
import { usePaper } from "../hooks/useApi";
import { formatBytes, formatDate } from "../lib/utils";

const HUMAN_REVIEW_STEPS = ["Reviewer Assigned", "Reviewer Receives Paper", "Reviewer Evaluates Paper", "Human Review Decision"];

export default function PaperDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: paper, isLoading } = usePaper(id, { poll: true });

  if (isLoading || !paper) return <p className="py-10 text-center text-sm text-ink-400">Loading paper…</p>;

  const quickLinks = [
    { label: "Multi-Agent Review", icon: Bot, to: `/papers/${paper.id}/agents`, enabled: paper.agents.some((a) => a.status === "completed") },
    { label: "Unified Report", icon: ClipboardList, to: `/papers/${paper.id}/report`, enabled: !!paper.report },
    { label: "Similarity Analysis", icon: Copyleft, to: `/papers/${paper.id}/similarity`, enabled: !!paper.report },
    { label: "Reviewer Assignment", icon: Users, to: `/papers/${paper.id}/reviewers`, enabled: !!paper.similarity },
  ];

  return (
    <div className="space-y-5">
      <PageHeading
        title={paper.title}
        description={paper.authors.join(", ") || "Authors pending extraction"}
        action={<PaperStatusBadge status={paper.status} />}
      />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader title="Paper Lifecycle" subtitle="Full journey from upload to human peer review" />
          <CardBody>
            <Stepper steps={paper.timeline} orientation="vertical" />
          </CardBody>
        </Card>

        <div className="space-y-4">
          <Card>
            <CardBody className="flex flex-col items-center gap-2 pt-5 text-center">
              {paper.overall_score != null ? (
                <ScoreRing score={paper.overall_score} label="Overall" />
              ) : (
                <p className="py-6 text-sm text-ink-400">Score pending analysis</p>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Paper Details" />
            <CardBody className="space-y-2.5 text-xs">
              <DetailRow icon={FileText} label="File" value={`${paper.filename} · ${formatBytes(paper.file_size)}`} />
              <DetailRow icon={Calendar} label="Uploaded" value={formatDate(paper.uploaded_at)} />
              <DetailRow icon={Target} label="Target Venue" value={paper.target_venue || "Not specified"} />
              <DetailRow icon={Layers} label="Revision" value={String(paper.revision)} />
            </CardBody>
          </Card>
        </div>
      </div>

      <Card>
        <CardHeader title="Jump to Stage" />
        <CardBody className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          {quickLinks.map(({ label, icon: Icon, to, enabled }) => (
            <button
              key={label}
              disabled={!enabled}
              onClick={() => navigate(to)}
              className="flex flex-col items-center gap-2 rounded-xl border border-ink-200 bg-white px-3 py-4 text-center text-xs font-medium text-ink-600 transition-colors hover:bg-ink-50 disabled:cursor-not-allowed disabled:opacity-40"
            >
              <Icon size={18} className="text-brand-500" />
              {label}
            </button>
          ))}
        </CardBody>
      </Card>

      {(paper.status === "under_human_review" || paper.assigned_reviewer_id) && (
        <Card>
          <CardHeader title="Human Peer Review" subtitle="Final stage — outside AI's control" />
          <CardBody>
            <div className="flex items-center overflow-x-auto">
              {HUMAN_REVIEW_STEPS.map((label, i) => (
                <div key={label} className="flex shrink-0 items-center">
                  <div className="flex flex-col items-center gap-1.5">
                    <span className={`flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold ${i === 0 ? "bg-success-500 text-white" : "bg-ink-200 text-ink-500"}`}>
                      {i + 1}
                    </span>
                    <span className="max-w-[100px] text-center text-[11px] font-medium text-ink-600">{label}</span>
                  </div>
                  {i < HUMAN_REVIEW_STEPS.length - 1 && <ArrowRight size={14} className="mx-2 mb-5 text-ink-300" />}
                </div>
              ))}
            </div>
            <p className="mt-4 text-xs font-medium text-brand-600">Status: Review Pending</p>
          </CardBody>
        </Card>
      )}
    </div>
  );
}

function DetailRow({ icon: Icon, label, value }: { icon: typeof FileText; label: string; value: string }) {
  return (
    <div className="flex items-center gap-2">
      <Icon size={13} className="shrink-0 text-ink-400" />
      <span className="text-ink-400">{label}:</span>
      <span className="ml-auto truncate font-medium text-ink-700">{value}</span>
    </div>
  );
}
