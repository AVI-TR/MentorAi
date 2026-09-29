from fastapi.testclient import TestClient


def test_create_and_get_user(client: TestClient):
    """Test creating and retrieving a user."""
    # Create user
    res = client.post("/api/v1/users", json={"email": "student@example.com"})
    assert res.status_code == 201
    user = res.json()
    assert user["email"] == "student@example.com"
    user_id = user["id"]

    # Get user
    get_res = client.get(f"/api/v1/users/{user_id}")
    assert get_res.status_code == 200
    assert get_res.json()["email"] == "student@example.com"


def test_duplicate_user_email(client: TestClient):
    """Test creating duplicate user email results in 409 conflict."""
    client.post("/api/v1/users", json={"email": "unique@example.com"})
    dup_res = client.post("/api/v1/users", json={"email": "unique@example.com"})
    assert dup_res.status_code == 409


def test_user_student_profile_lifecycle(client: TestClient):
    """Test creating, reading, and updating student profile."""
    # 1. Create user
    user_res = client.post("/api/v1/users", json={"email": "profile_test@example.com"})
    user_id = user_res.json()["id"]

    # 2. Get non-existent profile returns 404
    not_found_res = client.get(f"/api/v1/users/{user_id}/profile")
    assert not_found_res.status_code == 404

    # 3. Create profile
    create_profile_res = client.post(
        f"/api/v1/users/{user_id}/profile",
        json={
            "education": "B.Tech Computer Science",
            "year": "3rd Year",
            "interests": "Backend Development, Cloud Computing",
        },
    )
    assert create_profile_res.status_code == 201
    profile = create_profile_res.json()
    assert profile["education"] == "B.Tech Computer Science"
    assert profile["year"] == "3rd Year"

    # 4. Get profile
    get_profile_res = client.get(f"/api/v1/users/{user_id}/profile")
    assert get_profile_res.status_code == 200
    assert get_profile_res.json()["interests"] == "Backend Development, Cloud Computing"

    # 5. Update profile
    update_res = client.put(
        f"/api/v1/users/{user_id}/profile",
        json={"year": "4th Year"},
    )
    assert update_res.status_code == 200
    assert update_res.json()["year"] == "4th Year"
    assert update_res.json()["education"] == "B.Tech Computer Science"

    # 6. User detail returns profile
    user_detail_res = client.get(f"/api/v1/users/{user_id}")
    assert user_detail_res.status_code == 200
    assert user_detail_res.json()["profile"]["year"] == "4th Year"

    # 7. POST on existing profile updates and returns 200 OK
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
    assert upsert_existing_res.json()["year"] == "1st Year"
