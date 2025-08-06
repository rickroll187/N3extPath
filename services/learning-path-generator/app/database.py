"""
Database Configuration for Learning Path Generator Service
Where learning journeys are stored with more care than your mom's recipe collection! 🛤️💾
Coded with love and caffeine by rickroll187 at 2025-08-03 18:06:49 UTC
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from common.vault import get_db_creds

logger = logging.getLogger(__name__)

# Database base class
Base = declarative_base()

class DatabaseBro:
    """Database connection manager for learning paths - your data's personal trainer! 💪"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._connect()
    
    def _connect(self):
        """Connect to the learning database like a wise sensei connecting to the universe"""
        try:
            # Get credentials from Vault (our digital monk)
            creds = get_db_creds()
            
            # Construct database URL (the path to enlightenment!)
            database_url = (
                f"postgresql://{creds['username']}:{creds['password']}"
                f"@{creds['host']}:{creds['port']}/{os.getenv('DB_NAME', 'learning_path_generator')}"
            )
            
            self.engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=os.getenv("SQL_DEBUG", "false").lower() == "true"
            )
            
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info("🛤️ Learning path database connection established - ready to navigate careers!")
            
        except Exception as e:
            logger.error(f"💥 Database connection failed (even GPS needs signal sometimes): {e}")
            raise

    def create_tables(self):
        """Create all learning path tables - building the foundation for greatness!"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("📋 Learning path database tables created - time to start some journeys!")
        except Exception as e:
            logger.error(f"💥 Failed to create tables: {e}")
            raise

# Global database instance
db_manager = DatabaseBro()

def get_db() -> Session:
    """Dependency to get database session - your ticket to the learning data universe!"""
    db = db_manager.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database tables - let the learning begin!"""
    db_manager.create_tables()
