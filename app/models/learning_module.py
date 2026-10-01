from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, PrimaryKeyMixin, TimestampMixin


class LearningModule(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "learning_modules"

    skill_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    to_level: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    outline: Mapped[str] = mapped_column(Text, nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)

    skill: Mapped["Skill"] = relationship("Skill", back_populates="learning_modules")
    roadmap_items: Mapped[list["RoadmapItem"]] = relationship(
        "RoadmapItem",
        back_populates="module",
    )

    __table_args__ = (
        UniqueConstraint("skill_id", "to_level", name="uq_learning_module_skill_level"),
        CheckConstraint("to_level >= 1 AND to_level <= 5", name="ck_learning_module_to_level"),
        CheckConstraint("sequence >= 1", name="ck_learning_module_sequence"),
    )
