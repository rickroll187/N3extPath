"""
Database Configuration for Skill Assessment Service
Where skill data lives with more precision than academic transcripts! 🎓💾
Coded with educational excellence by rickroll187 at 2025-08-03 19:22:38 UTC
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
    """Database connection manager for skill assessments - your data's personal tutor! 🎓"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._connect()
    
    def _connect(self):
        """Connect to the skill assessment database like knowledge connecting to wisdom"""
        try:
            # Get credentials from Vault (our digital academy registrar)
            creds = get_db_creds()
            
            # Construct database URL (the connection string to academic excellence!)
            database_url = (
                f"postgresql://{creds['username']}:{creds['password']}"
                f"@{creds['host']}:{creds['port']}/{os.getenv('DB_NAME', 'skill_assessment')}"
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
            
            logger.info("🎓 Skill assessment database connection established - ready to measure excellence!")
            
        except Exception as e:
            logger.error(f"💥 Database connection failed (even databases need good grades): {e}")
            raise

    def create_tables(self):
        """Create all skill assessment tables - building the foundation for academic achievement!"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("📋 Skill assessment database tables created - time to assess some brilliance!")
        except Exception as e:
            logger.error(f"💥 Failed to create tables: {e}")
            raise

# Global database instance
db_manager = DatabaseBro()

def get_db() -> Session:
    """Dependency to get database session - your ticket to the skill assessment universe!"""
    db = db_manager.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database tables - let the skill assessment begin!"""
    db_manager.create_tables()
