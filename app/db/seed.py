import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.career import Skill
from app.services.module_service import seed_learning_modules_for_skill

logger = logging.getLogger(__name__)


def seed_learning_modules(db: Session) -> None:
    """Create five deterministic learning modules for every catalog skill."""
    skills = list(db.scalars(select(Skill).order_by(Skill.id)).all())
    created = sum(seed_learning_modules_for_skill(db, skill) for skill in skills)

    if created:
        db.commit()

    logger.info("Learning module seed processed successfully (%s created).", created)


def seed_database(db: Session) -> None:
    """Seed catalog data, then deterministic learning modules."""
    from app.services.catalog_service import catalog_service

    catalog_service.seed_catalog(db)
    seed_learning_modules(db)
