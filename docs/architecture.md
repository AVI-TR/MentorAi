# Mentor AI - Architecture Decision Record (ADR)

## 1. System Overview & Layered Architecture

Mentor AI follows a layered, modular architecture:

```text
app/
├── api/          # HTTP transport layer: routing, parameter extraction, status codes
├── schemas/      # Pydantic models: request/response data contracts and serialization
├── models/       # SQLAlchemy ORM entity definitions and relationships
├── services/     # Business logic layer: orchestrates domain flows and transaction boundaries
├── core/         # Cross-cutting concerns: config (Pydantic Settings), logging, exceptions
└── db/           # Persistence foundations: engine, session management, base models
```

---

## 2. Core Architectural Decisions

### Synchronous SQLAlchemy
* **Decision**: Use synchronous SQLAlchemy 2.0 with standard blocking sessions.
* **Rationale**: Simplifies transaction lifecycles, debugging, and service logic without async overhead or greenlet complexity, perfectly suited for the relational workload and roadmap generation pipelines.
* **Default URL**: `sqlite:///./mentor_ai.db`

### Transaction Ownership & Session Lifecycle
* **Decision**: Routers contain **no business logic**.
* **Services Own Transactions**: Services are responsible for initiating operations, executing domain rules, and committing transactions (`db.commit()`).
* **`get_db` Lifecycle**: The `get_db` dependency opens a new session, yields it to the request handler, rolls back on unhandled exceptions (`db.rollback()`), and guarantees session cleanup (`db.close()`). `get_db` does **not** auto-commit.

### Primary Keys & Model Standards
* **Decision**: Use integer autoincrement primary keys consistently across all entity models (`PrimaryKeyMixin` with `id: Mapped[int]`).
* **Auditability**: Entities requiring creation and modification tracking inherit from `TimestampMixin` (`created_at`, `updated_at`).

### Central Model Registration
* **Decision**: All ORM models are registered in `app/models/__init__.py`.
* **Rationale**: Guarantees that `Base.metadata.create_all(bind=engine)` and future migration tools (Alembic) discover all entity schemas at startup without missing tables.

### Security & CORS
* **Decision**: Restrict CORS to explicit local development origins (`http://localhost:3000`, `http://localhost:5173`, `http://127.0.0.1:3000`, `http://127.0.0.1:5173`).
* **Rationale**: Prevent wildcard (`*`) origins when credentials/cookies are enabled, adhering to strict CORS security standards.

### Environment Defaults
* **`DEBUG`**: `False` (explicitly enabled only for local development debugging).
* **`HOST`**: `127.0.0.1` (safe local loopback default).
* **`PORT`**: `8000`.
* **`SQL_ECHO`**: `False` (SQL statement echo disabled by default to avoid noisy logging).
