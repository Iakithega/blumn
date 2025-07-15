#!/usr/bin/env python3
"""
Test database connection script
Run this to test if your PostgreSQL database connection is working
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

def test_database_connection():
    """Test the database connection"""
    print("🔍 Testing database connection...")
    
    # Check if DATABASE_URL is set
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL environment variable is not set!")
        return False
    
    # Hide password in URL for display
    display_url = database_url
    if '@' in display_url:
        parts = display_url.split('@')
        user_part = parts[0]
        if ':' in user_part:
            user_part = user_part.split(':')[0] + ':****'
        display_url = user_part + '@' + parts[1]
    
    print(f"📡 Database URL: {display_url}")
    
    try:
        from app.database.connection import SessionLocal, engine
        
        # Test basic connection
        db = SessionLocal()
        result = db.execute("SELECT version()")
        version = result.fetchone()[0]
        print(f"✅ PostgreSQL Version: {version}")
        
        # Test if we can create a simple table
        db.execute("""
            CREATE TABLE IF NOT EXISTS connection_test (
                id SERIAL PRIMARY KEY,
                test_message TEXT
            )
        """)
        
        # Insert test data
        db.execute("INSERT INTO connection_test (test_message) VALUES ('Hello from Blumn!')")
        db.commit()
        
        # Read test data
        result = db.execute("SELECT test_message FROM connection_test ORDER BY id DESC LIMIT 1")
        test_message = result.fetchone()[0]
        print(f"✅ Test message: {test_message}")
        
        # Clean up
        db.execute("DROP TABLE connection_test")
        db.commit()
        db.close()
        
        print("✅ Database connection test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("🌱 Blumn Plant Care Tracker - Database Connection Test")
    print("=" * 50)
    
    if test_database_connection():
        print("\n🎉 Your database is ready to use!")
    else:
        print("\n❌ Database connection failed. Please check your configuration.")
        sys.exit(1) 