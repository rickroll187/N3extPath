"""
Database Configuration for Training-to-Role Service
Where data lives and dreams come true!
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
    """Database connection manager - your data's best friend"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._connect()
    
    def _connect(self):
        """Connect to the database like a boss"""
        try:
            # Get credentials from Vault
            creds = get_db_creds()
            
            # Construct database URL
            database_url = (
                f"postgresql://{creds['username']}:{creds['password']}"
                f"@{creds['host']}:{creds['port']}/{os.getenv('DB_NAME', 'training_to_role')}"
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
            
            logger.info("🗄️ Database connection established")
            
        except Exception as e:
            logger.error(f"💥 Database connection failed: {e}")
            raise

    def create_tables(self):
        """Create all tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("📋 Database tables created")
        except Exception as e:
            logger.error(f"💥 Failed to create tables: {e}")
            raise

# Global database instance
db_manager = DatabaseBro()

def get_db() -> Session:
    """Dependency to get database session"""
    db = db_manager.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database tables"""
    db_manager.create_tables()
