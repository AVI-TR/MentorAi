"""Central ORM Model Registry."""
from app.db.base import Base
from app.models.user import User, StudentProfile
from app.models.career import Career, Skill, CareerSkill
from app.models.student_skill import StudentSkill
from app.models.career_goal import CareerGoal
from app.models.gap_analysis import GapAnalysis, GapAnalysisItem
from app.models.learning_module import LearningModule
from app.models.roadmap import Roadmap
from app.models.roadmap_item import RoadmapItem

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
    "LearningModule",
    "Roadmap",
    "RoadmapItem",
]
