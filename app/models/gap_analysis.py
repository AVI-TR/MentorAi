from typing import List
from sqlalchemy import CheckConstraint, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, PrimaryKeyMixin, TimestampMixin


class GapAnalysis(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "gap_analyses"

    goal_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("career_goals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    readiness_percent: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    total_skills: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    skills_met: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    weighted_required: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    weighted_achieved: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # Relationships
    goal: Mapped["CareerGoal"] = relationship(
        "CareerGoal",
        back_populates="gap_analyses",
    )
    items: Mapped[List["GapAnalysisItem"]] = relationship(
        "GapAnalysisItem",
        back_populates="gap_analysis",
        cascade="all, delete-orphan",
        order_by="desc(GapAnalysisItem.priority_score)",
    )

    __table_args__ = (
        CheckConstraint(
            "readiness_percent >= 0.0 AND readiness_percent <= 100.0",
            name="ck_gap_analysis_readiness_percent",
        ),
        CheckConstraint("total_skills >= 0", name="ck_gap_analysis_total_skills"),
        CheckConstraint("skills_met >= 0", name="ck_gap_analysis_skills_met"),
        CheckConstraint("weighted_required >= 0", name="ck_gap_analysis_weighted_required"),
        CheckConstraint("weighted_achieved >= 0", name="ck_gap_analysis_weighted_achieved"),
    )


class GapAnalysisItem(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "gap_analysis_items"

    gap_analysis_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("gap_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    required_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    student_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    gap: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    weight: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    priority_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Relationships
    gap_analysis: Mapped["GapAnalysis"] = relationship(
        "GapAnalysis",
        back_populates="items",
    )
    skill: Mapped["Skill"] = relationship(
        "Skill",
    )

    __table_args__ = (
        CheckConstraint(
            "required_level >= 1 AND required_level <= 5",
            name="ck_gap_item_required_level",
        ),
        CheckConstraint(
            "student_level >= 0 AND student_level <= 5",
            name="ck_gap_item_student_level",
        ),
        CheckConstraint("gap >= 0 AND gap <= 5", name="ck_gap_item_gap"),
        CheckConstraint("weight >= 1 AND weight <= 5", name="ck_gap_item_weight"),
        CheckConstraint("priority_score >= 0", name="ck_gap_item_priority_score"),
    )
