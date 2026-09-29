# Mentor AI

> **An AI Career & Learning Mentor** providing personalized career roadmaps, adaptive learning modules, progress tracking, study PDFs, and intelligent practice assessments.

---

## Product Vision & MVP Flow

Mentor AI guides learners from their current state to their target career outcomes through a structured, adaptive learning lifecycle:

```text
User Profile
  └──> Career Goal
        └──> Skill Gap Analysis
              └──> Personalized Roadmap
                    └──> Learning Module
                          ├──> Personalized Study PDF
                          └──> Quiz & Practice
                                └──> Progress Tracking
                                      └──> Adaptive Roadmap (Dynamic Refinement)
```

---

## Architecture & Project Structure

The project uses a modular, layered architecture built on **FastAPI**, **SQLAlchemy 2.0 (Synchronous)**, and **Pydantic v2**. For detailed design standards and guidelines, see [docs/architecture.md](docs/architecture.md).

```text
MentorAi/
├── .env.example              # Sample environment variables
├── .env                      # Local environment configuration (git-ignored)
├── .gitignore                # Standard Python/IDE ignores
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
│
├── docs/
│   └── architecture.md       # Architecture Decision Record (ADR)
│
├── app/
│   ├── __init__.py
│   ├── main.py               # Application factory, lifespan, CORS, and root routes
│   │
│   ├── api/                  # API routing layer
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py     # Aggregates versioned routes
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── health.py # Health & DB status endpoint
│   │
│   ├── core/                 # Global configuration, logging, and exceptions
│   │   ├── __init__.py
│   │   ├── config.py         # Pydantic BaseSettings for env loading
│   │   ├── exceptions.py     # Custom HTTP exceptions
│   │   └── logging.py        # Centralized logger configuration
│   │
│   ├── db/                   # Database session & ORM base
│   │   ├── __init__.py
│   │   ├── base.py           # DeclarativeBase, PrimaryKeyMixin & TimestampMixin
│   │   └── session.py        # Synchronous engine & session dependency
│   │
│   ├── models/               # Central ORM model registry
│   │   └── __init__.py
│   │
│   ├── schemas/              # Pydantic schemas (request/response validation)
│   │   ├── __init__.py
│   │   └── health.py         # Health schemas
│   │
│   └── services/             # Business logic layer (owns transactions)
│       └── __init__.py
│
└── tests/                    # Pytest test suite
    ├── __init__.py
    ├── conftest.py           # Pytest fixtures & in-memory test database
    └── test_health.py        # Unit & integration tests
```

---

##  Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Git

### 2. Environment Setup
Create and activate a virtual environment:

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
# Production dependencies
pip install -r requirements.txt

# Or development & test dependencies
pip install -r requirements-dev.txt
```

### 4. Configure Environment
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 5. Run the Server
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- API Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- API Docs (ReDoc): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- Health Check: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)

---

## Running Tests

Execute the automated test suite with `pytest`:

```bash
pytest -v
```
