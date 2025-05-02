from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import openpyxl
from openpyxl.styles import PatternFill, Border, Side
from dateutil.parser import parse

class ExcelHandler:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure the Excel file exists, create if it doesn't"""
        if not self.file_path.exists():
            wb = openpyxl.Workbook()
            ws = wb.active
            # Add headers
            headers = ["date", "plant name", "days without water", "water", "fertilizer", "wash", "size"]
            for col, header in enumerate(headers, 1):
                ws.cell(row=1, column=col, value=header)
            wb.save(self.file_path)
    
    def _get_plant_names(self, ws) -> List[str]:
        """Get unique plant names from the Excel file"""
        plant_names = set()
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[1]:  # plant name column
                plant_names.add(row[1])
        return sorted(list(plant_names))
    
    def _ensure_dates_exist(self, ws):
        """Ensure entries exist for today and next 7 days"""
        today = datetime.now().date()
        end_date = today + timedelta(days=7)
        
        # Get existing dates
        existing_dates = set()
        for row in ws.iter_rows(min_row=2, max_col=1, values_only=True):
            if row[0]:
                try:
                    date = parse(row[0]).date()
                    existing_dates.add(date)
                except:
                    continue
        
        # Get plant names
        plant_names = self._get_plant_names(ws)
        
        # Add missing dates
        current_date = today
        while current_date <= end_date:
            if current_date not in existing_dates:
                # Add entries for each plant
                for plant in plant_names:
                    ws.append([
                        current_date.strftime("%m/%d/%Y"),
                        plant,
                        "",  # days without water
                        "",  # water
                        "",  # fertilizer
                        "",  # wash
                        ""   # size
                    ])
            current_date += timedelta(days=1)
    
    def read_data(self) -> List[Dict[str, Any]]:
        """Read data from Excel file, ensuring dates exist"""
        wb = openpyxl.load_workbook(self.file_path, data_only=True)
        ws = wb.active
        
        # Ensure dates exist
        self._ensure_dates_exist(ws)
        wb.save(self.file_path)
        
        # Read data
        data = []
        headers = [cell.value for cell in ws[1]]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if any(row):  # Skip empty rows
                data.append(dict(zip(headers, row)))
        
        return data
    
    def write_data(self, data: List[Dict[str, Any]]):
        """Write data to Excel file while preserving formatting"""
        wb = openpyxl.load_workbook(self.file_path)
        ws = wb.active
        
        # Clear existing data (except headers)
        for row in range(2, ws.max_row + 1):
            for col in range(1, ws.max_column + 1):
                ws.cell(row=row, column=col).value = None
        
        # Write new data
        headers = [cell.value for cell in ws[1]]
        for row_data in data:
            row = []
            for header in headers:
                row.append(row_data.get(header, ""))
            ws.append(row)
        
        wb.save(self.file_path) 