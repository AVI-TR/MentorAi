from typing import List, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.core.exceptions import NotFoundException
from app.models.student_skill import StudentSkill
from app.schemas.student_skill import StudentSkillBatchItem, StudentSkillCreate, StudentSkillUpdate
from app.services.catalog_service import catalog_service
from app.services.user_service import user_service


class StudentSkillService:
    def list_user_skills(self, db: Session, user_id: int) -> List[StudentSkill]:
        user_service.get_user(db, user_id)
        return list(db.scalars(select(StudentSkill).options(selectinload(StudentSkill.skill)).where(StudentSkill.user_id == user_id)).all())

    def get_user_skill(self, db: Session, user_id: int, skill_id: int) -> StudentSkill:
        user_service.get_user(db, user_id)
        row = db.scalar(select(StudentSkill).options(selectinload(StudentSkill.skill)).where(StudentSkill.user_id == user_id, StudentSkill.skill_id == skill_id))
        if not row:
            raise NotFoundException(f"Skill with id {skill_id} not recorded for user {user_id}.")
        return row

    def upsert_user_skill(self, db: Session, user_id: int, skill_in: StudentSkillCreate) -> StudentSkill:
        user_service.get_user(db, user_id)
        catalog_service.get_skill(db, skill_in.skill_id)
        row = db.scalar(select(StudentSkill).where(StudentSkill.user_id == user_id, StudentSkill.skill_id == skill_in.skill_id))
        if row:
            row.level, row.source = skill_in.level, skill_in.source
        else:
            row = StudentSkill(user_id=user_id, skill_id=skill_in.skill_id, level=skill_in.level, source=skill_in.source)
            db.add(row)
        db.commit()
        db.refresh(row)
        return row

    def replace_user_skills(self, db: Session, user_id: int, skills: Sequence[StudentSkillBatchItem]) -> List[StudentSkill]:
        user_service.get_user(db, user_id)
        skill_ids = [item.skill_id for item in skills]

        for skill_id in skill_ids:
            catalog_service.get_skill(db, skill_id)

        existing = (
            list(db.scalars(select(StudentSkill).where(StudentSkill.user_id == user_id, StudentSkill.skill_id.in_(skill_ids))).all())
            if skill_ids else []
        )
        by_skill = {row.skill_id: row for row in existing}

        try:
            for item in skills:
                row = by_skill.get(item.skill_id)
                if item.level == 0:
                    if row:
                        db.delete(row)
                    continue
                if row:
                    row.level, row.source = item.level, item.source
                else:
                    row = StudentSkill(user_id=user_id, skill_id=item.skill_id, level=item.level, source=item.source)
                    db.add(row)
                    by_skill[item.skill_id] = row
            db.commit()
        except Exception:
            db.rollback()
            raise

        refreshed = (
            list(db.scalars(select(StudentSkill).options(selectinload(StudentSkill.skill)).where(StudentSkill.user_id == user_id, StudentSkill.skill_id.in_(skill_ids))).all())
            if skill_ids else []
        )
        refreshed_by_skill = {row.skill_id: row for row in refreshed}
        return [refreshed_by_skill[item.skill_id] for item in skills if item.level > 0]

    def update_user_skill(self, db: Session, user_id: int, skill_id: int, skill_in: StudentSkillUpdate) -> StudentSkill:
        row = self.get_user_skill(db, user_id, skill_id)
        for field, value in skill_in.model_dump(exclude_unset=True).items():
            setattr(row, field, value)
        db.commit()
        db.refresh(row)
        return row

    def delete_user_skill(self, db: Session, user_id: int, skill_id: int) -> None:
        row = self.get_user_skill(db, user_id, skill_id)
        db.delete(row)
        db.commit()


student_skill_service = StudentSkillService()
