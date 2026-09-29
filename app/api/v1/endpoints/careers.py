from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.career import (
    CareerCreate,
    CareerDetailRead,
    CareerRead,
    CareerSkillCreate,
    CareerSkillDetailRead,
)
from app.services.catalog_service import catalog_service

router = APIRouter()


@router.get("", response_model=List[CareerRead], summary="List career tracks")
def list_careers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return catalog_service.list_careers(db=db, skip=skip, limit=limit)


@router.get("/{career_id}", response_model=CareerDetailRead, summary="Get career track with required skills")
def get_career(
    career_id: int,
    db: Session = Depends(get_db),
):
    return catalog_service.get_career(db=db, career_id=career_id)


@router.post("", response_model=CareerRead, status_code=status.HTTP_201_CREATED, summary="Create a new career track")
def create_career(
    career_in: CareerCreate,
    db: Session = Depends(get_db),
):
    return catalog_service.create_career(db=db, career_in=career_in)


@router.post("/{career_id}/skills", response_model=CareerSkillDetailRead, status_code=status.HTTP_201_CREATED, summary="Map required skill to career")
def add_skill_to_career(
    career_id: int,
    career_skill_in: CareerSkillCreate,
    db: Session = Depends(get_db),
):
    return catalog_service.add_skill_to_career(
        db=db,
        career_id=career_id,
        career_skill_in=career_skill_in,
    )
