from fastapi.testclient import TestClient


def test_seed_catalog_contains_backend_developer(seeded_client: TestClient):
    """Verify default seeded careers include Backend Developer and mapped skills."""
    response = seeded_client.get("/api/v1/careers")
    assert response.status_code == 200
    careers = response.json()
    assert len(careers) >= 3

    career_names = [c["name"] for c in careers]
    assert "Backend Developer" in career_names
    assert "Frontend Developer" in career_names
    assert "Data Scientist / AI Engineer" in career_names


def test_get_career_detail_with_skills(seeded_client: TestClient):
    """Verify career detail endpoint includes required skills and levels."""
    # Find Backend Developer
    response = seeded_client.get("/api/v1/careers")
    careers = response.json()
    backend = next(c for c in careers if c["name"] == "Backend Developer")

    detail_res = seeded_client.get(f"/api/v1/careers/{backend['id']}")
    assert detail_res.status_code == 200
    detail = detail_res.json()

    assert detail["name"] == "Backend Developer"
    assert len(detail["career_skills"]) > 0

    skill_names = [cs["skill"]["name"] for cs in detail["career_skills"]]
    assert "Python" in skill_names
    assert "FastAPI" in skill_names
    assert "SQL & Relational Databases" in skill_names


def test_create_career_and_skills(client: TestClient):
    """Test creating a new career, skill, and mapping them."""
    # 1. Create skill
    skill_res = client.post(
        "/api/v1/skills",
        json={"name": "Rust", "category": "Programming"},
    )
    assert skill_res.status_code == 201
    skill_data = skill_res.json()
    skill_id = skill_data["id"]

    # 2. Duplicate skill returns 409
    dup_res = client.post(
        "/api/v1/skills",
        json={"name": "Rust", "category": "Programming"},
    )
    assert dup_res.status_code == 409

    # 3. Create career
    career_res = client.post(
        "/api/v1/careers",
        json={"name": "Systems Engineer", "description": "Low-level systems programming."},
    )
    assert career_res.status_code == 201
    career_data = career_res.json()
    career_id = career_data["id"]

    # 4. Map skill to career
    map_res = client.post(
        f"/api/v1/careers/{career_id}/skills",
        json={"skill_id": skill_id, "required_level": 5, "weight": 5},
    )
    assert map_res.status_code == 201
    map_data = map_res.json()
    assert map_data["skill"]["name"] == "Rust"
    assert map_data["required_level"] == 5

    # 5. Verify in career detail
    detail_res = client.get(f"/api/v1/careers/{career_id}")
    assert detail_res.status_code == 200
    assert len(detail_res.json()["career_skills"]) == 1


def test_list_skills_filter(seeded_client: TestClient):
    """Test filtering skills by category."""
    response = seeded_client.get("/api/v1/skills?category=Programming")
    assert response.status_code == 200
    skills = response.json()
    assert len(skills) > 0
    for s in skills:
        assert s["category"] == "Programming"


def test_catalog_not_found_errors(client: TestClient):
    """Test 404 responses for nonexistent career, skill, and invalid career-skill mapping."""
    # 1. Nonexistent career
    career_res = client.get("/api/v1/careers/99999")
    assert career_res.status_code == 404

    # 2. Nonexistent skill
    skill_res = client.get("/api/v1/skills/99999")
    assert skill_res.status_code == 404

    # 3. Create a valid career
    create_career_res = client.post(
        "/api/v1/careers",
        json={"name": "DevOps Engineer", "description": "CI/CD and infrastructure."},
    )
    assert create_career_res.status_code == 201
    career_id = create_career_res.json()["id"]

    # 4. Map nonexistent skill to existing career -> 404
    invalid_skill_res = client.post(
        f"/api/v1/careers/{career_id}/skills",
        json={"skill_id": 99999, "required_level": 3, "weight": 3},
    )
    assert invalid_skill_res.status_code == 404

    # 5. Map valid skill to nonexistent career -> 404
    create_skill_res = client.post(
        "/api/v1/skills",
        json={"name": "Kubernetes", "category": "DevOps"},
    )
    assert create_skill_res.status_code == 201
    skill_id = create_skill_res.json()["id"]

    invalid_career_res = client.post(
        "/api/v1/careers/99999/skills",
        json={"skill_id": skill_id, "required_level": 3, "weight": 3},
    )
    assert invalid_career_res.status_code == 404
