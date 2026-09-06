// Mirrors backend/schemas/schemas.py — kept in sync by hand since this is a
// prototype (no codegen step). If you add a field on the backend, add it here too.

export type PaperStatus =
  | "uploaded"
  | "parsing"
  | "analyzing"
  | "aggregating"
  | "revision_required"
  | "ready_for_review"
  | "not_recommended"
  | "similarity_check"
  | "similarity_flagged"
  | "reviewer_assignment"
  | "under_human_review"
  | "analysis_failed";

export type AgentStatus = "pending" | "running" | "completed" | "failed";
export type IssueSeverity = "low" | "medium" | "high" | "critical";
export type SimilarityStatus = "acceptable" | "high";
export type Workload = "low" | "medium" | "high";
export type EditorialDecisionType = "ready_for_review" | "revision_required" | "not_recommended";

export const AGENT_NAMES = [
  "Layout Agent",
  "Structure Agent",
  "Formatting Agent",
  "Language Agent",
  "Citation Agent",
  "Technical Agent",
  "Scope Matching Agent",
] as const;

export interface ReviewIssue {
  severity: IssueSeverity;
  title: string;
  description: string;
  source_agent: string;
}

export interface AgentReview {
  agent_name: string;
  score: number;
  status: AgentStatus;
  summary: string;
  strengths: string[];
  issues: ReviewIssue[];
  recommendations: string[];
  started_at: string | null;
  completed_at: string | null;
  ai_generated: boolean;
}

export interface ParsingChecklistItem {
  key: string;
  label: string;
  status: AgentStatus;
  detail: string;
}

export interface ExtractedContent {
  page_count: number;
  word_count: number;
  figure_count: number;
  table_count: number;
  equation_count: number;
  reference_count: number;
  title: string;
  authors: string[];
  abstract: string;
  sections_found: string[];
  domain_keywords: string[];
}

export interface AggregatedReport {
  overall_score: number;
  strengths: string[];
  major_concerns: string[];
  minor_concerns: string[];
  priority_issues: ReviewIssue[];
  recommended_actions: string[];
  agent_scores: Record<string, number>;
}

export interface EditorialDecision {
  decision: EditorialDecisionType | null;
  headline: string;
  message: string;
  next_step: string;
}

export interface SimilaritySource {
  title: string;
  source: string;
  similarity: number;
  matched_excerpt: string;
}

export interface SimilarityResult {
  overall_similarity: number;
  direct_matches: number;
  potential_sources: SimilaritySource[];
  status: SimilarityStatus | null;
  checked_at: string | null;
}

export interface Reviewer {
  id: string;
  name: string;
  expertise: string[];
  domains: string[];
  publications: number;
  workload: Workload;
  conflict_of_interest: boolean;
  match_score: number;
  recommendation_score: number;
  bio: string;
}

export interface TimelineStep {
  key: string;
  label: string;
  status: "done" | "current" | "pending";
  timestamp: string | null;
}

export interface Paper {
  id: string;
  title: string;
  authors: string[];
  filename: string;
  file_size: number;
  uploaded_at: string;
  target_venue: string | null;
  status: PaperStatus;
  revision: number;
  overall_score: number | null;

  extracted: ExtractedContent | null;
  parsing_checklist: ParsingChecklistItem[];
  agents: AgentReview[];
  report: AggregatedReport | null;
  editorial: EditorialDecision | null;
  similarity: SimilarityResult | null;
  assigned_reviewer_id: string | null;
  reviewers: Reviewer[];
  timeline: TimelineStep[];
  error: string | null;
  analysis_progress: number;
}

export interface PaperSummary {
  id: string;
  title: string;
  authors: string[];
  status: PaperStatus;
  overall_score: number | null;
  uploaded_at: string;
  target_venue: string | null;
  revision: number;
}

export interface DashboardStats {
  total_papers: number;
  ai_reviews_completed: number;
  revision_required: number;
  ready_for_review: number;
  similarity_alerts: number;
  under_human_review: number;
  status_breakdown: Record<string, number>;
}

export interface SystemStatus {
  ai_engine_mode: "demo" | "real";
  model: string | null;
  similarity_threshold: number;
  message: string;
}
