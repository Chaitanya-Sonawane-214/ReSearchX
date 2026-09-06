"""
Shared agent interface.

Every specialized review agent implements `run_mock()` (deterministic,
heuristic, offline analysis over the parsed PDF content) and exposes a
`build_prompt()` used only when real AI mode is enabled
(see services/ai_service.py). This keeps the abstraction from the spec:

    AIReviewService
        ├── layoutAgent()
        ├── structureAgent()
        ├── formattingAgent()
        ├── languageAgent()
        ├── citationAgent()
        ├── technicalAgent()
        └── scopeMatchingAgent()

so a real LLM can be dropped in per-agent without touching the pipeline.
"""
from __future__ import annotations

import random
from typing import List, Optional

from schemas import AgentReview, AgentStatus, ExtractedContent, ReviewIssue, IssueSeverity


class BaseAgent:
    name: str = "Base Agent"

    def rng(self, paper_id: str) -> random.Random:
        # Deterministic per (paper, agent) so re-viewing a paper is stable,
        # but a resubmitted revision (new paper_id suffix) yields fresh results.
        return random.Random(f"{paper_id}:{self.name}")

    def run_mock(
        self,
        paper_id: str,
        content: ExtractedContent,
        target_venue: Optional[str],
        full_text: str = "",
    ) -> AgentReview:
        raise NotImplementedError

    def build_prompt(self, content: ExtractedContent, target_venue: Optional[str]) -> str:
        raise NotImplementedError

    @staticmethod
    def issue(severity: IssueSeverity, title: str, description: str, source_agent: str) -> ReviewIssue:
        return ReviewIssue(severity=severity, title=title, description=description, source_agent=source_agent)

    @staticmethod
    def clamp(score: int) -> int:
        return max(0, min(100, score))
