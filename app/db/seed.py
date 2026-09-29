from sqlalchemy.orm import Session
from app.services.catalog_service import catalog_service


def seed_database(db: Session) -> None:
    """Seed initial catalog data into database."""
    catalog_service.seed_catalog(db)
