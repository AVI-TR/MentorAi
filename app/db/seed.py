import logging
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.career import Skill
from app.models.learning_module import LearningModule
from app.services.catalog_service import catalog_service

logger = logging.getLogger(__name__)


def seed_learning_modules(db: Session) -> None:
    """Create the five deterministic learning modules for every catalog skill."""
    skills = list(db.scalars(select(Skill).order_by(Skill.id)).all())
    created = 0
    for skill in skills:
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
                        f"Learn the core concepts, practice common tasks, "
                        f"and complete a small exercise to reach level {level}."
                    ),
                    sequence=level,
                )
            )
            created += 1
    if created:
        db.commit()
    logger.info("Learning module seed processed successfully (%s created).", created)


def seed_database(db: Session) -> None:
    """Seed catalog data, then deterministic learning modules."""
    catalog_service.seed_catalog(db)
    seed_learning_modules(db)
