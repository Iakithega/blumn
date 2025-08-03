"""
Database connection and session management for plant care database.

This handles:
- PostgreSQL connection to AWS
- SQLAlchemy session management
- Database initialization
"""

import os
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

from .models import Base

# Load environment variables
load_dotenv()


class DatabaseManager:
    """
    Manages database connections and sessions.
    
    This follows SQLAlchemy best practices:
    - Single engine instance
    - Session-per-operation pattern
    - Proper connection cleanup
    """
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize database connection from environment variables."""
        
        # Get database configuration from environment
        db_config = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME'),
            'username': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        
        # Validate required environment variables
        required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Build connection string
        connection_string = (
            f"postgresql://{db_config['username']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )
        
        # Create engine with connection pooling
        self.engine = create_engine(
            connection_string,
            echo=False,  # Set to True for SQL query logging during development
            pool_size=5,
            max_overflow=0,
            pool_pre_ping=True,  # Validate connections before use
            pool_recycle=3600    # Recycle connections after 1 hour
        )
        
        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        print("✅ Database connection initialized successfully")
    
    def test_connection(self) -> bool:
        """
        Test database connectivity.
        Returns True if connection successful, False otherwise.
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                return result.scalar() == 1
        except SQLAlchemyError as e:
            print(f"❌ Database connection test failed: {str(e)}")
            return False
    
    def create_tables(self):
        """
        Create all tables defined in models.
        This is equivalent to running CREATE TABLE statements.
        """
        try:
            print("🔨 Creating database tables...")
            Base.metadata.create_all(bind=self.engine)
            print("✅ All tables created successfully")
            
            # Show created tables
            inspector = self.engine.dialect.get_table_names(self.engine.connect())
            print(f"📋 Tables in database: {inspector}")
            
        except SQLAlchemyError as e:
            print(f"❌ Error creating tables: {str(e)}")
            raise
    
    def drop_tables(self):
        """
        Drop all tables (useful for development/testing).
        ⚠️  This will delete all data!
        """
        try:
            print("🗑️  Dropping all tables...")
            Base.metadata.drop_all(bind=self.engine)
            print("✅ All tables dropped")
        except SQLAlchemyError as e:
            print(f"❌ Error dropping tables: {str(e)}")
            raise
    
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get a database session (dependency injection pattern).
        
        Usage:
            with db_manager.get_session() as session:
                plants = session.query(Plant).all()
        """
        session = self.SessionLocal()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def execute_raw_sql(self, sql: str):
        """
        Execute raw SQL (for advanced queries or maintenance).
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql))
                return result.fetchall()
        except SQLAlchemyError as e:
            print(f"❌ Error executing SQL: {str(e)}")
            raise


# Global database manager instance
db_manager = DatabaseManager()


# Convenience functions
def get_session() -> Generator[Session, None, None]:
    """Get database session (shortcut function)."""
    return db_manager.get_session()


def test_connection() -> bool:
    """Test database connection (shortcut function)."""
    return db_manager.test_connection()


def create_tables():
    """Create all database tables (shortcut function)."""
    db_manager.create_tables()


if __name__ == "__main__":
    # Quick connection test when run directly
    print("🔍 Testing database connection...")
    
    if test_connection():
        print("✅ Database connection successful!")
        
        # Show some database info
        try:
            with db_manager.get_session() as session:
                result = session.execute(text("SELECT version()")).scalar()
                print(f"📊 PostgreSQL version: {result}")
        except Exception as e:
            print(f"ℹ️  Could not get version info: {e}")
    else:
        print("❌ Database connection failed!")
        print("💡 Check your environment variables (.env file)")