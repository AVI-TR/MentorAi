from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.career import Skill
from app.models.learning_module import LearningModule


def seed_learning_modules_for_skill(db: Session, skill: Skill) -> int:
    """Create the five deterministic learning modules for one skill."""
    created = 0

    for level in range(1, 6):
        existing = db.scalar(
            select(LearningModule).where(
                LearningModule.skill_id == skill.id,
                LearningModule.to_level == level,
            )
        )
        if existing:
            continue

        db.add(
            LearningModule(
                skill_id=skill.id,
                to_level=level,
                title=f"{skill.name}: Level {level}",
                outline=(
                    "Learn the core concepts, practice common tasks, "
                    f"and complete a small exercise to reach level {level}."
                ),
            )
        )
        created += 1

    return created
