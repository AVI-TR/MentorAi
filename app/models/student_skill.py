from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, PrimaryKeyMixin, TimestampMixin


class StudentSkill(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "student_skills"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    skill_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="self_assessed",
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="skills",
    )
    skill: Mapped["Skill"] = relationship(
        "Skill",
        back_populates="student_skills",
    )

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_student_skill"),
        CheckConstraint("level >= 1 AND level <= 5", name="ck_student_skill_level"),
    )
