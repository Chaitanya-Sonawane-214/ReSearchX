import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../services/api";
import type { Paper } from "../types";

const ACTIVE_STATES = new Set(["uploaded", "parsing", "analyzing", "aggregating"]);

export function useDashboardStats() {
  return useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: api.dashboardStats,
    refetchInterval: 5000,
  });
}

export function useSystemStatus() {
  return useQuery({ queryKey: ["system-status"], queryFn: api.systemStatus, staleTime: 60_000 });
}

export function usePapers() {
  return useQuery({ queryKey: ["papers"], queryFn: api.listPapers, refetchInterval: 4000 });
}

export function usePaper(id: string | undefined, opts: { poll?: boolean } = {}) {
  return useQuery({
    queryKey: ["paper", id],
    queryFn: () => api.getPaper(id as string),
    enabled: !!id,
    refetchInterval: (query) => {
      if (!opts.poll) return false;
      const data = query.state.data as Paper | undefined;
      if (!data) return 800;
      return ACTIVE_STATES.has(data.status) ? 900 : false;
    },
  });
}

export function useReviewerDirectory() {
  return useQuery({ queryKey: ["reviewer-directory"], queryFn: api.reviewerDirectory, staleTime: 60_000 });
}

export function useRecommendedReviewers(id: string | undefined) {
  return useQuery({
    queryKey: ["reviewers", id],
    queryFn: () => api.getRecommendedReviewers(id as string),
    enabled: !!id,
  });
}

function useInvalidateAll() {
  const qc = useQueryClient();
  return (id?: string) => {
    qc.invalidateQueries({ queryKey: ["papers"] });
    qc.invalidateQueries({ queryKey: ["dashboard-stats"] });
    if (id) qc.invalidateQueries({ queryKey: ["paper", id] });
  };
}

export function useUploadPaper() {
  const invalidate = useInvalidateAll();
  return useMutation({
    mutationFn: ({ file, targetVenue }: { file: File; targetVenue?: string }) =>
      api.uploadPaper(file, targetVenue),
    onSuccess: () => invalidate(),
  });
}

export function useAnalyzePaper() {
  const invalidate = useInvalidateAll();
  return useMutation({
    mutationFn: (id: string) => api.analyzePaper(id),
    onSuccess: (_data, id) => invalidate(id),
  });
}

export function useResubmitPaper() {
  const invalidate = useInvalidateAll();
  return useMutation({
    mutationFn: ({ id, file }: { id: string; file?: File }) => api.resubmitPaper(id, file),
    onSuccess: () => invalidate(),
  });
}

export function useRunSimilarity() {
  const invalidate = useInvalidateAll();
  return useMutation({
    mutationFn: (id: string) => api.runSimilarity(id),
    onSuccess: (_data, id) => invalidate(id),
  });
}

export function useResolveSimilarity() {
  const invalidate = useInvalidateAll();
  return useMutation({
    mutationFn: ({ id, action }: { id: string; action: "proceed" | "return_to_author" }) =>
      api.resolveSimilarity(id, action),
    onSuccess: (_data, { id }) => invalidate(id),
  });
}

export function useAssignReviewer() {
  const invalidate = useInvalidateAll();
  return useMutation({
    mutationFn: ({ id, reviewerId }: { id: string; reviewerId: string }) =>
      api.assignReviewer(id, reviewerId),
    onSuccess: (_data, { id }) => invalidate(id),
  });
}
