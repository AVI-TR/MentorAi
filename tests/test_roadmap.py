from fastapi.testclient import TestClient


def _setup_goal_with_analysis(seeded_client: TestClient):
    user_id = seeded_client.post("/api/v1/users", json={"email": "roadmap@example.com"}).json()["id"]
    career = next(c for c in seeded_client.get("/api/v1/careers").json() if c["name"] == "Backend Developer")
    skills = {s["name"]: s["id"] for s in seeded_client.get("/api/v1/skills").json()}

    ratings = {
        "Python": 2,
        "FastAPI": 4,
        "SQL & Relational Databases": 4,
        "System Design & Architecture": 3,
        "Git & Version Control": 3,
        "Docker & Containerization": 3,
    }
    for name, level in ratings.items():
        seeded_client.post(f"/api/v1/users/{user_id}/skills", json={"skill_id": skills[name], "level": level})

    goal = seeded_client.post(f"/api/v1/users/{user_id}/goals", json={"career_id": career["id"], "status": "active"}).json()
    analysis = seeded_client.post(f"/api/v1/goals/{goal['id']}/gap-analysis").json()
    return user_id, goal["id"], analysis


def test_roadmap_requires_gap_analysis(seeded_client: TestClient):
    user_id = seeded_client.post("/api/v1/users", json={"email": "no-analysis@example.com"}).json()["id"]
    career = next(c for c in seeded_client.get("/api/v1/careers").json() if c["name"] == "Backend Developer")
    goal = seeded_client.post(f"/api/v1/users/{user_id}/goals", json={"career_id": career["id"], "status": "active"}).json()
    assert seeded_client.post(f"/api/v1/goals/{goal['id']}/roadmap").status_code == 404
    assert seeded_client.get(f"/api/v1/goals/{goal['id']}/roadmap/latest").status_code == 404


def test_create_latest_and_progress(seeded_client: TestClient):
    _, goal_id, analysis = _setup_goal_with_analysis(seeded_client)
    create = seeded_client.post(f"/api/v1/goals/{goal_id}/roadmap")
    assert create.status_code == 201
    roadmap = create.json()
    assert roadmap["version"] == 1
    assert roadmap["status"] == "active"
    assert roadmap["gap_analysis_id"] == analysis["id"]
    assert roadmap["total"] == 3
    assert roadmap["done"] == 0
    assert roadmap["percent"] == 0
    assert [item["position"] for item in roadmap["items"]] == [1, 2, 3]
    assert all(item["status"] == "todo" for item in roadmap["items"])
    assert all(item["module"]["skill"]["name"] == "Python" for item in roadmap["items"])

    latest = seeded_client.get(f"/api/v1/goals/{goal_id}/roadmap/latest")
    assert latest.status_code == 200
    first_item = roadmap["items"][0]
    update = seeded_client.patch(f"/api/v1/goals/{goal_id}/roadmap/items/{first_item['id']}", json={"status": "done"})
    assert update.status_code == 200
    latest_after = seeded_client.get(f"/api/v1/goals/{goal_id}/roadmap/latest")
    assert latest_after.json()["done"] == 1
    assert latest_after.json()["total"] == 3
    assert latest_after.json()["percent"] == 33.33


def test_new_roadmap_supersedes_previous(seeded_client: TestClient):
    _, goal_id, _ = _setup_goal_with_analysis(seeded_client)
    first = seeded_client.post(f"/api/v1/goals/{goal_id}/roadmap").json()
    done_item = first["items"][0]
    in_progress_item = first["items"][1]
    assert seeded_client.patch(f"/api/v1/goals/{goal_id}/roadmap/items/{done_item['id']}", json={"status": "done"}).status_code == 200
    assert seeded_client.patch(f"/api/v1/goals/{goal_id}/roadmap/items/{in_progress_item['id']}", json={"status": "in_progress"}).status_code == 200

    second = seeded_client.post(f"/api/v1/goals/{goal_id}/roadmap")
    assert second.status_code == 201
    second_body = second.json()
    assert second_body["version"] == 2
    assert second_body["id"] != first["id"]

    statuses = {item["module_id"]: item["status"] for item in second_body["items"]}
    assert statuses[done_item["module_id"]] == "done"
    assert statuses[in_progress_item["module_id"]] == "in_progress"

    old_item_update = seeded_client.patch(
        f"/api/v1/goals/{goal_id}/roadmap/items/{done_item['id']}",
        json={"status": "todo"},
    )
    assert old_item_update.status_code == 404


def test_roadmap_item_must_belong_to_goal(seeded_client: TestClient):
    _, goal_one, _ = _setup_goal_with_analysis(seeded_client)
    first = seeded_client.post(f"/api/v1/goals/{goal_one}/roadmap").json()
    user_two = seeded_client.post("/api/v1/users", json={"email": "roadmap-two@example.com"}).json()["id"]
    career = next(c for c in seeded_client.get("/api/v1/careers").json() if c["name"] == "Frontend Developer")
    goal_two = seeded_client.post(f"/api/v1/users/{user_two}/goals", json={"career_id": career["id"], "status": "active"}).json()["id"]
    response = seeded_client.patch(f"/api/v1/goals/{goal_two}/roadmap/items/{first['items'][0]['id']}", json={"status": "done"})
    assert response.status_code == 404


def test_learning_module_seed_is_complete_and_idempotent(db_session):
    from sqlalchemy import select
    from app.db.seed import seed_database
    from app.models.learning_module import LearningModule
    seed_database(db_session)
    first = list(db_session.scalars(select(LearningModule)).all())
    seed_database(db_session)
    second = list(db_session.scalars(select(LearningModule)).all())
    skill_count = len({module.skill_id for module in first})
    assert len(first) == skill_count * 5
    assert len(second) == len(first)
    assert {(module.skill_id, module.to_level) for module in second} == {(module.skill_id, module.to_level) for module in first}
