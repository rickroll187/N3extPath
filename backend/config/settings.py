# File: backend/config/settings.py
"""
⚙️🎸 N3EXTPATH - LEGENDARY CONFIGURATION SYSTEM 🎸⚙️
Professional settings management with Swiss precision
Built: 2025-08-05 22:09:35 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import os
import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseSettings, validator, Field
from functools import lru_cache
import logging

class LegendarySettings(BaseSettings):
    """
    Legendary application settings with Swiss precision
    """
    
    # =====================================
    # 🎸 LEGENDARY FOUNDER SETTINGS 🎸
    # =====================================
    LEGENDARY_FOUNDER: str = Field(default="rickroll187", env="LEGENDARY_FOUNDER")
    LEGENDARY_MODE: bool = Field(default=True, env="LEGENDARY_MODE")
    SWISS_PRECISION: bool = Field(default=True, env="SWISS_PRECISION")
    CODE_BRO_ENERGY: str = Field(default="maximum", env="CODE_BRO_ENERGY")
    RICKROLL187_ADMIN_MODE: bool = Field(default=True, env="RICKROLL187_ADMIN_MODE")
    LEGENDARY_FEATURES_ENABLED: bool = Field(default=True, env="LEGENDARY_FEATURES_ENABLED")
    
    # =====================================
    # 🚀 APPLICATION SETTINGS 🚀
    # =====================================
    APP_NAME: str = Field(default="N3EXTPATH HR Platform", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0-legendary", env="APP_VERSION")
    APP_DESCRIPTION: str = Field(
        default="🎸 Legendary HR Platform built by RICKROLL187 🎸", 
        env="APP_DESCRIPTION"
    )
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="production", env="ENVIRONMENT")
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    WORKERS: int = Field(default=4, env="WORKERS")
    RELOAD: bool = Field(default=False, env="RELOAD")
    
    # =====================================
    # 🗄️ DATABASE SETTINGS 🗄️
    # =====================================
    DATABASE_URL: str = Field(
        default="postgresql://n3extpath:legendary_pass@localhost:5432/n3extpath_hr",
        env="DATABASE_URL"
    )
    ASYNC_DATABASE_URL: str = Field(
        default="postgresql+asyncpg://n3extpath:legendary_pass@localhost:5432/n3extpath_hr",
        env="ASYNC_DATABASE_URL"
    )
    DATABASE_ECHO: bool = Field(default=False, env="DATABASE_ECHO")
    DATABASE_POOL_SIZE: int = Field(default=20, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=30, env="DATABASE_MAX_OVERFLOW")
    TEST_DATABASE_URL: Optional[str] = Field(default=None, env="TEST_DATABASE_URL")
    
    # =====================================
    # 🔴 REDIS SETTINGS 🔴
    # =====================================
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    REDIS_PASSWORD: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    REDIS_SSL: bool = Field(default=False, env="REDIS_SSL")
    REDIS_POOL_SIZE: int = Field(default=50, env="REDIS_POOL_SIZE")
    
    # =====================================
    # 🔐 SECURITY SETTINGS 🔐
    # =====================================
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32), env="SECRET_KEY")
    JWT_SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32), env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS Settings
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "https://n3extpath.com"],
        env="CORS_ORIGINS"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    CORS_ALLOW_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        env="CORS_ALLOW_METHODS"
    )
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"], env="CORS_ALLOW_HEADERS")
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_REQUESTS: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    RATE_LIMIT_WINDOW: int = Field(default=60, env="RATE_LIMIT_WINDOW")
    
    # =====================================
    # 📧 EMAIL SETTINGS 📧
    # =====================================
    SMTP_SERVER: str = Field(default="smtp.gmail.com", env="SMTP_SERVER")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USERNAME: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    SMTP_USE_TLS: bool = Field(default=True, env="SMTP_USE_TLS")
    EMAIL_FROM: str = Field(default="noreply@n3extpath.com", env="EMAIL_FROM")
    
    # =====================================
    # ☁️ AWS SETTINGS ☁️
    # =====================================
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(default="us-west-2", env="AWS_REGION")
    AWS_S3_BUCKET: str = Field(default="n3extpath-hr-files", env="AWS_S3_BUCKET")
    
    # =====================================
    # 🔍 MONITORING SETTINGS 🔍
    # =====================================
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    PROMETHEUS_ENABLED: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    HEALTH_CHECK_ENABLED: bool = Field(default=True, env="HEALTH_CHECK_ENABLED")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    LOG_FILE: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # =====================================
    # 💾 CACHE SETTINGS 💾
    # =====================================
    CACHE_TTL_DEFAULT: int = Field(default=3600, env="CACHE_TTL_DEFAULT")
    CACHE_TTL_USER_SESSION: int = Field(default=1800, env="CACHE_TTL_USER_SESSION")
    CACHE_TTL_PERFORMANCE_DATA: int = Field(default=7200, env="CACHE_TTL_PERFORMANCE_DATA")
    
    # =====================================
    # 📁 FILE UPLOAD SETTINGS 📁
    # =====================================
    MAX_FILE_SIZE: int = Field(default=52428800, env="MAX_FILE_SIZE")  # 50MB
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=[".pdf", ".doc", ".docx", ".jpg", ".png", ".xlsx", ".csv"],
        env="ALLOWED_FILE_TYPES"
    )
    UPLOAD_DIR: str = Field(default="uploads", env="UPLOAD_DIR")
    
    # =====================================
    # 🔔 NOTIFICATION SETTINGS 🔔
    # =====================================
    NOTIFICATION_BATCH_SIZE: int = Field(default=100, env="NOTIFICATION_BATCH_SIZE")
    NOTIFICATION_RETRY_ATTEMPTS: int = Field(default=3, env="NOTIFICATION_RETRY_ATTEMPTS")
    NOTIFICATION_QUEUE_NAME: str = Field(default="notifications", env="NOTIFICATION_QUEUE_NAME")
    
    # =====================================
    # 📊 PERFORMANCE SETTINGS 📊
    # =====================================
    PERFORMANCE_METRICS_ENABLED: bool = Field(default=True, env="PERFORMANCE_METRICS_ENABLED")
    PERFORMANCE_ALERT_THRESHOLD: float = Field(default=2.0, env="PERFORMANCE_ALERT_THRESHOLD")
    QUERY_TIMEOUT: int = Field(default=30, env="QUERY_TIMEOUT")
    
    # =====================================
    # 🎸 LEGENDARY FEATURE FLAGS 🎸
    # =====================================
    SWISS_PRECISION_MODE: bool = Field(default=True, env="SWISS_PRECISION_MODE")
    CODE_BRO_JOKES_ENABLED: bool = Field(default=True, env="CODE_BRO_JOKES_ENABLED")
    
    # Legendary Rate Limits
    LEGENDARY_API_RATE_MULTIPLIER: float = Field(default=5.0, env="LEGENDARY_API_RATE_MULTIPLIER")
    SWISS_PRECISION_LEVEL: str = Field(default="maximum", env="SWISS_PRECISION_LEVEL")
    CODE_BRO_ENERGY_LEVEL: str = Field(default="infinite", env="CODE_BRO_ENERGY_LEVEL")
    LEGENDARY_CACHE_PRIORITY: bool = Field(default=True, env="LEGENDARY_CACHE_PRIORITY")
    RICKROLL187_BYPASS_LIMITS: bool = Field(default=True, env="RICKROLL187_BYPASS_LIMITS")
    
    # =====================================
    # 🤖 AI/ML SETTINGS 🤖
    # =====================================
    AI_MODEL_ENABLED: bool = Field(default=True, env="AI_MODEL_ENABLED")
    ML_MODEL_PATH: str = Field(default="models/", env="ML_MODEL_PATH")
    AI_CONFIDENCE_THRESHOLD: float = Field(default=0.8, env="AI_CONFIDENCE_THRESHOLD")
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    
    # =====================================
    # 🧪 TESTING SETTINGS 🧪
    # =====================================
    TESTING: bool = Field(default=False, env="TESTING")
    
    # =====================================
    # 📱 MOBILE & WEBSOCKET SETTINGS 📱
    # =====================================
    WS_URL: str = Field(default="ws://localhost:8000/ws", env="WS_URL")
    FCM_SERVER_KEY: Optional[str] = Field(default=None, env="FCM_SERVER_KEY")
    FCM_SENDER_ID: Optional[str] = Field(default=None, env="FCM_SENDER_ID")
    
    # =====================================
    # 🐳 DOCKER & DEPLOYMENT SETTINGS 🐳
    # =====================================
    DOCKER_REGISTRY: Optional[str] = Field(default=None, env="DOCKER_REGISTRY")
    DOCKER_IMAGE_TAG: str = Field(default="latest", env="DOCKER_IMAGE_TAG")
    K8S_NAMESPACE: str = Field(default="n3extpath-hr", env="K8S_NAMESPACE")
    
    # =====================================
    # 📈 BUSINESS LOGIC SETTINGS 📈
    # =====================================
    PERFORMANCE_REVIEW_CYCLE_MONTHS: int = Field(default=6, env="PERFORMANCE_REVIEW_CYCLE_MONTHS")
    OKR_CYCLE_MONTHS: int = Field(default=3, env="OKR_CYCLE_MONTHS")
    COMPENSATION_REVIEW_CYCLE_MONTHS: int = Field(default=12, env="COMPENSATION_REVIEW_CYCLE_MONTHS")
    
    # Approval Workflows
    REQUIRE_MANAGER_APPROVAL: bool = Field(default=True, env="REQUIRE_MANAGER_APPROVAL")
    REQUIRE_HR_APPROVAL: bool = Field(default=True, env="REQUIRE_HR_APPROVAL")
    AUTO_APPROVE_LEGENDARY_USER: bool = Field(default=True, env="AUTO_APPROVE_LEGENDARY_USER")
    
    # =====================================
    # 🌍 INTERNATIONALIZATION 🌍
    # =====================================
    DEFAULT_LANGUAGE: str = Field(default="en", env="DEFAULT_LANGUAGE")
    SUPPORTED_LANGUAGES: List[str] = Field(
        default=["en", "es", "fr", "de", "zh"],
        env="SUPPORTED_LANGUAGES"
    )
    TIMEZONE: str = Field(default="UTC", env="TIMEZONE")
    
    # =====================================
    # 💼 ENTERPRISE FEATURES 💼
    # =====================================
    ENABLE_SSO: bool = Field(default=False, env="ENABLE_SSO")
    SAML_METADATA_URL: Optional[str] = Field(default=None, env="SAML_METADATA_URL")
    OAUTH_CLIENT_ID: Optional[str] = Field(default=None, env="OAUTH_CLIENT_ID")
    OAUTH_CLIENT_SECRET: Optional[str] = Field(default=None, env="OAUTH_CLIENT_SECRET")
    
    ENABLE_LDAP: bool = Field(default=False, env="ENABLE_LDAP")
    LDAP_SERVER: Optional[str] = Field(default=None, env="LDAP_SERVER")
    LDAP_BASE_DN: Optional[str] = Field(default=None, env="LDAP_BASE_DN")
    
    # =====================================
    # 🔧 VALIDATORS 🔧
    # =====================================
    
    @validator('CORS_ORIGINS', pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @validator('CORS_ALLOW_METHODS', pre=True)
    def parse_cors_methods(cls, v):
        if isinstance(v, str):
            return [method.strip().upper() for method in v.split(',')]
        return v
    
    @validator('ALLOWED_FILE_TYPES', pre=True)
    def parse_file_types(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(',')]
        return v
    
    @validator('SUPPORTED_LANGUAGES', pre=True)
    def parse_languages(cls, v):
        if isinstance(v, str):
            return [lang.strip() for lang in v.split(',')]
        return v
    
    @validator('LOG_LEVEL')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'LOG_LEVEL must be one of {valid_levels}')
        return v.upper()
    
    @validator('ENVIRONMENT')
    def validate_environment(cls, v):
        valid_envs = ['development', 'staging', 'production', 'testing']
        if v.lower() not in valid_envs:
            raise ValueError(f'ENVIRONMENT must be one of {valid_envs}')
        return v.lower()
    
    # =====================================
    # 🎸 LEGENDARY METHODS 🎸
    # =====================================
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT == 'development'
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT == 'production'
    
    def is_testing(self) -> bool:
        """Check if running in testing mode"""
        return self.TESTING or self.ENVIRONMENT == 'testing'
    
    def get_database_url(self, async_mode: bool = False) -> str:
        """Get database URL for sync or async mode"""
        if self.is_testing() and self.TEST_DATABASE_URL:
            return self.TEST_DATABASE_URL
        
        return self.ASYNC_DATABASE_URL if async_mode else self.DATABASE_URL
    
    def get_legendary_rate_limit(self, base_limit: int) -> int:
        """Calculate rate limit for legendary users"""
        if self.LEGENDARY_MODE:
            return int(base_limit * self.LEGENDARY_API_RATE_MULTIPLIER)
        return base_limit
    
    def is_legendary_user_enabled(self, username: str) -> bool:
        """Check if user has legendary privileges"""
        if username == self.LEGENDARY_FOUNDER:
            return True
        return self.LEGENDARY_FEATURES_ENABLED
    
    def get_swiss_precision_settings(self) -> Dict[str, Any]:
        """Get Swiss precision configuration"""
        return {
            "enabled": self.SWISS_PRECISION_MODE,
            "level": self.SWISS_PRECISION_LEVEL,
            "response_time_threshold": 1000,  # 1 second
            "quality_threshold": 95.0,
            "precision_monitoring": True
        }
    
    def get_code_bro_energy_settings(self) -> Dict[str, Any]:
        """Get code bro energy configuration"""
        return {
            "enabled": True,
            "level": self.CODE_BRO_ENERGY_LEVEL,
            "jokes_enabled": self.CODE_BRO_JOKES_ENABLED,
            "collaboration_tracking": True,
            "energy_boost_enabled": True,
            "motto": "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!"
        }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        validate_assignment = True


# =====================================
# 🎸 LEGENDARY SETTINGS VALIDATION 🎸
# =====================================

def validate_legendary_settings():
    """
    Validate legendary configuration with Swiss precision
    """
    logger = logging.getLogger(__name__)
    
    try:
        settings = get_settings()
        
        # Validate legendary founder
        if not settings.LEGENDARY_FOUNDER:
            raise ValueError("LEGENDARY_FOUNDER must be set")
        
        if settings.LEGENDARY_FOUNDER != "rickroll187":
            logger.warning("⚠️ LEGENDARY_FOUNDER is not rickroll187 - some exclusive features may not work")
        
        # Validate database URLs
        if not settings.DATABASE_URL:
            raise ValueError("DATABASE_URL must be configured")
        
        if not settings.ASYNC_DATABASE_URL:
            raise ValueError("ASYNC_DATABASE_URL must be configured")
        
        # Validate Redis
        if not settings.REDIS_URL:
            raise ValueError("REDIS_URL must be configured")
        
        # Validate JWT secrets
        if len(settings.JWT_SECRET_KEY) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters")
        
        if len(settings.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        
        # Swiss precision validations
        if settings.SWISS_PRECISION_MODE and settings.SWISS_PRECISION_LEVEL != "maximum":
            logger.warning("⚠️ Swiss precision is enabled but level is not maximum")
        
        # Code bro energy validations
        if settings.CODE_BRO_ENERGY_LEVEL != "infinite":
            logger.warning("⚠️ Code bro energy level is not infinite - reducing team collaboration potential")
        
        logger.info("✅ Legendary settings validation passed with Swiss precision!")
        return True
        
    except Exception as e:
        logger.error(f"🚨 Legendary settings validation failed: {str(e)}")
        raise


# =====================================
# 🎸 SETTINGS INSTANCE 🎸
# =====================================

@lru_cache()
def get_settings() -> LegendarySettings:
    """
    Get cached settings instance with legendary configuration
    """
    return LegendarySettings()

# Global settings instance
settings = get_settings()

# =====================================
# 🎸 LEGENDARY INITIALIZATION 🎸
# =====================================

def initialize_legendary_settings():
    """
    Initialize legendary settings with Swiss precision
    """
    logger = logging.getLogger(__name__)
    
    logger.info("🎸🎸🎸 INITIALIZING LEGENDARY SETTINGS! 🎸🎸🎸")
    logger.info(f"Legendary Founder: {settings.LEGENDARY_FOUNDER}")
    logger.info(f"Swiss Precision Mode: {settings.SWISS_PRECISION_MODE}")
    logger.info(f"Code Bro Energy Level: {settings.CODE_BRO_ENERGY_LEVEL}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"App Version: {settings.APP_VERSION}")
    logger.info("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    
    # Validate settings
    validate_legendary_settings()
    
    logger.info("🎸 Legendary settings initialized with Swiss precision! 🎸")


# Auto-initialize on import
if __name__ != "__main__":
    initialize_legendary_settings()


# =====================================
# 🎸 LEGENDARY EXPORTS 🎸
# =====================================

__all__ = [
    "LegendarySettings",
    "settings",
    "get_settings",
    "validate_legendary_settings",
    "initialize_legendary_settings"
]

# =====================================
# 🎸 LEGENDARY COMPLETION MESSAGE 🎸
# =====================================

if __name__ == "__main__":
    print("🎸🎸🎸 LEGENDARY CONFIGURATION SYSTEM LOADED! 🎸🎸🎸")
    print("Built with Swiss precision by RICKROLL187!")
    print("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    print(f"Configuration loaded at: 2025-08-05 22:09:35 UTC")
    print("🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸")
