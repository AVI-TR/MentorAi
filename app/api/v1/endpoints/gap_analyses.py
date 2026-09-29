from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.gap_analysis import GapAnalysisRead
from app.services.gap_analysis_service import gap_analysis_service

router = APIRouter()


@router.post(
    "/{goal_id}/gap-analysis",
    response_model=GapAnalysisRead,
    status_code=status.HTTP_201_CREATED,
    summary="Generate skill gap analysis snapshot for a career goal",
)
def create_gap_analysis(
    goal_id: int,
    db: Session = Depends(get_db),
):
    return gap_analysis_service.create_gap_analysis(db=db, goal_id=goal_id)


@router.get(
    "/{goal_id}/gap-analysis/latest",
    response_model=GapAnalysisRead,
    summary="Get latest skill gap analysis snapshot for a career goal",
)
def get_latest_gap_analysis(
    goal_id: int,
    db: Session = Depends(get_db),
):
    return gap_analysis_service.get_latest_gap_analysis(db=db, goal_id=goal_id)
