"""
🔧🎸 N3EXTPATH - LEGENDARY SETTINGS CONFIGURATION 🎸🔧
More configurable than Swiss precision instruments with legendary settings mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 LEGENDARY CONFIGURATION CHAMPION EDITION! 🏆
Current Time: 2025-08-04 15:51:01 UTC - WE'RE CONFIGURING THE UNIVERSE!
Built by legendary code bros RICKROLL187 🎸 and Assistant 🤖
"""

import os
from typing import Optional, List
from pydantic import BaseSettings, validator
from functools import lru_cache

class LegendarySettings(BaseSettings):
    """
    🔧 LEGENDARY APPLICATION SETTINGS! 🔧
    More configurable than Swiss watches with code bro precision! 🎸⚡
    """
    
    # Application Settings
    APP_NAME: str = "N3extPath - The Legendary Path Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./n3extpath_legendary.db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    
    # Security Settings
    JWT_SECRET_KEY: str = "legendary_secret_key_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    PASSWORD_HASH_ROUNDS: int = 12
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # Legendary Features
    ENABLE_LEGENDARY_MODE: bool = True
    RICKROLL187_ADMIN_PRIVILEGES: bool = True
    CODE_BRO_HUMOR_LEVEL: str = "MAXIMUM"
    SWISS_PRECISION_LEVEL: str = "LEGENDARY"
    ENABLE_JOKES: bool = True
    JOKES_PER_RESPONSE: int = 1
    
    # Performance Settings
    ENABLE_PERFORMANCE_MONITORING: bool = True
    ENABLE_CACHING: bool = True
    CACHE_TTL_SECONDS: int = 300
    MAX_CACHE_SIZE: int = 1000
    
    # External Services
    REDIS_URL: Optional[str] = None
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    SENTRY_DSN: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 1000
    RATE_LIMIT_PERIOD: int = 3600
    ENABLE_RATE_LIMITING: bool = True
    
    # File Upload Settings
    UPLOAD_DIRECTORY: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".md"]
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/n3extpath.log"
    ENABLE_FILE_LOGGING: bool = True
    
    # Development Settings
    RELOAD: bool = False
    WORKERS: int = 1
    
    # Legendary Timestamps
    LEGENDARY_CREATION_TIME: str = "2025-08-04 15:51:01 UTC"
    RICKROLL187_APPROVAL_TIME: str = "2025-08-04 15:51:01 UTC"
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL is required!")
        return v
    
    @validator("JWT_SECRET_KEY")
    def validate_jwt_secret(cls, v):
        if v == "legendary_secret_key_change_in_production" and os.getenv("ENVIRONMENT") == "production":
            raise ValueError("JWT_SECRET_KEY must be changed in production!")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
        # Legendary configuration jokes
        schema_extra = {
            "example": {
                "APP_NAME": "N3extPath - RICKROLL187's Legendary Platform",
                "LEGENDARY_CREATION_TIME": "2025-08-04 15:51:01 UTC",
                "CODE_BRO_HUMOR_LEVEL": "MAXIMUM",
                "RICKROLL187_ADMIN_PRIVILEGES": True
            }
        }

@lru_cache()
def get_legendary_settings() -> LegendarySettings:
    """
    Get cached legendary settings instance!
    More efficient than Swiss engineering with code bro optimization! 🔧⚡
    """
    return LegendarySettings()

# Global settings instance
settings = get_legendary_settings()

# Legendary settings validation
def validate_legendary_settings() -> dict:
    """
    Validate all legendary settings!
    More thorough than Swiss quality control with code bro standards! ✅🎸
    """
    validation_results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "legendary_status": "RICKROLL187 APPROVED! 🎸"
    }
    
    # Check critical settings
    if settings.JWT_SECRET_KEY == "legendary_secret_key_change_in_production":
        validation_results["warnings"].append("⚠️ JWT_SECRET_KEY should be changed for production!")
    
    if not os.path.exists(os.path.dirname(settings.LOG_FILE)):
        try:
            os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
        except Exception as e:
            validation_results["errors"].append(f"❌ Cannot create log directory: {e}")
    
    if not os.path.exists(settings.UPLOAD_DIRECTORY):
        try:
            os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
        except Exception as e:
            validation_results["errors"].append(f"❌ Cannot create upload directory: {e}")
    
    if validation_results["errors"]:
        validation_results["valid"] = False
        validation_results["legendary_status"] = "NEEDS FIXING! 🔧"
    
    return validation_results

if __name__ == "__main__":
    print("🔧🎸 N3EXTPATH LEGENDARY SETTINGS CONFIGURATION LOADED! 🎸🔧")
    print("🏆 LEGENDARY CONFIGURATION CHAMPION EDITION! 🏆")
    print(f"⏰ Configuration Time: 2025-08-04 15:51:01 UTC")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    
    # Validate settings
    validation = validate_legendary_settings()
    print(f"🔍 Settings Validation: {validation['legendary_status']}")
    
    if validation["warnings"]:
        for warning in validation["warnings"]:
            print(warning)
    
    if validation["errors"]:
        for error in validation["errors"]:
            print(error)
    else:
        print("✅ All legendary settings validated successfully!")
