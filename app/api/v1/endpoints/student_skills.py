from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.student_skill import (
    StudentSkillCreate,
    StudentSkillDetailRead,
    StudentSkillRead,
    StudentSkillUpdate,
)
from app.services.student_skill_service import student_skill_service

router = APIRouter()


@router.get("/{user_id}/skills", response_model=List[StudentSkillDetailRead], summary="List assessed skills for user")
def list_student_skills(
    user_id: int,
    db: Session = Depends(get_db),
):
    return student_skill_service.list_user_skills(db=db, user_id=user_id)


@router.post("/{user_id}/skills", response_model=StudentSkillRead, status_code=status.HTTP_201_CREATED, summary="Add or update assessed skill for user")
def upsert_student_skill(
    user_id: int,
    skill_in: StudentSkillCreate,
    db: Session = Depends(get_db),
):
    return student_skill_service.upsert_user_skill(db=db, user_id=user_id, skill_in=skill_in)


@router.put("/{user_id}/skills/{skill_id}", response_model=StudentSkillRead, summary="Update level/source for a student skill")
def update_student_skill(
    user_id: int,
    skill_id: int,
    skill_in: StudentSkillUpdate,
    db: Session = Depends(get_db),
):
    return student_skill_service.update_user_skill(
        db=db,
        user_id=user_id,
        skill_id=skill_id,
        skill_in=skill_in,
    )


@router.delete("/{user_id}/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove assessed skill from user")
def delete_student_skill(
    user_id: int,
    skill_id: int,
    db: Session = Depends(get_db),
):
    student_skill_service.delete_user_skill(db=db, user_id=user_id, skill_id=skill_id)
