from __future__ import annotations
from typing import Optional

from schemas import AgentReview, AgentStatus, ExtractedContent, IssueSeverity
from .base import BaseAgent

# Maps lowercase keywords that might appear in a user-entered target venue name
# to the domain categories produced by services.pdf_service.DOMAIN_KEYWORDS.
VENUE_DOMAIN_HINTS = {
    "artificial intelligence": "Artificial Intelligence / Machine Learning",
    "machine learning": "Artificial Intelligence / Machine Learning",
    "ai": "Artificial Intelligence / Machine Learning",
    "neural": "Artificial Intelligence / Machine Learning",
    "language": "Natural Language Processing",
    "nlp": "Natural Language Processing",
    "computational linguistics": "Natural Language Processing",
    "vision": "Computer Vision",
    "image": "Computer Vision",
    "network": "Networking / Systems",
    "systems": "Networking / Systems",
    "cloud": "Networking / Systems",
    "health": "Bioinformatics / Healthcare",
    "medical": "Bioinformatics / Healthcare",
    "bio": "Bioinformatics / Healthcare",
    "robot": "Robotics",
    "security": "Security",
    "cryptograph": "Security",
    "sustainab": "Environmental / Sustainability",
    "climate": "Environmental / Sustainability",
    "environment": "Environmental / Sustainability",
}


class ScopeAgent(BaseAgent):
    """Determines whether the paper fits a user-specified target venue, or
    falls back to a generic research-domain classification."""

    name = "Scope Matching Agent"

    def _infer_venue_domain(self, target_venue: Optional[str]) -> Optional[str]:
        if not target_venue:
            return None
        lowered = target_venue.lower()
        for hint, domain in VENUE_DOMAIN_HINTS.items():
            if hint in lowered:
                return domain
        return None

    def run_mock(self, paper_id: str, content: ExtractedContent, target_venue: Optional[str], full_text: str = "") -> AgentReview:
        rng = self.rng(paper_id)
        strengths = []
        issues = []
        recommendations = []

        top_domain = content.domain_keywords[0] if content.domain_keywords else "General Research"
        venue_domain = self._infer_venue_domain(target_venue)

        if not target_venue:
            match_score = self.clamp(70 + rng.randint(-10, 15))
            strengths.append(f"Generic domain classification: {top_domain}")
            recommendations.append("Provide a target venue for a more precise scope match.")
        elif venue_domain and venue_domain == top_domain:
            match_score = self.clamp(88 + rng.randint(-5, 10))
            strengths.append(f"Strong alignment between paper domain ({top_domain}) and target venue")
            strengths.append("Relevant research methodology for the target venue")
        elif venue_domain and content.domain_keywords and venue_domain in content.domain_keywords:
            match_score = self.clamp(70 + rng.randint(-5, 10))
            strengths.append(f"Paper touches on {venue_domain}, among other detected domains")
        else:
            match_score = self.clamp(40 + rng.randint(-10, 15))
            issues.append(self.issue(
                IssueSeverity.MEDIUM,
                "Scope mismatch risk",
                f"The paper's detected domain ({top_domain}) may not closely match the stated "
                f"target venue ('{target_venue}').",
                self.name,
            ))
            recommendations.append("Confirm the target venue's scope explicitly covers this paper's domain.")

        if content.domain_keywords:
            strengths.append(f"Appropriate application domain: {top_domain}")

        return AgentReview(
            agent_name=self.name,
            score=match_score,
            status=AgentStatus.COMPLETED,
            summary=f"Scope Match: {match_score}%",
            strengths=strengths or ["Domain classification completed"],
            issues=issues,
            recommendations=recommendations or ["Scope alignment looks appropriate for the stated venue."],
        )

    def build_prompt(self, content: ExtractedContent, target_venue: Optional[str]) -> str:
        return (
            "You are the Scope Matching Agent. Determine whether this paper fits the target venue "
            f"'{target_venue or 'unspecified — use a generic domain classification'}', given detected "
            f"domain keywords: {content.domain_keywords}. Return strict JSON with score (0-100, treated "
            "as a percentage match), strengths, issues, recommendations."
        )
