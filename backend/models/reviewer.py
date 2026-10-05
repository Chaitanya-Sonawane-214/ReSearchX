from sqlalchemy import Boolean, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Reviewer(Base):
    __tablename__ = "reviewers"

    id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    expertise: Mapped[list] = mapped_column(
        JSON,
        nullable=False
    )

    domains: Mapped[list] = mapped_column(
        JSON,
        nullable=False
    )

    publications: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    workload: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    coi: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    bio: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )