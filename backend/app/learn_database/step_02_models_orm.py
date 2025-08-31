"""
Step 02 (ORM): Define declarative models with relationships.

Simple schema decisions (confirmed):
- care_type: VARCHAR(50), no enum
- only notes column for extra details
- no cascade deletes; default FK behavior
- case-sensitive UNIQUE on plants.name
- only created_at (no updated_at)
- no source column
"""

from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Index,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    plant_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    plant_condition: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    care_activities: Mapped[List["CareActivity"]] = relationship(
        back_populates="plant",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Plant id={self.id} name='{self.name}'>"


class CareActivity(Base):
    __tablename__ = "care_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id"), nullable=False)
    care_date: Mapped[date] = mapped_column(Date, nullable=False)
    care_type: Mapped[str] = mapped_column(String(50), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    plant: Mapped[Plant] = relationship(
        back_populates="care_activities",
        lazy="joined",
    )

    __table_args__ = (
        UniqueConstraint("plant_id", "care_date", "care_type", name="uq_care_unique"),
        Index("ix_care_plant_date", "plant_id", "care_date"),
    )

    def __repr__(self) -> str:
        return f"<CareActivity id={self.id} plant_id={self.plant_id} date={self.care_date} type={self.care_type}>"


__all__ = [
    "Base",
    "Plant",
    "CareActivity",
]


