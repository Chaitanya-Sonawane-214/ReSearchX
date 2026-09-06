"""Report Aggregation Agent + Editorial Decision Agent.

Combines the seven specialized agent outputs into one unified review report,
then derives an editorial screening recommendation from it. This is still an
*AI-assisted* recommendation — the module docstring and every user-facing
string are careful to say "screening", never a final scientific verdict.
"""
from __future__ import annotations

from typing import List

from schemas import (
    AgentReview, AggregatedReport, EditorialDecision, EditorialDecisionType,
    IssueSeverity, ReviewIssue,
)

AGENT_WEIGHTS = {
    "Layout Agent": 0.10,
    "Structure Agent": 0.15,
    "Formatting Agent": 0.10,
    "Language Agent": 0.15,
    "Citation Agent": 0.15,
    "Technical Agent": 0.25,
    "Scope Matching Agent": 0.10,
}

_SEVERITY_RANK = {
    IssueSeverity.CRITICAL: 0,
    IssueSeverity.HIGH: 1,
    IssueSeverity.MEDIUM: 2,
    IssueSeverity.LOW: 3,
}


def aggregate(agent_reviews: List[AgentReview]) -> AggregatedReport:
    agent_scores = {a.agent_name: a.score for a in agent_reviews}

    weighted_total = sum(AGENT_WEIGHTS.get(name, 0) * score for name, score in agent_scores.items())
    weight_sum = sum(AGENT_WEIGHTS.get(name, 0) for name in agent_scores) or 1
    overall_score = round(weighted_total / weight_sum)

    strengths: List[str] = []
    for review in agent_reviews:
        if review.score >= 85 and review.strengths:
            strengths.append(review.strengths[0])
    if not strengths:
        strengths.append("Paper demonstrates baseline academic quality across most dimensions")

    all_issues: List[ReviewIssue] = []
    for review in agent_reviews:
        all_issues.extend(review.issues)
    all_issues.sort(key=lambda i: _SEVERITY_RANK.get(i.severity, 9))

    major = [f"{i.title}" for i in all_issues if i.severity in (IssueSeverity.CRITICAL, IssueSeverity.HIGH)]
    minor = [f"{i.title}" for i in all_issues if i.severity in (IssueSeverity.MEDIUM, IssueSeverity.LOW)]

    # de-dupe while preserving order
    major = list(dict.fromkeys(major))[:5]
    minor = list(dict.fromkeys(minor))[:6]

    recommended_actions = []
    for review in agent_reviews:
        recommended_actions.extend(review.recommendations)
    recommended_actions = list(dict.fromkeys(recommended_actions))[:6]

    return AggregatedReport(
        overall_score=overall_score,
        strengths=strengths[:5],
        major_concerns=major,
        minor_concerns=minor,
        priority_issues=all_issues[:10],
        recommended_actions=recommended_actions,
        agent_scores=agent_scores,
    )


def decide(report: AggregatedReport) -> EditorialDecision:
    has_critical = any(i.severity == IssueSeverity.CRITICAL for i in report.priority_issues)
    high_count = sum(1 for i in report.priority_issues if i.severity == IssueSeverity.HIGH)

    if report.overall_score < 55 or has_critical:
        return EditorialDecision(
            decision=EditorialDecisionType.NOT_RECOMMENDED,
            headline="NOT RECOMMENDED FOR CURRENT REVIEW",
            message="Significant issues were identified during automated screening. This is an "
                    "AI-assisted screening outcome, not a final scientific rejection.",
            next_step="Return to author for major revision, or editor override.",
        )
    if report.overall_score < 78 or high_count >= 1:
        return EditorialDecision(
            decision=EditorialDecisionType.REVISION_REQUIRED,
            headline="REVISION REQUIRED",
            message="The paper contains issues that should be addressed before entering human peer review.",
            next_step="Author resubmission after addressing flagged issues.",
        )
    return EditorialDecision(
        decision=EditorialDecisionType.READY_FOR_REVIEW,
        headline="READY FOR REVIEW",
        message="The paper satisfies the minimum AI-assisted screening criteria.",
        next_step="Plagiarism / Similarity Detection",
    )
