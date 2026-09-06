import { useNavigate } from "react-router-dom";
import { FileText, Bot, AlertTriangle, CheckCircle2, Copyleft, UserCheck, UploadCloud, ArrowRight } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { StatCard } from "../components/dashboard/StatCard";
import { StatusDistribution } from "../components/dashboard/StatusDistribution";
import { PapersTable } from "../components/dashboard/PapersTable";
import { Card, CardHeader, CardBody } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { ResponsibleAINotice } from "../components/ui/ResponsibleAINotice";
import { EmptyState } from "../components/ui/EmptyState";
import { useDashboardStats, usePapers } from "../hooks/useApi";

export default function Dashboard() {
  const navigate = useNavigate();
  const { data: stats } = useDashboardStats();
  const { data: papers } = usePapers();

  return (
    <div className="space-y-6">
      <PageHeading
        title="Research Review Dashboard"
        description="Editorial overview of every paper moving through AI-assisted pre-review screening."
        action={
          <Button icon={<UploadCloud size={15} />} onClick={() => navigate("/upload")}>
            Upload Paper
          </Button>
        }
      />

      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Total Papers" value={stats?.total_papers ?? "—"} icon={FileText} tone="brand" />
        <StatCard label="AI Reviews Done" value={stats?.ai_reviews_completed ?? "—"} icon={Bot} tone="info" />
        <StatCard label="Revision Required" value={stats?.revision_required ?? "—"} icon={AlertTriangle} tone="warning" />
        <StatCard label="Ready for Review" value={stats?.ready_for_review ?? "—"} icon={CheckCircle2} tone="success" />
        <StatCard label="Similarity Alerts" value={stats?.similarity_alerts ?? "—"} icon={Copyleft} tone="critical" />
        <StatCard label="Under Human Review" value={stats?.under_human_review ?? "—"} icon={UserCheck} tone="brand" />
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader title="Recent Papers" subtitle="Latest submissions across the editorial pipeline" />
          <CardBody>
            {papers && papers.length > 0 ? (
              <PapersTable papers={papers.slice(0, 6)} />
            ) : (
              <EmptyState
                icon={FileText}
                title="No papers yet"
                description="Upload a research paper to see it move through the AI review pipeline."
                action={<Button onClick={() => navigate("/upload")}>Upload Paper</Button>}
              />
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader title="Pipeline Distribution" subtitle="Where papers currently sit" />
          <CardBody>
            <StatusDistribution breakdown={stats?.status_breakdown ?? {}} />
          </CardBody>
        </Card>
      </div>

      <div className="flex flex-col gap-4 sm:flex-row">
        <ResponsibleAINotice className="flex-1" />
        <button
          onClick={() => navigate("/papers")}
          className="flex shrink-0 items-center gap-1.5 self-start rounded-xl border border-ink-200 bg-white px-4 py-3 text-sm font-medium text-ink-600 hover:bg-ink-50 sm:self-stretch"
        >
          View all papers <ArrowRight size={14} />
        </button>
      </div>
    </div>
  );
}
