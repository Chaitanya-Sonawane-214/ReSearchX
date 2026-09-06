import { useLocation, useNavigate } from "react-router-dom";
import { Sparkles, UploadCloud, CircuitBoard } from "lucide-react";
import { Button } from "../ui/Button";
import { useSystemStatus } from "../../hooks/useApi";

const SECTION_LABELS: [string, string][] = [
  ["/upload", "Upload Paper"],
  ["/analysis", "AI Analysis"],
  ["/reports", "Review Reports"],
  ["/similarity", "Similarity"],
  ["/reviewers", "Reviewers"],
  ["/settings", "Settings"],
  ["/papers", "Papers"],
  ["/", "Dashboard"],
];

function sectionFor(pathname: string) {
  return SECTION_LABELS.find(([prefix]) => pathname.startsWith(prefix))?.[1] ?? "";
}

export function Header() {
  const location = useLocation();
  const navigate = useNavigate();
  const { data: status } = useSystemStatus();
  const section = sectionFor(location.pathname);

  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-ink-200/70 bg-white/80 px-6 backdrop-blur">
      <div className="flex items-center gap-2 text-sm">
        <span className="text-ink-400">Platform</span>
        <span className="text-ink-300">/</span>
        <span className="font-semibold text-ink-800">{section}</span>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden items-center gap-1.5 rounded-full border border-ink-200 bg-white px-3 py-1.5 text-xs font-medium text-ink-600 sm:flex">
          {status?.ai_engine_mode === "real" ? (
            <CircuitBoard size={13} className="text-brand-500" />
          ) : (
            <Sparkles size={13} className="text-brand-500" />
          )}
          {status?.ai_engine_mode === "real" ? `Live AI · ${status.model}` : "AI Engine: Demo Mode"}
        </div>
        <Button size="sm" icon={<UploadCloud size={14} />} onClick={() => navigate("/upload")}>
          Upload Paper
        </Button>
      </div>
    </header>
  );
}
