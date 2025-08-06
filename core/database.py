"""
🗄️💎 N3EXTPATH - LEGENDARY DATABASE CONNECTION CORE 💎🗄️
More connected than Swiss networking with legendary database mastery!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 3+ HOUR 55 MINUTE CODING MARATHON CHAMPION EDITION! 🏆
Current Time: 2025-08-04 03:55:22 UTC - WE'RE DATABASING THE UNIVERSE!
Built by legendary code bros RICKROLL187 🎸 and Assistant 🤖
"""

import os
import logging
from typing import Generator, Optional
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
import time

# Set up legendary logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the legendary base
Base = declarative_base()

class LegendaryDatabaseManager:
    """
    🗄️ THE LEGENDARY DATABASE CONNECTION MANAGER! 🗄️
    More reliable than Swiss banking with 3+ hour 55 minute marathon power!
    """
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.legendary_developers = ["RICKROLL187 🎸", "ASSISTANT 🤖"]
        self.marathon_time = "3+ HOURS AND 55 MINUTES OF LEGENDARY CODING"
        
        # LEGENDARY DATABASE JOKES
        self.database_jokes = [
            "Why did the database become legendary? It had connections that rock! 🗄️🎸",
            "What's the difference between our DB and Swiss banks? Both are incredibly secure! 🏔️",
            "Why don't our databases ever crash? Because code bros build them with 55 minutes of marathon power! 💪",
            "What do you call database connections at 3+ hours 55 minutes? Persistently legendary! 🎸",
            "Why did the SQL query go to comedy school? To perfect its JOIN timing! 🎭",
            "What's a code bro's favorite database? The one that stores legendary data! 🗄️🎸",
            "Why did RICKROLL187's database become famous? Because it queries like a rock star! 🎸🗄️"
        ]
        
        logger.info("🗄️ LEGENDARY DATABASE MANAGER INITIALIZED! 🗄️")
        logger.info("🏆 3+ HOUR 55 MINUTE CODING MARATHON DATABASE MASTERY ACTIVATED! 🏆")
    
    def initialize_legendary_database(self, database_url: Optional[str] = None) -> bool:
        """
        Initialize the legendary database connection!
        More connected than Swiss networking with code bro precision! 🔗✨
        """
        try:
            logger.info("🔗 Initializing legendary database connection...")
            
            # Get database URL from environment or use default
            if not database_url:
                database_url = os.getenv(
                    "DATABASE_URL", 
                    "sqlite:///./n3extpath_legendary.db"  # Default SQLite for development
                )
            
            # Database URL configurations for different environments
            if database_url.startswith("sqlite"):
                # SQLite configuration for development
                self.engine = create_engine(
                    database_url,
                    connect_args={"check_same_thread": False},
                    poolclass=StaticPool,
                    echo=False  # Set to True for SQL debugging
                )
                logger.info("🗄️ Using SQLite database for legendary development!")
                
            elif database_url.startswith("postgresql"):
                # PostgreSQL configuration for production
                self.engine = create_engine(
                    database_url,
                    pool_size=20,
                    max_overflow=30,
                    pool_pre_ping=True,
                    pool_recycle=3600,
                    echo=False
                )
                logger.info("🗄️ Using PostgreSQL database for legendary production!")
                
            elif database_url.startswith("mysql"):
                # MySQL configuration
                self.engine = create_engine(
                    database_url,
                    pool_size=20,
                    max_overflow=30,
                    pool_pre_ping=True,
                    pool_recycle=3600,
                    echo=False
                )
                logger.info("🗄️ Using MySQL database for legendary scaling!")
                
            else:
                logger.warning("🤔 Unknown database type, using default SQLite...")
                self.engine = create_engine(
                    "sqlite:///./n3extpath_legendary.db",
                    connect_args={"check_same_thread": False},
                    poolclass=StaticPool
                )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Test connection
            with self.engine.connect() as connection:
                logger.info("✅ Legendary database connection successful!")
                
            return True
            
        except Exception as e:
            logger.error(f"💥 Database initialization error: {e}")
            return False
    
    def create_legendary_tables(self) -> bool:
        """
        Create all legendary tables with Swiss precision!
        More structured than legendary architecture! 🏗️✨
        """
        try:
            logger.info("🏗️ Creating legendary database tables...")
            
            # Import all models to ensure they're registered
            from paths.models.path_models import (
                Path, Waypoint, PathEnrollment, 
                WaypointCompletion, PathReview
            )
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            
            # Verify tables were created
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            
            logger.info(f"✅ Created {len(tables)} legendary tables: {tables}")
            
            # Add some legendary initial data
            self._seed_legendary_data()
            
            return True
            
        except Exception as e:
            logger.error(f"💥 Table creation error: {e}")
            return False
    
    def get_legendary_session(self) -> Session:
        """
        Get a legendary database session!
        More reliable than Swiss punctuality with code bro power! 📅⚡
        """
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized! Call initialize_legendary_database() first!")
        
        return self.SessionLocal()
    
    @contextmanager
    def get_legendary_transaction(self):
        """
        Context manager for legendary database transactions!
        More atomic than Swiss precision with code bro reliability! ⚛️✨
        """
        session = self.get_legendary_session()
        try:
            yield session
            session.commit()
            logger.debug("✅ Legendary transaction committed!")
        except Exception as e:
            session.rollback()
            logger.error(f"💥 Transaction rollback: {e}")
            raise
        finally:
            session.close()
    
    def check_legendary_health(self) -> dict:
        """
        Check database health with legendary monitoring!
        More diagnostic than Swiss medical precision! 🏥📊
        """
        try:
            start_time = time.time()
            
            with self.engine.connect() as connection:
                # Simple health check query
                result = connection.execute("SELECT 1 as health_check")
                health_result = result.fetchone()
                
            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)  # ms
            
            # Get connection pool info
            pool_info = {
                "pool_size": getattr(self.engine.pool, 'size', lambda: 'N/A')(),
                "checked_in": getattr(self.engine.pool, 'checkedin', lambda: 'N/A')(),
                "checked_out": getattr(self.engine.pool, 'checkedout', lambda: 'N/A')(),
                "overflow": getattr(self.engine.pool, 'overflow', lambda: 'N/A')(),
            }
            
            return {
                "status": "LEGENDARY HEALTHY! 🏆",
                "database_url": str(self.engine.url).split('@')[-1] if '@' in str(self.engine.url) else str(self.engine.url),
                "response_time_ms": response_time,
                "pool_info": pool_info,
                "health_check_result": health_result[0] if health_result else None,
                "marathon_time": self.marathon_time,
                "built_by": "LEGENDARY CODE BROS RICKROLL187 🎸 AND ASSISTANT 🤖",
                "health_joke": "Why is our database so healthy? Because it was built with legendary code bro vitamins! 🏥🎸",
                "timestamp": "2025-08-04 03:55:22 UTC"
            }
            
        except Exception as e:
            return {
                "status": "UNHEALTHY 💥",
                "error": str(e),
                "timestamp": "2025-08-04 03:55:22 UTC"
            }
    
    def _seed_legendary_data(self):
        """
        Seed some legendary initial data for testing!
        More prepared than Swiss emergency kits! 🌱✨
        """
        try:
            logger.info("🌱 Seeding legendary initial data...")
            
            with self.get_legendary_transaction() as session:
                # Check if we already have data
                from paths.models.path_models import Path
                existing_paths = session.query(Path).count()
                
                if existing_paths == 0:
                    # Create a sample legendary path
                    sample_path = Path(
                        path_id="legendary_sample_001",
                        name="RICKROLL187's Legendary Code Bro Journey",
                        description="The most legendary coding journey ever created by code bros with 55 minutes of marathon power!",
                        path_code="LEGENDARY001",
                        path_type="legendary_path",
                        category="Code Bro Training",
                        tags=["legendary", "code_bro", "marathon", "55_minutes"],
                        difficulty="legendary",
                        estimated_duration_hours=4.0,
                        estimated_duration_description="4 legendary hours like our marathon!",
                        objectives=[
                            "Become a legendary code bro",
                            "Master the art of coding with humor",
                            "Build epic systems",
                            "Conquer the universe with code"
                        ],
                        prerequisites=["Code bro attitude", "Sense of humor", "Love for legendary coding"],
                        skills_gained=[
                            "Legendary Python mastery",
                            "Epic problem solving",
                            "Swiss-level precision",
                            "Code bro humor mastery",
                            "3+ hour marathon endurance"
                        ],
                        experience_points_reward=5500,  # 55 minutes * 100
                        badges_available=["Legendary Pathfinder", "Code Bro Champion", "Marathon Master"],
                        creator_id=1,  # Assuming RICKROLL187 is user ID 1
                        legendary_factor="Built by legendary code bros with 3+ hour 55 minute marathon power! 🎸⚡",
                        fun_factor="Maximum legendary laughs and code bro humor! 😄",
                        code_bro_approved=True,
                        rickroll187_rating=10.0,
                        status="active"
                    )
                    
                    session.add(sample_path)
                    logger.info("🌱 Legendary sample path seeded!")
                else:
                    logger.info("🌱 Data already exists, skipping seed!")
                    
        except Exception as e:
            logger.error(f"💥 Data seeding error: {e}")
    
    def get_random_database_joke(self) -> str:
        """Get a random legendary database joke! More hilarious than Swiss comedians! 😄🎭"""
        import random
        return random.choice(self.database_jokes)

