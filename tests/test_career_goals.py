from fastapi.testclient import TestClient


def test_career_goals_lifecycle(seeded_client: TestClient):
    """Test full lifecycle of user career goals."""
    # 1. Create a user
    user_res = seeded_client.post("/api/v1/users", json={"email": "goal_user@example.com"})
    user_id = user_res.json()["id"]

    # 2. Get career
    careers_res = seeded_client.get("/api/v1/careers")
    careers = careers_res.json()
    backend = next(c for c in careers if c["name"] == "Backend Developer")

    # 3. Create career goal
    create_goal_res = seeded_client.post(
        f"/api/v1/users/{user_id}/goals",
        json={
            "career_id": backend["id"],
            "target_date": "2026-12-31T00:00:00Z",
            "status": "active",
        },
    )
    assert create_goal_res.status_code == 201
    goal = create_goal_res.json()
    assert goal["career_id"] == backend["id"]
    assert goal["status"] == "active"
    goal_id = goal["id"]

    # 4. List career goals for user
    list_res = seeded_client.get(f"/api/v1/users/{user_id}/goals")
    assert list_res.status_code == 200
    goals = list_res.json()
    assert len(goals) == 1
    assert goals[0]["career"]["name"] == "Backend Developer"

    # 5. Update goal status
    patch_res = seeded_client.patch(
        f"/api/v1/users/{user_id}/goals/{goal_id}",
        json={"status": "completed"},
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "completed"

    # 6. Delete goal
    del_res = seeded_client.delete(f"/api/v1/users/{user_id}/goals/{goal_id}")
    assert del_res.status_code == 204

    # 7. Verify list is empty
    empty_list_res = seeded_client.get(f"/api/v1/users/{user_id}/goals")
    assert empty_list_res.status_code == 200
    assert len(empty_list_res.json()) == 0


def test_career_goal_not_found_errors(seeded_client: TestClient):
    """Test 404 when creating goal for nonexistent user or career."""
    # 1. Nonexistent user
    res_user_404 = seeded_client.post(
        "/api/v1/users/99999/goals",
        json={"career_id": 1, "status": "active"},
    )
    assert res_user_404.status_code == 404

    # 2. Existing user, nonexistent career
    user_res = seeded_client.post("/api/v1/users", json={"email": "goal_404_user@example.com"})
    assert user_res.status_code == 201
    user_id = user_res.json()["id"]

    res_career_404 = seeded_client.post(
        f"/api/v1/users/{user_id}/goals",
        json={"career_id": 99999, "status": "active"},
    )
    assert res_career_404.status_code == 404
