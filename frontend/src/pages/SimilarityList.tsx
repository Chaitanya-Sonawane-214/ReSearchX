import { Copyleft } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardBody } from "../components/ui/Card";
import { EmptyState } from "../components/ui/EmptyState";
import { PapersTable } from "../components/dashboard/PapersTable";
import { usePapers } from "../hooks/useApi";

const HAS_SIMILARITY = new Set(["similarity_flagged", "reviewer_assignment", "under_human_review"]);

export default function SimilarityList() {
  const { data: papers, isLoading } = usePapers();
  const checked = papers?.filter((p) => HAS_SIMILARITY.has(p.status)) ?? [];

  return (
    <div className="space-y-5">
      <PageHeading
        title="Similarity"
        description="Plagiarism / similarity detection results for papers that reached review-ready status."
      />
      <Card>
        <CardBody className="pt-5">
          {isLoading ? (
            <p className="py-8 text-center text-sm text-ink-400">Loading…</p>
          ) : checked.length > 0 ? (
            <PapersTable papers={checked} linkTo={(id) => `/papers/${id}/similarity`} />
          ) : (
            <EmptyState icon={Copyleft} title="No similarity checks yet" description="Run a similarity check from a paper's review report once it's ready for review." />
          )}
        </CardBody>
      </Card>
    </div>
  );
}
