import { useState } from "react";
import { Dialog } from "../ui/Dialog";
import { Button } from "../ui/Button";
import { UploadDropzone } from "../upload/UploadDropzone";
import { useResubmitPaper } from "../../hooks/useApi";
import { useToast } from "../ui/Toast";

export function ResubmitDialog({
  paperId,
  open,
  onClose,
  onResubmitted,
}: {
  paperId: string;
  open: boolean;
  onClose: () => void;
  onResubmitted: (newPaperId: string) => void;
}) {
  const [file, setFile] = useState<File | null>(null);
  const resubmit = useResubmitPaper();
  const { push } = useToast();

  const handleResubmit = () => {
    resubmit.mutate(
      { id: paperId, file: file ?? undefined },
      {
        onSuccess: (paper) => {
          push({ kind: "success", title: "Revised paper submitted", description: "Ready for a fresh AI review pass." });
          onResubmitted(paper.id);
        },
        onError: (err: Error) => push({ kind: "error", title: "Resubmission failed", description: err.message }),
      },
    );
  };

  return (
    <Dialog open={open} onClose={onClose} title="Resubmit Revised Paper">
      <p className="mb-4 text-sm text-ink-500">
        Upload the revised PDF, or leave blank to resubmit the same file for this prototype
        demonstration — either way it starts a fresh AI review pass.
      </p>
      <UploadDropzone file={file} onFileSelected={setFile} onClear={() => setFile(null)} />
      <div className="mt-5 flex justify-end gap-2">
        <Button variant="ghost" onClick={onClose}>Cancel</Button>
        <Button loading={resubmit.isPending} onClick={handleResubmit}>Resubmit Paper</Button>
      </div>
    </Dialog>
  );
}
