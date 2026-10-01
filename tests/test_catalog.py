from fastapi.testclient import TestClient
from sqlalchemy import text


def test_seed_catalog_contains_backend_developer(seeded_client: TestClient):
    response = seeded_client.get("/api/v1/careers")
    assert response.status_code == 200
    careers = response.json()
    assert len(careers) >= 3
    career_names = [c["name"] for c in careers]
    assert "Backend Developer" in career_names
    assert "Frontend Developer" in career_names
    assert "Data Scientist / AI Engineer" in career_names


def test_get_career_detail_with_skills(seeded_client: TestClient):
    response = seeded_client.get("/api/v1/careers")
    backend = next(c for c in response.json() if c["name"] == "Backend Developer")
    detail_res = seeded_client.get(f"/api/v1/careers/{backend['id']}")
    assert detail_res.status_code == 200
    assert len(detail_res.json()["career_skills"]) > 0


def test_create_career_and_skills(client: TestClient):
    skill_res = client.post("/api/v1/skills", json={"name": "Rust", "category": "Programming"})
    assert skill_res.status_code == 201
    skill_id = skill_res.json()["id"]

    assert client.post("/api/v1/skills", json={"name": "Rust", "category": "Programming"}).status_code == 409

    career_res = client.post("/api/v1/careers", json={"name": "Systems Engineer", "description": "Low-level systems programming."})
    assert career_res.status_code == 201
    career_id = career_res.json()["id"]

    map_res = client.post(f"/api/v1/careers/{career_id}/skills", json={"skill_id": skill_id, "required_level": 5, "weight": 5})
    assert map_res.status_code == 201
    assert map_res.json()["skill"]["name"] == "Rust"

    assert len(client.get(f"/api/v1/careers/{career_id}").json()["career_skills"]) == 1


def test_list_skills_filter(seeded_client: TestClient):
    response = seeded_client.get("/api/v1/skills?category=Programming")
    assert response.status_code == 200
    assert all(s["category"] == "Programming" for s in response.json())


def test_catalog_not_found_errors(client: TestClient):
    assert client.get("/api/v1/careers/99999").status_code == 404
    assert client.get("/api/v1/skills/99999").status_code == 404

    create_career_res = client.post("/api/v1/careers", json={"name": "DevOps Engineer", "description": "CI/CD and infrastructure."})
    career_id = create_career_res.json()["id"]

    assert client.post(f"/api/v1/careers/{career_id}/skills", json={"skill_id": 99999, "required_level": 3, "weight": 3}).status_code == 404

    create_skill_res = client.post("/api/v1/skills", json={"name": "Kubernetes", "category": "DevOps"})
    skill_id = create_skill_res.json()["id"]
    assert client.post(f"/api/v1/careers/99999/skills", json={"skill_id": skill_id, "required_level": 3, "weight": 3}).status_code == 404


def test_sqlite_foreign_keys_are_enabled(db_session):
    result = db_session.execute(text("PRAGMA foreign_keys")).scalar_one()
    assert result == 1
