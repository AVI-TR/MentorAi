import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.core.exceptions import ConflictException, NotFoundException
from app.models.career import Career, CareerSkill, Skill
from app.schemas.career import CareerCreate, CareerSkillCreate, SkillCreate

logger = logging.getLogger(__name__)


class CatalogService:
    # -------------------- Skills --------------------
    def list_skills(
        self,
        db: Session,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Skill]:
        stmt = select(Skill)
        if category:
            stmt = stmt.where(Skill.category == category)
        stmt = stmt.offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def get_skill(self, db: Session, skill_id: int) -> Skill:
        skill = db.get(Skill, skill_id)
        if not skill:
            raise NotFoundException(f"Skill with id {skill_id} not found.")
        return skill

    def create_skill(self, db: Session, skill_in: SkillCreate) -> Skill:
        existing = db.scalar(select(Skill).where(Skill.name == skill_in.name))
        if existing:
            raise ConflictException(f"Skill '{skill_in.name}' already exists.")

        skill = Skill(name=skill_in.name, category=skill_in.category)
        db.add(skill)
        db.commit()
        db.refresh(skill)
        return skill

    # -------------------- Careers --------------------
    def list_careers(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Career]:
        stmt = (
            select(Career)
            .options(
                selectinload(Career.career_skills).selectinload(CareerSkill.skill)
            )
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    def get_career(self, db: Session, career_id: int) -> Career:
        stmt = (
            select(Career)
            .options(
                selectinload(Career.career_skills).selectinload(CareerSkill.skill)
            )
            .where(Career.id == career_id)
        )
        career = db.scalar(stmt)
        if not career:
            raise NotFoundException(f"Career with id {career_id} not found.")
        return career

    def create_career(self, db: Session, career_in: CareerCreate) -> Career:
        existing = db.scalar(select(Career).where(Career.name == career_in.name))
        if existing:
            raise ConflictException(f"Career '{career_in.name}' already exists.")

        career = Career(name=career_in.name, description=career_in.description)
        db.add(career)
        db.commit()
        db.refresh(career)
        return career

    def add_skill_to_career(
        self,
        db: Session,
        career_id: int,
        career_skill_in: CareerSkillCreate,
    ) -> CareerSkill:
        career = self.get_career(db, career_id)
        skill = self.get_skill(db, career_skill_in.skill_id)

        existing = db.scalar(
            select(CareerSkill).where(
                CareerSkill.career_id == career.id,
                CareerSkill.skill_id == skill.id,
            )
        )
        if existing:
            # Update existing association
            existing.required_level = career_skill_in.required_level
            existing.weight = career_skill_in.weight
            db.commit()
            career_skill_id = existing.id
        else:
            career_skill = CareerSkill(
                career_id=career.id,
                skill_id=skill.id,
                required_level=career_skill_in.required_level,
                weight=career_skill_in.weight,
            )
            db.add(career_skill)
            db.commit()
            career_skill_id = career_skill.id

        stmt = (
            select(CareerSkill)
            .options(selectinload(CareerSkill.skill))
            .where(CareerSkill.id == career_skill_id)
        )
        return db.scalar(stmt)

    # -------------------- Seed Data --------------------
    def seed_catalog(self, db: Session) -> None:
        """Seed default careers and skills idempotently."""
        seed_data = [
            {
                "career": {
                    "name": "Backend Developer",
                    "description": "Designs, builds, and maintains server-side web applications, databases, and APIs.",
                },
                "skills": [
                    {"name": "Python", "category": "Programming", "required_level": 4, "weight": 5},
                    {"name": "FastAPI", "category": "Frameworks", "required_level": 4, "weight": 4},
                    {"name": "SQL & Relational Databases", "category": "Databases", "required_level": 4, "weight": 5},
                    {"name": "System Design & Architecture", "category": "Architecture", "required_level": 3, "weight": 4},
                    {"name": "Git & Version Control", "category": "Tools", "required_level": 3, "weight": 3},
                    {"name": "Docker & Containerization", "category": "DevOps", "required_level": 3, "weight": 3},
                ],
            },
            {
                "career": {
                    "name": "Frontend Developer",
                    "description": "Builds interactive, accessible, and responsive user interfaces.",
                },
                "skills": [
                    {"name": "JavaScript/TypeScript", "category": "Programming", "required_level": 4, "weight": 5},
                    {"name": "React", "category": "Frameworks", "required_level": 4, "weight": 5},
                    {"name": "HTML & CSS", "category": "Core Web", "required_level": 4, "weight": 4},
                    {"name": "Git & Version Control", "category": "Tools", "required_level": 3, "weight": 3},
                    {"name": "Web Performance & SEO", "category": "Core Web", "required_level": 3, "weight": 3},
                ],
            },
            {
                "career": {
                    "name": "Data Scientist / AI Engineer",
                    "description": "Develops machine learning models and analyzes complex data to derive actionable insights.",
                },
                "skills": [
                    {"name": "Python", "category": "Programming", "required_level": 5, "weight": 5},
                    {"name": "Machine Learning & Deep Learning", "category": "AI/ML", "required_level": 4, "weight": 5},
                    {"name": "SQL & Relational Databases", "category": "Databases", "required_level": 4, "weight": 4},
                    {"name": "Data Analysis & Pandas", "category": "Data", "required_level": 4, "weight": 4},
                    {"name": "Mathematics & Statistics", "category": "Fundamentals", "required_level": 4, "weight": 4},
                ],
            },
        ]

        for item in seed_data:
            career_info = item["career"]
            career = db.scalar(select(Career).where(Career.name == career_info["name"]))
            if not career:
                career = Career(name=career_info["name"], description=career_info["description"])
                db.add(career)
                db.flush()

            for skill_info in item["skills"]:
                skill = db.scalar(select(Skill).where(Skill.name == skill_info["name"]))
                if not skill:
                    skill = Skill(name=skill_info["name"], category=skill_info["category"])
                    db.add(skill)
                    db.flush()

                career_skill = db.scalar(
                    select(CareerSkill).where(
                        CareerSkill.career_id == career.id,
                        CareerSkill.skill_id == skill.id,
                    )
                )
                if not career_skill:
                    career_skill = CareerSkill(
                        career_id=career.id,
                        skill_id=skill.id,
                        required_level=skill_info["required_level"],
                        weight=skill_info["weight"],
                    )
                    db.add(career_skill)

        db.commit()
        logger.info("Catalog seed data processed successfully.")


catalog_service = CatalogService()
