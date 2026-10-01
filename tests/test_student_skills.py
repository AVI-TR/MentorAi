from fastapi.testclient import TestClient


def test_student_skills_crud_and_validation(seeded_client: TestClient):
    user_id = seeded_client.post("/api/v1/users", json={"email": "skills_user@example.com"}).json()["id"]
    python_skill = next(s for s in seeded_client.get("/api/v1/skills").json() if s["name"] == "Python")

    add_res = seeded_client.post(f"/api/v1/users/{user_id}/skills", json={"skill_id": python_skill["id"], "level": 3, "source": "self_assessed"})
    assert add_res.status_code == 201
    upsert_res = seeded_client.post(f"/api/v1/users/{user_id}/skills", json={"skill_id": python_skill["id"], "level": 4, "source": "quiz"})
    assert upsert_res.status_code == 201

    list_res = seeded_client.get(f"/api/v1/users/{user_id}/skills")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1
    assert list_res.json()[0]["level"] == 4

    assert seeded_client.post(f"/api/v1/users/{user_id}/skills", json={"skill_id": python_skill["id"], "level": 0}).status_code == 422
    assert seeded_client.post(f"/api/v1/users/{user_id}/skills", json={"skill_id": python_skill["id"], "level": 6}).status_code == 422
    assert seeded_client.delete(f"/api/v1/users/{user_id}/skills/{python_skill['id']}").status_code == 204
    assert seeded_client.get(f"/api/v1/users/{user_id}/skills").json() == []


def test_batch_student_skill_upsert_is_atomic(seeded_client):
    user_id = seeded_client.post("/api/v1/users", json={"email": "batch_skills@example.com"}).json()["id"]
    skills = seeded_client.get("/api/v1/skills").json()
    python_id = next(s["id"] for s in skills if s["name"] == "Python")
    fastapi_id = next(s["id"] for s in skills if s["name"] == "FastAPI")

    batch = seeded_client.put(
        f"/api/v1/users/{user_id}/skills",
        json=[
            {"skill_id": python_id, "level": 3, "source": "self_assessed"},
            {"skill_id": fastapi_id, "level": 4, "source": "self_assessed"},
        ],
    )
    assert batch.status_code == 200
    assert {item["skill_id"] for item in batch.json()} == {python_id, fastapi_id}

    invalid_batch = seeded_client.put(
        f"/api/v1/users/{user_id}/skills",
        json=[
            {"skill_id": python_id, "level": 5, "source": "self_assessed"},
            {"skill_id": 99999, "level": 4, "source": "self_assessed"},
        ],
    )
    assert invalid_batch.status_code == 404

    duplicate_batch = seeded_client.put(f"/api/v1/users/{user_id}/skills", json=[{"skill_id": python_id, "level": 4, "source": "self_assessed"}, {"skill_id": python_id, "level": 5, "source": "self_assessed"}])
    assert duplicate_batch.status_code == 422

    current = {item["skill_id"]: item for item in seeded_client.get(f"/api/v1/users/{user_id}/skills").json()}
    assert current[python_id]["level"] == 3
    assert current[fastapi_id]["level"] == 4

    delete_with_zero = seeded_client.put(
        f"/api/v1/users/{user_id}/skills",
        json=[
            {"skill_id": python_id, "level": 0, "source": "self_assessed"},
            {"skill_id": fastapi_id, "level": 4, "source": "self_assessed"},
        ],
    )
    assert delete_with_zero.status_code == 200
    assert {item["skill_id"] for item in delete_with_zero.json()} == {fastapi_id}
