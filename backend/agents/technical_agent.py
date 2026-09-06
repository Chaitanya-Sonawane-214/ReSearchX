from __future__ import annotations
import re
from typing import Optional

from schemas import AgentReview, AgentStatus, ExtractedContent, IssueSeverity
from .base import BaseAgent

_CATEGORY_KEYWORDS = {
    "problem definition": ["problem statement", "we address", "this paper proposes", "objective of this"],
    "methodology": ["method", "approach", "algorithm", "framework", "architecture"],
    "experiments/results": ["experiment", "result", "evaluation", "we observe", "table", "figure"],
    "limitations": ["limitation", "future work", "threats to validity", "does not account for"],
    "reproducibility": ["dataset", "code available", "implementation detail", "hyperparameter", "open source", "github"],
    "novelty": ["novel", "first to", "unlike prior work", "in contrast to previous"],
}


class TechnicalAgent(BaseAgent):
    """Evaluates technical quality signals: problem definition, methodology,
    experimental design, limitations, reproducibility, novelty indicators."""

    name = "Technical Agent"

    def run_mock(self, paper_id: str, content: ExtractedContent, target_venue: Optional[str], full_text: str = "") -> AgentReview:
        rng = self.rng(paper_id)
        text = (full_text or content.abstract).lower()

        coverage = {}
        for category, keywords in _CATEGORY_KEYWORDS.items():
            coverage[category] = any(kw in text for kw in keywords)

        covered = sum(coverage.values())
        score = self.clamp(int(45 + (covered / len(_CATEGORY_KEYWORDS)) * 45 + rng.randint(-3, 6)))

        strengths = []
        issues = []
        recommendations = []

        if coverage["problem definition"]:
            strengths.append("Problem is clearly defined")
        else:
            issues.append(self.issue(
                IssueSeverity.MEDIUM,
                "Problem statement not clearly signposted",
                "No clear explicit problem-statement phrasing was detected near the introduction.",
                self.name,
            ))
            recommendations.append("State the research problem explicitly in the introduction.")

        if coverage["methodology"]:
            strengths.append("Methodology is reasonably detailed")
        if coverage["experiments/results"]:
            strengths.append("Experimental results are presented with supporting evidence")
        else:
            issues.append(self.issue(
                IssueSeverity.HIGH,
                "Limited experimental evidence",
                "Little indication of concrete experimental results or evaluation was detected.",
                self.name,
            ))
            recommendations.append("Include a dedicated results/evaluation section with quantitative evidence.")

        if not coverage["limitations"]:
            issues.append(self.issue(
                IssueSeverity.HIGH,
                "Dataset/approach limitations are not sufficiently discussed",
                "No explicit limitations or threats-to-validity discussion was detected.",
                self.name,
            ))
            recommendations.append("Add an explicit limitations discussion (dataset scope, generalizability).")

        if not coverage["reproducibility"]:
            issues.append(self.issue(
                IssueSeverity.MEDIUM,
                "Reproducibility information could be improved",
                "No mention of dataset availability, code release, or implementation details was found.",
                self.name,
            ))
            recommendations.append("State dataset source and, if possible, share code/implementation details.")

        if coverage["novelty"]:
            strengths.append("Novelty relative to prior work is explicitly framed")

        if not strengths:
            strengths.append("Core technical narrative (problem → method → results) is present")

        return AgentReview(
            agent_name=self.name,
            score=score,
            status=AgentStatus.COMPLETED,
            summary=f"Technical Score: {score}/100",
            strengths=strengths,
            issues=issues,
            recommendations=recommendations or ["Technical presentation is solid; minor polish recommended."],
        )

    def build_prompt(self, content: ExtractedContent, target_venue: Optional[str]) -> str:
        return (
            "You are the Technical Review Agent. Evaluate problem definition, methodology, "
            "experimental design, limitations, reproducibility and novelty for a paper with "
            f"abstract: \"{content.abstract[:600]}\". These are AI-generated review findings, "
            "not guaranteed scientific truth — phrase issues as observations, not verdicts. "
            "Return strict JSON with score, strengths, issues, recommendations."
        )
