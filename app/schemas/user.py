from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudentProfileBase(BaseModel):
    education: Optional[str] = Field(None, max_length=255, description="Degree or academic background")
    year: Optional[str] = Field(None, max_length=50, description="Current academic year or level")
    interests: Optional[str] = Field(None, description="Areas of interest or hobbies")


class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileUpdate(BaseModel):
    education: Optional[str] = Field(None, max_length=255)
    year: Optional[str] = Field(None, max_length=50)
    interests: Optional[str] = None


class StudentProfileRead(StudentProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: str = Field(..., pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", max_length=255, description="Valid email address; normalized to lowercase")

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserDetailRead(UserRead):
    profile: Optional[StudentProfileRead] = None
    model_config = ConfigDict(from_attributes=True)
