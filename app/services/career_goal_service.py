from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.core.exceptions import NotFoundException
from app.models.career_goal import CareerGoal
from app.schemas.career_goal import CareerGoalCreate, CareerGoalUpdate
from app.services.catalog_service import catalog_service
from app.services.user_service import user_service


class CareerGoalService:
    def list_user_goals(self, db: Session, user_id: int) -> List[CareerGoal]:
        user_service.get_user(db, user_id)
        return list(db.scalars(select(CareerGoal).options(selectinload(CareerGoal.career)).where(CareerGoal.user_id == user_id)).all())

    def get_user_goal(self, db: Session, user_id: int, goal_id: int) -> CareerGoal:
        user_service.get_user(db, user_id)
        goal = db.scalar(select(CareerGoal).options(selectinload(CareerGoal.career)).where(CareerGoal.id == goal_id, CareerGoal.user_id == user_id))
        if not goal:
            raise NotFoundException(f"Career goal with id {goal_id} not found for user {user_id}.")
        return goal

    def create_user_goal(self, db: Session, user_id: int, goal_in: CareerGoalCreate) -> CareerGoal:
        user_service.get_user(db, user_id)
        catalog_service.get_career(db, goal_in.career_id)

        if goal_in.status == "active":
            active_goals = list(db.scalars(select(CareerGoal).options(selectinload(CareerGoal.career)).where(CareerGoal.user_id == user_id, CareerGoal.status == "active")).all())
            matching = next((goal for goal in active_goals if goal.career_id == goal_in.career_id), None)
            if matching:
                return matching
            for goal in active_goals:
                goal.status = "paused"

        goal = CareerGoal(user_id=user_id, career_id=goal_in.career_id, target_date=goal_in.target_date, status=goal_in.status)
        db.add(goal)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
        db.refresh(goal)
        return goal

    def update_user_goal(self, db: Session, user_id: int, goal_id: int, goal_in: CareerGoalUpdate) -> CareerGoal:
        goal = self.get_user_goal(db, user_id, goal_id)
        for field, value in goal_in.model_dump(exclude_unset=True).items():
            setattr(goal, field, value)
        db.commit()
        db.refresh(goal)
        return goal

    def delete_user_goal(self, db: Session, user_id: int, goal_id: int) -> None:
        goal = self.get_user_goal(db, user_id, goal_id)
        db.delete(goal)
        db.commit()


career_goal_service = CareerGoalService()
