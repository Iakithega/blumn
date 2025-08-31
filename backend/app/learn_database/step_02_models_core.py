"""
Step 02 (Core): Define tables using SQLAlchemy Core.

Simple schema decisions (confirmed):
- care_type: VARCHAR(50), no enum
- only notes column for extra details
- no cascade deletes; default FK behavior
- case-sensitive UNIQUE on plants.name
- only created_at (no updated_at)
- no source column
"""

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    MetaData,
    UniqueConstraint,
    Index,
    func,
)


metadata = MetaData()


plants = Table(
    "plants",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False, unique=True),
    Column("plant_info", Text, nullable=True),
    Column("plant_condition", String(255), nullable=True),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
)


care_activities = Table(
    "care_activities",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("plant_id", Integer, ForeignKey("plants.id"), nullable=False),
    Column("care_date", Date, nullable=False),
    Column("care_type", String(50), nullable=False),
    Column("notes", Text, nullable=True),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    UniqueConstraint("plant_id", "care_date", "care_type", name="uq_care_unique"),
    Index("ix_care_plant_date", "plant_id", "care_date"),
)


# When you do from step_02_models_core import *, only the names listed in __all__ are imported: metadata, plants, care_activities.
# If you DO include __all__, then when someone does from module import *, Python uses those strings to import names. Any name listed that doesn’t actually exist will cause that star-import to fail.
# It’s optional; useful to make the module’s intended exports clear and to avoid leaking helpers.
__all__ = [
    "metadata",
    "plants",
    "care_activities",
]


