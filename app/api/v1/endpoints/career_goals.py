from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.career_goal import CareerGoalCreate, CareerGoalDetailRead, CareerGoalRead, CareerGoalUpdate
from app.services.career_goal_service import career_goal_service

router = APIRouter()


@router.get("/{user_id}/goals", response_model=List[CareerGoalDetailRead], summary="List career goals for user")
def list_user_goals(user_id: int, db: Session = Depends(get_db)):
    return career_goal_service.list_user_goals(db=db, user_id=user_id)


@router.get("/{user_id}/goals/{goal_id}", response_model=CareerGoalDetailRead, summary="Get career goal details")
def get_user_goal(user_id: int, goal_id: int, db: Session = Depends(get_db)):
    return career_goal_service.get_user_goal(db=db, user_id=user_id, goal_id=goal_id)


@router.post("/{user_id}/goals", response_model=CareerGoalRead, status_code=status.HTTP_201_CREATED, summary="Create or return the active career goal for user")
def create_user_goal(user_id: int, goal_in: CareerGoalCreate, response: Response, db: Session = Depends(get_db)):
    goal, created = career_goal_service.create_user_goal(db=db, user_id=user_id, goal_in=goal_in)
    response.status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return goal


@router.patch("/{user_id}/goals/{goal_id}", response_model=CareerGoalRead, summary="Update target date or status of a career goal")
def update_user_goal(user_id: int, goal_id: int, goal_in: CareerGoalUpdate, db: Session = Depends(get_db)):
    return career_goal_service.update_user_goal(db=db, user_id=user_id, goal_id=goal_id, goal_in=goal_in)


@router.delete("/{user_id}/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a career goal")
def delete_user_goal(user_id: int, goal_id: int, db: Session = Depends(get_db)):
    career_goal_service.delete_user_goal(db=db, user_id=user_id, goal_id=goal_id)
