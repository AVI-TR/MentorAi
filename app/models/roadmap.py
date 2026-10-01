from typing import List
from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, PrimaryKeyMixin, TimestampMixin


class Roadmap(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "roadmaps"

    goal_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("career_goals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    gap_analysis_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("gap_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active", index=True)

    goal: Mapped["CareerGoal"] = relationship("CareerGoal", back_populates="roadmaps")
    gap_analysis: Mapped["GapAnalysis"] = relationship("GapAnalysis")
    items: Mapped[List["RoadmapItem"]] = relationship(
        "RoadmapItem",
        back_populates="roadmap",
        cascade="all, delete-orphan",
        order_by="RoadmapItem.position",
    )

    __table_args__ = (
        UniqueConstraint("goal_id", "version", name="uq_roadmap_goal_version"),
        CheckConstraint("version >= 1", name="ck_roadmap_version"),
        CheckConstraint(
            "status IN ('active', 'superseded')",
            name="ck_roadmap_status",
        ),
    )
