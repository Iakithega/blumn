#!/usr/bin/env python3
"""
Database initialization script
Run this to create tables in your PostgreSQL database
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.database.connection import engine, Base, create_tables
from app.database.models import PlantDB

def init_database():
    """Initialize the database by creating all tables"""
    print("Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Print table information
        print("\nCreated tables:")
        for table in Base.metadata.tables:
            print(f"  - {table}")
            
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False
    
    return True

def check_database_connection():
    """Check if database connection is working"""
    try:
        # Test database connection
        from app.database.connection import SessionLocal
        
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("✅ Database connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🌱 Blumn Plant Care Tracker - Database Initialization")
    print("=" * 50)
    
    # Check if DATABASE_URL is set
    if not os.environ.get("DATABASE_URL"):
        print("❌ DATABASE_URL environment variable is not set!")
        print("Please set your DATABASE_URL before running this script.")
        sys.exit(1)
    
    # Check database connection
    if not check_database_connection():
        sys.exit(1)
    
    # Initialize database
    if init_database():
        print("\n🎉 Database initialization completed successfully!")
        print("You can now run your FastAPI application.")
    else:
        print("\n❌ Database initialization failed!")
        sys.exit(1) 