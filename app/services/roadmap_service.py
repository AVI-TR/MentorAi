from typing import List, Optional
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, selectinload
from app.core.exceptions import NotFoundException
from app.models.career_goal import CareerGoal
from app.models.gap_analysis import GapAnalysis, GapAnalysisItem
from app.models.learning_module import LearningModule
from app.models.roadmap import Roadmap
from app.models.roadmap_item import RoadmapItem
from app.schemas.roadmap import RoadmapItemRead, RoadmapItemStatusUpdate, RoadmapRead
from app.services.gap_analysis_service import gap_analysis_service
from app.services.roadmap_engine import RoadmapGapItem, RoadmapModule, build_roadmap
from app.services.user_service import user_service


class RoadmapService:
    def _get_goal(self, db: Session, goal_id: int) -> CareerGoal:
        goal = db.get(CareerGoal, goal_id)
        if not goal:
            raise NotFoundException(f"Career goal with id {goal_id} not found.")
        return goal

    def _load_roadmap(self, db: Session, roadmap_id: int) -> Roadmap:
        stmt = (
            select(Roadmap)
            .options(
                selectinload(Roadmap.items)
                .selectinload(RoadmapItem.module)
                .selectinload(LearningModule.skill)
            )
            .where(Roadmap.id == roadmap_id)
        )
        roadmap = db.scalar(stmt)
        if not roadmap:
            raise NotFoundException(f"Roadmap with id {roadmap_id} not found.")
        return roadmap

    def _to_response(self, roadmap: Roadmap) -> RoadmapRead:
        items = sorted(roadmap.items, key=lambda item: item.position)
        total = len(items)
        done = sum(item.status == "done" for item in items)
        percent = round((done / total) * 100.0, 2) if total else 0.0
        return RoadmapRead(
            id=roadmap.id,
            goal_id=roadmap.goal_id,
            gap_analysis_id=roadmap.gap_analysis_id,
            version=roadmap.version,
            status=roadmap.status,
            items=items,
            done=done,
            total=total,
            percent=percent,
            created_at=roadmap.created_at,
            updated_at=roadmap.updated_at,
        )

    def create_roadmap(self, db: Session, goal_id: int) -> RoadmapRead:
        goal = self._get_goal(db, goal_id)
        analysis = gap_analysis_service.get_latest_gap_analysis(db, goal_id)

        gap_items = [
            RoadmapGapItem(
                skill_id=item.skill_id,
                student_level=item.student_level,
                required_level=item.required_level,
                gap=item.gap,
                priority_score=item.priority_score,
            )
            for item in analysis.items
        ]

        skill_ids = {item.skill_id for item in gap_items if item.gap > 0}
        modules = list(
            db.scalars(
                select(LearningModule).where(LearningModule.skill_id.in_(skill_ids))
            ).all()
        ) if skill_ids else []

        plan = build_roadmap(
            gap_items=gap_items,
            available_modules=[
                RoadmapModule(
                    module_id=module.id,
                    skill_id=module.skill_id,
                    to_level=module.to_level,
                )
                for module in modules
            ],
        )

        max_version = db.scalar(
            select(func.max(Roadmap.version)).where(Roadmap.goal_id == goal_id)
        ) or 0

        active_roadmaps = list(
            db.scalars(
                select(Roadmap).where(
                    Roadmap.goal_id == goal_id,
                    Roadmap.status == "active",
                )
            ).all()
        )

        for roadmap in active_roadmaps:
            roadmap.status = "superseded"

        roadmap = Roadmap(
            goal_id=goal_id,
            gap_analysis_id=analysis.id,
            version=max_version + 1,
            status="active",
        )
        db.add(roadmap)
        db.flush()

        if plan.module_ids:
            module_position_by_id = {
                module_id: position
                for position, module_id in enumerate(plan.module_ids, start=1)
            }
            for module_id, position in module_position_by_id.items():
                db.add(
                    RoadmapItem(
                        roadmap_id=roadmap.id,
                        module_id=module_id,
                        position=position,
                        status="todo",
                    )
                )

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        return self._to_response(self._load_roadmap(db, roadmap.id))

    def get_latest_roadmap(self, db: Session, goal_id: int) -> RoadmapRead:
        self._get_goal(db, goal_id)
        roadmap = db.scalar(
            select(Roadmap)
            .where(Roadmap.goal_id == goal_id, Roadmap.status == "active")
            .order_by(desc(Roadmap.version))
        )
        if not roadmap:
            raise NotFoundException(f"No active roadmap found for career goal {goal_id}.")
        return self._to_response(self._load_roadmap(db, roadmap.id))

    def update_item_status(
        self,
        db: Session,
        goal_id: int,
        item_id: int,
        update: RoadmapItemStatusUpdate,
    ) -> RoadmapItemRead:
        self._get_goal(db, goal_id)
        stmt = (
            select(RoadmapItem)
            .join(Roadmap, Roadmap.id == RoadmapItem.roadmap_id)
            .options(
                selectinload(RoadmapItem.module).selectinload(LearningModule.skill)
            )
            .where(Roadmap.goal_id == goal_id, RoadmapItem.id == item_id)
        )
        item = db.scalar(stmt)
        if not item:
            raise NotFoundException(
                f"Roadmap item with id {item_id} not found for career goal {goal_id}."
            )
        item.status = update.status
        db.commit()
        db.refresh(item)
        return item


roadmap_service = RoadmapService()
