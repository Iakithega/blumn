from sqlalchemy import Column, Integer, String, Date, Boolean, Float, DateTime, Text
from sqlalchemy.sql import func
from .connection import Base

class PlantDB(Base):
    __tablename__ = "plants"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic plant information
    plant_name = Column(String(255), index=True, nullable=False)
    
    # Care tracking
    last_watered = Column(Date, nullable=True)
    last_fertilized = Column(Date, nullable=True)
    last_washed = Column(Date, nullable=True)
    
    # Days tracking
    days_without_water = Column(Integer, nullable=True)
    days_since_watering = Column(Integer, nullable=True)
    days_since_fertilizing = Column(Integer, nullable=True)
    
    # Schedule configuration
    watering_schedule = Column(Integer, default=7)  # default to weekly
    fertilizing_schedule = Column(Integer, default=14)  # default to bi-weekly
    
    # Status flags
    needs_water = Column(Boolean, default=False)
    needs_fertilizer = Column(Boolean, default=False)
    
    # Care actions (for tracking what was done)
    water = Column(String(50), nullable=True)  # "yes", "no", or specific notes
    fertilizer = Column(String(50), nullable=True)
    wash = Column(String(50), nullable=True)
    
    # Plant characteristics
    size = Column(String(50), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Additional notes
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<PlantDB(id={self.id}, name='{self.plant_name}', last_watered={self.last_watered})>" 