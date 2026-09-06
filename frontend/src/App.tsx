import { BrowserRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AppLayout } from "./components/layout/AppLayout";
import { ToastProvider } from "./components/ui/Toast";

import Dashboard from "./pages/Dashboard";
import Papers from "./pages/Papers";
import UploadPaper from "./pages/UploadPaper";
import AnalysisPipeline from "./pages/AnalysisPipeline";
import AgentReview from "./pages/AgentReview";
import ReviewReport from "./pages/ReviewReport";
import SimilarityReport from "./pages/SimilarityReport";
import ReviewerAssignment from "./pages/ReviewerAssignment";
import PaperDetails from "./pages/PaperDetails";
import AIAnalysisList from "./pages/AIAnalysisList";
import ReviewReportsList from "./pages/ReviewReportsList";
import SimilarityList from "./pages/SimilarityList";
import Reviewers from "./pages/Reviewers";
import Settings from "./pages/Settings";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, refetchOnWindowFocus: false } },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ToastProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<AppLayout />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/papers" element={<Papers />} />
              <Route path="/upload" element={<UploadPaper />} />
              <Route path="/analysis" element={<AIAnalysisList />} />
              <Route path="/reports" element={<ReviewReportsList />} />
              <Route path="/similarity" element={<SimilarityList />} />
              <Route path="/reviewers" element={<Reviewers />} />
              <Route path="/settings" element={<Settings />} />

              <Route path="/papers/:id" element={<PaperDetails />} />
              <Route path="/papers/:id/pipeline" element={<AnalysisPipeline />} />
              <Route path="/papers/:id/agents" element={<AgentReview />} />
              <Route path="/papers/:id/report" element={<ReviewReport />} />
              <Route path="/papers/:id/similarity" element={<SimilarityReport />} />
              <Route path="/papers/:id/reviewers" element={<ReviewerAssignment />} />

              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </ToastProvider>
    </QueryClientProvider>
  );
}
