# Mentor AI - Architecture Decision Record (ADR)

## 1. System Overview & Layered Architecture

Mentor AI follows a layered, modular architecture:

```text
app/
├── api/          # HTTP transport layer: routing, parameter extraction, status codes
├── schemas/      # Pydantic models: request/response data contracts and serialization
├── models/       # SQLAlchemy ORM entity definitions and relationships
├── services/     # Business logic layer: domain flows and transaction boundaries
├── core/         # Cross-cutting concerns: config, logging, exceptions
└── db/           # Persistence foundations: engine, session management, base models
```

## 2. Core Architectural Decisions

### Synchronous SQLAlchemy
* **Decision**: Use synchronous SQLAlchemy 2.0 with standard blocking sessions.
* **Default URL**: `sqlite:///./mentor_ai.db`

### Transaction Ownership & Session Lifecycle
* **Decision**: Routers contain no business logic.
* **Services Own Transactions**: Services execute domain rules and own transaction boundaries.
* **`get_db` Lifecycle**: The dependency opens a session, yields it, rolls back on unhandled exceptions, and guarantees cleanup.

### Skill Assessment Levels
Mentor AI uses a six-level self-assessment scale:

| Level | Meaning |
|---|---|
| 0 | None / no experience |
| 1 | Beginner |
| 2 | Basic |
| 3 | Working |
| 4 | Proficient |
| 5 | Expert |

A missing persisted student skill is interpreted as level **0** by the gap engine. Level 0 is therefore represented by absence of a `StudentSkill` row; the batch skills API accepts level 0 and removes that row.

### Identity Limitation
Email-only identity is a known MVP limitation. The current system uses email as the user lookup key and does not yet provide authentication, verified identity, or account/session security.

### Primary Keys & Model Standards
* **Decision**: Use integer autoincrement primary keys consistently.
* **Auditability**: Entities requiring creation/modification tracking inherit from `TimestampMixin`.

### Central Model Registration
* **Decision**: All ORM models are registered in `app/models/__init__.py`.

### Security & CORS
* **Decision**: Restrict CORS to explicit local development origins.

### Environment Defaults
* **`ENVIRONMENT`**: `development` by default; tests set it to `test`.
* **`DEBUG`**: `False`.
* **`HOST`**: `127.0.0.1`.
* **`PORT`**: `8000`.
* **`SQL_ECHO`**: `False`.
