import { Bot } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardBody } from "../components/ui/Card";
import { EmptyState } from "../components/ui/EmptyState";
import { PapersTable } from "../components/dashboard/PapersTable";
import { usePapers } from "../hooks/useApi";

const ACTIVE = new Set(["uploaded", "parsing", "analyzing", "aggregating", "analysis_failed"]);

export default function AIAnalysisList() {
  const { data: papers, isLoading } = usePapers();
  const active = papers?.filter((p) => ACTIVE.has(p.status)) ?? [];

  return (
    <div className="space-y-5">
      <PageHeading
        title="AI Analysis"
        description="Papers currently awaiting or undergoing PDF parsing and the 7-agent review pipeline."
      />
      <Card>
        <CardBody className="pt-5">
          {isLoading ? (
            <p className="py-8 text-center text-sm text-ink-400">Loading…</p>
          ) : active.length > 0 ? (
            <PapersTable papers={active} linkTo={(id) => `/papers/${id}/pipeline`} />
          ) : (
            <EmptyState icon={Bot} title="No papers in analysis" description="Upload a paper to start the AI review pipeline." />
          )}
        </CardBody>
      </Card>
    </div>
  );
}
