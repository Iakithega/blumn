from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

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
    # Path to the static export directory produced by `next export`
    EXPORT_DIR = os.path.join(BASE_DIR, "frontend", "out")

    # The exported site will contain an "_next" folder with JS chunks + assets
    next_export_static = os.path.join(EXPORT_DIR, "_next")

    # Plant images directory
    plant_images_dir = os.path.join(EXPORT_DIR, "plant_images")

    # Mount the entire export directory at "/" **after** API routes are defined via a catch-all.
    # We still mount the _next folder explicitly so that hashed asset URLs are served efficiently.
    if os.path.exists(next_export_static):
        app.mount("/_next", StaticFiles(directory=next_export_static), name="next-export-static")

    # Mount exported root at /static for CSS/JS chunks created by Next build (e.g. "assets/..." when using Tailwind etc.)
    app.mount("/static", StaticFiles(directory=EXPORT_DIR), name="frontend-static")

    # Mount plant images directory explicitly so <img src="/plant_images/foo.jpg" /> works
    if os.path.exists(plant_images_dir):
        app.mount("/plant_images", StaticFiles(directory=plant_images_dir), name="plant-images")

    # Make the export directory path accessible to other handlers
    FRONTEND_EXPORT_DIR = EXPORT_DIR
else:
    FRONTEND_EXPORT_DIR = None

@app.get("/")
async def root(request: Request):
    # In production, serve the frontend's main index.html
    if IS_PRODUCTION and FRONTEND_EXPORT_DIR:
        index_html_path = os.path.join(FRONTEND_EXPORT_DIR, "index.html")

        if os.path.exists(index_html_path):
            return FileResponse(index_html_path, media_type="text/html")
        else:
            print(f"Warning: Frontend index.html not found at {index_html_path}")
            return {"message": "Welcome to Blumn Plant Care Tracker - Frontend not found"}

    # Default API response if not production or index.html not found
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
        
        # Print a header to the console (commented out for performance)
        # print("\n" + "="*80)
        # print(f"{'PLANT NAME':<30} {'PERIODICITY':<15} {'FIRST RECORD':<15} {'DAYS SINCE':<12} {'EVENTS':<8} {'DEFAULT'}")
        # print("-"*80)
        
        for plant in plants:
            # Calculate periodicity
            periodicity, calculation_method = calculate_watering_periodicity(plant.name)
            
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
            
            # Print to console (commented out for performance)
            # first_record_str = first_record.strftime("%d.%m.%Y") if first_record else "N/A"
            # periodicity_str = f"{round(periodicity, 1)}" if periodicity is not None else "N/A"
            # days_str = f"{days_since_first_record}" if days_since_first_record is not None else "N/A"
            # 
            # print(f"{plant.name:<30} {periodicity_str:<15} {first_record_str:<15} {days_str:<12} {watering_events:<8} {plant.watering_schedule}")
            
            # Add to results
            results.append({
                "plant_name": plant.name,
                "calculated_periodicity": round(periodicity, 1) if periodicity is not None else None,
                "calculation_method": calculation_method,
                "first_record_date": first_record.strftime("%d.%m.%Y") if first_record else None,
                "days_since_first_record": days_since_first_record,
                "watering_events": watering_events,
                "default_schedule": plant.watering_schedule
            })
        
        # Print footer (commented out for performance)
        # print("="*80 + "\n")
        
        return {"status": "success", "data": results}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e), "traceback": str(e.__traceback__)}

