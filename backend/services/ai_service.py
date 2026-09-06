"""
AIReviewService — the single seam where a real LLM can be plugged in per
agent without touching the pipeline that calls it.

Mode selection:
    - If ANTHROPIC_API_KEY is set in the environment, each agent call is
      attempted against the Claude API first; any failure (network, bad
      JSON, rate limit, timeout) falls back to the offline heuristic mock
      so the demo never breaks mid-presentation.
    - Otherwise, every agent runs in fully offline "Demo / Mock AI mode"
      as required by the spec (section 19) — grounded in the *real*
      extracted PDF statistics, just scored/explained heuristically
      instead of via an LLM.
"""
from __future__ import annotations

import json
import os
import re
from typing import Optional

from agents.base import BaseAgent
from schemas import AgentReview, AgentStatus, ExtractedContent, ReviewIssue

MODEL_NAME = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")


class AIReviewService:
    def __init__(self) -> None:
        self.api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        self.use_real_ai = bool(self.api_key)
        self._client = None
        if self.use_real_ai:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except Exception:
                self.use_real_ai = False
                self._client = None

    @property
    def mode(self) -> str:
        return "real" if self.use_real_ai else "demo"

    async def run_agent(
        self,
        agent: BaseAgent,
        paper_id: str,
        content: ExtractedContent,
        target_venue: Optional[str],
        full_text: str = "",
    ) -> AgentReview:
        if self.use_real_ai:
            try:
                review = await self._run_real(agent, content, target_venue)
                if review is not None:
                    return review
            except Exception:
                pass  # fall through to mock — never let the demo fail
        return agent.run_mock(paper_id, content, target_venue, full_text)

    async def _run_real(self, agent: BaseAgent, content: ExtractedContent, target_venue: Optional[str]):
        prompt = agent.build_prompt(content, target_venue)
        message = self._client.messages.create(
            model=MODEL_NAME,
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in message.content if getattr(block, "type", "") == "text")
        data = _extract_json(text)
        if not data:
            return None

        issues = [
            ReviewIssue(
                severity=item.get("severity", "medium"),
                title=item.get("title", "Issue"),
                description=item.get("description", ""),
                source_agent=agent.name,
            )
            for item in data.get("issues", [])
        ]

        return AgentReview(
            agent_name=agent.name,
            score=max(0, min(100, int(data.get("score", 70)))),
            status=AgentStatus.COMPLETED,
            summary=f"{agent.name.replace(' Agent', '')} Score: {int(data.get('score', 70))}/100",
            strengths=data.get("strengths", []),
            issues=issues,
            recommendations=data.get("recommendations", []),
            ai_generated=True,
        )


def _extract_json(text: str) -> Optional[dict]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


ai_review_service = AIReviewService()
