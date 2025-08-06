# File: core/database_config.py
"""
🗄️🎸 N3EXTPATH - DATABASE CONFIGURATION & CONNECTION MANAGEMENT 🎸🗄️
Professional database setup with SQLAlchemy and connection pooling
Built: 2025-08-05 15:11:35 UTC by RICKROLL187
"""

import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import QueuePool
from typing import Generator
import asyncpg
import asyncio

# Database configuration
DATABASE_CONFIG = {
    "postgresql": {
        "driver": "postgresql+asyncpg",
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "database": os.getenv("DB_NAME", "n3extpath_hr"),
        "username": os.getenv("DB_USER", "n3extpath_user"),
        "password": os.getenv("DB_PASSWORD", "legendary_password"),
        "pool_size": 20,
        "max_overflow": 30,
        "pool_timeout": 30,
        "pool_recycle": 3600
    },
    "sqlite": {
        "driver": "sqlite+aiosqlite",
        "database": "n3extpath_hr.db",
        "pool_size": 5,
        "echo": True
    }
}

# SQLAlchemy setup
Base = declarative_base()
metadata = MetaData()

# Database URL construction
def get_database_url(config_type: str = "postgresql") -> str:
    """Construct database URL from configuration"""
    config = DATABASE_CONFIG[config_type]
    
    if config_type == "postgresql":
        return f"{config['driver']}://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    elif config_type == "sqlite":
        return f"{config['driver']}:///{config['database']}"

# Create engine with connection pooling
engine = create_engine(
    get_database_url(),
    poolclass=QueuePool,
    pool_size=DATABASE_CONFIG["postgresql"]["pool_size"],
    max_overflow=DATABASE_CONFIG["postgresql"]["max_overflow"],
    pool_timeout=DATABASE_CONFIG["postgresql"]["pool_timeout"],
    pool_recycle=DATABASE_CONFIG["postgresql"]["pool_recycle"],
    echo=False  # Set to True for SQL debugging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database dependency for FastAPI
def get_db() -> Generator:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database models
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="employee")
    department = Column(String, nullable=False)
    status = Column(String, nullable=False, default="active")
    is_legendary = Column(Boolean, default=False)
    hire_date = Column(DateTime)
    last_login = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    # Relationships
    objectives = relationship("Objective", back_populates="owner")
    performance_reviews = relationship("PerformanceReview", back_populates="employee")

class Objective(Base):
    __tablename__ = "objectives"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    category = Column(String, default="individual")
    priority = Column(String, default="medium")
    target_date = Column(DateTime)
    status = Column(String, default="active")
    progress = Column(Float, default=0.0)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="objectives")
    key_results = relationship("KeyResult", back_populates="objective")

class KeyResult(Base):
    __tablename__ = "key_results"
    
    id = Column(String, primary_key=True)
    objective_id = Column(String, ForeignKey("objectives.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, default=0.0)
    unit = Column(String)
    progress = Column(Float, default=0.0)
    status = Column(String, default="active")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    # Relationships
    objective = relationship("Objective", back_populates="key_results")

class PerformanceReview(Base):
    __tablename__ = "performance_reviews"
    
    id = Column(String, primary_key=True)
    employee_id = Column(String, ForeignKey("users.id"), nullable=False)
    manager_id = Column(String, ForeignKey("users.id"), nullable=False)
    review_period_start = Column(DateTime, nullable=False)
    review_period_end = Column(DateTime, nullable=False)
    review_type = Column(String, default="quarterly")
    status = Column(String, default="draft")
    final_rating = Column(Float)
    manager_feedback = Column(Text)
    employee_feedback = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    # Relationships
    employee = relationship("User", back_populates="performance_reviews", foreign_keys=[employee_id])

# Database initialization
async def init_database():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_sample_data():
    """Create sample data for development"""
    from datetime import datetime
    import uuid
    
    session = SessionLocal()
    
    try:
        # Create RICKROLL187 user
        rickroll_user = User(
            id="rickroll187",
            username="rickroll187",
            email="rickroll187@n3extpath.com",
            hashed_password="$2b$12$legendary_hash",
            first_name="RICKROLL187",
            last_name="Legendary Founder",
            role="rickroll187",
            department="legendary",
            status="legendary",
            is_legendary=True,
            hire_date=datetime(2024, 1, 1),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        session.add(rickroll_user)
        
        # Create sample objective
        sample_objective = Objective(
            id=str(uuid.uuid4()),
            title="Build Legendary HR Platform",
            description="Create the most professional HR platform with legendary features",
            owner_id="rickroll187",
            category="company",
            priority="critical",
            target_date=datetime(2025, 12, 31),
            status="active",
            progress=75.0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        session.add(sample_objective)
        session.commit()
        
    except Exception as e:
        session.rollback()
        print(f"Error creating sample data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    print("🗄️ N3EXTPATH Database Configuration Ready!")
    print(f"Database URL: {get_database_url()}")
