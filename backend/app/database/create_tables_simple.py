#!/usr/bin/env python3
"""
Simple table creation script that works with your existing .env setup.
Run this from your project root directory.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, DateTime, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Database models (simplified version)
Base = declarative_base()

class Plant(Base):
    __tablename__ = "plants"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    care_records = relationship("DailyCare", back_populates="plant", cascade="all, delete-orphan")

class DailyCare(Base):
    __tablename__ = "daily_care"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    care_date = Column(Date, nullable=False)
    water_ml = Column(Integer, nullable=True)
    fertilizer = Column(String(50), nullable=True)
    treatment = Column(String(50), nullable=True)
    condition = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (UniqueConstraint('plant_id', 'care_date', name='unique_plant_date'),)
    
    plant = relationship("Plant", back_populates="care_records")

def main():
    print("🌱 Plant Care Database Setup (Simple Version)")
    print("=" * 50)
    
    # Get database credentials from environment
    db_config = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME'),
        'username': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    
    print(f"📋 Database Configuration:")
    print(f"   Host: {db_config['host']}")
    print(f"   Port: {db_config['port']}")
    print(f"   Database: {db_config['database']}")
    print(f"   User: {db_config['username']}")
    print(f"   Password: {'*' * len(db_config['password']) if db_config['password'] else 'Not set'}")
    
    # Check if all required variables are set
    required_vars = ['host', 'database', 'username', 'password']
    missing_vars = [var for var in required_vars if not db_config[var]]
    
    if missing_vars:
        print(f"\n❌ Missing required variables: {', '.join(missing_vars)}")
        print("   Check your .env file in the project root")
        return False
    
    # Build connection string
    connection_string = (
        f"postgresql://{db_config['username']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )
    
    try:
        print(f"\n🔌 Connecting to database...")
        engine = create_engine(connection_string, echo=False)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        print(f"\n🔨 Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # Show created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        print(f"\n📋 Created tables: {table_names}")
        
        # Test table access
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        plant_count = session.query(Plant).count()
        care_count = session.query(DailyCare).count()
        
        print(f"\n📊 Table verification:")
        print(f"   plants table: {plant_count} records")
        print(f"   daily_care table: {care_count} records")
        
        session.close()
        
        print(f"\n🎉 Database setup complete!")
        print(f"\n💡 Next step: python backend/app/database/migrate_excel_simple.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()