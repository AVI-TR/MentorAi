from fastapi.testclient import TestClient


def test_create_and_get_user(client: TestClient):
    res = client.post("/api/v1/users", json={"email": "student@example.com"})
    assert res.status_code == 201
    user = res.json()
    assert user["email"] == "student@example.com"
    user_id = user["id"]

    get_res = client.get(f"/api/v1/users/{user_id}")
    assert get_res.status_code == 200
    assert get_res.json()["email"] == "student@example.com"


def test_idempotent_user_creation(client: TestClient):
    first = client.post("/api/v1/users", json={"email": "unique@example.com"})
    assert first.status_code == 201

    second = client.post("/api/v1/users", json={"email": "unique@example.com"})
    assert second.status_code == 200
    assert second.json()["id"] == first.json()["id"]

    list_res = client.get("/api/v1/users")
    assert list_res.status_code != 200


def test_user_student_profile_lifecycle(client: TestClient):
    user_res = client.post("/api/v1/users", json={"email": "profile_test@example.com"})
    user_id = user_res.json()["id"]

    not_found_res = client.get(f"/api/v1/users/{user_id}/profile")
    assert not_found_res.status_code == 404

    create_profile_res = client.post(
        f"/api/v1/users/{user_id}/profile",
        json={
            "education": "B.Tech Computer Science",
            "year": "3rd Year",
            "interests": "Backend Development, Cloud Computing",
        },
    )
    assert create_profile_res.status_code == 201
    assert create_profile_res.json()["education"] == "B.Tech Computer Science"

    get_profile_res = client.get(f"/api/v1/users/{user_id}/profile")
    assert get_profile_res.status_code == 200
    assert get_profile_res.json()["interests"] == "Backend Development, Cloud Computing"

    update_res = client.put(f"/api/v1/users/{user_id}/profile", json={"year": "4th Year"})
    assert update_res.status_code == 200
    assert update_res.json()["year"] == "4th Year"
    assert update_res.json()["education"] == "B.Tech Computer Science"

    user_detail_res = client.get(f"/api/v1/users/{user_id}")
    assert user_detail_res.status_code == 200
    assert user_detail_res.json()["profile"]["year"] == "4th Year"

    upsert_existing_res = client.post(
        f"/api/v1/users/{user_id}/profile",
        json={
            "education": "M.Tech Computer Science",
            "year": "1st Year",
            "interests": "Distributed Systems",
        },
    )
    assert upsert_existing_res.status_code == 200
    assert upsert_existing_res.json()["education"] == "M.Tech Computer Science"
