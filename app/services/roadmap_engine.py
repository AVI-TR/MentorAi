"""Deterministic roadmap planning engine. No database or external dependencies."""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RoadmapGapItem:
    skill_id: int
    student_level: int
    required_level: int
    gap: int
    priority_score: int


@dataclass(frozen=True)
class RoadmapModule:
    module_id: int
    skill_id: int
    to_level: int


@dataclass(frozen=True)
class RoadmapPlan:
    module_ids: List[int]


def build_roadmap(
    gap_items: List[RoadmapGapItem],
    available_modules: List[RoadmapModule],
) -> RoadmapPlan:
    """Build an ordered list of learning modules from gap analysis data."""
    modules_by_skill_level = {
        (module.skill_id, module.to_level): module
        for module in available_modules
    }

    ordered_gaps = sorted(
        (item for item in gap_items if item.gap > 0),
        key=lambda item: (-item.priority_score, item.skill_id),
    )

    module_ids: List[int] = []
    for item in ordered_gaps:
        start_level = max(item.student_level + 1, 1)
        end_level = min(item.required_level, 5)
        for level in range(start_level, end_level + 1):
            module = modules_by_skill_level.get((item.skill_id, level))
            if module is not None:
                module_ids.append(module.module_id)

    return RoadmapPlan(module_ids=module_ids)
