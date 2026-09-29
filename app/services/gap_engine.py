"""Deterministic Skill-Gap Calculation Engine.

Pure, unit-testable business logic for computing skill gaps, priority scores,
and readiness percentages. No database or external dependencies.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class SkillRequirement:
    """Skill requirement from a career track."""
    skill_id: int
    required_level: int
    weight: int
    skill_name: Optional[str] = None


@dataclass(frozen=True)
class ComputedGapItem:
    """Computed gap details for a single skill."""
    skill_id: int
    required_level: int
    student_level: int
    gap: int
    weight: int
    priority_score: int
    skill_name: Optional[str] = None


@dataclass(frozen=True)
class ComputedGapAnalysis:
    """Full computed gap analysis summary."""
    readiness_percent: float
    total_skills: int
    skills_met: int
    weighted_required: int
    weighted_achieved: int
    items: List[ComputedGapItem]


def calculate_skill_gap(
    requirements: List[SkillRequirement],
    student_skill_levels: Dict[int, int],
) -> ComputedGapAnalysis:
    """Compute deterministic skill gap analysis.

    Rules:
    - gap = max(required_level - student_level, 0)
    - missing StudentSkill means student_level = 0
    - priority_score = gap * weight
    - weighted_required = sum(required_level * weight)
    - weighted_achieved = sum(min(student_level, required_level) * weight)
    - readiness_percent = round((weighted_achieved / weighted_required) * 100, 2)
      (defaults to 100.0 if weighted_required is 0)

    Items are sorted by priority_score descending, then gap descending, then weight descending.
    """
    if not requirements:
        return ComputedGapAnalysis(
            readiness_percent=100.0,
            total_skills=0,
            skills_met=0,
            weighted_required=0,
            weighted_achieved=0,
            items=[],
        )

    items: List[ComputedGapItem] = []
    weighted_required = 0
    weighted_achieved = 0
    skills_met = 0

    for req in requirements:
        student_level = student_skill_levels.get(req.skill_id, 0)
        gap = max(req.required_level - student_level, 0)
        priority_score = gap * req.weight

        w_req = req.required_level * req.weight
        w_ach = min(student_level, req.required_level) * req.weight

        weighted_required += w_req
        weighted_achieved += w_ach

        if gap == 0:
            skills_met += 1

        items.append(
            ComputedGapItem(
                skill_id=req.skill_id,
                required_level=req.required_level,
                student_level=student_level,
                gap=gap,
                weight=req.weight,
                priority_score=priority_score,
                skill_name=req.skill_name,
            )
        )

    # Sort items by priority_score descending, then gap descending, then weight descending
    items.sort(key=lambda x: (x.priority_score, x.gap, x.weight), reverse=True)

    if weighted_required > 0:
        readiness_percent = round((weighted_achieved / weighted_required) * 100.0, 2)
    else:
        readiness_percent = 100.0

    return ComputedGapAnalysis(
        readiness_percent=readiness_percent,
        total_skills=len(requirements),
        skills_met=skills_met,
        weighted_required=weighted_required,
        weighted_achieved=weighted_achieved,
        items=items,
    )
