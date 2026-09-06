"""Plagiarism / Similarity Detection (demo).

Important: this module intentionally never claims to definitively detect
plagiarism. It reports "similarity", "potential overlap" and "sources
requiring inspection" only, per the product's responsible-AI requirement.
"""
from __future__ import annotations

import random
from typing import List, Optional

from schemas import SimilarityResult, SimilarityStatus, SimilaritySource

SIMILARITY_THRESHOLD = 30  # percent; above this is flagged HIGH

_FAKE_SOURCE_POOL = [
    ("Prior Conference Proceedings Archive", "conference-archive.example"),
    ("Institutional Preprint Repository", "preprints.example.edu"),
    ("Open Research Index", "openresearch.example.org"),
    ("Related Journal Publication (2021)", "journal-db.example"),
    ("Public Thesis Repository", "theses.example.edu"),
    ("Cross-referenced Workshop Paper", "workshop-papers.example"),
]


def run_similarity_check(paper_id: str, title: str, domain_keywords: List[str]) -> SimilarityResult:
    rng = random.Random(f"similarity:{paper_id}")
    overall = rng.randint(3, 45)

    sources: List[SimilaritySource] = []
    num_sources = 0
    if overall > 8:
        num_sources = rng.randint(1, 5)
        pool = _FAKE_SOURCE_POOL[:]
        rng.shuffle(pool)
        for i in range(num_sources):
            name, domain = pool[i % len(pool)]
            sim = max(2, overall - rng.randint(0, 20) + rng.randint(-5, 5))
            sources.append(SimilaritySource(
                title=f"{name}",
                source=domain,
                similarity=max(2, min(overall + 5, sim)),
                matched_excerpt="Overlapping phrasing detected in methodology / related-work framing.",
            ))
        sources.sort(key=lambda s: -s.similarity)

    direct_matches = sum(1 for s in sources if s.similarity >= 15)
    status = SimilarityStatus.HIGH if overall > SIMILARITY_THRESHOLD else SimilarityStatus.ACCEPTABLE

    from datetime import datetime, timezone
    return SimilarityResult(
        overall_similarity=overall,
        direct_matches=direct_matches,
        potential_sources=sources,
        status=status,
        checked_at=datetime.now(timezone.utc).isoformat(),
    )
