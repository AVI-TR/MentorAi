from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.career import SkillRead


class StudentSkillBase(BaseModel):
    skill_id: int
    level: int = Field(1, ge=1, le=5, description="Proficiency level from 1 to 5")
    source: str = Field("self_assessed", max_length=50, description="Origin of assessment (e.g. self_assessed, quiz)")


class StudentSkillCreate(StudentSkillBase):
    pass


class StudentSkillUpdate(BaseModel):
    level: Optional[int] = Field(None, ge=1, le=5)
    source: Optional[str] = Field(None, max_length=50)


class StudentSkillRead(StudentSkillBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StudentSkillDetailRead(StudentSkillRead):
    skill: SkillRead

    model_config = ConfigDict(from_attributes=True)
