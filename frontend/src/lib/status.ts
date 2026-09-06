import type { AgentStatus, IssueSeverity, PaperStatus } from "../types";

export type Tone = "success" | "warning" | "critical" | "info" | "brand" | "neutral";

export const TONE_CLASSES: Record<Tone, { bg: string; text: string; ring: string; dot: string }> = {
  success: { bg: "bg-success-50", text: "text-success-700", ring: "ring-success-100", dot: "bg-success-500" },
  warning: { bg: "bg-warning-50", text: "text-warning-700", ring: "ring-warning-100", dot: "bg-warning-500" },
  critical: { bg: "bg-critical-50", text: "text-critical-700", ring: "ring-critical-100", dot: "bg-critical-500" },
  info: { bg: "bg-info-50", text: "text-info-700", ring: "ring-info-100", dot: "bg-info-500" },
  brand: { bg: "bg-brand-50", text: "text-brand-700", ring: "ring-brand-100", dot: "bg-brand-500" },
  neutral: { bg: "bg-ink-100", text: "text-ink-600", ring: "ring-ink-200", dot: "bg-ink-400" },
};

interface StatusMeta {
  label: string;
  tone: Tone;
  animated?: boolean;
}

export const PAPER_STATUS_META: Record<PaperStatus, StatusMeta> = {
  uploaded: { label: "Ready for Analysis", tone: "neutral" },
  parsing: { label: "Parsing PDF…", tone: "info", animated: true },
  analyzing: { label: "AI Agents Running…", tone: "info", animated: true },
  aggregating: { label: "Aggregating Report…", tone: "info", animated: true },
  revision_required: { label: "Revision Required", tone: "warning" },
  ready_for_review: { label: "Ready for Review", tone: "success" },
  not_recommended: { label: "Not Recommended", tone: "critical" },
  similarity_check: { label: "Checking Similarity…", tone: "info", animated: true },
  similarity_flagged: { label: "High Similarity Flagged", tone: "critical" },
  reviewer_assignment: { label: "Reviewer Assignment", tone: "brand" },
  under_human_review: { label: "Human Review Pending", tone: "brand" },
  analysis_failed: { label: "Analysis Failed", tone: "critical" },
};

export const AGENT_STATUS_META: Record<AgentStatus, StatusMeta> = {
  pending: { label: "Pending", tone: "neutral" },
  running: { label: "Running", tone: "info", animated: true },
  completed: { label: "Completed", tone: "success" },
  failed: { label: "Failed", tone: "critical" },
};

export const SEVERITY_META: Record<IssueSeverity, StatusMeta & { rank: number }> = {
  critical: { label: "Critical", tone: "critical", rank: 0 },
  high: { label: "High", tone: "critical", rank: 1 },
  medium: { label: "Medium", tone: "warning", rank: 2 },
  low: { label: "Low", tone: "neutral", rank: 3 },
};

export const TONE_HEX: Record<Tone, string> = {
  success: "#10b981",
  warning: "#f59e0b",
  critical: "#ef4444",
  info: "#3b82f6",
  brand: "#3864db",
  neutral: "#94a3b8",
};

export function scoreTone(score: number): Tone {
  if (score >= 80) return "success";
  if (score >= 60) return "warning";
  return "critical";
}

/** For metrics where lower is better (e.g. similarity %). */
export function scoreToneInverted(value: number): Tone {
  if (value <= 15) return "success";
  if (value <= 30) return "warning";
  return "critical";
}
