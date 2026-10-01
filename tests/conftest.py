import os
os.environ["ENVIRONMENT"] = "test"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.session import get_db
from app.main import app
from app.models import Base

test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool, future=True)


@event.listens_for(test_engine, "connect")
def enable_test_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=ON")
    finally:
        cursor.close()


TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False, expire_on_commit=False)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session):
    def override_get_db():
        try:
            yield db_session
        except Exception:
            db_session.rollback()
            raise
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def seeded_client(client: TestClient, db_session: Session):
    from app.services.catalog_service import catalog_service
    catalog_service.seed_catalog(db_session)
    return client
