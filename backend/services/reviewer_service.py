"""Human Reviewer Assignment (AI-suggested — the editor retains final control)."""
from __future__ import annotations

import random
from typing import List, Optional

from schemas import Reviewer, Workload

REVIEWER_POOL: List[dict] = [
    dict(id="rev-ananya-sharma", name="Dr. Ananya Sharma",
         expertise=["Machine Learning", "Deep Learning", "NLP"],
         domains=["Artificial Intelligence / Machine Learning", "Natural Language Processing"],
         publications=47, workload=Workload.LOW, coi=False,
         bio="Associate Professor of Computer Science focusing on representation learning and NLP."),
    dict(id="rev-rahul-mehta", name="Dr. Rahul Mehta",
         expertise=["Computer Vision", "Deep Learning", "Multi-Agent Systems"],
         domains=["Artificial Intelligence / Machine Learning", "Computer Vision"],
         publications=38, workload=Workload.MEDIUM, coi=False,
         bio="Research scientist specializing in vision architectures and multi-agent coordination."),
    dict(id="rev-sara-iyer", name="Dr. Sara Iyer",
         expertise=["Distributed Systems", "Cloud Computing", "Networking"],
         domains=["Networking / Systems"],
         publications=29, workload=Workload.LOW, coi=False,
         bio="Systems researcher with a focus on distributed and edge computing architectures."),
    dict(id="rev-david-chen", name="Dr. David Chen",
         expertise=["Bioinformatics", "Clinical ML", "Healthcare Analytics"],
         domains=["Bioinformatics / Healthcare"],
         publications=52, workload=Workload.HIGH, coi=False,
         bio="Faculty researcher applying machine learning to clinical and genomic datasets."),
    dict(id="rev-meera-nair", name="Dr. Meera Nair",
         expertise=["Robotics", "Control Systems", "Sensor Fusion"],
         domains=["Robotics"],
         publications=24, workload=Workload.MEDIUM, coi=False,
         bio="Robotics lab lead working on autonomous navigation and sensor fusion."),
    dict(id="rev-omar-farouk", name="Dr. Omar Farouk",
         expertise=["Cybersecurity", "Applied Cryptography", "Systems Security"],
         domains=["Security"],
         publications=33, workload=Workload.LOW, coi=False,
         bio="Security researcher focused on applied cryptography and intrusion detection."),
    dict(id="rev-lena-petrova", name="Dr. Lena Petrova",
         expertise=["Sustainability Modeling", "Environmental Data Science", "Time-Series ML"],
         domains=["Environmental / Sustainability", "Artificial Intelligence / Machine Learning"],
         publications=31, workload=Workload.MEDIUM, coi=False,
         bio="Applies machine learning to climate and environmental forecasting problems."),
    dict(id="rev-james-okoro", name="Dr. James Okoro",
         expertise=["Machine Learning", "Reinforcement Learning", "Optimization"],
         domains=["Artificial Intelligence / Machine Learning"],
         publications=41, workload=Workload.HIGH, coi=False,
         bio="Works on reinforcement learning and large-scale optimization methods."),
]

_WORKLOAD_BONUS = {Workload.LOW: 8, Workload.MEDIUM: 2, Workload.HIGH: -6}


def recommend_reviewers(paper_id: str, domain_keywords: List[str], target_venue: Optional[str], limit: int = 5) -> List[Reviewer]:
    rng = random.Random(f"reviewers:{paper_id}")
    top_domains = set(domain_keywords[:3]) if domain_keywords else set()

    scored: List[Reviewer] = []
    for entry in REVIEWER_POOL:
        overlap = len(top_domains & set(entry["domains"]))
        base = 45 + overlap * 20
        match_score = max(10, min(99, base + rng.randint(-6, 8)))
        recommendation_score = max(10, min(99, match_score + _WORKLOAD_BONUS[entry["workload"]] + rng.randint(-3, 3)))

        scored.append(Reviewer(
            id=entry["id"],
            name=entry["name"],
            expertise=entry["expertise"],
            domains=entry["domains"],
            publications=entry["publications"],
            workload=entry["workload"],
            conflict_of_interest=entry["coi"],
            match_score=match_score,
            recommendation_score=recommendation_score,
            bio=entry["bio"],
        ))

    scored.sort(key=lambda r: -r.recommendation_score)
    return scored[:limit]


def get_reviewer(reviewer_id: str) -> Optional[dict]:
    return next((r for r in REVIEWER_POOL if r["id"] == reviewer_id), None)
