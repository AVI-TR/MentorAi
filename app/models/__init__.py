"""Central ORM Model Registry.

All SQLAlchemy models are imported here so that Base.metadata.create_all
discovers all model schemas at application startup and in migrations.
"""
from app.db.base import Base
from app.models.user import User, StudentProfile
from app.models.career import Career, Skill, CareerSkill
from app.models.student_skill import StudentSkill
from app.models.career_goal import CareerGoal
from app.models.gap_analysis import GapAnalysis, GapAnalysisItem

__all__ = [
    "Base",
    "User",
    "StudentProfile",
    "Career",
    "Skill",
    "CareerSkill",
    "StudentSkill",
    "CareerGoal",
    "GapAnalysis",
    "GapAnalysisItem",
]
