import { useRef, useState, type DragEvent } from "react";
import { UploadCloud, FileText, X, AlertCircle } from "lucide-react";
import { cn, formatBytes } from "../../lib/utils";

export function UploadDropzone({
  file,
  onFileSelected,
  onClear,
}: {
  file: File | null;
  onFileSelected: (file: File) => void;
  onClear: () => void;
}) {
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (f: File | undefined) => {
    if (!f) return;
    if (!f.name.toLowerCase().endsWith(".pdf")) {
      setError("Invalid File. Please upload a PDF research paper.");
      return;
    }
    setError(null);
    onFileSelected(f);
  };

  const onDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files?.[0]);
  };

  if (file) {
    return (
      <div className="flex items-center gap-3 rounded-2xl border border-ink-200 bg-white px-5 py-4">
        <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-600">
          <FileText size={20} />
        </div>
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold text-ink-900">{file.name}</p>
          <p className="text-xs text-ink-400">{formatBytes(file.size)} · Ready for Analysis</p>
        </div>
        <button
          onClick={onClear}
          className="flex h-8 w-8 items-center justify-center rounded-lg text-ink-400 hover:bg-ink-100 hover:text-ink-700"
        >
          <X size={16} />
        </button>
      </div>
    );
  }

  return (
    <div>
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        className={cn(
          "flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-14 text-center transition-colors",
          dragging ? "border-brand-400 bg-brand-50/60" : "border-ink-200 bg-white hover:border-brand-300 hover:bg-brand-50/30",
        )}
      >
        <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-brand-50 text-brand-600">
          <UploadCloud size={26} />
        </div>
        <p className="text-sm font-semibold text-ink-800">Drag &amp; drop PDF here</p>
        <p className="my-2 text-xs text-ink-400">or</p>
        <span className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm shadow-brand-600/20 hover:bg-brand-700">
          Browse PDF
        </span>
        <p className="mt-4 text-xs text-ink-400">Supported format: PDF · up to 25MB</p>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf,.pdf"
          className="hidden"
          onChange={(e) => handleFile(e.target.files?.[0])}
        />
      </div>
      {error && (
        <div className="mt-3 flex items-center gap-2 rounded-lg bg-critical-50 px-3 py-2 text-xs font-medium text-critical-700">
          <AlertCircle size={14} />
          {error}
        </div>
      )}
    </div>
  );
}
