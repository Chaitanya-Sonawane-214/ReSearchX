import { createContext, useCallback, useContext, useState, type ReactNode } from "react";
import { CheckCircle2, AlertTriangle, XCircle, Info, X } from "lucide-react";
import { cn } from "../../lib/utils";

type ToastKind = "success" | "error" | "warning" | "info";
interface Toast {
  id: number;
  kind: ToastKind;
  title: string;
  description?: string;
}

interface ToastContextValue {
  push: (toast: Omit<Toast, "id">) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

const KIND_STYLE: Record<ToastKind, { icon: typeof CheckCircle2; classes: string }> = {
  success: { icon: CheckCircle2, classes: "border-success-100 bg-success-50 text-success-700" },
  error: { icon: XCircle, classes: "border-critical-100 bg-critical-50 text-critical-700" },
  warning: { icon: AlertTriangle, classes: "border-warning-100 bg-warning-50 text-warning-700" },
  info: { icon: Info, classes: "border-info-100 bg-info-50 text-info-700" },
};

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const push = useCallback((toast: Omit<Toast, "id">) => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev, { ...toast, id }]);
    setTimeout(() => setToasts((prev) => prev.filter((t) => t.id !== id)), 5000);
  }, []);

  const dismiss = (id: number) => setToasts((prev) => prev.filter((t) => t.id !== id));

  return (
    <ToastContext.Provider value={{ push }}>
      {children}
      <div className="fixed bottom-4 right-4 z-[100] flex w-full max-w-sm flex-col gap-2">
        {toasts.map((t) => {
          const style = KIND_STYLE[t.kind];
          const Icon = style.icon;
          return (
            <div
              key={t.id}
              className={cn(
                "animate-fade-in-up flex items-start gap-2.5 rounded-xl border px-4 py-3 shadow-lg",
                style.classes,
              )}
            >
              <Icon size={18} className="mt-0.5 shrink-0" />
              <div className="flex-1">
                <p className="text-sm font-semibold">{t.title}</p>
                {t.description && <p className="mt-0.5 text-xs opacity-90">{t.description}</p>}
              </div>
              <button onClick={() => dismiss(t.id)} className="opacity-60 hover:opacity-100">
                <X size={14} />
              </button>
            </div>
          );
        })}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within ToastProvider");
  return ctx;
}
