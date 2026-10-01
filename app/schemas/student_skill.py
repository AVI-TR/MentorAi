from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator
from app.schemas.career import SkillRead


class StudentSkillBase(BaseModel):
    skill_id: int
    level: int = Field(1, ge=1, le=5, description="Proficiency level from 1 to 5")
    source: str = Field("self_assessed", max_length=50)


class StudentSkillCreate(StudentSkillBase):
    pass


class StudentSkillUpdate(BaseModel):
    level: Optional[int] = Field(None, ge=1, le=5)
    source: Optional[str] = Field(None, max_length=50)


class StudentSkillBatchItem(BaseModel):
    skill_id: int
    level: int = Field(..., ge=0, le=5, description="0 means no experience and deletes the persisted row.")
    source: str = Field("self_assessed", max_length=50)


class StudentSkillBatchRequest(RootModel[List[StudentSkillBatchItem]]):
    @field_validator("root")
    @classmethod
    def reject_duplicate_skill_ids(cls, value):
        skill_ids = [item.skill_id for item in value]
        if len(skill_ids) != len(set(skill_ids)):
            raise ValueError("Each skill_id may appear only once in a batch.")
        return value


class StudentSkillRead(StudentSkillBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class StudentSkillDetailRead(StudentSkillRead):
    skill: SkillRead
    model_config = ConfigDict(from_attributes=True)
