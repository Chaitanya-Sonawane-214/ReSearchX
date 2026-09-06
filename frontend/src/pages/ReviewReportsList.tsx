import { ClipboardList } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardBody } from "../components/ui/Card";
import { EmptyState } from "../components/ui/EmptyState";
import { PapersTable } from "../components/dashboard/PapersTable";
import { usePapers } from "../hooks/useApi";

const NOT_YET_REPORTED = new Set(["uploaded", "parsing", "analyzing", "aggregating", "analysis_failed"]);

export default function ReviewReportsList() {
  const { data: papers, isLoading } = usePapers();
  const reported = papers?.filter((p) => !NOT_YET_REPORTED.has(p.status)) ?? [];

  return (
    <div className="space-y-5">
      <PageHeading
        title="Review Reports"
        description="Unified AI review reports produced by the Report Aggregation Agent."
      />
      <Card>
        <CardBody className="pt-5">
          {isLoading ? (
            <p className="py-8 text-center text-sm text-ink-400">Loading…</p>
          ) : reported.length > 0 ? (
            <PapersTable papers={reported} linkTo={(id) => `/papers/${id}/report`} />
          ) : (
            <EmptyState icon={ClipboardList} title="No reports yet" description="Reports appear here once a paper completes AI analysis." />
          )}
        </CardBody>
      </Card>
    </div>
  );
}
