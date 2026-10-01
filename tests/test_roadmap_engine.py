from app.services.roadmap_engine import RoadmapGapItem, RoadmapModule, build_roadmap


def test_gap_zero_contributes_no_modules():
    plan = build_roadmap(
        [RoadmapGapItem(skill_id=1, student_level=4, required_level=4, gap=0, priority_score=0)],
        [RoadmapModule(module_id=101, skill_id=1, to_level=5)],
    )
    assert plan.module_ids == []


def test_partial_gap_includes_next_levels_in_order():
    plan = build_roadmap(
        [RoadmapGapItem(skill_id=1, student_level=2, required_level=4, gap=2, priority_score=8)],
        [
            RoadmapModule(module_id=104, skill_id=1, to_level=4),
            RoadmapModule(module_id=103, skill_id=1, to_level=3),
            RoadmapModule(module_id=101, skill_id=1, to_level=1),
        ],
    )
    assert plan.module_ids == [103, 104]


def test_skill_with_no_modules_is_skipped():
    plan = build_roadmap(
        [RoadmapGapItem(skill_id=7, student_level=1, required_level=4, gap=3, priority_score=12)],
        [RoadmapModule(module_id=201, skill_id=8, to_level=2)],
    )
    assert plan.module_ids == []


def test_ordering_uses_priority_then_skill_id():
    plan = build_roadmap(
        [
            RoadmapGapItem(skill_id=5, student_level=1, required_level=2, gap=1, priority_score=4),
            RoadmapGapItem(skill_id=2, student_level=1, required_level=2, gap=1, priority_score=4),
            RoadmapGapItem(skill_id=9, student_level=1, required_level=2, gap=1, priority_score=6),
        ],
        [
            RoadmapModule(module_id=502, skill_id=5, to_level=2),
            RoadmapModule(module_id=202, skill_id=2, to_level=2),
            RoadmapModule(module_id=902, skill_id=9, to_level=2),
        ],
    )
    assert plan.module_ids == [902, 202, 502]


def test_student_at_level_zero_starts_at_level_one():
    plan = build_roadmap(
        [RoadmapGapItem(skill_id=1, student_level=0, required_level=3, gap=3, priority_score=15)],
        [
            RoadmapModule(module_id=101, skill_id=1, to_level=1),
            RoadmapModule(module_id=102, skill_id=1, to_level=2),
            RoadmapModule(module_id=103, skill_id=1, to_level=3),
        ],
    )
    assert plan.module_ids == [101, 102, 103]
