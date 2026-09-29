from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.core.exceptions import NotFoundException
from app.models.student_skill import StudentSkill
from app.schemas.student_skill import StudentSkillCreate, StudentSkillUpdate
from app.services.catalog_service import catalog_service
from app.services.user_service import user_service


class StudentSkillService:
    def list_user_skills(self, db: Session, user_id: int) -> List[StudentSkill]:
        user_service.get_user(db, user_id)  # verify user exists
        stmt = (
            select(StudentSkill)
            .options(selectinload(StudentSkill.skill))
            .where(StudentSkill.user_id == user_id)
        )
        return list(db.scalars(stmt).all())

    def get_user_skill(self, db: Session, user_id: int, skill_id: int) -> StudentSkill:
        user_service.get_user(db, user_id)  # verify user exists
        stmt = (
            select(StudentSkill)
            .options(selectinload(StudentSkill.skill))
            .where(
                StudentSkill.user_id == user_id,
                StudentSkill.skill_id == skill_id,
            )
        )
        student_skill = db.scalar(stmt)
        if not student_skill:
            raise NotFoundException(f"Skill with id {skill_id} not recorded for user {user_id}.")
        return student_skill

    def upsert_user_skill(
        self,
        db: Session,
        user_id: int,
        skill_in: StudentSkillCreate,
    ) -> StudentSkill:
        user_service.get_user(db, user_id)  # verify user exists
        catalog_service.get_skill(db, skill_in.skill_id)  # verify skill exists

        stmt = select(StudentSkill).where(
            StudentSkill.user_id == user_id,
            StudentSkill.skill_id == skill_in.skill_id,
        )
        student_skill = db.scalar(stmt)

        if student_skill:
            student_skill.level = skill_in.level
            student_skill.source = skill_in.source
        else:
            student_skill = StudentSkill(
                user_id=user_id,
                skill_id=skill_in.skill_id,
                level=skill_in.level,
                source=skill_in.source,
            )
            db.add(student_skill)

        db.commit()
        db.refresh(student_skill)
        return student_skill

    def update_user_skill(
        self,
        db: Session,
        user_id: int,
        skill_id: int,
        skill_in: StudentSkillUpdate,
    ) -> StudentSkill:
        student_skill = self.get_user_skill(db, user_id, skill_id)

        update_data = skill_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(student_skill, field, value)

        db.commit()
        db.refresh(student_skill)
        return student_skill

    def delete_user_skill(self, db: Session, user_id: int, skill_id: int) -> None:
        student_skill = self.get_user_skill(db, user_id, skill_id)
        db.delete(student_skill)
        db.commit()


student_skill_service = StudentSkillService()
