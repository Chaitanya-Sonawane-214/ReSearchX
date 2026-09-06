import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowRight, UserCheck } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardBody } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { ReviewerCard } from "../components/reviewers/ReviewerCard";
import { ReviewerProfileDialog } from "../components/reviewers/ReviewerProfileDialog";
import { ResponsibleAINotice } from "../components/ui/ResponsibleAINotice";
import { useAssignReviewer, usePaper, useRecommendedReviewers } from "../hooks/useApi";
import { useToast } from "../components/ui/Toast";
import type { Reviewer } from "../types";

export default function ReviewerAssignment() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { push } = useToast();
  const { data: paper, isLoading: paperLoading } = usePaper(id, { poll: true });
  const { data: reviewers, isLoading: reviewersLoading } = useRecommendedReviewers(id);
  const assign = useAssignReviewer();
  const [profile, setProfile] = useState<Reviewer | null>(null);

  if (paperLoading || !paper) return <p className="py-10 text-center text-sm text-ink-400">Loading reviewer assignment…</p>;

  if (!paper.similarity) {
    return (
      <Card>
        <CardBody className="py-10 text-center">
          <p className="text-sm text-ink-500">Run the similarity check before assigning a human reviewer.</p>
          <Button className="mt-4" onClick={() => navigate(`/papers/${paper.id}/similarity`)}>Go to Similarity Analysis</Button>
        </CardBody>
      </Card>
    );
  }

  const assignedReviewer = reviewers?.find((r) => r.id === paper.assigned_reviewer_id);

  return (
    <div className="space-y-5">
      <PageHeading
        title="Reviewer Assignment"
        description="AI-suggested reviewers ranked by expertise match, workload and conflict-of-interest checks. The editor retains final control over assignment."
      />

      {paper.assigned_reviewer_id ? (
        <Card className="border-success-100 bg-success-50/50">
          <CardBody className="flex items-center justify-between pt-5">
            <div className="flex items-center gap-3">
              <UserCheck size={22} className="text-success-600" />
              <div>
                <p className="text-sm font-semibold text-success-800">
                  {assignedReviewer?.name ?? "Reviewer"} has been assigned
                </p>
                <p className="text-xs text-success-600">Status: Human Peer Review — Review Pending</p>
              </div>
            </div>
            <Button icon={<ArrowRight size={15} />} onClick={() => navigate(`/papers/${paper.id}`)}>
              View Paper Lifecycle
            </Button>
          </CardBody>
        </Card>
      ) : reviewersLoading ? (
        <p className="py-6 text-center text-sm text-ink-400">Matching reviewers to this paper's domain…</p>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {reviewers?.map((reviewer) => (
            <ReviewerCard
              key={reviewer.id}
              reviewer={reviewer}
              assigning={assign.isPending && assign.variables?.reviewerId === reviewer.id}
              onViewProfile={() => setProfile(reviewer)}
              onAssign={() =>
                assign.mutate(
                  { id: paper.id, reviewerId: reviewer.id },
                  {
                    onSuccess: () =>
                      push({ kind: "success", title: "Reviewer assigned", description: `${reviewer.name} will receive this paper for human peer review.` }),
                    onError: (err: Error) => push({ kind: "error", title: "Assignment failed", description: err.message }),
                  },
                )
              }
            />
          ))}
        </div>
      )}

      <ResponsibleAINotice compact />
      <ReviewerProfileDialog reviewer={profile} onClose={() => setProfile(null)} />
    </div>
  );
}
