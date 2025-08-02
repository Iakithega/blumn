from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

# Alternative: Build DATABASE_URL from individual components
if not DATABASE_URL:
    # Try to build from individual environment variables
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT", "5432")  # Default PostgreSQL port
    DB_NAME = os.environ.get("DB_NAME", "postgres")  # Default database name
    
    if all([DB_USER, DB_PASSWORD, DB_HOST]):
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(f"Built DATABASE_URL from individual components: postgresql://{DB_USER}:****@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Fix for Heroku PostgreSQL URL format (postgres:// -> postgresql://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Validate connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=False           # Set to True for SQL query logging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Function to drop all tables (use carefully!)
def drop_tables():
    Base.metadata.drop_all(bind=engine) 