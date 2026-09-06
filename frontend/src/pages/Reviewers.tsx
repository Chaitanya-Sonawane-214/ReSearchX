import { useState } from "react";
import { Search, Users } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { EmptyState } from "../components/ui/EmptyState";
import { ReviewerCard } from "../components/reviewers/ReviewerCard";
import { ReviewerProfileDialog } from "../components/reviewers/ReviewerProfileDialog";
import { useReviewerDirectory } from "../hooks/useApi";
import type { Reviewer } from "../types";

export default function Reviewers() {
  const { data: reviewers, isLoading } = useReviewerDirectory();
  const [query, setQuery] = useState("");
  const [profile, setProfile] = useState<Reviewer | null>(null);

  const filtered = (reviewers ?? []).filter(
    (r) =>
      !query ||
      r.name.toLowerCase().includes(query.toLowerCase()) ||
      r.expertise.some((e) => e.toLowerCase().includes(query.toLowerCase())),
  );

  return (
    <div className="space-y-5">
      <PageHeading
        title="Reviewer Directory"
        description="The full pool of human reviewers available for AI-suggested assignment."
        action={
          <div className="relative">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-300" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search reviewers…"
              className="w-56 rounded-lg border border-ink-200 bg-white py-2 pl-8 pr-3 text-sm text-ink-700 placeholder:text-ink-300 focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-100"
            />
          </div>
        }
      />

      {isLoading ? (
        <p className="py-8 text-center text-sm text-ink-400">Loading reviewers…</p>
      ) : filtered.length > 0 ? (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filtered.map((reviewer) => (
            <ReviewerCard key={reviewer.id} reviewer={reviewer} onViewProfile={() => setProfile(reviewer)} />
          ))}
        </div>
      ) : (
        <EmptyState icon={Users} title="No reviewers found" description="Try a different search term." />
      )}

      <ReviewerProfileDialog reviewer={profile} onClose={() => setProfile(null)} />
    </div>
  );
}
