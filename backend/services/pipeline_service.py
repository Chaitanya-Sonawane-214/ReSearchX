"""Orchestrates the full paper lifecycle pipeline:

    Upload -> PDF Parsing -> 7 AI Agents -> Aggregation -> Editorial Decision
    -> (Revision | Ready for Review) -> Similarity -> Reviewer Assignment
    -> Human Peer Review

Runs as an asyncio background task so the frontend can poll GET /papers/{id}
and watch each stage animate in, per spec section 24 ("simulated delays ...
to make the AI workflow visually understandable").
"""
from __future__ import annotations

import asyncio
import random
from datetime import datetime, timezone
from typing import List, Optional

from agents import ALL_AGENTS
from models import store
from schemas import (
    AgentStatus, EditorialDecisionType, Paper, PaperStatus, TimelineStep,
)
from services import pdf_service
from services.ai_service import ai_review_service
from services.aggregation_service import aggregate, decide

PARSING_DELAYS = dict(text=0.35, figures=0.25, tables=0.25, equations=0.25, references=0.3, metadata=0.3)

_SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

_background_tasks: set = set()


def spawn_background(coro) -> None:
    """Fire-and-forget an asyncio coroutine while keeping a strong reference
    to the Task so it can't be garbage-collected mid-run."""
    task = asyncio.create_task(coro)
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def run_analysis_pipeline(paper_id: str) -> None:
    paper = store.get(paper_id)
    if paper is None:
        return

    try:
        paper.status = PaperStatus.PARSING
        paper.error = None
        paper.analysis_progress = 5
        store.save(paper)

        raw_bytes = store.RAW_BYTES.get(paper_id)
        if raw_bytes is None:
            raise RuntimeError("Original PDF bytes not found for parsing.")

        content, full_text = await asyncio.to_thread(pdf_service.parse_pdf, raw_bytes)
        store.FULL_TEXT[paper_id] = full_text
        paper.extracted = content
        if content.title and content.title != "Untitled Paper":
            paper.title = content.title
        if content.authors:
            paper.authors = content.authors

        checklist = {item.key: item for item in paper.parsing_checklist}
        details = {
            "text": f"{content.word_count} words extracted",
            "figures": f"{content.figure_count} figures",
            "tables": f"{content.table_count} tables",
            "equations": f"{content.equation_count} equations",
            "references": f"{content.reference_count} references",
            "metadata": "Title, authors & sections identified",
        }
        for key, delay in PARSING_DELAYS.items():
            await asyncio.sleep(delay)
            item = checklist[key]
            item.status = AgentStatus.COMPLETED
            item.detail = details[key]
            paper.analysis_progress = min(35, paper.analysis_progress + 5)
            store.save(paper)

        # --- Multi-agent review layer -------------------------------------------------
        paper.status = PaperStatus.ANALYZING
        store.save(paper)

        for review in paper.agents:
            review.status = AgentStatus.RUNNING
            review.started_at = _now()
        store.save(paper)

        async def run_one(agent):
            await asyncio.sleep(random.uniform(1.4, 3.2))
            result = await ai_review_service.run_agent(
                agent, paper_id, content, paper.target_venue, full_text,
            )
            result.started_at = _now()
            result.completed_at = _now()
            return result

        results = await asyncio.gather(*(run_one(agent) for agent in ALL_AGENTS))

        if paper.revision > 1:
            # Spec section 10: "it is acceptable to simulate a revised paper
            # and show an improved score" — reward each resubmission by
            # resolving its single worst issue and nudging the score up.
            boost = min(15, 5 * (paper.revision - 1))
            for r in results:
                if r.issues:
                    r.issues.sort(key=lambda i: _SEVERITY_ORDER.get(i.severity.value, 9))
                    r.issues = r.issues[1:]
                r.score = min(98, r.score + boost)
                r.summary = f"{r.agent_name.replace(' Agent', '')} Score: {r.score}/100"

        paper.agents = list(results)
        paper.analysis_progress = 75
        store.save(paper)

        # --- Report Aggregation Agent ---------------------------------------------------
        paper.status = PaperStatus.AGGREGATING
        store.save(paper)
        await asyncio.sleep(1.4)

        report = aggregate(paper.agents)
        paper.report = report
        paper.overall_score = report.overall_score
        paper.analysis_progress = 92

        # --- Editorial Decision Agent -----------------------------------------------------
        editorial = decide(report)
        paper.editorial = editorial
        if editorial.decision == EditorialDecisionType.READY_FOR_REVIEW:
            paper.status = PaperStatus.READY_FOR_REVIEW
        elif editorial.decision == EditorialDecisionType.REVISION_REQUIRED:
            paper.status = PaperStatus.REVISION_REQUIRED
        else:
            paper.status = PaperStatus.NOT_RECOMMENDED
        paper.analysis_progress = 100
        store.save(paper)

    except Exception as exc:  # pragma: no cover - defensive: keep demo alive
        paper.status = PaperStatus.ANALYSIS_FAILED
        paper.error = str(exc)
        store.save(paper)


def compute_timeline(paper: Paper) -> List[TimelineStep]:
    def step(key, label, done, current=False):
        return TimelineStep(
            key=key, label=label,
            status="current" if current else ("done" if done else "pending"),
        )

    parsed = paper.extracted is not None
    reviewed = bool(paper.agents) and all(a.status == AgentStatus.COMPLETED for a in paper.agents)
    reported = paper.report is not None
    screened = paper.editorial is not None
    similarity_done = paper.similarity is not None
    reviewer_assigned = paper.assigned_reviewer_id is not None
    human_review_started = paper.status == PaperStatus.UNDER_HUMAN_REVIEW

    return [
        step("uploaded", "Paper Uploaded", True),
        step("parsed", "PDF Parsed", parsed, current=paper.status == PaperStatus.PARSING),
        step("ai_review", "AI Review", reviewed, current=paper.status == PaperStatus.ANALYZING),
        step("report", "Report Generated", reported, current=paper.status == PaperStatus.AGGREGATING),
        step("editorial", "Editorial Screening", screened),
        step("similarity", "Similarity Check", similarity_done, current=paper.status == PaperStatus.SIMILARITY_CHECK),
        step("reviewer", "Reviewer Assigned", reviewer_assigned, current=paper.status == PaperStatus.REVIEWER_ASSIGNMENT),
        # Human review is never marked "done" in this prototype — it's the final,
        # ongoing stage that stays outside AI's control (spec section 13).
        step("human_review", "Human Review", False, current=human_review_started),
    ]
