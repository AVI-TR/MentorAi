from fastapi.testclient import TestClient


def _career_ids(seeded_client: TestClient):
    careers = seeded_client.get("/api/v1/careers").json()
    backend = next(c for c in careers if c["name"] == "Backend Developer")
    frontend = next(c for c in careers if c["name"] == "Frontend Developer")
    return backend["id"], frontend["id"]


def test_active_goal_rule(seeded_client: TestClient):
    user_id = seeded_client.post("/api/v1/users", json={"email": "goal_rule@example.com"}).json()["id"]
    backend_id, frontend_id = _career_ids(seeded_client)

    first = seeded_client.post(f"/api/v1/users/{user_id}/goals", json={"career_id": backend_id, "status": "active"})
    assert first.status_code == 201
    first_goal = first.json()

    same_career = seeded_client.post(f"/api/v1/users/{user_id}/goals", json={"career_id": backend_id, "status": "active"})
    assert same_career.status_code == 200
    assert same_career.json()["id"] == first_goal["id"]

    different = seeded_client.post(f"/api/v1/users/{user_id}/goals", json={"career_id": frontend_id, "status": "active"})
    assert different.status_code == 201
    second_goal = different.json()
    assert second_goal["id"] != first_goal["id"]
    assert second_goal["status"] == "active"

    goals = seeded_client.get(f"/api/v1/users/{user_id}/goals").json()
    by_id = {goal["id"]: goal for goal in goals}
    assert by_id[first_goal["id"]]["status"] == "paused"
    assert by_id[second_goal["id"]]["status"] == "active"
    assert sum(goal["status"] == "active" for goal in goals) == 1

    reactivated = seeded_client.post(f"/api/v1/users/{user_id}/goals", json={"career_id": backend_id, "status": "active"})
    assert reactivated.status_code == 200
    assert reactivated.json()["id"] == first_goal["id"]
    assert reactivated.json()["status"] == "active"


def test_career_goals_lifecycle(seeded_client: TestClient):
    user_id = seeded_client.post("/api/v1/users", json={"email": "goal_user@example.com"}).json()["id"]
    backend_id, _ = _career_ids(seeded_client)

    create_goal_res = seeded_client.post(
        f"/api/v1/users/{user_id}/goals",
        json={"career_id": backend_id, "target_date": "2026-12-31T00:00:00Z", "status": "active"},
    )
    assert create_goal_res.status_code == 201
    goal_id = create_goal_res.json()["id"]

    assert seeded_client.get(f"/api/v1/users/{user_id}/goals").status_code == 200
    patch_res = seeded_client.patch(f"/api/v1/users/{user_id}/goals/{goal_id}", json={"status": "completed"})
    assert patch_res.status_code == 200
    assert seeded_client.delete(f"/api/v1/users/{user_id}/goals/{goal_id}").status_code == 204
    assert seeded_client.get(f"/api/v1/users/{user_id}/goals").json() == []


def test_career_goal_not_found_errors(seeded_client: TestClient):
    assert seeded_client.post("/api/v1/users/99999/goals", json={"career_id": 1, "status": "active"}).status_code == 404
    user_id = seeded_client.post("/api/v1/users", json={"email": "goal_404_user@example.com"}).json()["id"]
    assert seeded_client.post(f"/api/v1/users/{user_id}/goals", json={"career_id": 99999, "status": "active"}).status_code == 404
