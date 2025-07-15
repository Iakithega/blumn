from fastapi import Depends
from sqlalchemy.orm import Session
from .connection import get_db
from .crud import get_plant_crud, PlantCRUD

def get_database_session() -> Session:
    """Dependency to get database session"""
    return next(get_db())

def get_plant_crud_dependency(db: Session = Depends(get_db)) -> PlantCRUD:
    """Dependency to get PlantCRUD instance"""
    return get_plant_crud(db) 