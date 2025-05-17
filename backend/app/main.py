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
    # Check if Next.js output directory exists
    next_static_dir = os.path.join(BASE_DIR, "frontend", ".next", "static")
    public_dir = os.path.join(BASE_DIR, "frontend", "public") # Renamed for clarity
    
    if os.path.exists(next_static_dir):
        app.mount("/_next", StaticFiles(directory=next_static_dir), name="next-static")
    if os.path.exists(public_dir): # Use public_dir here
        app.mount("/static", StaticFiles(directory=public_dir), name="public-static") # Use public_dir here

@app.get("/")
async def root(request: Request): # Add request parameter
    # In production, serve the frontend's main index.html
    if IS_PRODUCTION:
        # For Next.js, the entry point is usually within the .next/server/pages or .next/server/app directory
        # A common pattern is to serve the index.html and let client-side routing take over.
        # Let's try a more general path for Next.js 13+ App Router or Pages Router
        
        # Path for Pages Router (typical)
        index_html_path = os.path.join(BASE_DIR, "frontend", ".next", "server", "pages", "index.html")

        # Fallback for App Router (might be different, often a root layout)
        # For simplicity, we'll stick to a common index.html for now.
        # If using App router and this fails, this path needs to point to the main entry HTML.
        
        if os.path.exists(index_html_path):
            return FileResponse(index_html_path)
        else:
            # If specific index.html isn't found, it might indicate an issue with build or paths.
            # Log this or handle appropriately. For now, falling back to API message.
            # In a real scenario, you'd want to ensure this index.html always exists.
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
    if full_path.startswith("api/") or full_path.startswith("_next/") or full_path.startswith("static/"):
        # Let FastAPI handle these if they are actual API routes or static file requests
        # If they are not matched by other routes, FastAPI will return its own 404
        # For this specific case, if it starts with "api/", it's an API call, so return 404.
        if full_path.startswith("api/"):
             return {"detail": "API route not found"}, 404 # Return a proper 404 for API
        # For _next and static, StaticFiles middleware should handle it. If it reaches here, something is wrong.
        # However, it's better to let StaticFiles do its job or FastAPI's default 404.
        # This return statement will likely not be hit if StaticFiles is configured correctly.
        return {"detail": "Resource not found"}, 404


    if IS_PRODUCTION:
        # For any non-API path, serve the main index.html from Next.js.
        # Next.js client-side router will handle the specific page (e.g., /plants/overview)
        
        # Path for Pages Router (typical index.html)
        index_html_path = os.path.join(BASE_DIR, "frontend", ".next", "server", "pages", "index.html")

        # Alternative path if Next.js build places a generic index.html in a different location
        # For example, some build configurations might output to `frontend/out/index.html` for static export
        # Check your `next.config.js` if `output: 'export'` is used.
        # If `output: 'export'` is used, the path would be `os.path.join(BASE_DIR, "frontend", "out", "index.html")`
        # and for specific pages like /plants/overview, it would be `frontend/out/plants/overview.html`

        # The `full_path` for /plants/overview will be "plants/overview"
        # If Next.js `output: 'export'` is used, you'd serve `frontend/out/{full_path}.html` or `frontend/out/{full_path}/index.html`
        # And for the root, `frontend/out/index.html`

        # For a standard Next.js SSR/SSG setup (not `output: 'export'`), serving the root index.html 
        # from the .next/server/pages directory is a common approach for the catch-all.
        
        if os.path.exists(index_html_path):
            return FileResponse(index_html_path, media_type="text/html")
        else:
            # This indicates a critical issue: the main entry point for the frontend is missing.
            print(f"CRITICAL: Frontend entry point 'index.html' not found at {index_html_path}")
            return {"detail": "Frontend entry point not found. Check deployment."}, 500
            
    # If not IS_PRODUCTION, or if somehow the index.html was not served (should not happen if IS_PRODUCTION and file exists)
    # This fallback is mostly for non-production or misconfiguration.
    return {"detail": "Not Found - Ensure IS_PRODUCTION is set and frontend is built correctly."} 