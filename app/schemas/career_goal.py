from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.career import CareerRead


class CareerGoalBase(BaseModel):
    career_id: int
    target_date: Optional[datetime] = Field(None, description="Target completion or goal achievement date")
    status: str = Field("active", max_length=50, description="Status of the goal (e.g. active, completed, paused)")


class CareerGoalCreate(CareerGoalBase):
    pass


class CareerGoalUpdate(BaseModel):
    target_date: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=50)


class CareerGoalRead(CareerGoalBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CareerGoalDetailRead(CareerGoalRead):
    career: CareerRead

    model_config = ConfigDict(from_attributes=True)