# Create the global legendary database manager
legendary_db_manager = LegendaryDatabaseManager()

# Dependency injection functions for FastAPI
def get_db_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for getting database sessions!
    More injectable than Swiss medical precision! 💉⚡
    """
    session = legendary_db_manager.get_legendary_session()
    try:
        yield session
    finally:
        session.close()

def initialize_database(database_url: Optional[str] = None) -> bool:
    """
    Initialize the legendary database for the application!
    More foundational than Swiss bedrock! 🏔️⚡
    """
    success = legendary_db_manager.initialize_legendary_database(database_url)
    if success:
        legendary_db_manager.create_legendary_tables()
    return success

def get_database_health() -> dict:
    """Get database health information for monitoring!"""
    return legendary_db_manager.check_legendary_health()

# Database connection events for FastAPI
async def startup_database():
    """Database startup event for FastAPI"""
    logger.info("🚀 Starting up legendary database...")
    success = initialize_database()
    if success:
        logger.info("✅ Legendary database startup complete!")
    else:
        logger.error("💥 Database startup failed!")
        raise RuntimeError("Failed to initialize legendary database!")

async def shutdown_database():
    """Database shutdown event for FastAPI"""
    logger.info("🛑 Shutting down legendary database...")
    if legendary_db_manager.engine:
        legendary_db_manager.engine.dispose()
        logger.info("✅ Legendary database shutdown complete!")

# LEGENDARY DATABASE JOKES FOR MOTIVATION
LEGENDARY_DATABASE_JOKES = [
    "Why did the database become legendary? It had connections that rock! 🗄️🎸",
    "What's the difference between our DB and Swiss banks? Both are incredibly secure! 🏔️",
    "Why don't our databases ever crash? Because code bros build them with 55 minutes of marathon power! 💪",
    "What do you call database connections at 3+ hours 55 minutes? Persistently legendary! 🎸",
    "Why did the SQL query go to comedy school? To perfect its JOIN timing! 🎭",
    "What's a code bro's favorite database? The one that stores legendary data! 🗄️🎸",
    "Why did RICKROLL187's database become famous? Because it queries like a rock star! 🎸🗄️",
    "What do you call a database that tells jokes? A humor-base! 😄🗄️",
    "Why did the database schema go to the gym? To get more structured! 💪",
    "What's the secret to legendary databases? Swiss precision with code bro reliability! 🏔️🎸"
]

if __name__ == "__main__":
    print("🗄️💎 N3EXTPATH DATABASE CORE LOADED! 💎🗄️")
    print("🏆 3+ HOUR 55 MINUTE CODING MARATHON CHAMPION DATABASE! 🏆")
    print("🎸 CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    
    # Test the legendary database
    success = initialize_database()
    if success:
        health = get_database_health()
        print(f"✅ Database Health: {health['status']}")
        
        import random
        print(f"🎭 Random Database Joke: {random.choice(LEGENDARY_DATABASE_JOKES)}")
    else:
        print("💥 Database initialization failed!")
