from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import (
    StudentProfileCreate,
    StudentProfileRead,
    StudentProfileUpdate,
    UserCreate,
    UserDetailRead,
    UserRead,
)
from app.services.user_service import user_service

router = APIRouter()


@router.get("", response_model=List[UserDetailRead], summary="List all users")
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return user_service.list_users(db=db, skip=skip, limit=limit)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Create a new user")
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    return user_service.create_user(db=db, user_in=user_in)


@router.get("/{user_id}", response_model=UserDetailRead, summary="Get user details by ID")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    return user_service.get_user(db=db, user_id=user_id)


# -------------------- Profile Sub-routes --------------------
@router.get("/{user_id}/profile", response_model=StudentProfileRead, summary="Get user student profile")
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
):
    return user_service.get_profile(db=db, user_id=user_id)


@router.post("/{user_id}/profile", response_model=StudentProfileRead, summary="Create or update student profile")
def upsert_user_profile(
    user_id: int,
    profile_in: StudentProfileCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    profile, created = user_service.upsert_profile(db=db, user_id=user_id, profile_in=profile_in)
    if created:
        response.status_code = status.HTTP_201_CREATED
    else:
        response.status_code = status.HTTP_200_OK
    return profile


@router.put("/{user_id}/profile", response_model=StudentProfileRead, summary="Update student profile")
def update_user_profile(
    user_id: int,
    profile_in: StudentProfileUpdate,
    db: Session = Depends(get_db),
):
    return user_service.update_profile(db=db, user_id=user_id, profile_in=profile_in)
