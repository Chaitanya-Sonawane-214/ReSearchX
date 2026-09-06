import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { PlayCircle, Info } from "lucide-react";
import { PageHeading } from "../components/ui/PageHeading";
import { Card, CardHeader, CardBody } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { UploadDropzone } from "../components/upload/UploadDropzone";
import { PaperStatusBadge } from "../components/ui/StatusBadge";
import { useAnalyzePaper, useUploadPaper } from "../hooks/useApi";
import { useToast } from "../components/ui/Toast";
import { formatBytes } from "../lib/utils";
import type { Paper } from "../types";

export default function UploadPaper() {
  const navigate = useNavigate();
  const { push } = useToast();
  const [file, setFile] = useState<File | null>(null);
  const [targetVenue, setTargetVenue] = useState("");
  const [uploaded, setUploaded] = useState<Paper | null>(null);

  const upload = useUploadPaper();
  const analyze = useAnalyzePaper();

  const handleUpload = () => {
    if (!file) return;
    upload.mutate(
      { file, targetVenue: targetVenue.trim() || undefined },
      {
        onSuccess: (paper) => {
          setUploaded(paper);
          push({ kind: "success", title: "Upload complete", description: `${paper.filename} is ready for analysis.` });
        },
        onError: (err: Error) =>
          push({ kind: "error", title: "Upload failed", description: err.message }),
      },
    );
  };

  const handleStartAnalysis = () => {
    if (!uploaded) return;
    analyze.mutate(uploaded.id, {
      onSuccess: () => navigate(`/papers/${uploaded.id}/pipeline`),
      onError: (err: Error) => push({ kind: "error", title: "Could not start analysis", description: err.message }),
    });
  };

  return (
    <div className="mx-auto max-w-2xl space-y-5">
      <PageHeading
        title="Upload Research Paper"
        description="Submit a PDF to begin AI-assisted pre-review screening. This does not publish or reject your paper — it's an editorial pre-check."
      />

      <Card>
        <CardHeader title="1. Paper File" subtitle="Drag and drop, or browse for a PDF" />
        <CardBody>
          <UploadDropzone file={file} onFileSelected={(f) => { setFile(f); setUploaded(null); }} onClear={() => { setFile(null); setUploaded(null); }} />
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="2. Target Venue (optional)" subtitle="Used by the Scope Matching Agent to assess domain fit" />
        <CardBody>
          <input
            value={targetVenue}
            onChange={(e) => setTargetVenue(e.target.value)}
            placeholder="e.g. International Conference on Artificial Intelligence"
            disabled={!!uploaded}
            className="w-full rounded-lg border border-ink-200 bg-white px-3.5 py-2.5 text-sm text-ink-700 placeholder:text-ink-300 focus:border-brand-400 focus:outline-none focus:ring-2 focus:ring-brand-100 disabled:bg-ink-50"
          />
          <p className="mt-2 flex items-center gap-1.5 text-xs text-ink-400">
            <Info size={12} /> Leave blank to fall back to a generic research-domain classification.
          </p>
        </CardBody>
      </Card>

      {!uploaded ? (
        <Button size="lg" className="w-full" disabled={!file} loading={upload.isPending} onClick={handleUpload}>
          Upload Paper
        </Button>
      ) : (
        <Card className="border-brand-100 bg-brand-50/40">
          <CardBody className="pt-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-ink-900">{uploaded.title}</p>
                <p className="text-xs text-ink-500">
                  {formatBytes(uploaded.file_size)} · {uploaded.authors.join(", ") || "Authors pending extraction"}
                </p>
              </div>
              <PaperStatusBadge status={uploaded.status} />
            </div>
            <Button
              size="lg"
              className="mt-4 w-full"
              icon={<PlayCircle size={16} />}
              loading={analyze.isPending}
              onClick={handleStartAnalysis}
            >
              Start AI Review
            </Button>
          </CardBody>
        </Card>
      )}
    </div>
  );
}
