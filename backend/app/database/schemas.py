from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class PlantBase(BaseModel):
    """Base plant schema"""
    plant_name: str = Field(..., min_length=1, max_length=255)
    watering_schedule: int = Field(default=7, ge=1, le=365)
    fertilizing_schedule: int = Field(default=14, ge=1, le=365)
    size: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None

class PlantCreate(PlantBase):
    """Schema for creating a plant"""
    last_watered: Optional[date] = None
    last_fertilized: Optional[date] = None
    last_washed: Optional[date] = None

class PlantUpdate(BaseModel):
    """Schema for updating a plant"""
    plant_name: Optional[str] = Field(None, min_length=1, max_length=255)
    watering_schedule: Optional[int] = Field(None, ge=1, le=365)
    fertilizing_schedule: Optional[int] = Field(None, ge=1, le=365)
    size: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    last_watered: Optional[date] = None
    last_fertilized: Optional[date] = None
    last_washed: Optional[date] = None

class PlantResponse(PlantBase):
    """Schema for plant response"""
    id: int
    last_watered: Optional[date] = None
    last_fertilized: Optional[date] = None
    last_washed: Optional[date] = None
    days_without_water: Optional[int] = None
    days_since_watering: Optional[int] = None
    days_since_fertilizing: Optional[int] = None
    needs_water: bool = False
    needs_fertilizer: bool = False
    water: Optional[str] = None
    fertilizer: Optional[str] = None
    wash: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PlantCareUpdate(BaseModel):
    """Schema for updating plant care"""
    watered: Optional[bool] = None
    fertilized: Optional[bool] = None
    washed: Optional[bool] = None
    care_date: Optional[date] = None

class PlantListResponse(BaseModel):
    """Schema for plant list response"""
    status: str
    data: list[PlantResponse]
    message: Optional[str] = None

class PlantDetailResponse(BaseModel):
    """Schema for single plant response"""
    status: str
    data: Optional[PlantResponse] = None
    message: Optional[str] = None 