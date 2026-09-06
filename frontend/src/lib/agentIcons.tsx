import {
  LayoutGrid, ListTree, Type, Languages, Quote, FlaskConical, Target, type LucideIcon,
} from "lucide-react";

export const AGENT_ICONS: Record<string, LucideIcon> = {
  "Layout Agent": LayoutGrid,
  "Structure Agent": ListTree,
  "Formatting Agent": Type,
  "Language Agent": Languages,
  "Citation Agent": Quote,
  "Technical Agent": FlaskConical,
  "Scope Matching Agent": Target,
};

export function agentIcon(name: string): LucideIcon {
  return AGENT_ICONS[name] ?? Target;
}
