"""In-memory data store for the prototype (spec section 17: "local mock
JSON/state, no production database required"). All state lives in this
single process, which is why the backend must run as a single worker
(see main.py / run instructions) — polling endpoints rely on shared memory.
"""
from __future__ import annotations

import itertools
from typing import Dict, List, Optional

from schemas import Paper, PaperStatus, PaperSummary, DashboardStats

PAPERS: Dict[str, Paper] = {}
FULL_TEXT: Dict[str, str] = {}  # paper_id -> extracted plain text (internal only)
RAW_BYTES: Dict[str, bytes] = {}  # paper_id -> original uploaded PDF bytes, pending parse

_id_counter = itertools.count(1)


def next_paper_id() -> str:
    return f"paper-{next(_id_counter):04d}"


def save(paper: Paper) -> None:
    PAPERS[paper.id] = paper


def get(paper_id: str) -> Optional[Paper]:
    return PAPERS.get(paper_id)


def all_papers() -> List[Paper]:
    return sorted(PAPERS.values(), key=lambda p: p.uploaded_at, reverse=True)


def to_summary(paper: Paper) -> PaperSummary:
    return PaperSummary(
        id=paper.id,
        title=paper.title,
        authors=paper.authors,
        status=paper.status,
        overall_score=paper.overall_score,
        uploaded_at=paper.uploaded_at,
        target_venue=paper.target_venue,
        revision=paper.revision,
    )


_ANALYSIS_COMPLETE_STATES = {
    PaperStatus.REVISION_REQUIRED, PaperStatus.READY_FOR_REVIEW, PaperStatus.NOT_RECOMMENDED,
    PaperStatus.SIMILARITY_CHECK, PaperStatus.SIMILARITY_FLAGGED,
    PaperStatus.REVIEWER_ASSIGNMENT, PaperStatus.UNDER_HUMAN_REVIEW,
}


def dashboard_stats() -> DashboardStats:
    papers = all_papers()
    breakdown: Dict[str, int] = {}
    for p in papers:
        breakdown[p.status.value] = breakdown.get(p.status.value, 0) + 1

    return DashboardStats(
        total_papers=len(papers),
        ai_reviews_completed=sum(1 for p in papers if p.status in _ANALYSIS_COMPLETE_STATES),
        revision_required=sum(1 for p in papers if p.status == PaperStatus.REVISION_REQUIRED),
        ready_for_review=sum(1 for p in papers if p.status in (
            PaperStatus.READY_FOR_REVIEW, PaperStatus.SIMILARITY_CHECK,
            PaperStatus.REVIEWER_ASSIGNMENT,
        )),
        similarity_alerts=sum(1 for p in papers if p.status == PaperStatus.SIMILARITY_FLAGGED),
        under_human_review=sum(1 for p in papers if p.status == PaperStatus.UNDER_HUMAN_REVIEW),
        status_breakdown=breakdown,
    )
