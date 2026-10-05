from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import List, Literal, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from agents import ALL_AGENTS
from models import store
from schemas import (
    AgentReview, AgentStatus, DashboardStats, Paper, PaperStatus, PaperSummary,
    Reviewer, SimilarityStatus, SystemStatus, Workload,
)
from services import pdf_service, pipeline_service, reviewer_service, similarity_service
from services.ai_service import MODEL_NAME, ai_review_service

router = APIRouter(prefix="/api", tags=["papers"])

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB


def _get_or_404(paper_id: str) -> Paper:
    paper = store.get(paper_id)
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found.")
    return paper


def _fresh_agent_list() -> List[AgentReview]:
    return [AgentReview(agent_name=a.name, status=AgentStatus.PENDING) for a in ALL_AGENTS]


def _with_timeline(paper: Paper) -> Paper:
    paper.timeline = pipeline_service.compute_timeline(paper)
    return paper


# --------------------------------------------------------------------------
# Upload & lifecycle
# --------------------------------------------------------------------------

@router.post("/papers/upload", response_model=Paper)
async def upload_paper(file: UploadFile = File(...), target_venue: Optional[str] = Form(None)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid File. Please upload a PDF research paper.")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Invalid File. The uploaded PDF appears to be empty.")
    if len(raw) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Please upload a PDF under 25MB.")

    paper_id = store.next_paper_id()
    store.RAW_BYTES[paper_id] = raw

    paper = Paper(
        id=paper_id,
        title=file.filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").strip() or "Untitled Paper",
        authors=[],
        filename=file.filename,
        file_size=len(raw),
        uploaded_at=datetime.now(timezone.utc).isoformat(),
        target_venue=(target_venue or "").strip() or None,
        status=PaperStatus.UPLOADED,
        revision=1,
        parsing_checklist=pdf_service.default_parsing_checklist(),
        agents=_fresh_agent_list(),
    )
    store.save(paper)
    return _with_timeline(paper)


@router.post("/papers/{paper_id}/analyze", response_model=Paper)
async def analyze_paper(paper_id: str):
    paper = _get_or_404(paper_id)
    if paper.status not in (PaperStatus.UPLOADED, PaperStatus.ANALYSIS_FAILED):
        raise HTTPException(status_code=409, detail="Analysis has already been started for this paper.")

    paper.status = PaperStatus.UPLOADED
    paper.parsing_checklist = pdf_service.default_parsing_checklist()
    paper.agents = _fresh_agent_list()
    paper.report = None
    paper.editorial = None
    paper.similarity = None
    paper.analysis_progress = 0
    paper.error = None
    store.save(paper)

    pipeline_service.spawn_background(pipeline_service.run_analysis_pipeline(paper_id))
    return _with_timeline(paper)


@router.get("/papers", response_model=List[PaperSummary])
async def list_papers():
    return [store.to_summary(p) for p in store.all_papers()]


@router.get("/papers/{paper_id}", response_model=Paper)
async def get_paper(paper_id: str):
    return _with_timeline(_get_or_404(paper_id))


@router.get("/papers/{paper_id}/agents", response_model=List[AgentReview])
async def get_paper_agents(paper_id: str):
    return _get_or_404(paper_id).agents


@router.get("/papers/{paper_id}/report")
async def get_paper_report(paper_id: str):
    paper = _get_or_404(paper_id)
    if paper.report is None:
        raise HTTPException(status_code=404, detail="The unified review report is not yet available.")
    return {"report": paper.report, "editorial": paper.editorial}


