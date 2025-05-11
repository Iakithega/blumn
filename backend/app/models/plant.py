from datetime import date
from typing import Optional
from pydantic import BaseModel

class Plant(BaseModel):
    id: int
    name: str
    last_watered: Optional[date] = None
    last_fertilized: Optional[date] = None
    days_since_watering: Optional[int] = None
    days_since_fertilizing: Optional[int] = None
    watering_schedule: int = 7  # default to weekly
    fertilizing_schedule: int = 14  # default to bi-weekly
    needs_water: bool = False
    needs_fertilizer: bool = False 