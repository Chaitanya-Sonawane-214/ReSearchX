import type {
  Paper, PaperSummary, DashboardStats, SystemStatus, Reviewer, AgentReview,
} from "../types";

export const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000/api";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers:
      options.body && !(options.body instanceof FormData)
        ? { "Content-Type": "application/json", ...options.headers }
        : options.headers,
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const data = await res.json();
      detail = data.detail ?? detail;
    } catch {
      /* no JSON body */
    }
    throw new ApiError(detail, res.status);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  listPapers: () => request<PaperSummary[]>("/papers"),
  getPaper: (id: string) => request<Paper>(`/papers/${id}`),
  getAgents: (id: string) => request<AgentReview[]>(`/papers/${id}/agents`),
  getReport: (id: string) =>
    request<{ report: Paper["report"]; editorial: Paper["editorial"] }>(`/papers/${id}/report`),
  downloadReportUrl: (id: string) => `${API_BASE}/papers/${id}/report/download`,

  uploadPaper: (file: File, targetVenue?: string) => {
    const form = new FormData();
    form.append("file", file);
    if (targetVenue) form.append("target_venue", targetVenue);
    return request<Paper>("/papers/upload", { method: "POST", body: form });
  },

  analyzePaper: (id: string) => request<Paper>(`/papers/${id}/analyze`, { method: "POST" }),

  resubmitPaper: (id: string, file?: File) => {
    const form = new FormData();
    if (file) form.append("file", file);
    return request<Paper>(`/papers/${id}/resubmit`, { method: "POST", body: form });
  },

  runSimilarity: (id: string) => request<Paper>(`/papers/${id}/similarity`, { method: "POST" }),
  resolveSimilarity: (id: string, action: "proceed" | "return_to_author") =>
    request<Paper>(`/papers/${id}/similarity/resolve`, {
      method: "POST",
      body: JSON.stringify({ action }),
    }),

  getRecommendedReviewers: (id: string) => request<Reviewer[]>(`/papers/${id}/reviewers`),
  assignReviewer: (id: string, reviewerId: string) =>
    request<Paper>(`/papers/${id}/assign-reviewer`, {
      method: "POST",
      body: JSON.stringify({ reviewer_id: reviewerId }),
    }),

  reviewerDirectory: () => request<Reviewer[]>("/reviewers"),
  dashboardStats: () => request<DashboardStats>("/dashboard/stats"),
  systemStatus: () => request<SystemStatus>("/system/status"),
};
