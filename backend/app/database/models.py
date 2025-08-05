"""
SQLAlchemy models for plant care database.

Normalized design with two tables:
- plants: Master plant data (each plant once)
- daily_care: Daily care activities (references plants)
"""

from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped

Base = declarative_base()


class Plant(Base):
    """
    Master table for plants - each plant stored once.
    
    This follows database normalization principles:
    - No duplicate plant names
    - Single source of truth for plant information
    - Referenced by foreign key from daily_care table
    """
    __tablename__ = "plants"
    
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False, unique=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to daily care records
    # back_populates creates bidirectional relationship
    care_records: Mapped[List["DailyCare"]] = relationship(
        "DailyCare", 
        back_populates="plant",
        cascade="all, delete-orphan"  # Delete care records if plant is deleted
    )
    
    def __repr__(self) -> str:
        return f"<Plant(id={self.id}, name='{self.name}')>"


class DailyCare(Base):
    """
    Daily care activities table - one record per plant per day.
    
    This preserves your Excel structure while being normalized:
    - References plant by ID (not name repetition)
    - One row per plant per day (like Excel)
    - NULL values for days without care activities
    """
    __tablename__ = "daily_care"
    
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    plant_id: Mapped[int] = Column(Integer, ForeignKey("plants.id"), nullable=False)
    care_date: Mapped[date] = Column(Date, nullable=False)
    
    # Care activities (NULL = no care that day)
    water_ml: Mapped[Optional[int]] = Column(Integer, nullable=True)
    fertilizer: Mapped[Optional[str]] = Column(String(50), nullable=True)
    treatment: Mapped[Optional[str]] = Column(String(50), nullable=True)  # wash/neemoil/pestmix combined
    condition: Mapped[Optional[str]] = Column(Text, nullable=True)  # plant condition notes
    
    # Metadata
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    
    # Ensure one record per plant per day
    __table_args__ = (
        UniqueConstraint('plant_id', 'care_date', name='unique_plant_date'),
    )
    
    # Relationship back to plant
    plant: Mapped["Plant"] = relationship("Plant", back_populates="care_records")
    
    def __repr__(self) -> str:
        return f"<DailyCare(plant_id={self.plant_id}, date={self.care_date}, water={self.water_ml})>"


# Convenience functions for common queries
def get_plant_by_name(session, plant_name: str) -> Optional[Plant]:
    """Get a plant by name."""
    return session.query(Plant).filter(Plant.name == plant_name).first()


def get_last_watering_date(session, plant_id: int) -> Optional[date]:
    """Get the last date a plant was watered."""
    result = session.query(DailyCare.care_date)\
        .filter(DailyCare.plant_id == plant_id)\
        .filter(DailyCare.water_ml.isnot(None))\
        .order_by(DailyCare.care_date.desc())\
        .first()
    
    return result[0] if result else None


def get_days_without_water(session, plant_id: int, reference_date: date = None) -> Optional[int]:
    """
    Calculate days without water for a plant.
    This replaces the Excel calculated column with a proper database query.
    """
    if reference_date is None:
        reference_date = date.today()
    
    last_watered = get_last_watering_date(session, plant_id)
    
    if last_watered is None:
        return None  # Never been watered
    
    return (reference_date - last_watered).days


def get_plant_status(session, plant_id: int, reference_date: date = None) -> dict:
    """
    Get comprehensive status of a plant (like your Excel view).
    Returns days without water, last fertilizer, etc.
    """
    if reference_date is None:
        reference_date = date.today()
    
    plant = session.query(Plant).get(plant_id)
    if not plant:
        return None
    
    # Get last care activities
    last_watered = get_last_watering_date(session, plant_id)
    
    last_fertilized = session.query(DailyCare.care_date)\
        .filter(DailyCare.plant_id == plant_id)\
        .filter(DailyCare.fertilizer.isnot(None))\
        .order_by(DailyCare.care_date.desc())\
        .first()
    
    last_treatment = session.query(DailyCare.care_date, DailyCare.treatment)\
        .filter(DailyCare.plant_id == plant_id)\
        .filter(DailyCare.treatment.isnot(None))\
        .order_by(DailyCare.care_date.desc())\
        .first()
    
    return {
        "plant_name": plant.name,
        "last_watered": last_watered,
        "days_without_water": get_days_without_water(session, plant_id, reference_date),
        "last_fertilized": last_fertilized[0] if last_fertilized else None,
        "last_treatment": {
            "date": last_treatment[0],
            "type": last_treatment[1]
        } if last_treatment else None
    }