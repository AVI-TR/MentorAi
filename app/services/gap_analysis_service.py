import logging
from typing import Optional
from sqlalchemy import desc, select
from sqlalchemy.orm import Session, selectinload
from app.core.exceptions import NotFoundException
from app.models.career import CareerSkill
from app.models.career_goal import CareerGoal
from app.models.gap_analysis import GapAnalysis, GapAnalysisItem
from app.models.student_skill import StudentSkill
from app.services.gap_engine import SkillRequirement, calculate_skill_gap

logger = logging.getLogger(__name__)


class GapAnalysisService:
    def create_gap_analysis(self, db: Session, goal_id: int) -> GapAnalysis:
        """Calculate and persist a deterministic skill gap snapshot for a career goal."""
        goal = db.get(CareerGoal, goal_id)
        if not goal:
            raise NotFoundException(f"Career goal with id {goal_id} not found.")

        # 1. Fetch career skill requirements
        career_skills = list(
            db.scalars(
                select(CareerSkill)
                .where(CareerSkill.career_id == goal.career_id)
                .options(selectinload(CareerSkill.skill))
            ).all()
        )

        # 2. Fetch student's current assessed skills
        student_skills = list(
            db.scalars(
                select(StudentSkill).where(StudentSkill.user_id == goal.user_id)
            ).all()
        )
        student_levels = {ss.skill_id: ss.level for ss in student_skills}

        # 3. Build requirements list
        requirements = [
            SkillRequirement(
                skill_id=cs.skill_id,
                required_level=cs.required_level,
                weight=cs.weight,
                skill_name=cs.skill.name if cs.skill else None,
            )
            for cs in career_skills
        ]

        # 4. Pure deterministic calculation
        computed = calculate_skill_gap(requirements, student_levels)

        # 5. Persist snapshot
        analysis = GapAnalysis(
            goal_id=goal.id,
            readiness_percent=computed.readiness_percent,
            total_skills=computed.total_skills,
            skills_met=computed.skills_met,
            weighted_required=computed.weighted_required,
            weighted_achieved=computed.weighted_achieved,
        )
        db.add(analysis)
        db.flush()

        for item_data in computed.items:
            item = GapAnalysisItem(
                gap_analysis_id=analysis.id,
                skill_id=item_data.skill_id,
                required_level=item_data.required_level,
                student_level=item_data.student_level,
                gap=item_data.gap,
                weight=item_data.weight,
                priority_score=item_data.priority_score,
            )
            db.add(item)

        db.commit()
        logger.info(
            f"Created gap analysis snapshot {analysis.id} for goal {goal_id} (Readiness: {analysis.readiness_percent}%)"
        )

        # 6. Eagerly reload with relationships for response serialization
        stmt = (
            select(GapAnalysis)
            .options(
                selectinload(GapAnalysis.items).selectinload(GapAnalysisItem.skill)
            )
            .where(GapAnalysis.id == analysis.id)
        )
        return db.scalar(stmt)

    def get_latest_gap_analysis(self, db: Session, goal_id: int) -> GapAnalysis:
        """Fetch the most recent gap analysis snapshot for a career goal."""
        goal = db.get(CareerGoal, goal_id)
        if not goal:
            raise NotFoundException(f"Career goal with id {goal_id} not found.")

        stmt = (
            select(GapAnalysis)
            .options(
                selectinload(GapAnalysis.items).selectinload(GapAnalysisItem.skill)
            )
            .where(GapAnalysis.goal_id == goal_id)
            .order_by(desc(GapAnalysis.created_at), desc(GapAnalysis.id))
            .limit(1)
        )
        analysis = db.scalar(stmt)
        if not analysis:
            raise NotFoundException(f"No gap analysis found for career goal {goal_id}.")
        return analysis


gap_analysis_service = GapAnalysisService()
