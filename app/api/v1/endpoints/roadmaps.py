from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.roadmap import RoadmapItemRead, RoadmapItemStatusUpdate, RoadmapRead
from app.services.roadmap_service import roadmap_service

router = APIRouter()


@router.post(
    "/{goal_id}/roadmap",
    response_model=RoadmapRead,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a deterministic roadmap for a career goal",
)
def create_roadmap(goal_id: int, db: Session = Depends(get_db)):
    return roadmap_service.create_roadmap(db=db, goal_id=goal_id)


@router.get(
    "/{goal_id}/roadmap/latest",
    response_model=RoadmapRead,
    summary="Get the active roadmap for a career goal",
)
def get_latest_roadmap(goal_id: int, db: Session = Depends(get_db)):
    return roadmap_service.get_latest_roadmap(db=db, goal_id=goal_id)


@router.patch(
    "/{goal_id}/roadmap/items/{item_id}",
    response_model=RoadmapItemRead,
    summary="Update roadmap item status",
)
def update_roadmap_item(
    goal_id: int,
    item_id: int,
    update: RoadmapItemStatusUpdate,
    db: Session = Depends(get_db),
):
    return roadmap_service.update_item_status(
        db=db,
        goal_id=goal_id,
        item_id=item_id,
        update=update,
    )
