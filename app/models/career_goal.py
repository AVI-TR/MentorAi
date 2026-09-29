from datetime import datetime
from typing import List, Optional
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, PrimaryKeyMixin, TimestampMixin


class CareerGoal(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "career_goals"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    career_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("careers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
        index=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="career_goals",
    )
    career: Mapped["Career"] = relationship(
        "Career",
        back_populates="career_goals",
    )
    gap_analyses: Mapped[List["GapAnalysis"]] = relationship(
        "GapAnalysis",
        back_populates="goal",
        cascade="all, delete-orphan",
        order_by="desc(GapAnalysis.created_at)",
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'completed', 'paused')",
            name="ck_career_goal_status",
        ),
    )
