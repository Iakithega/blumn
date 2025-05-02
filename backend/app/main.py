from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

from .core.excel_handler import ExcelHandler

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
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)} 