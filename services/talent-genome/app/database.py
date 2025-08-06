"""
Database Configuration for Talent Genome Service
Where talent DNA is stored with more care than the actual Human Genome Project! 🧬💾
Coded with genetic precision by rickroll187 at 2025-08-03 18:22:04 UTC
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
    """Database connection manager for talent genomes - your data's personal geneticist! 🧬"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._connect()
    
    def _connect(self):
        """Connect to the talent genome database like a DNA helix connecting to success"""
        try:
            # Get credentials from Vault (our digital genetics lab)
            creds = get_db_creds()
            
            # Construct database URL (the genetic sequence for connection!)
            database_url = (
                f"postgresql://{creds['username']}:{creds['password']}"
                f"@{creds['host']}:{creds['port']}/{os.getenv('DB_NAME', 'talent_genome')}"
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
            
            logger.info("🧬 Talent genome database connection established - ready to sequence careers!")
            
        except Exception as e:
            logger.error(f"💥 Database connection failed (even DNA needs proper sequencing): {e}")
            raise

    def create_tables(self):
        """Create all talent genome tables - building the foundation for genetic career analysis!"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("📋 Talent genome database tables created - time to decode some careers!")
        except Exception as e:
            logger.error(f"💥 Failed to create tables: {e}")
            raise

# Global database instance
db_manager

