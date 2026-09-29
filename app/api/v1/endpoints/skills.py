from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.career import SkillCreate, SkillRead
from app.services.catalog_service import catalog_service

router = APIRouter()


@router.get("", response_model=List[SkillRead], summary="List skills catalog")
def list_skills(
    category: Optional[str] = Query(None, description="Filter skills by category"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return catalog_service.list_skills(db=db, category=category, skip=skip, limit=limit)


@router.get("/{skill_id}", response_model=SkillRead, summary="Get skill by ID")
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db),
):
    return catalog_service.get_skill(db=db, skill_id=skill_id)


@router.post("", response_model=SkillRead, status_code=status.HTTP_201_CREATED, summary="Create a new skill")
def create_skill(
    skill_in: SkillCreate,
    db: Session = Depends(get_db),
):
    return catalog_service.create_skill(db=db, skill_in=skill_in)
