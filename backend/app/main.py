from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

from .core.excel_handler import ExcelHandler
from .models.plant import Plant

# Initialize FastAPI app
app = FastAPI(title="Blumn Plant Care Tracker")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Excel handler with absolute path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
EXCEL_FILE_PATH = os.path.join(BASE_DIR, "data", "blumen_data.xlsx")
excel_handler = ExcelHandler(EXCEL_FILE_PATH)

@app.get("/")
async def root():
    return {"message": "Welcome to Blumn Plant Care Tracker"}

@app.get("/api/plants")
async def get_plants():
    """Get all plant data"""
    try:
        data = excel_handler.read_data()
        # Format dates as dd.mm.yyyy
        for item in data:
            if item.get("date") and not isinstance(item["date"], str):
                try:
                    item["date"] = item["date"].strftime("%d.%m.%Y")
                except:
                    pass
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/plants/today")
async def get_todays_plants():
    """Get all plants with their current care status"""
    try:
        plants = excel_handler.get_todays_plants()
        # Convert to dict and format dates
        plants_data = []
        for plant in plants:
            plant_dict = plant.dict()
            # Format dates as dd.mm.yyyy
            if plant_dict.get("last_watered"):
                plant_dict["last_watered"] = plant_dict["last_watered"].strftime("%d.%m.%Y")
            if plant_dict.get("last_fertilized"):
                plant_dict["last_fertilized"] = plant_dict["last_fertilized"].strftime("%d.%m.%Y")
            plants_data.append(plant_dict)
        return plants_data
    except Exception as e:
        return {"status": "error", "message": str(e)} 