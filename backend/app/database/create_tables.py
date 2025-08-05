#!/usr/bin/env python3
"""
Create database tables for the plant care system.

This script:
1. Tests database connection
2. Creates the normalized tables (plants, daily_care)
3. Shows table structure
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from backend.app.database.connection import db_manager, test_connection
from backend.app.database.models import Plant, DailyCare


def main():
    """Create database tables and verify setup."""
    
    print("🌱 Plant Care Database Setup")
    print("=" * 40)
    
    # Step 1: Test connection
    print("\n1️⃣ Testing database connection...")
    if not test_connection():
        print("❌ Cannot connect to database. Check your .env file!")
        sys.exit(1)
    
    print("✅ Database connection successful!")
    
    # Step 2: Create tables
    print("\n2️⃣ Creating database tables...")
    try:
        db_manager.create_tables()
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        sys.exit(1)
    
    # Step 3: Verify tables were created
    print("\n3️⃣ Verifying tables...")
    try:
        with db_manager.get_session() as session:
            # Try to query each table (should be empty but should work)
            plant_count = session.query(Plant).count()
            care_count = session.query(DailyCare).count()
            
            print(f"✅ plants table: {plant_count} records")
            print(f"✅ daily_care table: {care_count} records")
            
    except Exception as e:
        print(f"❌ Error verifying tables: {e}")
        sys.exit(1)
    
    # Step 4: Show table structure
    print("\n4️⃣ Database schema created:")
    print("""
    📋 PLANTS TABLE
    ├── id (Primary Key)
    ├── name (Unique plant name) 
    ├── created_at
    └── updated_at
    
    📋 DAILY_CARE TABLE  
    ├── id (Primary Key)
    ├── plant_id (Foreign Key → plants.id)
    ├── care_date
    ├── water_ml (NULL = no watering)
    ├── fertilizer (NULL = no fertilizer)
    ├── treatment (wash/neemoil/pestmix)
    ├── condition (plant notes)
    ├── created_at
    └── UNIQUE(plant_id, care_date)
    """)
    
    print("🎉 Database setup complete!")
    print("\n💡 Next steps:")
    print("   1. Run: python migrate_excel.py")
    print("   2. Verify your data migration")
    print("   3. Try some queries!")


if __name__ == "__main__":
    main()