"""
Database Configuration for Performance Management Service
Where performance data lives with more security than classified government files! 📊💾
Coded with performance precision by rickroll187 at 2025-08-03 19:10:09 UTC
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
    """Database connection manager for performance data - your data's personal trainer! 📊"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._connect()
    
    def _connect(self):
        """Connect to the performance database like a goal connecting to achievement"""
        try:
            # Get credentials from Vault (our digital performance coach)
            creds = get_db_creds()
            
            # Construct database URL (the connection string to performance heaven!)
            database_url = (
                f"postgresql://{creds['username']}:{creds['password']}"
                f"@{creds['host']}:{creds['port']}/{os.getenv('DB_NAME', 'performance_management')}"
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
            
            logger.info("📊 Performance management database connection established - ready to track greatness!")
            
        except Exception as e:
            logger.error(f"💥 Database connection failed (even databases need good performance reviews): {e}")
            raise

    def create_tables(self):
        """Create all performance management tables - building the foundation for tracking excellence!"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("📋 Performance management database tables created - time to measure some greatness!")
        except Exception as e:
            logger.error(f"💥 Failed to create tables: {e}")
            raise

# Global database instance
db_manager = DatabaseBro()

def get_db() -> Session:
    """Dependency to get database session - your ticket to the performance universe!"""
    db = db_manager.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database tables - let the performance tracking begin!"""
    db_manager.create_tables()
