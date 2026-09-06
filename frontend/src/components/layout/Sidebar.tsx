import { NavLink } from "react-router-dom";
import {
  LayoutDashboard, FileText, UploadCloud, Bot, ClipboardList,
  Copyleft, Users, Settings, GraduationCap,
} from "lucide-react";
import { cn } from "../../lib/utils";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/papers", label: "Papers", icon: FileText },
  { to: "/upload", label: "Upload Paper", icon: UploadCloud },
  { to: "/analysis", label: "AI Analysis", icon: Bot },
  { to: "/reports", label: "Review Reports", icon: ClipboardList },
  { to: "/similarity", label: "Similarity", icon: Copyleft },
  { to: "/reviewers", label: "Reviewers", icon: Users },
  { to: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="hidden w-60 shrink-0 flex-col border-r border-ink-200/70 bg-white md:flex">
      <div className="flex items-center gap-2.5 px-5 py-5">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-600 text-white shadow-sm shadow-brand-600/30">
          <GraduationCap size={19} />
        </div>
        <div className="leading-tight">
          <p className="text-sm font-bold text-ink-900">AI Research Review</p>
          <p className="text-[11px] text-ink-400">Editorial Screening Platform</p>
        </div>
      </div>

      <nav className="flex-1 space-y-0.5 px-3 py-2">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-brand-50 text-brand-700"
                  : "text-ink-600 hover:bg-ink-50 hover:text-ink-900",
              )
            }
          >
            <Icon size={17} strokeWidth={2} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="mx-3 mb-4 rounded-xl bg-ink-50 px-3.5 py-3">
        <p className="text-[11px] font-semibold uppercase tracking-wide text-ink-400">Human-in-the-loop</p>
        <p className="mt-1 text-xs leading-snug text-ink-600">
          Final publication decisions always rest with human editors &amp; reviewers.
        </p>
      </div>
    </aside>
  );
}
