"""
Pydantic schemas shared across the API.

These mirror the TypeScript interfaces in the product spec (README section 21)
plus the extra fields needed to drive the pipeline / UI animations.
"""
from __future__ import annotations

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


# --------------------------------------------------------------------------
# Enums
# --------------------------------------------------------------------------

class PaperStatus(str, Enum):
    UPLOADED = "uploaded"                       # file received, not yet analyzed
    PARSING = "parsing"                         # PDF parsing in progress
    ANALYZING = "analyzing"                     # 7 agents running
    AGGREGATING = "aggregating"                 # report aggregation agent running
    REVISION_REQUIRED = "revision_required"
    READY_FOR_REVIEW = "ready_for_review"
    NOT_RECOMMENDED = "not_recommended"
    SIMILARITY_CHECK = "similarity_check"
    SIMILARITY_FLAGGED = "similarity_flagged"
    REVIEWER_ASSIGNMENT = "reviewer_assignment"
    UNDER_HUMAN_REVIEW = "under_human_review"
    ANALYSIS_FAILED = "analysis_failed"


class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class IssueSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SimilarityStatus(str, Enum):
    ACCEPTABLE = "acceptable"
    HIGH = "high"


class Workload(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EditorialDecisionType(str, Enum):
    READY_FOR_REVIEW = "ready_for_review"
    REVISION_REQUIRED = "revision_required"
    NOT_RECOMMENDED = "not_recommended"


AGENT_NAMES = [
    "Layout Agent",
    "Structure Agent",
    "Formatting Agent",
    "Language Agent",
    "Citation Agent",
    "Technical Agent",
    "Scope Matching Agent",
]


# --------------------------------------------------------------------------
# Core models
# --------------------------------------------------------------------------

class ReviewIssue(BaseModel):
    severity: IssueSeverity
    title: str
    description: str
    source_agent: str = ""


class AgentReview(BaseModel):
    agent_name: str
    score: int = 0
    status: AgentStatus = AgentStatus.PENDING
    summary: str = ""
    strengths: List[str] = Field(default_factory=list)
    issues: List[ReviewIssue] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    ai_generated: bool = False  # true if produced by a real LLM call vs heuristic mock


class ParsingChecklistItem(BaseModel):
    key: str
    label: str
    status: AgentStatus = AgentStatus.PENDING
    detail: str = ""


class ExtractedContent(BaseModel):
    page_count: int = 0
    word_count: int = 0
    figure_count: int = 0
    table_count: int = 0
    equation_count: int = 0
    reference_count: int = 0
    title: str = ""
    authors: List[str] = Field(default_factory=list)
    abstract: str = ""
    sections_found: List[str] = Field(default_factory=list)
    domain_keywords: List[str] = Field(default_factory=list)


class AggregatedReport(BaseModel):
    overall_score: int = 0
    strengths: List[str] = Field(default_factory=list)
    major_concerns: List[str] = Field(default_factory=list)
    minor_concerns: List[str] = Field(default_factory=list)
    priority_issues: List[ReviewIssue] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    agent_scores: dict[str, int] = Field(default_factory=dict)


class EditorialDecision(BaseModel):
    decision: Optional[EditorialDecisionType] = None
    headline: str = ""
    message: str = ""
    next_step: str = ""


class SimilaritySource(BaseModel):
    title: str
    source: str
    similarity: int
    matched_excerpt: str = ""


class SimilarityResult(BaseModel):
    overall_similarity: int = 0
    direct_matches: int = 0
    potential_sources: List[SimilaritySource] = Field(default_factory=list)
    status: Optional[SimilarityStatus] = None
    checked_at: Optional[str] = None


class Reviewer(BaseModel):
    id: str
    name: str
    expertise: List[str]
    domains: List[str]
    publications: int
    workload: Workload
    conflict_of_interest: bool = False
    match_score: int = 0
    recommendation_score: int = 0
    bio: str = ""


class TimelineStep(BaseModel):
    key: str
    label: str
    status: str  # "done" | "current" | "pending"
    timestamp: Optional[str] = None


class Paper(BaseModel):
    id: str
    title: str
    authors: List[str] = Field(default_factory=list)
    filename: str
    file_size: int
    uploaded_at: str
    target_venue: Optional[str] = None
    status: PaperStatus = PaperStatus.UPLOADED
    revision: int = 1
    overall_score: Optional[int] = None

    extracted: Optional[ExtractedContent] = None
    parsing_checklist: List[ParsingChecklistItem] = Field(default_factory=list)
    agents: List[AgentReview] = Field(default_factory=list)
    report: Optional[AggregatedReport] = None
    editorial: Optional[EditorialDecision] = None
    similarity: Optional[SimilarityResult] = None
    assigned_reviewer_id: Optional[str] = None
    reviewers: List[Reviewer] = Field(default_factory=list)
    timeline: List[TimelineStep] = Field(default_factory=list)
    error: Optional[str] = None
    analysis_progress: int = 0  # 0-100, coarse progress for the pipeline page


class PaperSummary(BaseModel):
    """Lightweight shape for list views (Dashboard / Papers table)."""
    id: str
    title: str
    authors: List[str]
    status: PaperStatus
    overall_score: Optional[int] = None
    uploaded_at: str
    target_venue: Optional[str] = None
    revision: int = 1


class DashboardStats(BaseModel):
    total_papers: int
    ai_reviews_completed: int
    revision_required: int
    ready_for_review: int
    similarity_alerts: int
    under_human_review: int
    status_breakdown: dict[str, int]


class SystemStatus(BaseModel):
    ai_engine_mode: str  # "demo" | "real"
    model: Optional[str] = None
    similarity_threshold: int
    message: str
