from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .core.excel_handler import ExcelHandler
from .models.plant import Plant

# Initialize FastAPI app
app = FastAPI(title="Blumn Plant Care Tracker")

# Configure CORS
origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Excel handler with absolute path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Check if running on Heroku (use DATA_PATH env var if provided)
EXCEL_FILE_PATH = os.environ.get('DATA_PATH', os.path.join(BASE_DIR, "data", "blumen_data.xlsx"))
excel_handler = ExcelHandler(EXCEL_FILE_PATH)

# Check if running in production mode (Heroku)
IS_PRODUCTION = os.environ.get("PRODUCTION", "False").lower() == "true"

# If in production, serve frontend static files
if IS_PRODUCTION:
    # Check if Next.js output directory exists
    frontend_dir = os.path.join(BASE_DIR, "frontend", ".next")
    static_dir = os.path.join(BASE_DIR, "frontend", "public")
    if os.path.exists(frontend_dir):
        app.mount("/_next", StaticFiles(directory=frontend_dir), name="next-static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    # In production, serve the frontend
    if IS_PRODUCTION:
        frontend_index = os.path.join(BASE_DIR, "frontend", ".next", "server", "pages", "index.html")
        if os.path.exists(frontend_index):
            return FileResponse(frontend_index)
    
    # Default API response
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

@app.get("/api/plants/periodicity")
async def test_watering_periodicity():
    """Test the watering periodicity calculation for all plants"""
    try:
        plants = excel_handler.get_todays_plants()
        results = []
        
        # Print a header to the console
        print("\n" + "="*80)
        print(f"{'PLANT NAME':<30} {'PERIODICITY':<15} {'FIRST RECORD':<15} {'DAYS SINCE':<12} {'EVENTS':<8} {'DEFAULT'}")
        print("-"*80)
        
        for plant in plants:
            # Calculate periodicity
            periodicity = calculate_watering_periodicity(plant.name)
            
            # Get the first record date for this plant
            plant_history = excel_handler.get_plant_history(plant.name)
            first_record = plant_history[0]["date"] if plant_history else None
            days_since_first_record = (datetime.now().date() - first_record).days if first_record else None
            
            # Count watering events
            watering_events = 0
            for entry in plant_history:
                days_wo_water = entry.get("days without water")
                water_entry = entry.get("water")
                if days_wo_water == 0 or (isinstance(days_wo_water, str) and days_wo_water.strip() == "0") or water_entry:
                    watering_events += 1
            
            # Print to console
            first_record_str = first_record.strftime("%d.%m.%Y") if first_record else "N/A"
            periodicity_str = f"{round(periodicity, 1)}" if periodicity is not None else "N/A"
            days_str = f"{days_since_first_record}" if days_since_first_record is not None else "N/A"
            
            print(f"{plant.name:<30} {periodicity_str:<15} {first_record_str:<15} {days_str:<12} {watering_events:<8} {plant.watering_schedule}")
            
            # Add to results
            results.append({
                "plant_name": plant.name,
                "calculated_periodicity": round(periodicity, 1) if periodicity is not None else None,
                "first_record_date": first_record.strftime("%d.%m.%Y") if first_record else None,
                "days_since_first_record": days_since_first_record,
                "watering_events": watering_events,
                "default_schedule": plant.watering_schedule
            })
        
        # Print footer
        print("="*80 + "\n")
        
        return {"status": "success", "data": results}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e), "traceback": str(e.__traceback__)}

def calculate_watering_periodicity(plant_name: str) -> float:
    """
    Calculate the actual watering periodicity of a plant considering only
    the time between actual watering events.
    
    Returns:
        The average days between waterings
    """
    # Get all rows for this plant, ordered by date
    plant_data = excel_handler.get_plant_history(plant_name)
    
    if not plant_data:
        return None  # No data available
    
    # Find all watering events (days where days_without_water = 0)
    watering_dates = []
    for entry in plant_data:
        days_wo_water = entry.get("days without water")
        water_entry = entry.get("water")
        if days_wo_water == 0 or (isinstance(days_wo_water, str) and days_wo_water.strip() == "0") or water_entry:
            watering_dates.append(entry["date"])
    
    if len(watering_dates) <= 1:
        # Not enough data points to calculate periodicity
        return None
    
    # Calculate time differences between consecutive waterings
    intervals = []
    for i in range(1, len(watering_dates)):
        days_between = (watering_dates[i] - watering_dates[i-1]).days
        intervals.append(days_between)
    
    # Calculate average interval
    if intervals:
        return sum(intervals) / len(intervals)
    
    return None  # If we couldn't calculate periodicity

# Catch-all route for serving Next.js frontend pages in production
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str, request: Request):
    # Only serve frontend in production mode
    if not IS_PRODUCTION or full_path.startswith("api/"):
        return {"detail": "Not Found"}
    
    # Find the appropriate file from the Next.js build
    requested_path = full_path
    
    # Check if the requested path exists
    possible_paths = [
        os.path.join(BASE_DIR, "frontend", ".next", "server", "pages", requested_path, "index.html"),
        os.path.join(BASE_DIR, "frontend", ".next", "server", "pages", f"{requested_path}.html")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return FileResponse(path)
    
    # If no specific page found, try to serve the 404 page
    not_found_path = os.path.join(BASE_DIR, "frontend", ".next", "server", "pages", "404.html")
    if os.path.exists(not_found_path):
        return FileResponse(not_found_path)
    
    # Last resort fallback
    return {"detail": "Not Found"} 