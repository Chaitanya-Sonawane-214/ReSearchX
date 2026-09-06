from __future__ import annotations
import re
from typing import Optional

from schemas import AgentReview, AgentStatus, ExtractedContent, IssueSeverity
from .base import BaseAgent

_WORD_RE = re.compile(r"[A-Za-z']+")
_FILLER_PHRASES = ["in order to", "due to the fact that", "a large number of", "it should be noted that"]


def _split_sentences(text: str):
    # Lightweight sentence splitter; good enough for heuristic scoring, no NLP deps.
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


class LanguageAgent(BaseAgent):
    """Evaluates writing quality: grammar signals, sentence construction,
    clarity, academic tone, repetition — via lightweight text statistics
    (no external NLP dependency, so it always works offline)."""

    name = "Language Agent"

    def run_mock(self, paper_id: str, content: ExtractedContent, target_venue: Optional[str], full_text: str = "") -> AgentReview:
        rng = self.rng(paper_id)
        text = full_text or content.abstract
        sentences = _split_sentences(text)[:400]  # cap for performance

        score = 82
        strengths = []
        issues = []
        recommendations = []

        long_sentences = [s for s in sentences if len(_WORD_RE.findall(s)) > 32]
        long_ratio = len(long_sentences) / max(len(sentences), 1)

        if long_ratio > 0.2:
            issues.append(self.issue(
                IssueSeverity.MEDIUM,
                "Overly complex sentences",
                f"{len(long_sentences)} sentences exceed 32 words, which can hurt readability.",
                self.name,
            ))
            recommendations.append("Break long sentences into shorter, single-idea sentences.")
            score -= 8
        else:
            strengths.append("Sentence length is generally reader-friendly")

        words = [w.lower() for w in _WORD_RE.findall(text)]
        if words:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.35:
                issues.append(self.issue(
                    IssueSeverity.LOW,
                    "Repetitive vocabulary",
                    "Vocabulary diversity is lower than typical for academic writing; some phrases repeat often.",
                    self.name,
                ))
                score -= 4
            else:
                strengths.append("Vocabulary is varied and reads with professional academic tone")

        filler_hits = sum(text.lower().count(p) for p in _FILLER_PHRASES)
        if filler_hits >= 3:
            issues.append(self.issue(
                IssueSeverity.LOW,
                "Wordy filler phrases",
                f"Detected {filler_hits} instances of filler phrasing (e.g. 'in order to', 'due to the fact that').",
                self.name,
            ))
            recommendations.append("Replace filler phrases with direct wording (e.g. 'to' instead of 'in order to').")
            score -= 3

        if content.word_count < 1500:
            issues.append(self.issue(
                IssueSeverity.LOW,
                "Brief overall length",
                "Total word count is on the shorter side for a full research submission.",
                self.name,
            ))

        score = self.clamp(score + rng.randint(-4, 6))
        if not strengths:
            strengths.append("Writing maintains a consistent academic register")

        return AgentReview(
            agent_name=self.name,
            score=score,
            status=AgentStatus.COMPLETED,
            summary=f"Language Score: {score}/100",
            strengths=strengths,
            issues=issues,
            recommendations=recommendations or ["Minor grammar pass recommended before submission."],
        )

    def build_prompt(self, content: ExtractedContent, target_venue: Optional[str]) -> str:
        return (
            "You are the Language Agent. Evaluate grammar, clarity, sentence construction, "
            f"academic tone and repetition for a paper with abstract: \"{content.abstract[:600]}\". "
            "Return strict JSON with score, strengths, issues, recommendations."
        )
