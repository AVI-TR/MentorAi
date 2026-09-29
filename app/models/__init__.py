"""Central ORM Model Registry.

All SQLAlchemy models must be imported here so that Base.metadata.create_all
discovers all model schemas at application startup and in migrations.
"""
from app.db.base import Base

# Future domain models will be imported here:
# from app.models.user import User
# from app.models.roadmap import Roadmap
# etc.

__all__ = ["Base"]
