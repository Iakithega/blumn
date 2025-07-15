from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import date, datetime
from .models import PlantDB

class PlantCRUD:
    """CRUD operations for Plant model"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_plant(self, plant_data: dict) -> PlantDB:
        """Create a new plant"""
        db_plant = PlantDB(**plant_data)
        self.db.add(db_plant)
        self.db.commit()
        self.db.refresh(db_plant)
        return db_plant
    
    def get_plant_by_id(self, plant_id: int) -> Optional[PlantDB]:
        """Get a plant by ID"""
        return self.db.query(PlantDB).filter(PlantDB.id == plant_id).first()
    
    def get_plant_by_name(self, plant_name: str) -> Optional[PlantDB]:
        """Get a plant by name"""
        return self.db.query(PlantDB).filter(PlantDB.plant_name == plant_name).first()
    
    def get_all_plants(self) -> List[PlantDB]:
        """Get all plants"""
        return self.db.query(PlantDB).all()
    
    def update_plant(self, plant_id: int, update_data: dict) -> Optional[PlantDB]:
        """Update a plant"""
        db_plant = self.get_plant_by_id(plant_id)
        if db_plant:
            for key, value in update_data.items():
                setattr(db_plant, key, value)
            self.db.commit()
            self.db.refresh(db_plant)
        return db_plant
    
    def delete_plant(self, plant_id: int) -> bool:
        """Delete a plant"""
        db_plant = self.get_plant_by_id(plant_id)
        if db_plant:
            self.db.delete(db_plant)
            self.db.commit()
            return True
        return False
    
    def get_plants_needing_water(self) -> List[PlantDB]:
        """Get plants that need water"""
        return self.db.query(PlantDB).filter(PlantDB.needs_water == True).all()
    
    def get_plants_needing_fertilizer(self) -> List[PlantDB]:
        """Get plants that need fertilizer"""
        return self.db.query(PlantDB).filter(PlantDB.needs_fertilizer == True).all()
    
    def get_plants_watered_on_date(self, target_date: date) -> List[PlantDB]:
        """Get plants watered on a specific date"""
        return self.db.query(PlantDB).filter(PlantDB.last_watered == target_date).all()
    
    def get_plants_fertilized_on_date(self, target_date: date) -> List[PlantDB]:
        """Get plants fertilized on a specific date"""
        return self.db.query(PlantDB).filter(PlantDB.last_fertilized == target_date).all()
    
    def update_watering(self, plant_id: int, watered_date: date = None) -> Optional[PlantDB]:
        """Update plant watering information"""
        if watered_date is None:
            watered_date = date.today()
        
        return self.update_plant(plant_id, {
            'last_watered': watered_date,
            'water': 'yes',
            'needs_water': False
        })
    
    def update_fertilizing(self, plant_id: int, fertilized_date: date = None) -> Optional[PlantDB]:
        """Update plant fertilizing information"""
        if fertilized_date is None:
            fertilized_date = date.today()
        
        return self.update_plant(plant_id, {
            'last_fertilized': fertilized_date,
            'fertilizer': 'yes',
            'needs_fertilizer': False
        })
    
    def calculate_days_since_care(self, plant: PlantDB) -> dict:
        """Calculate days since last care for a plant"""
        today = date.today()
        result = {}
        
        if plant.last_watered:
            result['days_since_watering'] = (today - plant.last_watered).days
        else:
            result['days_since_watering'] = None
        
        if plant.last_fertilized:
            result['days_since_fertilizing'] = (today - plant.last_fertilized).days
        else:
            result['days_since_fertilizing'] = None
        
        return result
    
    def update_care_status(self, plant: PlantDB) -> PlantDB:
        """Update care status flags based on schedule"""
        days_info = self.calculate_days_since_care(plant)
        
        updates = {}
        
        # Check if needs water
        if days_info['days_since_watering'] is not None:
            updates['needs_water'] = days_info['days_since_watering'] >= plant.watering_schedule
        
        # Check if needs fertilizer
        if days_info['days_since_fertilizing'] is not None:
            updates['needs_fertilizer'] = days_info['days_since_fertilizing'] >= plant.fertilizing_schedule
        
        # Update days tracking
        updates['days_since_watering'] = days_info['days_since_watering']
        updates['days_since_fertilizing'] = days_info['days_since_fertilizing']
        
        return self.update_plant(plant.id, updates)

def get_plant_crud(db: Session) -> PlantCRUD:
    """Get PlantCRUD instance"""
    return PlantCRUD(db) 