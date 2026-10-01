from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.career import SkillRead


class LearningModuleRead(BaseModel):
    id: int
    skill_id: int
    to_level: int = Field(..., ge=1, le=5)
    title: str
    outline: str
    skill: SkillRead
    model_config = ConfigDict(from_attributes=True)


class RoadmapItemRead(BaseModel):
    id: int
    roadmap_id: int
    module_id: int
    position: int
    status: Literal["todo", "in_progress", "done"]
    module: LearningModuleRead
    model_config = ConfigDict(from_attributes=True)


class RoadmapItemStatusUpdate(BaseModel):
    status: Literal["todo", "in_progress", "done"]


class RoadmapRead(BaseModel):
    id: int
    goal_id: int
    gap_analysis_id: int
    version: int = Field(..., ge=1)
    status: Literal["active", "superseded"]
    items: List[RoadmapItemRead] = Field(default_factory=list)
    done: int = Field(..., ge=0)
    total: int = Field(..., ge=0)
    percent: float = Field(..., ge=0.0, le=100.0)
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
