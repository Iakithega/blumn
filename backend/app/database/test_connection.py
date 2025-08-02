#!/usr/bin/env python3
"""
Test database connection script
Run this to test if your PostgreSQL database connection is working
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import text
import traceback

# Load environment variables from .env file
env_path = Path('.') / '.env'
print(f"🔍 Looking for .env file at: {env_path.absolute()}")
if env_path.exists():
    print("✅ Found .env file")
    load_dotenv(env_path)
else:
    print("⚠️  No .env file found, using system environment variables")
    load_dotenv()

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

def test_database_connection():
    """Test the database connection"""
    print("\n🔍 Testing database connection...")
    print("=" * 50)
    
    # Debug: Show all database-related environment variables
    print("\n📋 Environment Variables Check:")
    env_vars = {
        "DATABASE_URL": os.environ.get("DATABASE_URL"),
        "DB_USER": os.environ.get("DB_USER"),
        "DB_PASSWORD": os.environ.get("DB_PASSWORD"),
        "DB_HOST": os.environ.get("DB_HOST"),
        "DB_PORT": os.environ.get("DB_PORT"),
        "DB_NAME": os.environ.get("DB_NAME")
    }
    
    for key, value in env_vars.items():
        if value:
            if "PASSWORD" in key or "DATABASE_URL" in key:
                # Hide sensitive information
                if "DATABASE_URL" in key and "@" in value:
                    parts = value.split('@')
                    if len(parts) > 1:
                        user_part = parts[0].split('://')[-1]
                        if ':' in user_part:
                            user = user_part.split(':')[0]
                            display_value = f"postgresql://{user}:****@{parts[1]}"
                        else:
                            display_value = value
                    else:
                        display_value = value
                else:
                    display_value = "****" if value else None
            else:
                display_value = value
            print(f"   {key}: {display_value}")
        else:
            print(f"   {key}: Not set")
    
    # Check if DATABASE_URL is set
    database_url = os.environ.get("DATABASE_URL")
    
    # Check for individual components if DATABASE_URL is not set
    if not database_url:
        db_user = os.environ.get("DB_USER")
        db_password = os.environ.get("DB_PASSWORD")
        db_host = os.environ.get("DB_HOST")
        db_port = os.environ.get("DB_PORT", "5432")
        db_name = os.environ.get("DB_NAME", "postgres")
        
        if all([db_user, db_password, db_host]):
            database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            print(f"\n📡 Built connection string from individual variables")
        else:
            print("\n❌ Database connection not configured!")
            print("\nYou can configure the database connection in two ways:")
            print("\n1. Using a single DATABASE_URL environment variable:")
            print("   DATABASE_URL=postgresql://username:password@host:port/database")
            print("\n2. Using individual environment variables:")
            print("   DB_USER=your_username")
            print("   DB_PASSWORD=your_password")
            print("   DB_HOST=your_host")
            print("   DB_PORT=5432 (optional, defaults to 5432)")
            print("   DB_NAME=postgres (optional, defaults to postgres)")
            print("\nFor Windows PowerShell, set them like this:")
            print('   $env:DB_USER="your_username"')
            print('   $env:DB_PASSWORD="your_password"')
            print('   $env:DB_HOST="your_host"')
            return False
    
    # Parse and display connection details
    print("\n📊 Connection Details:")
    try:
        if "@" in database_url:
            parts = database_url.split('@')
            host_part = parts[1]
            user_part = parts[0].split('://')[-1]
            
            if ':' in user_part:
                username = user_part.split(':')[0]
            else:
                username = user_part
                
            if '/' in host_part:
                host_port, db_name = host_part.split('/', 1)
                if ':' in host_port:
                    host, port = host_port.split(':')
                else:
                    host = host_port
                    port = "5432"
            else:
                host = host_part
                port = "5432"
                db_name = "postgres"
                
            print(f"   Host: {host}")
            print(f"   Port: {port}")
            print(f"   Database: {db_name}")
            print(f"   Username: {username}")
    except Exception as e:
        print(f"   Could not parse connection string: {e}")
    
    print("\n🔌 Attempting to connect...")
    print("=" * 50)
    
    try:
        # Import with detailed error handling
        print("📦 Importing database modules...")
        try:
            from app.database.connection import SessionLocal, engine
            print("✅ Successfully imported database modules")
        except ImportError as e:
            print(f"❌ Failed to import database modules: {e}")
            print("   Make sure you're running from the project root directory")
            return False
        except Exception as e:
            print(f"❌ Error during import: {e}")
            traceback.print_exc()
            return False
        
        # Test basic connection
        print("\n🔗 Creating database session...")
        db = SessionLocal()
        
        print("🔍 Testing connection with SELECT version()...")
        result = db.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"✅ Connected! PostgreSQL Version: {version}")
        
        # Test permissions
        print("\n🔐 Testing database permissions...")
        
        # Test if we can create a simple table
        print("   Creating test table...")
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS connection_test (
                id SERIAL PRIMARY KEY,
                test_message TEXT
            )
        """))
        print("   ✅ CREATE TABLE permission: OK")
        
        # Insert test data
        print("   Inserting test data...")
        db.execute(text("INSERT INTO connection_test (test_message) VALUES ('Hello from Blumn!')"))
        db.commit()
        print("   ✅ INSERT permission: OK")
        
        # Read test data
        print("   Reading test data...")
        result = db.execute(text("SELECT test_message FROM connection_test ORDER BY id DESC LIMIT 1"))
        test_message = result.fetchone()[0]
        print(f"   ✅ SELECT permission: OK (message: {test_message})")
        
        # Clean up
        print("   Cleaning up test table...")
        db.execute(text("DROP TABLE connection_test"))
        db.commit()
        print("   ✅ DROP TABLE permission: OK")
        
        db.close()
        
        print("\n✅ All database tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database connection test failed!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        
        # Provide specific troubleshooting based on error type
        error_msg = str(e).lower()
        
        print("\n🔧 Troubleshooting suggestions:")
        
        if "could not connect to server" in error_msg or "connection refused" in error_msg:
            print("   1. Check if the RDS instance is running")
            print("   2. Verify the hostname is correct")
            print("   3. Check AWS Security Group allows inbound traffic on port 5432")
            print("   4. Ensure RDS instance is publicly accessible")
            print("   5. Check if you're behind a firewall or VPN")
            
        elif "password authentication failed" in error_msg:
            print("   1. Verify the password is correct")
            print("   2. Check if the username exists in the database")
            print("   3. Ensure no special characters need escaping in the password")
            
        elif "database" in error_msg and "does not exist" in error_msg:
            print("   1. Verify the database name is correct")
            print("   2. Check if the database was created in RDS")
            print("   3. Try connecting to 'postgres' database first")
            
        elif "timeout" in error_msg:
            print("   1. Check network connectivity to AWS")
            print("   2. Verify Security Group settings")
            print("   3. Check if RDS is in a private subnet")
            print("   4. Try increasing connection timeout")
            
        else:
            print("   Check the full error details above")
            
        print("\n📋 Full error traceback:")
        traceback.print_exc()
        
        return False

if __name__ == "__main__":
    print("🌱 Blumn Plant Care Tracker - Database Connection Test")
    print("=" * 50)
    
    # Show current working directory
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    
    if test_database_connection():
        print("\n🎉 Your database is ready to use!")
    else:
        print("\n❌ Database connection failed. Please check your configuration.")
        sys.exit(1) 