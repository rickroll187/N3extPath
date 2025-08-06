"""
Database Configuration for Hiring Process Service
Where recruitment data lives with more security than Fort Knox! 🎯💾
Coded with hiring precision by rickroll187 at 2025-08-03 18:38:13 UTC
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
    """Database connection manager for hiring processes - your data's personal recruiter! 🎯"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._connect()
    
    def _connect(self):
        """Connect to the hiring database like a perfect candidate connecting to their dream job"""
        try:
            # Get credentials from Vault (our digital HR department)
            creds = get_db_creds()
            
            # Construct database URL (the connection string to employment heaven!)
            database_url = (
                f"postgresql://{creds['username']}:{creds['password']}"
                f"@{creds['host']}:{creds['port']}/{os.getenv('DB_NAME', 'hiring_process')}"
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
            
            logger.info("🎯 Hiring process database connection established - ready to find perfect matches!")
            
        except Exception as e:
            logger.error(f"💥 Database connection failed (even databases need good interviews): {e}")
            raise

    def create_tables(self):
        """Create all hiring process tables - building the foundation for perfect hires!"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("📋 Hiring process database tables created - time to start recruiting legends!")
        except Exception as e:
            logger.error(f"💥 Failed to create tables: {e}")
            raise

# Global database instance
db_manager = DatabaseBro()

def get_db() -> Session:
    """Dependency to get database session - your ticket to the recruitment universe!"""
    db = db_manager.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database tables - let the hiring begin!"""
    db_manager.create_tables()
