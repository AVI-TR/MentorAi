from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


# Skill Schemas
class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    category: Optional[str] = Field(None, max_length=100)


class SkillCreate(SkillBase):
    pass


class SkillRead(SkillBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# CareerSkill Schemas
class CareerSkillBase(BaseModel):
    skill_id: int
    required_level: int = Field(1, ge=1, le=5, description="Required proficiency level (1-5)")
    weight: int = Field(1, ge=1, le=5, description="Importance weight (1-5)")


class CareerSkillCreate(CareerSkillBase):
    pass


class CareerSkillRead(CareerSkillBase):
    id: int
    career_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CareerSkillDetailRead(CareerSkillRead):
    skill: SkillRead

    model_config = ConfigDict(from_attributes=True)


# Career Schemas
class CareerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None


class CareerCreate(CareerBase):
    pass


class CareerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None


class CareerRead(CareerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CareerDetailRead(CareerRead):
    career_skills: List[CareerSkillDetailRead] = []

    model_config = ConfigDict(from_attributes=True)
