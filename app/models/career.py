from typing import List, Optional
from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, PrimaryKeyMixin, TimestampMixin


class Career(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "careers"

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    career_skills: Mapped[List["CareerSkill"]] = relationship(
        "CareerSkill",
        back_populates="career",
        cascade="all, delete-orphan",
    )
    career_goals: Mapped[List["CareerGoal"]] = relationship(
        "CareerGoal",
        back_populates="career",
    )


class Skill(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )
    category: Mapped[Optional[str]] = mapped_column(
        String(100),
        index=True,
        nullable=True,
    )

    # Relationships
    career_skills: Mapped[List["CareerSkill"]] = relationship(
        "CareerSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )
    student_skills: Mapped[List["StudentSkill"]] = relationship(
        "StudentSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
    )


class CareerSkill(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "career_skills"

    career_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("careers.id", ondelete="CASCADE"),
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
        default=1,
    )
    weight: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    # Relationships
    career: Mapped["Career"] = relationship(
        "Career",
        back_populates="career_skills",
    )
    skill: Mapped["Skill"] = relationship(
        "Skill",
        back_populates="career_skills",
    )

    __table_args__ = (
        UniqueConstraint("career_id", "skill_id", name="uq_career_skill"),
        CheckConstraint("required_level >= 1 AND required_level <= 5", name="ck_career_skill_required_level"),
        CheckConstraint("weight >= 1 AND weight <= 5", name="ck_career_skill_weight"),
    )
