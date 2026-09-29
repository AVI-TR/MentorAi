from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, PrimaryKeyMixin, TimestampMixin


class User(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    # Relationships
    profile: Mapped[Optional["StudentProfile"]] = relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    skills: Mapped[List["StudentSkill"]] = relationship(
        "StudentSkill",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    career_goals: Mapped[List["CareerGoal"]] = relationship(
        "CareerGoal",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class StudentProfile(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "student_profiles"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    education: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    year: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    interests: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
    )
