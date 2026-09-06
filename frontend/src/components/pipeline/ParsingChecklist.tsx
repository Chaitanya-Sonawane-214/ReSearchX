import { Check, Loader2, FileSearch } from "lucide-react";
import { Card, CardHeader, CardBody } from "../ui/Card";
import type { ParsingChecklistItem } from "../../types";
import { cn } from "../../lib/utils";

export function ParsingChecklist({ items }: { items: ParsingChecklistItem[] }) {
  return (
    <Card>
      <CardHeader
        title="PDF Parsing & Preprocessing"
        subtitle="Extracting text, figures, tables, equations, references and metadata"
        action={<FileSearch size={18} className="text-ink-300" />}
      />
      <CardBody>
        <ul className="space-y-2.5">
          {items.map((item) => (
            <li key={item.key} className="flex items-center gap-3 text-sm">
              <span
                className={cn(
                  "flex h-6 w-6 shrink-0 items-center justify-center rounded-full",
                  item.status === "completed" && "bg-success-100 text-success-700",
                  item.status === "running" && "bg-info-100 text-info-700",
                  item.status === "pending" && "bg-ink-100 text-ink-400",
                )}
              >
                {item.status === "completed" && <Check size={13} strokeWidth={3} />}
                {item.status === "running" && <Loader2 size={13} className="animate-spin" />}
                {item.status === "pending" && <span className="h-1.5 w-1.5 rounded-full bg-ink-300" />}
              </span>
              <span className={cn("font-medium", item.status === "pending" ? "text-ink-400" : "text-ink-800")}>
                {item.label}
              </span>
              <span className="ml-auto text-xs text-ink-400">
                {item.status === "completed" ? item.detail : item.status === "running" ? "Processing…" : "Pending"}
              </span>
            </li>
          ))}
        </ul>
      </CardBody>
    </Card>
  );
}
