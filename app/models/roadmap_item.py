from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, PrimaryKeyMixin, TimestampMixin


class RoadmapItem(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "roadmap_items"

    roadmap_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roadmaps.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    module_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("learning_modules.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="todo", index=True)

    roadmap: Mapped["Roadmap"] = relationship("Roadmap", back_populates="items")
    module: Mapped["LearningModule"] = relationship(
        "LearningModule",
        back_populates="roadmap_items",
    )

    __table_args__ = (
        CheckConstraint("position >= 1", name="ck_roadmap_item_position"),
        CheckConstraint(
            "status IN ('todo', 'in_progress', 'done')",
            name="ck_roadmap_item_status",
        ),
    )
