from app.services.gap_engine import (
    ComputedGapAnalysis,
    SkillRequirement,
    calculate_skill_gap,
)


def test_gap_engine_pure_calculation():
    """Test standard deterministic gap calculation across multiple skills."""
    requirements = [
        SkillRequirement(skill_id=1, required_level=4, weight=5, skill_name="Python"),
        SkillRequirement(skill_id=2, required_level=4, weight=4, skill_name="FastAPI"),
        SkillRequirement(skill_id=3, required_level=3, weight=3, skill_name="SQL"),
    ]
    # Student has Python at level 2, SQL at level 3, missing FastAPI
    student_skills = {
        1: 2,
        3: 3,
    }

    result: ComputedGapAnalysis = calculate_skill_gap(requirements, student_skills)

    # Required weights: (4*5) + (4*4) + (3*3) = 20 + 16 + 9 = 45
    assert result.weighted_required == 45

    # Achieved weights:
    # Python: min(2, 4) * 5 = 10
    # FastAPI: min(0, 4) * 4 = 0
    # SQL: min(3, 3) * 3 = 9
    # Total achieved = 10 + 0 + 9 = 19
    assert result.weighted_achieved == 19

    # Readiness: (19 / 45) * 100 = 42.22%
    assert result.readiness_percent == 42.22
    assert result.total_skills == 3
    assert result.skills_met == 1  # Only SQL is fully met

    # Check item calculations and ordering (highest priority_score first)
    # FastAPI: gap = 4, priority_score = 4 * 4 = 16
    # Python: gap = 2, priority_score = 2 * 5 = 10
    # SQL: gap = 0, priority_score = 0 * 3 = 0
    items = result.items
    assert len(items) == 3
    assert items[0].skill_id == 2  # FastAPI has highest priority
    assert items[0].student_level == 0
    assert items[0].gap == 4
    assert items[0].priority_score == 16

    assert items[1].skill_id == 1  # Python
    assert items[1].student_level == 2
    assert items[1].gap == 2
    assert items[1].priority_score == 10

    assert items[2].skill_id == 3  # SQL
    assert items[2].student_level == 3
    assert items[2].gap == 0
    assert items[2].priority_score == 0


def test_gap_engine_missing_skills_default_to_zero():
    """Verify missing student skills are treated as student_level = 0."""
    requirements = [
        SkillRequirement(skill_id=10, required_level=5, weight=5, skill_name="Docker"),
    ]
    student_skills = {}  # No skills

    result = calculate_skill_gap(requirements, student_skills)

    assert result.total_skills == 1
    assert result.skills_met == 0
    assert result.weighted_required == 25
    assert result.weighted_achieved == 0
    assert result.readiness_percent == 0.0

    item = result.items[0]
    assert item.student_level == 0
    assert item.gap == 5
    assert item.priority_score == 25


def test_gap_engine_exceeded_skills_capped_at_required():
    """Verify that student skills exceeding the required level are capped at min(student, required)."""
    requirements = [
        SkillRequirement(skill_id=1, required_level=2, weight=4, skill_name="Git"),
        SkillRequirement(skill_id=2, required_level=3, weight=5, skill_name="Linux"),
    ]
    # Student has level 5 for both (exceeding requirements)
    student_skills = {
        1: 5,
        2: 5,
    }

    result = calculate_skill_gap(requirements, student_skills)

    # Required: (2*4) + (3*5) = 8 + 15 = 23
    assert result.weighted_required == 23
    # Achieved should be capped: min(5, 2)*4 + min(5, 3)*5 = 8 + 15 = 23 (not 5*4 + 5*5)
    assert result.weighted_achieved == 23
    assert result.readiness_percent == 100.0
    assert result.skills_met == 2

    for item in result.items:
        assert item.gap == 0
        assert item.priority_score == 0


def test_gap_engine_empty_requirements():
    """Verify handling when a career track has no requirements."""
    result = calculate_skill_gap([], {})
    assert result.total_skills == 0
    assert result.skills_met == 0
    assert result.weighted_required == 0
    assert result.weighted_achieved == 0
    assert result.readiness_percent == 100.0
    assert result.items == []
