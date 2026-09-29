from fastapi.testclient import TestClient


def test_student_skills_crud_and_validation(seeded_client: TestClient):
    """Test full lifecycle of student assessed skills."""
    # 1. Create a user
    user_res = seeded_client.post("/api/v1/users", json={"email": "skills_user@example.com"})
    user_id = user_res.json()["id"]

    # 2. Get existing skills from catalog
    skills_res = seeded_client.get("/api/v1/skills")
    skills = skills_res.json()
    python_skill = next(s for s in skills if s["name"] == "Python")

    # 3. Add student skill
    add_res = seeded_client.post(
        f"/api/v1/users/{user_id}/skills",
        json={"skill_id": python_skill["id"], "level": 3, "source": "self_assessed"},
    )
    assert add_res.status_code == 201
    assert add_res.json()["level"] == 3

    # 4. Upserting same skill updates the level
    upsert_res = seeded_client.post(
        f"/api/v1/users/{user_id}/skills",
        json={"skill_id": python_skill["id"], "level": 4, "source": "quiz"},
    )
    assert upsert_res.status_code == 201
    assert upsert_res.json()["level"] == 4
    assert upsert_res.json()["source"] == "quiz"

    # 5. List skills for user
    list_res = seeded_client.get(f"/api/v1/users/{user_id}/skills")
    assert list_res.status_code == 200
    user_skills = list_res.json()
    assert len(user_skills) == 1
    assert user_skills[0]["skill"]["name"] == "Python"
    assert user_skills[0]["level"] == 4

    # 6. Validation: level out of bounds (<1 or >5)
    invalid_low = seeded_client.post(
        f"/api/v1/users/{user_id}/skills",
        json={"skill_id": python_skill["id"], "level": 0},
    )
    assert invalid_low.status_code == 422

    invalid_high = seeded_client.post(
        f"/api/v1/users/{user_id}/skills",
        json={"skill_id": python_skill["id"], "level": 6},
    )
    assert invalid_high.status_code == 422

    # 7. Delete skill
    del_res = seeded_client.delete(f"/api/v1/users/{user_id}/skills/{python_skill['id']}")
    assert del_res.status_code == 204

    # 8. List skills should be empty
    list_after_res = seeded_client.get(f"/api/v1/users/{user_id}/skills")
    assert list_after_res.status_code == 200
    assert len(list_after_res.json()) == 0