@router.get("/papers/{paper_id}/report/download", response_class=PlainTextResponse)
async def download_report(paper_id: str):
    paper = _get_or_404(paper_id)
    if paper.report is None:
        raise HTTPException(status_code=404, detail="The unified review report is not yet available.")

    r, e = paper.report, paper.editorial
    lines = [
        f"AI-ASSISTED REVIEW REPORT (Revision {paper.revision})",
        f"Paper: {paper.title}",
        f"Authors: {', '.join(paper.authors) or 'Unknown'}",
        f"Target Venue: {paper.target_venue or 'Not specified'}",
        "",
        f"OVERALL AI REVIEW SCORE: {r.overall_score}/100",
        f"EDITORIAL RECOMMENDATION: {e.headline if e else 'Pending'}",
        "",
        "-- Agent Scores --",
        *[f"  {name}: {score}/100" for name, score in r.agent_scores.items()],
        "",
        "-- Strengths --",
        *[f"  + {s}" for s in r.strengths],
        "",
        "-- Major Concerns --",
        *([f"  ! {s}" for s in r.major_concerns] or ["  (none)"]),
        "",
        "-- Minor Concerns --",
        *([f"  - {s}" for s in r.minor_concerns] or ["  (none)"]),
        "",
        "-- Recommended Actions --",
        *[f"  * {s}" for s in r.recommended_actions],
        "",
        "NOTE: This is an AI-assisted screening report. Final publication and",
        "peer-review decisions are made by qualified human reviewers/editors.",
    ]
    content = "\n".join(lines)
    filename = f"{paper.id}-review-report.txt"
    return PlainTextResponse(content, headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@router.post("/papers/{paper_id}/resubmit", response_model=Paper)
async def resubmit_paper(paper_id: str, file: Optional[UploadFile] = File(None)):
    old = _get_or_404(paper_id)
    if old.status not in (PaperStatus.REVISION_REQUIRED, PaperStatus.NOT_RECOMMENDED):
        raise HTTPException(status_code=400, detail="Only papers marked for revision can be resubmitted.")

    if file is not None and file.filename:
        raw = await file.read()
        filename = file.filename
    else:
        raw = store.RAW_BYTES.get(paper_id)
        filename = old.filename
        if raw is None:
            raise HTTPException(
                status_code=400,
                detail="Original file is no longer available; please upload the revised PDF.",
            )

    new_id = store.next_paper_id()
    store.RAW_BYTES[new_id] = raw

    new_paper = Paper(
        id=new_id,
        title=old.title,
        authors=old.authors,
        filename=filename,
        file_size=len(raw),
        uploaded_at=datetime.now(timezone.utc).isoformat(),
        target_venue=old.target_venue,
        status=PaperStatus.UPLOADED,
        revision=old.revision + 1,
        parsing_checklist=pdf_service.default_parsing_checklist(),
        agents=_fresh_agent_list(),
    )
    store.save(new_paper)
    return _with_timeline(new_paper)


# --------------------------------------------------------------------------
# Similarity
# --------------------------------------------------------------------------

class ResolveSimilarityRequest(BaseModel):
    action: Literal["proceed", "return_to_author"]


@router.post("/papers/{paper_id}/similarity", response_model=Paper)
async def run_similarity(paper_id: str):
    paper = _get_or_404(paper_id)
    if paper.report is None:
        raise HTTPException(status_code=400, detail="Run the AI analysis before checking similarity.")

    await asyncio.sleep(1.2)
    domain_keywords = paper.extracted.domain_keywords if paper.extracted else []
    result = similarity_service.run_similarity_check(paper_id, paper.title, domain_keywords)
    paper.similarity = result
    paper.status = (
        PaperStatus.SIMILARITY_FLAGGED if result.status == SimilarityStatus.HIGH
        else PaperStatus.REVIEWER_ASSIGNMENT
    )
    store.save(paper)
    return _with_timeline(paper)


@router.post("/papers/{paper_id}/similarity/resolve", response_model=Paper)
async def resolve_similarity(paper_id: str, body: ResolveSimilarityRequest):
    paper = _get_or_404(paper_id)
    if paper.status != PaperStatus.SIMILARITY_FLAGGED:
        raise HTTPException(status_code=400, detail="No flagged similarity case to resolve for this paper.")

    if body.action == "proceed":
        paper.status = PaperStatus.REVIEWER_ASSIGNMENT
    else:
        paper.status = PaperStatus.REVISION_REQUIRED
    store.save(paper)
    return _with_timeline(paper)


# --------------------------------------------------------------------------
# Reviewer assignment
# --------------------------------------------------------------------------

class AssignReviewerRequest(BaseModel):
    reviewer_id: str


@router.get("/papers/{paper_id}/reviewers", response_model=List[Reviewer])
async def get_recommended_reviewers(paper_id: str):
    paper = _get_or_404(paper_id)
    domain_keywords = paper.extracted.domain_keywords if paper.extracted else []
    reviewers = reviewer_service.recommend_reviewers(paper_id, domain_keywords, paper.target_venue)
    paper.reviewers = reviewers
    store.save(paper)
    return reviewers


@router.post("/papers/{paper_id}/assign-reviewer", response_model=Paper)
async def assign_reviewer(paper_id: str, body: AssignReviewerRequest):
    paper = _get_or_404(paper_id)
    reviewer = next((r for r in paper.reviewers if r.id == body.reviewer_id), None)
    if reviewer is None:
        domain_keywords = paper.extracted.domain_keywords if paper.extracted else []
        paper.reviewers = reviewer_service.recommend_reviewers(paper_id, domain_keywords, paper.target_venue)
        reviewer = next((r for r in paper.reviewers if r.id == body.reviewer_id), None)
    if reviewer is None:
        raise HTTPException(status_code=404, detail="Reviewer not found among recommendations.")

    paper.assigned_reviewer_id = reviewer.id
    paper.status = PaperStatus.UNDER_HUMAN_REVIEW
    store.save(paper)
    return _with_timeline(paper)


# --------------------------------------------------------------------------
# Directory / dashboard / system
# --------------------------------------------------------------------------

# @router.get("/reviewers", response_model=List[Reviewer])
# async def reviewer_directory():
#     return [
#         Reviewer(
#             id=entry["id"], name=entry["name"], expertise=entry["expertise"],
#             domains=entry["domains"], publications=entry["publications"],
#             workload=entry["workload"], conflict_of_interest=entry["coi"],
#             match_score=0, recommendation_score=0, bio=entry["bio"],
#         )
#         for entry in reviewer_service.REVIEWER_POOL
#     ]

@router.get("/reviewers", response_model=List[Reviewer])
async def reviewer_directory():
    return [
        Reviewer(
            id=entry["id"],
            name=entry["name"],
            expertise=entry["expertise"],
            domains=entry["domains"],
            publications=entry["publications"],
            workload=entry["workload"],
            conflict_of_interest=entry["coi"],
            match_score=0,
            recommendation_score=0,
            bio=entry["bio"],
        )
        # for entry in reviewer_service.get_reviewer_pool()
        for entry in reviewer_service.get_all_reviewers()
    ]


@router.get("/dashboard/stats", response_model=DashboardStats)
async def dashboard_stats():
    return store.dashboard_stats()


@router.get("/system/status", response_model=SystemStatus)
async def system_status():
    mode = ai_review_service.mode
    return SystemStatus(
        ai_engine_mode=mode,
        model=MODEL_NAME if mode == "real" else None,
        similarity_threshold=similarity_service.SIMILARITY_THRESHOLD,
        message=(
            "All AI analysis results are simulated for prototype demonstration."
            if mode == "demo"
            else "Connected to a live Claude model for AI-generated review findings."
        ),
    )
