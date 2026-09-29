from fastapi.testclient import TestClient


def test_gap_analysis_lifecycle_and_calculations(seeded_client: TestClient):
    """Test creating and retrieving gap analysis snapshots for a student's career goal."""
    # 1. Create a user
    user_res = seeded_client.post("/api/v1/users", json={"email": "gap_student@example.com"})
    assert user_res.status_code == 201
    user_id = user_res.json()["id"]

    # 2. Get Backend Developer career ID
    careers_res = seeded_client.get("/api/v1/careers")
    careers = careers_res.json()
    backend = next(c for c in careers if c["name"] == "Backend Developer")
    career_id = backend["id"]

    # Get skill IDs for Python and FastAPI from seeded catalog
    skills_res = seeded_client.get("/api/v1/skills")
    skills = skills_res.json()
    python_skill = next(s for s in skills if s["name"] == "Python")
    fastapi_skill = next(s for s in skills if s["name"] == "FastAPI")

    # 3. Add student skills: Python (level 2), FastAPI (level 5 - exceeds required 4)
    # Backend Developer has 6 skills: Python (req 4, wt 5), FastAPI (req 4, wt 4),
    # SQL (req 4, wt 5), System Design (req 3, wt 4), Git (req 3, wt 3), Docker (req 3, wt 3)
    seeded_client.post(
        f"/api/v1/users/{user_id}/skills",
        json={"skill_id": python_skill["id"], "level": 2},
    )
    seeded_client.post(
        f"/api/v1/users/{user_id}/skills",
        json={"skill_id": fastapi_skill["id"], "level": 5},
    )

    # 4. Create career goal
    goal_res = seeded_client.post(
        f"/api/v1/users/{user_id}/goals",
        json={"career_id": career_id, "status": "active"},
    )
    assert goal_res.status_code == 201
    goal_id = goal_res.json()["id"]

    # 5. Check 404 on GET latest before any analysis exists
    latest_404 = seeded_client.get(f"/api/v1/goals/{goal_id}/gap-analysis/latest")
    assert latest_404.status_code == 404

    # 6. Generate gap analysis snapshot
    create_analysis_res = seeded_client.post(f"/api/v1/goals/{goal_id}/gap-analysis")
    assert create_analysis_res.status_code == 201
    analysis = create_analysis_res.json()

    assert analysis["goal_id"] == goal_id
    assert analysis["total_skills"] == 6
    assert len(analysis["items"]) == 6
    assert analysis["skills_met"] == 1  # Only FastAPI is met/exceeded

    # Check items sorting by priority_score descending
    priority_scores = [item["priority_score"] for item in analysis["items"]]
    assert priority_scores == sorted(priority_scores, reverse=True)

    # Verify FastAPI item (exceeded level)
    fastapi_item = next(item for item in analysis["items"] if item["skill_id"] == fastapi_skill["id"])
    assert fastapi_item["student_level"] == 5
    assert fastapi_item["required_level"] == 4
    assert fastapi_item["gap"] == 0
    assert fastapi_item["priority_score"] == 0
    assert fastapi_item["skill"]["name"] == "FastAPI"

    # Verify Python item
    python_item = next(item for item in analysis["items"] if item["skill_id"] == python_skill["id"])
    assert python_item["student_level"] == 2
    assert python_item["required_level"] == 4
    assert python_item["gap"] == 2
    assert python_item["weight"] == 5
    assert python_item["priority_score"] == 10

    # 7. Get latest snapshot returns the created analysis
    latest_res = seeded_client.get(f"/api/v1/goals/{goal_id}/gap-analysis/latest")
    assert latest_res.status_code == 200
    assert latest_res.json()["id"] == analysis["id"]
    assert latest_res.json()["readiness_percent"] == analysis["readiness_percent"]

    # 8. Add another skill for user, trigger new analysis snapshot
    sql_skill = next(s for s in skills if s["name"] == "SQL & Relational Databases")
    seeded_client.post(
        f"/api/v1/users/{user_id}/skills",
        json={"skill_id": sql_skill["id"], "level": 4},
    )

    create_analysis_2 = seeded_client.post(f"/api/v1/goals/{goal_id}/gap-analysis")
    assert create_analysis_2.status_code == 201
    analysis_2 = create_analysis_2.json()

    assert analysis_2["id"] != analysis["id"]
    assert analysis_2["skills_met"] == 2  # FastAPI and SQL now met
    assert analysis_2["readiness_percent"] > analysis["readiness_percent"]

    # Verify GET latest returns the new snapshot
    latest_res_2 = seeded_client.get(f"/api/v1/goals/{goal_id}/gap-analysis/latest")
    assert latest_res_2.status_code == 200
    assert latest_res_2.json()["id"] == analysis_2["id"]


def test_gap_analysis_not_found_errors(client: TestClient):
    """Test 404 responses for nonexistent career goals."""
    # 1. POST gap analysis for nonexistent goal
    post_res = client.post("/api/v1/goals/99999/gap-analysis")
    assert post_res.status_code == 404

    # 2. GET latest gap analysis for nonexistent goal
    get_res = client.get("/api/v1/goals/99999/gap-analysis/latest")
    assert get_res.status_code == 404
