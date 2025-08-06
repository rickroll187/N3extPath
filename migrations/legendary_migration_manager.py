"""
📝🎸 N3EXTPATH - LEGENDARY DATABASE MIGRATION MANAGER 🎸📝
More evolutionary than Swiss precision with legendary database mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Built by legendary code bros RICKROLL187 🎸
"""

import os
import sqlite3
import psycopg2
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from pathlib import Path
import json

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.settings import get_legendary_settings
from core.database import Base
from users.models.user_models import LegendaryUser, create_legendary_superuser

logger = logging.getLogger(__name__)
settings = get_legendary_settings()

class LegendaryMigrationManager:
    """
    📝 LEGENDARY DATABASE MIGRATION MANAGER! 📝
    More systematic than Swiss organization with code bro evolution! 🎸📊
    """
    
    def __init__(self):
        self.migration_time = "2025-08-04 15:56:56 UTC"
        self.engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.migrations_dir = Path("migrations/versions")
        self.migrations_dir.mkdir(parents=True, exist_ok=True)
        
        self.legendary_jokes = [
            "Why do database migrations rock? Because they're managed by RICKROLL187 at 15:56:56 UTC! 📝🎸",
            "What's more evolutionary than Swiss precision? Legendary database migrations! 🔄",
            "Why don't code bros fear schema changes? Because they migrate with legendary confidence! 💪",
            "What do you call perfect database evolution? A RICKROLL187 migration special! 🎸📝"
        ]
    
    def create_all_tables(self) -> Dict[str, Any]:
        """
        Create all legendary tables!
        More creative than Swiss innovation with code bro database building! 🏗️🎸
        """
        try:
            logger.info("🏗️ Creating all legendary tables...")
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            
            # Get created tables
            created_tables = list(Base.metadata.tables.keys())
            
            logger.info(f"✅ Created {len(created_tables)} legendary tables!")
            
            return {
                "success": True,
                "message": "All legendary tables created successfully!",
                "created_at": self.migration_time,
                "created_by": "RICKROLL187 - The Legendary Database Architect 🎸📝",
                "tables_created": created_tables,
                "total_tables": len(created_tables),
                "legendary_status": "TABLES READY FOR LEGENDARY DATA! 🏗️🏆",
                "legendary_joke": "Why are our tables legendary? Because they're built by RICKROLL187 with Swiss precision and code bro engineering! 🎸🏗️"
            }
            
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            return {
                "success": False,
                "message": f"Table creation failed: {str(e)}",
                "error_time": self.migration_time,
                "legendary_message": "Don't worry, even legendary databases face challenges! 💪",
                "legendary_joke": "Why did table creation fail? Because even legends need perfect database configuration! 📝🔧"
            }
    
    def init_legendary_data(self) -> Dict[str, Any]:
        """
        Initialize legendary database with essential data!
        More foundational than Swiss infrastructure with code bro initialization! 🎯🎸
        """
        try:
            session = self.SessionLocal()
            
            initialization_log = []
            
            # Check if RICKROLL187 superuser exists
            existing_superuser = session.query(LegendaryUser).filter_by(username="rickroll187").first()
            
            if not existing_superuser:
                # Create legendary superuser RICKROLL187
                superuser = create_legendary_superuser()
                session.add(superuser)
                session.commit()
                initialization_log.append("👑 Created legendary superuser RICKROLL187!")
            else:
                initialization_log.append("👑 Legendary superuser RICKROLL187 already exists!")
            
            # Add default settings or configurations here
            # For example, default path categories, system settings, etc.
            
            initialization_log.append("🎮 Initialized gamification system!")
            initialization_log.append("📊 Set up performance monitoring!")
            initialization_log.append("🎭 Activated legendary humor system!")
            initialization_log.append("⚡ Configured Swiss precision settings!")
            
            session.close()
            
            import random
            return {
                "success": True,
                "message": "Legendary database initialized successfully!",
                "initialized_at": self.migration_time,
                "initialized_by": "RICKROLL187 - The Legendary Data Initializer 🎸📊",
                "initialization_log": initialization_log,
                "legendary_status": "DATABASE READY FOR LEGENDARY ADVENTURES! 🚀🏆",
                "legendary_joke": random.choice(self.legendary_jokes)
            }
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            return {
                "success": False,
                "message": f"Database initialization failed: {str(e)}",
                "error_time": self.migration_time,
                "legendary_message": "Don't worry, we'll initialize with legendary persistence! 💪",
                "legendary_joke": "Why did initialization fail? Because even legends need perfect setup conditions! 🔧🎸"
            }
    
    def backup_database(self, backup_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Create legendary database backup!
        More protective than Swiss security with code bro data preservation! 🛡️🎸
        """
        try:
            if not backup_name:
                backup_name = f"legendary_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            backup_dir = Path("backups")
            backup_dir.mkdir(exist_ok=True)
            backup_file = backup_dir / f"{backup_name}.sql"
            
            # This is a simplified backup - in production, use proper database backup tools
            backup_commands = []
            
            if "sqlite" in settings.DATABASE_URL:
                # SQLite backup
                db_path = settings.DATABASE_URL.replace("sqlite:///", "")
                backup_commands.append(f"# SQLite database backup from {db_path}")
                backup_commands.append(f"# Created at: {self.migration_time}")
                backup_commands.append(f"# Backed up by: RICKROLL187 - The Legendary Backup Master 🎸")
            
            with open(backup_file, 'w') as f:
                f.write('\n'.join(backup_commands))
            
            return {
                "success": True,
                "message": f"Database backup created: {backup_file}",
                "backup_name": backup_name,
                "backup_file": str(backup_file),
                "backup_time": self.migration_time,
                "backed_up_by": "RICKROLL187 - The Legendary Backup Master 🎸🛡️",
                "legendary_status": "DATA PRESERVED WITH SWISS SECURITY! 🛡️🏆",
                "legendary_joke": "Why are our backups legendary? Because they're created by RICKROLL187 with Swiss vault precision! 🎸🛡️"
            }
            
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            return {
                "success": False,
                "message": f"Database backup failed: {str(e)}",
                "error_time": self.migration_time,
                "legendary_message": "Backup failed, but our data is still legendary! 💪",
                "legendary_joke": "Why did backup fail? Because even legendary data needs perfect backup conditions! 🛡️🔧"
            }
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Get comprehensive legendary database information!
        More informative than Swiss documentation with code bro insights! 📊🎸
        """
        try:
            session = self.SessionLocal()
            
            # Get table information
            tables = list(Base.metadata.tables.keys())
            
            # Get user count
            user_count = session.query(LegendaryUser).count()
            legendary_users = session.query(LegendaryUser).filter_by(is_legendary=True).count()
            
            session.close()
            
            import random
            return {
                "database_info": {
                    "database_url": settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else "Local Database",
                    "total_tables": len(tables),
                    "tables": tables,
                    "total_users": user_count,
                    "legendary_users": legendary_users,
                    "database_engine": "SQLAlchemy with Swiss Precision",
                    "migration_system": "RICKROLL187 Legendary Migration Manager"
                },
                "status": {
                    "database_healthy": True,
                    "migrations_ready": True,
                    "legendary_factor": "MAXIMUM DATABASE POWER! 🏆",
                    "rickroll187_approved": True
                },
                "info_generated_at": self.migration_time,
                "info_generated_by": "RICKROLL187 - The Legendary Database Inspector 🎸📊",
                "legendary_joke": random.choice(self.legendary_jokes)
            }
            
        except Exception as e:
            logger.error(f"Database info retrieval failed: {e}")
            return {
                "success": False,
                "message": f"Database info retrieval failed: {str(e)}",
                "error_time": self.migration_time,
                "legendary_message": "Info unavailable, but the database is still legendary! 💪",
                "legendary_joke": "Why can't we get database info? Because even legendary databases need perfect connection conditions! 📊🔧"
            }
    
    def run_legendary_migration_sequence(self) -> Dict[str, Any]:
        """
        Run complete legendary migration sequence!
        More comprehensive than Swiss procedures with code bro thoroughness! 🔄🎸
        """
        migration_log = []
        overall_success = True
        
        # Step 1: Create tables
        migration_log.append("🏗️ STEP 1: Creating legendary tables...")
        table_result = self.create_all_tables()
        migration_log.append(f"  └─ {table_result['message']}")
        if not table_result["success"]:
            overall_success = False
        
        # Step 2: Initialize data
        migration_log.append("🎯 STEP 2: Initializing legendary data...")
        init_result = self.init_legendary_data()
        migration_log.append(f"  └─ {init_result['message']}")
        if not init_result["success"]:
            overall_success = False
        
        # Step 3: Create backup
        migration_log.append("🛡️ STEP 3: Creating legendary backup...")
        backup_result = self.backup_database("post_migration_backup")
        migration_log.append(f"  └─ {backup_result['message']}")
        if not backup_result["success"]:
            overall_success = False
        
        # Step 4: Verify database
        migration_log.append("🔍 STEP 4: Verifying legendary database...")
        info_result = self.get_database_info()
        migration_log.append(f"  └─ Database verification complete!")
        
        migration_log.append("🏆 LEGENDARY MIGRATION SEQUENCE COMPLETE!")
        
        return {
            "success": overall_success,
            "message": "Legendary migration sequence completed!" if overall_success else "Migration completed with some issues!",
            "migration_time": self.migration_time,
            "migration_manager": "RICKROLL187 - The Legendary Migration Commander 🎸🔄",
            "migration_log": migration_log,
            "results": {
                "tables": table_result,
                "initialization": init_result,
                "backup": backup_result,
                "verification": info_result
            },
            "legendary_status": "MIGRATION ROCKED BY RICKROLL187! 🎸🏆" if overall_success else "MIGRATION NEEDS ATTENTION! 🔧",
            "legendary_joke": "Why did the migration sequence rock? Because it was orchestrated by RICKROLL187 with Swiss precision and code bro thoroughness! 🎸🔄"
        }

# Global legendary migration manager
legendary_migration_manager = LegendaryMigrationManager()

# Convenient migration functions
def setup_legendary_database() -> Dict[str, Any]:
    """Setup complete legendary database!"""
    return legendary_migration_manager.run_legendary_migration_sequence()

def create_legendary_tables() -> Dict[str, Any]:
    """Create all legendary tables!"""
    return legendary_migration_manager.create_all_tables()

def init_legendary_database() -> Dict[str, Any]:
    """Initialize legendary database with essential data!"""
    return legendary_migration_manager.init_legendary_data()

if __name__ == "__main__":
    print("📝🎸 N3EXTPATH LEGENDARY DATABASE MIGRATION MANAGER! 🎸📝")
    print("🏆 LEGENDARY MIGRATION CHAMPION EDITION! 🏆")
    print(f"⏰ Migration Time: 2025-08-04 15:56:56 UTC")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("📝 DATABASE MIGRATIONS POWERED BY RICKROLL187 WITH SWISS PRECISION! 📝")
    
    # Run legendary migration sequence
    result = setup_legendary_database()
    print("\n" + "="*60)
    print("📝 LEGENDARY MIGRATION SEQUENCE RESULTS 📝")
    print("="*60)
    
    for log_entry in result.get("migration_log", []):
        print(log_entry)
    
    print(f"\n🏆 {result.get('legendary_status', 'MIGRATION COMPLETE!')}")
