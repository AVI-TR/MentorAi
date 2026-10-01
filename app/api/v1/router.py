from fastapi import APIRouter
from app.api.v1.endpoints import (
    career_goals,
    careers,
    gap_analyses,
    health,
    roadmaps,
    skills,
    student_skills,
    users,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(careers.router, prefix="/careers", tags=["Careers"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skills"])
api_router.include_router(users.router, prefix="/users", tags=["Users & Profiles"])
api_router.include_router(student_skills.router, prefix="/users", tags=["Student Skills"])
api_router.include_router(career_goals.router, prefix="/users", tags=["Career Goals"])
api_router.include_router(gap_analyses.router, prefix="/goals", tags=["Skill Gap Analysis"])
api_router.include_router(roadmaps.router, prefix="/goals", tags=["Roadmaps"])
