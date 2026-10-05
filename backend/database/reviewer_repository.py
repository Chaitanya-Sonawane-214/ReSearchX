from sqlalchemy import select

from database.connection import SessionLocal
from models.reviewer import Reviewer as ReviewerDB
from schemas import Workload


def get_reviewer_pool() -> list[dict]:
    """
    Fetch reviewers from PostgreSQL and return them
    in the same dictionary structure used by the
    existing reviewer matching algorithm.
    """

    db = SessionLocal()

    try:
        rows = db.scalars(
            select(ReviewerDB)
        ).all()

        return [
            {
                "id": row.id,
                "name": row.name,
                "expertise": row.expertise,
                "domains": row.domains,
                "publications": row.publications,
                "workload": Workload(row.workload),
                "coi": row.coi,
                "bio": row.bio or "",
            }
            for row in rows
        ]

    finally:
        db.close()