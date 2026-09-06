from __future__ import annotations
from typing import Optional

from schemas import AgentReview, AgentStatus, ExtractedContent, IssueSeverity
from .base import BaseAgent

EXPECTED_SECTIONS = [
    "Abstract", "Introduction", "Related Work", "Methodology",
    "Results", "Discussion", "Conclusion", "References",
]

# sections that can reasonably substitute for one of the expected ones
SYNONYMS = {
    "Related Work": {"Literature Review", "Background"},
    "Methodology": {"Method", "Materials And Methods"},
    "Results": {"Evaluation", "Experiments", "Experimental Setup"},
    "Conclusion": {"Conclusions"},
    "Discussion": set(),
}


class StructureAgent(BaseAgent):
    """Evaluates the organization of the paper against the standard IMRaD-style
    academic structure."""

    name = "Structure Agent"

    def run_mock(self, paper_id: str, content: ExtractedContent, target_venue: Optional[str], full_text: str = "") -> AgentReview:
        rng = self.rng(paper_id)
        found = set(content.sections_found)
        matched = []
        missing = []

        for expected in EXPECTED_SECTIONS:
            candidates = {expected} | SYNONYMS.get(expected, set())
            if candidates & found:
                matched.append(expected)
            else:
                missing.append(expected)

        coverage = len(matched) / len(EXPECTED_SECTIONS)
        score = self.clamp(int(55 + coverage * 40 + rng.randint(-3, 5)))

        strengths = ["Clear section hierarchy detected"] if coverage >= 0.75 else []
        if len(matched) >= 5:
            strengths.append("Logical progression from introduction through conclusion")

        issues = []
        recommendations = []
        for section in missing:
            severity = IssueSeverity.HIGH if section in ("Abstract", "Introduction", "Methodology", "References") else IssueSeverity.MEDIUM
            issues.append(self.issue(
                severity,
                f"{section} section not clearly detected",
                f"A distinct '{section}' heading could not be located in the document structure.",
                self.name,
            ))
            recommendations.append(f"Add or clearly label a '{section}' section.")

        if "Related Work" in matched or "Related Work" in [s for s in EXPECTED_SECTIONS if s in matched]:
            if rng.random() < 0.4:
                issues.append(self.issue(
                    IssueSeverity.LOW,
                    "Related Work connection could be stronger",
                    "The Related Work section could be better connected to the proposed methodology.",
                    self.name,
                ))

        if not strengths:
            strengths.append("Core narrative arc (problem, method, results) is present")

        return AgentReview(
            agent_name=self.name,
            score=score,
            status=AgentStatus.COMPLETED,
            summary=f"Structure Score: {score}/100",
            strengths=strengths,
            issues=issues,
            recommendations=recommendations or ["Structure follows standard academic conventions."],
        )

    def build_prompt(self, content: ExtractedContent, target_venue: Optional[str]) -> str:
        return (
            "You are the Structure Agent. Evaluate the organization of this research paper "
            f"against standard academic structure. Detected sections: {content.sections_found}. "
            "Return strict JSON with score (0-100), strengths, issues "
            "([{severity, title, description}]) and recommendations."
        )
