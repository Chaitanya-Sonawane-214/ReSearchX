"""Seeds the in-memory store with demo data on startup (spec section 22):

  - One real, fully-parseable sample PDF ("hero" paper) left at UPLOADED
    status, ready to be driven through the live pipeline during a demo.
  - Several additional papers already at various later pipeline stages,
    handcrafted directly as state (no PDF behind them) purely so the
    Dashboard / Papers list look like a populated, real editorial platform.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from data.generate_sample import build_pdf, TITLE as SAMPLE_TITLE, AUTHORS as SAMPLE_AUTHORS
from models import store
from schemas import (
    AgentReview, AgentStatus, AggregatedReport, EditorialDecision, EditorialDecisionType,
    ExtractedContent, IssueSeverity, Paper, PaperStatus, ParsingChecklistItem, ReviewIssue,
    Reviewer, SimilarityResult, SimilarityStatus, SimilaritySource, Workload,
)
from services.aggregation_service import AGENT_WEIGHTS
from services.reviewer_service import REVIEWER_POOL

AGENT_NAMES = list(AGENT_WEIGHTS.keys())


def _iso(days_ago: float) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


def _completed_checklist() -> List[ParsingChecklistItem]:
    return [
        ParsingChecklistItem(key="text", label="Text Extraction", status=AgentStatus.COMPLETED, detail="Completed"),
        ParsingChecklistItem(key="figures", label="Figures Detection", status=AgentStatus.COMPLETED, detail="figures"),
        ParsingChecklistItem(key="tables", label="Tables Detection", status=AgentStatus.COMPLETED, detail="tables"),
        ParsingChecklistItem(key="equations", label="Equations Detection", status=AgentStatus.COMPLETED, detail="equations"),
        ParsingChecklistItem(key="references", label="References Extraction", status=AgentStatus.COMPLETED, detail="references"),
        ParsingChecklistItem(key="metadata", label="Metadata Extraction", status=AgentStatus.COMPLETED, detail="Completed"),
    ]


def _fabricate_agents(agent_scores: Dict[str, int]) -> List[AgentReview]:
    reviews = []
    for name, score in agent_scores.items():
        issues = []
        strengths = [f"{name.replace(' Agent', '')} quality is above the acceptance threshold"] if score >= 80 else []
        if score < 85:
            issues.append(ReviewIssue(
                severity=IssueSeverity.MEDIUM if score >= 65 else IssueSeverity.HIGH,
                title=f"{name.replace(' Agent', '')} needs attention",
                description=f"{name} flagged points worth reviewing before this paper proceeds.",
                source_agent=name,
            ))
        if not strengths:
            strengths.append(f"{name} completed its evaluation")
        reviews.append(AgentReview(
            agent_name=name, score=score, status=AgentStatus.COMPLETED,
            summary=f"{name.replace(' Agent', '')} Score: {score}/100",
            strengths=strengths, issues=issues,
            recommendations=[f"Address flagged {name.replace(' Agent', '').lower()} issues."] if issues else [],
        ))
    return reviews


def _report_from_agents(agents: List[AgentReview]) -> AggregatedReport:
    agent_scores = {a.agent_name: a.score for a in agents}
    weighted = sum(AGENT_WEIGHTS.get(n, 0) * s for n, s in agent_scores.items())
    overall = round(weighted / (sum(AGENT_WEIGHTS.get(n, 0) for n in agent_scores) or 1))
    all_issues = [i for a in agents for i in a.issues]
    return AggregatedReport(
        overall_score=overall,
        strengths=[a.strengths[0] for a in agents if a.score >= 85][:5] or ["Solid overall academic quality"],
        major_concerns=[i.title for i in all_issues if i.severity in (IssueSeverity.HIGH, IssueSeverity.CRITICAL)][:5],
        minor_concerns=[i.title for i in all_issues if i.severity in (IssueSeverity.MEDIUM, IssueSeverity.LOW)][:6],
        priority_issues=all_issues[:10],
        recommended_actions=[r for a in agents for r in a.recommendations][:6],
        agent_scores=agent_scores,
    )


def _editorial_from_score(overall: int) -> EditorialDecision:
    if overall < 55:
        return EditorialDecision(
            decision=EditorialDecisionType.NOT_RECOMMENDED,
            headline="NOT RECOMMENDED FOR CURRENT REVIEW",
            message="Significant issues were identified during automated screening.",
            next_step="Return to author for major revision, or editor override.",
        )
    if overall < 78:
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


def _reviewer(entry_id: str, match: int, rec: int) -> Reviewer:
    e = next(r for r in REVIEWER_POOL if r["id"] == entry_id)
    return Reviewer(
        id=e["id"], name=e["name"], expertise=e["expertise"], domains=e["domains"],
        publications=e["publications"], workload=e["workload"], conflict_of_interest=e["coi"],
        match_score=match, recommendation_score=rec, bio=e["bio"],
    )


def _make_paper(
    *, id_num: int, title: str, authors: List[str], target_venue: str,
    status: PaperStatus, agent_scores: Dict[str, int], days_ago: float,
    domain_keywords: List[str], similarity: Optional[SimilarityResult] = None,
    reviewers: Optional[List[Reviewer]] = None, assigned_reviewer_id: Optional[str] = None,
    revision: int = 1,
) -> Paper:
    agents = _fabricate_agents(agent_scores)
    report = _report_from_agents(agents)
    editorial = _editorial_from_score(report.overall_score)

    return Paper(
        id=f"paper-{id_num:04d}",
        title=title,
        authors=authors,
        filename=f"{title.lower().replace(' ', '_')[:40]}.pdf",
        file_size=1_200_000 + id_num * 37_000,
        uploaded_at=_iso(days_ago),
        target_venue=target_venue,
        status=status,
        revision=revision,
        overall_score=report.overall_score,
        extracted=ExtractedContent(
            page_count=10 + (id_num % 5),
            word_count=4200 + id_num * 113,
            figure_count=3 + (id_num % 4),
            table_count=1 + (id_num % 3),
            equation_count=id_num % 5,
            reference_count=22 + (id_num % 15),
            title=title,
            authors=authors,
            abstract="",
            sections_found=["Abstract", "Introduction", "Related Work", "Methodology", "Results", "Conclusion", "References"],
            domain_keywords=domain_keywords,
        ),
        parsing_checklist=_completed_checklist(),
        agents=agents,
        report=report,
        editorial=editorial,
        similarity=similarity,
        reviewers=reviewers or [],
        assigned_reviewer_id=assigned_reviewer_id,
        analysis_progress=100,
    )


def seed_demo_data() -> None:
    if store.PAPERS:
        return  # already seeded (e.g. hot-reload)

    # --- Hero paper: the one used for the full live walkthrough -----------------
    from services import pdf_service

    hero_id = store.next_paper_id()
    store.RAW_BYTES[hero_id] = build_pdf()
    hero = Paper(
        id=hero_id,
        title=SAMPLE_TITLE,
        authors=[a.strip() for a in SAMPLE_AUTHORS.split(",")],
        filename="AI-Driven_Carbon_Emission_Prediction_Using_Multi-Agent_Systems.pdf",
        file_size=len(store.RAW_BYTES[hero_id]),
        uploaded_at=_iso(0.02),
        target_venue="International Conference on Artificial Intelligence",
        status=PaperStatus.UPLOADED,
        revision=1,
        parsing_checklist=pdf_service.default_parsing_checklist(),
        agents=[AgentReview(agent_name=n, status=AgentStatus.PENDING) for n in AGENT_NAMES],
    )
    store.save(hero)

    # --- Supporting demo papers at various pipeline stages -----------------------
    store.save(_make_paper(
        id_num=int(store.next_paper_id().split("-")[1]),
        title="Deep Reinforcement Learning for Adaptive Traffic Signal Control",
        authors=["N. Kapoor", "V. Rao"],
        target_venue="IEEE Intelligent Transportation Systems Conference",
        status=PaperStatus.READY_FOR_REVIEW,
        agent_scores={"Layout Agent": 90, "Structure Agent": 92, "Formatting Agent": 87,
                      "Language Agent": 89, "Citation Agent": 85, "Technical Agent": 88,
                      "Scope Matching Agent": 94},
        days_ago=1.4,
        domain_keywords=["Artificial Intelligence / Machine Learning"],
    ))

    store.save(_make_paper(
        id_num=int(store.next_paper_id().split("-")[1]),
        title="A Survey of Transformer Architectures in Computer Vision",
        authors=["T. Fernandes"],
        target_venue="International Conference on Artificial Intelligence",
        status=PaperStatus.REVISION_REQUIRED,
        agent_scores={"Layout Agent": 74, "Structure Agent": 68, "Formatting Agent": 71,
                      "Language Agent": 70, "Citation Agent": 55, "Technical Agent": 60,
                      "Scope Matching Agent": 82},
        days_ago=2.7,
        domain_keywords=["Computer Vision", "Artificial Intelligence / Machine Learning"],
    ))

    fed_reviewers = [_reviewer("rev-david-chen", 91, 88), _reviewer("rev-ananya-sharma", 76, 79)]
    store.save(_make_paper(
        id_num=int(store.next_paper_id().split("-")[1]),
        title="Federated Learning for Privacy-Preserving Healthcare Analytics",
        authors=["P. Desai", "L. Zhou", "M. Osei"],
        target_venue="International Conference on Machine Learning in Healthcare",
        status=PaperStatus.SIMILARITY_FLAGGED,
        agent_scores={"Layout Agent": 86, "Structure Agent": 88, "Formatting Agent": 84,
                      "Language Agent": 85, "Citation Agent": 80, "Technical Agent": 83,
                      "Scope Matching Agent": 90},
        days_ago=3.5,
        domain_keywords=["Bioinformatics / Healthcare", "Artificial Intelligence / Machine Learning"],
        similarity=SimilarityResult(
            overall_similarity=38, direct_matches=4, status=SimilarityStatus.HIGH,
            checked_at=_iso(3.4),
            potential_sources=[
                SimilaritySource(title="Prior Conference Proceedings Archive", source="conference-archive.example",
                                  similarity=34, matched_excerpt="Overlapping phrasing in methodology framing."),
                SimilaritySource(title="Related Journal Publication (2021)", source="journal-db.example",
                                  similarity=22, matched_excerpt="Similar dataset description."),
            ],
        ),
        reviewers=fed_reviewers,
    ))

    store.save(_make_paper(
        id_num=int(store.next_paper_id().split("-")[1]),
        title="Blockchain-Based Supply Chain Traceability System",
        authors=["R. Alvarez", "K. Nguyen"],
        target_venue="ACM Conference on Distributed Systems",
        status=PaperStatus.UNDER_HUMAN_REVIEW,
        agent_scores={"Layout Agent": 93, "Structure Agent": 91, "Formatting Agent": 90,
                      "Language Agent": 92, "Citation Agent": 88, "Technical Agent": 91,
                      "Scope Matching Agent": 89},
        days_ago=6.1,
        domain_keywords=["Networking / Systems"],
        similarity=SimilarityResult(overall_similarity=9, direct_matches=0, status=SimilarityStatus.ACCEPTABLE,
                                     checked_at=_iso(5.9), potential_sources=[]),
        reviewers=[_reviewer("rev-sara-iyer", 88, 90)],
        assigned_reviewer_id="rev-sara-iyer",
    ))

    store.save(_make_paper(
        id_num=int(store.next_paper_id().split("-")[1]),
        title="Lightweight CNN Architectures for Edge Devices",
        authors=["J. Kowalski"],
        target_venue="",
        status=PaperStatus.NOT_RECOMMENDED,
        agent_scores={"Layout Agent": 60, "Structure Agent": 52, "Formatting Agent": 58,
                      "Language Agent": 61, "Citation Agent": 40, "Technical Agent": 45,
                      "Scope Matching Agent": 66},
        days_ago=4.2,
        domain_keywords=["Computer Vision"],
    ))

    store.save(_make_paper(
        id_num=int(store.next_paper_id().split("-")[1]),
        title="Graph Neural Networks for Drug Discovery",
        authors=["A. Krishnan", "F. Bianchi"],
        target_venue="International Conference on Artificial Intelligence",
        status=PaperStatus.REVIEWER_ASSIGNMENT,
        agent_scores={"Layout Agent": 88, "Structure Agent": 90, "Formatting Agent": 85,
                      "Language Agent": 87, "Citation Agent": 84, "Technical Agent": 89,
                      "Scope Matching Agent": 86},
        days_ago=1.9,
        domain_keywords=["Bioinformatics / Healthcare", "Artificial Intelligence / Machine Learning"],
        similarity=SimilarityResult(overall_similarity=15, direct_matches=1, status=SimilarityStatus.ACCEPTABLE,
                                     checked_at=_iso(1.8), potential_sources=[
                                         SimilaritySource(title="Open Research Index", source="openresearch.example.org",
                                                           similarity=15, matched_excerpt="Shared background phrasing."),
                                     ]),
        reviewers=[_reviewer("rev-david-chen", 82, 85), _reviewer("rev-james-okoro", 74, 70)],
    ))
