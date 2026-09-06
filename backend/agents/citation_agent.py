from __future__ import annotations
import re
from typing import Optional

from schemas import AgentReview, AgentStatus, ExtractedContent, IssueSeverity
from .base import BaseAgent

_INTEXT_CITATION_RE = re.compile(r"\[\d+(?:,\s*\d+)*\]|\([A-Z][a-zA-Z]+(?:\s+et al\.)?,\s*\d{4}\)")
_CLAIM_WORDS = re.compile(
    r"\b(demonstrates?|shows?|proves?|significant(?:ly)?|outperforms?|state[- ]of[- ]the[- ]art|"
    r"best results|superior)\b",
    re.IGNORECASE,
)


def _split_sentences(text: str):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


class CitationAgent(BaseAgent):
    """Evaluates citation & reference quality: presence, consistency,
    unsupported claims, reference completeness."""

    name = "Citation Agent"

    def run_mock(self, paper_id: str, content: ExtractedContent, target_venue: Optional[str], full_text: str = "") -> AgentReview:
        rng = self.rng(paper_id)
        text = full_text or content.abstract
        sentences = _split_sentences(text)[:400]

        intext_count = len(_INTEXT_CITATION_RE.findall(text))
        score = 75
        strengths = []
        issues = []
        recommendations = []

        if intext_count == 0:
            issues.append(self.issue(
                IssueSeverity.CRITICAL,
                "No in-text citations detected",
                "The document does not appear to contain recognizable in-text citation markers.",
                self.name,
            ))
            score -= 25
        elif intext_count < 8:
            issues.append(self.issue(
                IssueSeverity.MEDIUM,
                "Sparse in-text citation coverage",
                f"Only {intext_count} in-text citation markers detected across the document.",
                self.name,
            ))
            score -= 8
        else:
            strengths.append("Most major claims are cited with recognizable in-text markers")
            score += 8

        unsupported = 0
        for s in sentences:
            if _CLAIM_WORDS.search(s) and not _INTEXT_CITATION_RE.search(s):
                unsupported += 1
        if unsupported > 0:
            issues.append(self.issue(
                IssueSeverity.MEDIUM if unsupported <= 5 else IssueSeverity.HIGH,
                "Potentially unsupported claims",
                f"{unsupported} sentence(s) make strong claims (e.g. 'demonstrates', 'state-of-the-art') "
                "without an adjacent citation marker.",
                self.name,
            ))
            recommendations.append("Add citations to support strong or comparative claims.")
            score -= min(15, unsupported * 2)

        if content.reference_count == 0:
            issues.append(self.issue(
                IssueSeverity.HIGH,
                "Reference list not detected",
                "No reference list could be located to cross-check citation completeness.",
                self.name,
            ))
            score -= 12
        elif content.reference_count < intext_count * 0.5 and intext_count > 0:
            issues.append(self.issue(
                IssueSeverity.LOW,
                "Reference list may be incomplete",
                f"{content.reference_count} references detected versus {intext_count} in-text citation markers.",
                self.name,
            ))
            recommendations.append("Verify every in-text citation has a matching reference list entry.")
            score -= 4
        else:
            strengths.append("Reference count is consistent with in-text citation volume")

        score = self.clamp(score + rng.randint(-3, 5))
        if not strengths:
            strengths.append("Citation style is applied consistently where present")

        return AgentReview(
            agent_name=self.name,
            score=score,
            status=AgentStatus.COMPLETED,
            summary=f"Citation Score: {score}/100",
            strengths=strengths,
            issues=issues,
            recommendations=recommendations or ["Citation coverage looks reasonable; spot-check reference matching."],
        )

    def build_prompt(self, content: ExtractedContent, target_venue: Optional[str]) -> str:
        return (
            "You are the Citation Agent. Evaluate citation presence, consistency and reference "
            f"completeness given reference_count={content.reference_count}. "
            "Return strict JSON with score, strengths, issues, recommendations."
        )
