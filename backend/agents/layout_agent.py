from __future__ import annotations
from typing import Optional

from schemas import AgentReview, AgentStatus, ExtractedContent, IssueSeverity
from .base import BaseAgent


class LayoutAgent(BaseAgent):
    """Evaluates visual/structural presentation: page consistency, margins,
    figure/table placement, heading consistency, spacing."""

    name = "Layout Agent"

    def run_mock(self, paper_id: str, content: ExtractedContent, target_venue: Optional[str], full_text: str = "") -> AgentReview:
        rng = self.rng(paper_id)
        score = 78
        strengths = ["Consistent page structure across sections"]
        issues = []
        recommendations = []

        visual_density = content.figure_count + content.table_count
        if content.page_count and visual_density / max(content.page_count, 1) > 0.6:
            issues.append(self.issue(
                IssueSeverity.MEDIUM,
                "Dense visual layout",
                "Figures and tables are packed closely relative to page count; some may crowd section boundaries.",
                self.name,
            ))
            recommendations.append("Distribute figures/tables more evenly across sections.")
            score -= 6
        else:
            strengths.append("Figures and tables are proportionate to document length")
            score += 6

        if content.figure_count > 0:
            strengths.append("Figures generally positioned correctly relative to referencing text")
        if content.page_count < 4:
            issues.append(self.issue(
                IssueSeverity.LOW,
                "Short document length",
                "Page count is on the low side for a full research paper submission.",
                self.name,
            ))
            score -= 4

        jitter = rng.randint(-4, 6)
        score = self.clamp(score + jitter)

        if rng.random() < 0.5:
            issues.append(self.issue(
                IssueSeverity.LOW,
                "Minor spacing inconsistency",
                "Two figures appear too close to section boundaries.",
                self.name,
            ))
            recommendations.append("Add breathing room between floated figures and adjacent headings.")

        return AgentReview(
            agent_name=self.name,
            score=score,
            status=AgentStatus.COMPLETED,
            summary=f"Layout Score: {score}/100",
            strengths=strengths,
            issues=issues,
            recommendations=recommendations or ["Maintain current spacing conventions in the final revision."],
        )

    def build_prompt(self, content: ExtractedContent, target_venue: Optional[str]) -> str:
        return (
            "You are the Layout Agent in an academic paper pre-review pipeline. "
            "Evaluate visual/structural presentation quality (page consistency, margins, "
            "figure/table placement, heading consistency, spacing) using ONLY the extracted "
            f"statistics: pages={content.page_count}, figures={content.figure_count}, "
            f"tables={content.table_count}, equations={content.equation_count}. "
            "Return strict JSON: {\"score\": int 0-100, \"strengths\": [str], "
            "\"issues\": [{\"severity\": \"low|medium|high|critical\", \"title\": str, \"description\": str}], "
            "\"recommendations\": [str]}. Be specific but concise."
        )
