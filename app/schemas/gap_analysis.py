from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.career import SkillRead


class GapAnalysisItemRead(BaseModel):
    id: int
    gap_analysis_id: int
    skill_id: int
    required_level: int = Field(..., ge=1, le=5, description="Required proficiency level (1-5)")
    student_level: int = Field(..., ge=0, le=5, description="Student current proficiency level (0-5, 0 if missing)")
    gap: int = Field(..., ge=0, le=5, description="Proficiency gap: max(required - student, 0)")
    weight: int = Field(..., ge=1, le=5, description="Importance weight of the skill in this career (1-5)")
    priority_score: int = Field(..., ge=0, description="Priority score: gap * weight")
    skill: Optional[SkillRead] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GapAnalysisRead(BaseModel):
    id: int
    goal_id: int
    readiness_percent: float = Field(..., ge=0.0, le=100.0, description="Career readiness percentage (0.0 to 100.0)")
    total_skills: int = Field(..., ge=0, description="Total number of required skills for the career track")
    skills_met: int = Field(..., ge=0, description="Number of skills where student_level >= required_level")
    weighted_required: int = Field(..., ge=0, description="Sum of (required_level * weight)")
    weighted_achieved: int = Field(..., ge=0, description="Sum of (min(student_level, required_level) * weight)")
    items: List[GapAnalysisItemRead] = Field(default_factory=list, description="Skill gap breakdown items")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
