import { Sparkles, CircuitBoard, Copyleft, Info } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardHeader, CardBody } from "../components/ui/Card";
import { ResponsibleAINotice } from "../components/ui/ResponsibleAINotice";
import { useSystemStatus } from "../hooks/useApi";

export default function Settings() {
  const { data: status } = useSystemStatus();
  const isReal = status?.ai_engine_mode === "real";

  return (
    <div className="mx-auto max-w-2xl space-y-5">
      <PageHeading title="Settings" description="System configuration for this prototype instance." />

      <Card>
        <CardHeader title="AI Engine" subtitle="How agent findings are generated" />
        <CardBody className="space-y-4">
          <div className="flex items-center gap-3 rounded-xl border border-ink-100 bg-ink-50/60 px-4 py-3">
            {isReal ? <CircuitBoard size={20} className="text-brand-600" /> : <Sparkles size={20} className="text-brand-600" />}
            <div>
              <p className="text-sm font-semibold text-ink-800">
                {isReal ? `Live AI · ${status?.model}` : "AI Engine: Demo Mode"}
              </p>
              <p className="text-xs text-ink-500">{status?.message}</p>
            </div>
          </div>
          <p className="flex items-start gap-2 text-xs text-ink-500">
            <Info size={13} className="mt-0.5 shrink-0" />
            Set an <code className="rounded bg-ink-100 px-1 py-0.5">ANTHROPIC_API_KEY</code> environment variable on the
            backend to switch every agent to live Claude-generated findings — the pipeline falls back to demo mode
            automatically if a live call ever fails, so the demo never breaks mid-presentation.
          </p>
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="Similarity Detection" subtitle="Threshold used to flag high similarity" />
        <CardBody>
          <div className="flex items-center gap-3 rounded-xl border border-ink-100 bg-ink-50/60 px-4 py-3">
            <Copyleft size={20} className="text-brand-600" />
            <div>
              <p className="text-sm font-semibold text-ink-800">{status?.similarity_threshold ?? 30}% threshold</p>
              <p className="text-xs text-ink-500">Papers above this similarity score are flagged for editor review.</p>
            </div>
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="About" />
        <CardBody className="space-y-1 text-sm text-ink-600">
          <p>AI-Based Research Paper Review System — prototype v1.0.0</p>
          <p className="text-xs text-ink-400">
            A pre-review and editorial screening layer. It does not replace human peer reviewers.
          </p>
        </CardBody>
      </Card>

      <ResponsibleAINotice />
    </div>
  );
}
