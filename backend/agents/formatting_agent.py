from __future__ import annotations
from typing import Optional

from schemas import AgentReview, AgentStatus, ExtractedContent, IssueSeverity
from .base import BaseAgent


class FormattingAgent(BaseAgent):
    """Evaluates formatting consistency: fonts, headings, captions, numbering,
    reference formatting."""

    name = "Formatting Agent"

    def run_mock(self, paper_id: str, content: ExtractedContent, target_venue: Optional[str], full_text: str = "") -> AgentReview:
        rng = self.rng(paper_id)
        score = 80
        strengths = ["Heading formatting is consistent across sections"]
        issues = []
        recommendations = []

        if content.reference_count == 0:
            issues.append(self.issue(
                IssueSeverity.HIGH,
                "No reference list detected",
                "A clearly numbered or formatted reference list could not be located.",
                self.name,
            ))
            score -= 15
        elif content.reference_count < 10:
            issues.append(self.issue(
                IssueSeverity.MEDIUM,
                "Reference formatting inconsistencies",
                f"Only {content.reference_count} references detected with a consistent pattern; "
                "some entries may use a different citation style.",
                self.name,
            ))
            recommendations.append("Apply a single consistent reference style (e.g. IEEE or APA) throughout.")
            score -= 6
        else:
            strengths.append("Reference list follows a consistent numbering pattern")

        if content.table_count > 0 and rng.random() < 0.45:
            issues.append(self.issue(
                IssueSeverity.LOW,
                "Caption style variance",
                "Two table captions appear to use slightly different formatting conventions.",
                self.name,
            ))
            recommendations.append("Standardize caption style (bold label + period + sentence case).")
            score -= 3

        if content.equation_count > 0:
            strengths.append("Equations are consistently numbered")

        score = self.clamp(score + rng.randint(-3, 5))

        return AgentReview(
            agent_name=self.name,
            score=score,
            status=AgentStatus.COMPLETED,
            summary=f"Formatting Score: {score}/100",
            strengths=strengths,
            issues=issues,
            recommendations=recommendations or ["Formatting is largely consistent; no major action required."],
        )

    def build_prompt(self, content: ExtractedContent, target_venue: Optional[str]) -> str:
        return (
            "You are the Formatting Agent. Evaluate formatting consistency (fonts, headings, "
            f"captions, numbering, references) given reference_count={content.reference_count}, "
            f"table_count={content.table_count}, equation_count={content.equation_count}. "
            "Return strict JSON with score, strengths, issues, recommendations."
        )
