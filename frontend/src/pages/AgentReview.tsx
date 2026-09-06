import { useParams, Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardBody } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { AgentGrid } from "../components/pipeline/AgentGrid";
import { ResponsibleAINotice } from "../components/ui/ResponsibleAINotice";
import { usePaper } from "../hooks/useApi";

export default function AgentReview() {
  const { id } = useParams<{ id: string }>();
  const { data: paper, isLoading } = usePaper(id, { poll: true });

  if (isLoading || !paper) return <p className="py-10 text-center text-sm text-ink-400">Loading agent findings…</p>;

  return (
    <div className="space-y-5">
      <PageHeading
        title="Multi-Agent Review"
        description={`${paper.title} — click any completed agent card to inspect its detailed findings.`}
        action={
          paper.report && (
            <Link to={`/papers/${paper.id}/report`}>
              <Button variant="outline" icon={<ArrowRight size={14} />}>
                View Unified Report
              </Button>
            </Link>
          )
        }
      />

      <Card>
        <CardBody className="pt-5">
          <AgentGrid agents={paper.agents} />
        </CardBody>
      </Card>

      <ResponsibleAINotice />
    </div>
  );
}