def calculate_watering_periodicity(plant_name: str) -> tuple:
    """
    Calculate the actual watering periodicity of a plant considering only
    the time between actual watering events.
    
    For plants with less than 5 watering events, uses a simple average.
    For plants with 5 or more watering events, uses a moving average of the
    5 most recent watering intervals.
    
    Returns:
        Tuple: (periodicity_value, calculation_method)
        where calculation_method is 'mean' or 'moving_avg'
    """
    # Get all rows for this plant, ordered by date
    plant_data = excel_handler.get_plant_history(plant_name)
    
    if not plant_data:
        return None, None  # No data available
    
    # Find all watering events (days where days_without_water = 0)
    watering_dates = []
    for entry in plant_data:
        days_wo_water = entry.get("days without water")
        water_entry = entry.get("water")
        if days_wo_water == 0 or (isinstance(days_wo_water, str) and days_wo_water.strip() == "0") or water_entry:
            watering_dates.append(entry["date"])
    
    if len(watering_dates) <= 1:
        # Not enough data points to calculate periodicity
        return None, None
    
    # Calculate time differences between consecutive waterings
    intervals = []
    for i in range(1, len(watering_dates)):
        days_between = (watering_dates[i] - watering_dates[i-1]).days
        intervals.append(days_between)
    
    # Calculate average interval
    if intervals:
        if len(intervals) < 5:
            # For plants with fewer than 5 watering events, use simple average
            return sum(intervals) / len(intervals), "mean"
        else:
            # For plants with 5 or more watering events, use moving average of last 5 intervals
            recent_intervals = intervals[-5:]
            return sum(recent_intervals) / len(recent_intervals), "moving_avg"
    
    return None, None  # If we couldn't calculate periodicity

@app.get("/api/plants/overview")
async def plants_overview(request: Request):
    """API endpoint for plants overview"""
    # Return API data - frontend will handle the presentation
    return {
        "plants": [
            {"name": "Plant 1", "status": "Needs water", "days_since_watering": 7},
            {"name": "Plant 2", "status": "Healthy", "days_since_watering": 2}
        ]
    }

def request_is_browser(request=None):
    """Helper function to determine if request is from a browser"""
    if request is None:
        # Try to get request from current function frame
        import inspect
        frame = inspect.currentframe()
        while frame:
            if 'request' in frame.f_locals:
                request = frame.f_locals['request']
                break
            frame = frame.f_back
    
    if request and hasattr(request, 'headers'):
        accept = request.headers.get('accept', '')
        return 'text/html' in accept
    return False

# Catch-all route for serving Next.js frontend pages in production
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str, request: Request):
    # Skip API routes (this check should be robust)
    if (full_path.startswith("api/") or full_path.startswith("_next/") or
        full_path.startswith("static/") or full_path.startswith("plant_images/")):
        # Let FastAPI handle these if they are actual API routes or static file requests
        # If they are not matched by other routes, FastAPI will return its own 404
        # For this specific case, if it starts with "api/", it's an API call, so return 404.
        if full_path.startswith("api/"):
             return {"detail": "API route not found"}, 404 # Return a proper 404 for API
        # For _next and static, StaticFiles middleware should handle it. If it reaches here, something is wrong.
        # This return statement will likely not be hit if StaticFiles is configured correctly.
        return {"detail": "Resource not found"}, 404

    if IS_PRODUCTION and FRONTEND_EXPORT_DIR:
        # Attempt to resolve a static HTML file that matches the requested path within the export directory
        # e.g. /plants/overview -> frontend/out/plants/overview/index.html (preferred) or frontend/out/plants/overview.html

        # Normalise path to avoid directory traversal
        safe_path = os.path.normpath(full_path).lstrip("/\\")

        # First try folder style path (plants/overview/index.html)
        candidate_a = os.path.join(FRONTEND_EXPORT_DIR, safe_path, "index.html")
        # Then flat html (plants/overview.html)
        candidate_b = os.path.join(FRONTEND_EXPORT_DIR, f"{safe_path}.html")

        if os.path.exists(candidate_a):
            return FileResponse(candidate_a, media_type="text/html")
        if os.path.exists(candidate_b):
            return FileResponse(candidate_b, media_type="text/html")

        # Fallback to root index.html (client-side routing may handle it)
        fallback_index = os.path.join(FRONTEND_EXPORT_DIR, "index.html")
        if os.path.exists(fallback_index):
            return FileResponse(fallback_index, media_type="text/html")
        
        print(f"CRITICAL: Could not resolve static page for path '{full_path}' in export dir {FRONTEND_EXPORT_DIR}")
        return {"detail": "Frontend page not found in static export."}, 404

    # If not IS_PRODUCTION, or if somehow the index.html was not served (should not happen if IS_PRODUCTION and file exists)
    # This fallback is mostly for non-production or misconfiguration.
    return {"detail": "Not Found - Ensure IS_PRODUCTION is set and frontend is built correctly."} 