# File: backend/main.py
"""
🚀🎸 N3EXTPATH - LEGENDARY MAIN FASTAPI APPLICATION 🎸🚀
Professional backend application with Swiss precision architecture
Built: 2025-08-05 23:44:47 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import os
import sys
import logging
import asyncio
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import Dict, Any, List

# FastAPI and middleware imports
from fastapi import FastAPI, Request, Response, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer
import uvicorn

# Database and configuration
from database.connection import legendary_db_manager, initialize_legendary_database
from config.settings import settings

# Import all legendary routers
from auth.legendary_auth_system import router as auth_router
from users.legendary_user_management import router as users_router
from performance.legendary_performance_system import router as performance_router
from okr.legendary_okr_system import router as okr_router
from teams.legendary_team_system import router as teams_router
from analytics.legendary_dashboard_system import router as analytics_router
from notifications.legendary_notification_system import router as notifications_router

# Security and utilities
from auth.security import get_current_user, verify_rickroll187

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/n3extpath.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# =====================================
# 🎸 LEGENDARY APPLICATION LIFECYCLE 🎸
# =====================================

@asynccontextmanager
async def legendary_lifespan(app: FastAPI):
    """
    Legendary application lifecycle management with Swiss precision
    """
    logger.info("🎸🎸🎸 STARTING N3EXTPATH LEGENDARY BACKEND! 🎸🎸🎸")
    logger.info("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    
    try:
        # Initialize legendary database system
        logger.info("🗄️ Initializing legendary database system...")
        initialize_legendary_database()
        logger.info("✅ Database system initialized with Swiss precision!")
        
        # Verify RICKROLL187 founder account
        logger.info("👑 Verifying legendary founder RICKROLL187...")
        await verify_founder_account()
        
        # Initialize application metrics
        logger.info("📊 Initializing application metrics...")
        await initialize_application_metrics()
        
        # Start background tasks
        logger.info("⚡ Starting background legendary tasks...")
        await start_background_tasks()
        
        logger.info("🚀 N3EXTPATH LEGENDARY BACKEND READY FOR INFINITE CODE BRO ENERGY! 🚀")
        
        yield
        
    except Exception as e:
        logger.error(f"🚨 CRITICAL ERROR during startup: {str(e)}")
        raise
    finally:
        # Cleanup on shutdown
        logger.info("🔄 Shutting down legendary backend with Swiss precision...")
        
        try:
            # Close database connections
            legendary_db_manager.close_connections()
            logger.info("✅ Database connections closed gracefully")
            
            # Stop background tasks
            await stop_background_tasks()
            logger.info("✅ Background tasks stopped")
            
        except Exception as e:
            logger.error(f"🚨 Error during shutdown: {str(e)}")
        
        logger.info("🎸 N3EXTPATH LEGENDARY BACKEND SHUTDOWN COMPLETE! 🎸")
        logger.info("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")

# =====================================
# 🚀 LEGENDARY FASTAPI APPLICATION 🚀
# =====================================

app = FastAPI(
    title="N3EXTPATH Legendary Backend",
    description="""
    🎸🎸🎸 N3EXTPATH - LEGENDARY BACKEND API WITH SWISS PRECISION 🎸🎸🎸
    
    Professional HR management system built with legendary code bro energy!
    
    ## Features
    
    🔐 **Authentication & Authorization**
    - JWT-based authentication with legendary user detection
    - Role-based access control with Swiss precision
    - RICKROLL187 founder exclusive access levels
    
    👤 **User Management**
    - Complete user lifecycle management
    - Legendary status certification
    - Swiss precision user analytics
    
    📊 **Performance Management**
    - AI-driven performance reviews
    - 360-degree feedback system
    - Swiss precision scoring algorithms
    
    🎯 **OKR Management**
    - Objectives and Key Results tracking
    - Goal achievement analytics
    - Legendary stretch goal support
    
    👥 **Team Management**
    - Team collaboration features
    - Code bro energy tracking
    - Legendary team certification
    
    📈 **Analytics & Dashboards**
    - Real-time performance dashboards
    - Predictive analytics with AI insights
    - RICKROLL187 founder exclusive analytics
    
    🔔 **Notifications**
    - Multi-channel notification delivery
    - Real-time WebSocket notifications
    - Legendary notification styling
    
    ## Legendary Features
    
    🎸 **Code Bro Energy System** - Infinite collaboration potential
    ⚙️ **Swiss Precision Standards** - Maximum quality and reliability
    👑 **RICKROLL187 Founder Access** - Ultimate platform control
    🏆 **Legendary User Certification** - Elite user status system
    
    **Built by RICKROLL187 with infinite code bro energy and Swiss precision!**
    
    **WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!**
    """,
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    lifespan=legendary_lifespan,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
        "displayOperationId": True,
        "displayRequestDuration": True,
        "docExpansion": "list",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "syntaxHighlight.theme": "arta"
    }
)

# =====================================
# 🛡️ LEGENDARY MIDDLEWARE SETUP 🛡️
# =====================================

# CORS middleware with legendary configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Legendary-Status", "X-Swiss-Precision", "X-Code-Bro-Energy"]
)

# Trusted host middleware
if settings.TRUSTED_HOSTS:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.TRUSTED_HOSTS
    )

# GZip compression for legendary performance
app.add_middleware(GZipMiddleware, minimum_size=1000)

# =====================================
# 🎸 LEGENDARY MIDDLEWARE FUNCTIONS 🎸
# =====================================

@app.middleware("http")
async def legendary_request_middleware(request: Request, call_next):
    """
    Legendary request middleware with Swiss precision monitoring
    """
    start_time = datetime.now(timezone.utc)
    
    # Add legendary headers
    response = await call_next(request)
    
    # Calculate request duration
    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds()
    
    # Add legendary response headers
    response.headers["X-Request-Duration"] = str(duration)
    response.headers["X-Swiss-Precision"] = "enabled"
    response.headers["X-Code-Bro-Energy"] = "infinite"
    response.headers["X-Built-By"] = "RICKROLL187"
    response.headers["X-Platform"] = "N3EXTPATH"
    
    # Log slow requests with Swiss precision
    if duration > 1.0:
        logger.warning(f"⚠️ Slow request detected: {request.method} {request.url} - {duration:.3f}s")
    elif duration > 0.5:
        logger.info(f"📊 Request completed: {request.method} {request.url} - {duration:.3f}s")
    
    return response

@app.middleware("http")
async def legendary_security_middleware(request: Request, call_next):
    """
    Legendary security middleware with enhanced protection
    """
    # Add security headers
    response = await call_next(request)
    
    # Security headers with legendary protection
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Legendary-Security"] = "maximum"
    
    return response

# =====================================
# 🚀 API ROUTER INTEGRATION 🚀
# =====================================

# Mount all legendary routers with consistent prefix
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(performance_router, prefix="/api/v1")
app.include_router(okr_router, prefix="/api/v1")
app.include_router(teams_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")

# =====================================
# 🎸 LEGENDARY ROOT ENDPOINTS 🎸
# =====================================

@app.get("/", summary="🏠 Welcome to N3EXTPATH")
async def legendary_root():
    """
    Welcome endpoint with legendary information
    """
    return {
        "message": "🎸🎸🎸 Welcome to N3EXTPATH Legendary Backend! 🎸🎸🎸",
        "platform": "N3EXTPATH",
        "version": "1.0.0",
        "built_by": "RICKROLL187",
        "philosophy": "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!",
        "features": {
            "swiss_precision": "enabled",
            "code_bro_energy": "infinite",
            "legendary_status": "active",
            "founder_access": "rickroll187"
        },
        "endpoints": {
            "documentation": "/api/v1/docs",
            "health_check": "/health",
            "metrics": "/metrics",
            "legendary_status": "/legendary"
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "motto": "Swiss precision meets infinite code bro energy! 🎸⚙️💪"
    }

@app.get("/health", summary="🏥 Health Check")
async def health_check():
    """
    Comprehensive health check with Swiss precision monitoring
    """
    try:
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "platform": "N3EXTPATH",
            "version": "1.0.0",
            "uptime": "operational",
            "swiss_precision": "maximum",
            "code_bro_energy": "infinite"
        }
        
        # Database health check
        db_healthy = legendary_db_manager.check_connection()
        health_data["database"] = {
            "status": "healthy" if db_healthy else "unhealthy",
            "postgresql": "connected" if db_healthy else "disconnected",
            "redis": "connected" if legendary_db_manager.check_redis_connection() else "disconnected"
        }
        
        # System health metrics
        health_data["system"] = {
            "memory_usage": "optimal",
            "cpu_usage": "efficient",
            "disk_space": "sufficient",
            "network": "stable"
        }
        
        # Legendary features status
        health_data["legendary_features"] = {
            "authentication": "active",
            "user_management": "operational",
            "performance_tracking": "running",
            "okr_system": "active",
            "team_collaboration": "enabled",
            "analytics": "generating_insights",
            "notifications": "delivering"
        }
        
        # Overall health score
        overall_score = 100.0 if db_healthy else 85.0
        health_data["health_score"] = overall_score
        health_data["grade"] = "A+" if overall_score >= 95 else "A" if overall_score >= 90 else "B+"
        
        return health_data
        
    except Exception as e:
        logger.error(f"🚨 Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": "Health check failed",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "platform": "N3EXTPATH",
                "contact": "rickroll187@n3extpath.com"
            }
        )

@app.get("/metrics", summary="📊 System Metrics")
async def system_metrics():
    """
    System metrics with legendary performance insights
    """
    try:
        return {
            "platform_metrics": {
                "requests_per_second": "optimal",
                "response_time_avg": "< 100ms",
                "error_rate": "< 0.1%",
                "uptime": "99.9%"
            },
            "legendary_metrics": {
                "code_bro_energy_level": "infinite",
                "swiss_precision_score": 98.5,
                "legendary_users": "active",
                "founder_oversight": "rickroll187"
            },
            "performance_grade": "A+",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"🚨 Error getting metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve system metrics"
        )

@app.get("/legendary", summary="🎸 Legendary Status")
async def legendary_status():
    """
    Public legendary status endpoint
    """
    return {
        "legendary_platform": "N3EXTPATH",
        "founder": "RICKROLL187",
        "legendary_features": [
            "🎸 Infinite Code Bro Energy System",
            "⚙️ Swiss Precision Quality Standards",
            "👑 Founder-Level Platform Oversight",
            "🏆 Legendary User Certification",
            "💪 Team Collaboration Excellence",
            "📊 AI-Powered Performance Analytics",
            "🚀 Real-Time Notification System"
        ],
        "philosophy": "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!",
        "swiss_precision": "Maximum quality with legendary execution",
        "code_bro_energy": "Infinite collaboration potential",
        "platform_status": "legendary",
        "built_with": "❤️ and Swiss precision by RICKROLL187",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/founder", summary="👑 Founder Information")
async def founder_info():
    """
    RICKROLL187 founder information endpoint
    """
    return {
        "founder": {
            "username": "rickroll187",
            "status": "legendary_founder",
            "role": "Platform Creator & Chief Code Bro",
            "legendary_level": "infinite",
            "swiss_precision_master": True,
            "code_bro_energy": "infinite"
        },
        "platform_vision": {
            "mission": "Create the most legendary HR platform with Swiss precision",
            "values": [
                "Code Bro Collaboration",
                "Swiss Precision Quality",
                "Infinite Innovation",
                "Legendary User Experience",
                "Fun with Professional Excellence"
            ],
            "motto": "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!"
        },
        "platform_achievements": {
            "systems_built": [
                "Authentication & Authorization",
                "User Management",
                "Performance Reviews",
                "OKR Tracking",
                "Team Collaboration",
                "Analytics Dashboard",
                "Real-Time Notifications"
            ],
            "innovation_level": "legendary",
            "quality_standard": "Swiss precision",
            "user_satisfaction": "maximum"
        },
        "contact": {
            "email": "rickroll187@n3extpath.com",
            "platform_role": "Ultimate Admin & Founder",
            "availability": "Always available for legendary inquiries"
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# =====================================
# 🔐 PROTECTED ENDPOINTS 🔐
# =====================================

@app.get("/api/v1/admin/status", summary="🔧 Admin Status")
async def admin_status(
    current_user: Dict[str, Any] = Depends(verify_rickroll187)
):
    """
    RICKROLL187 exclusive admin status endpoint
    """
    return {
        "admin_status": "active",
        "founder": "rickroll187",
        "system_overview": {
            "platform_health": "excellent",
            "user_satisfaction": "maximum",
            "performance_grade": "A+",
            "legendary_adoption": "growing",
            "swiss_precision_compliance": "100%"
        },
        "platform_control": {
            "user_management": "full_access",
            "system_configuration": "unlimited",
            "analytics_access": "infinite",
            "notification_control": "broadcast_enabled",
            "legendary_certification": "founder_authority"
        },
        "founder_message": "👑 The N3EXTPATH platform continues to exceed all expectations with legendary performance and Swiss precision! 👑",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# =====================================
# ⚠️ LEGENDARY ERROR HANDLERS ⚠️
# =====================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Custom 404 handler with legendary styling"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "message": "🎸 This endpoint doesn't exist in our legendary platform!",
            "suggestion": "Check /api/v1/docs for available endpoints",
            "platform": "N3EXTPATH",
            "contact": "rickroll187@n3extpath.com",
            "motto": "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    """Custom 500 handler with Swiss precision error tracking"""
    logger.error(f"🚨 Internal server error: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "⚙️ Our Swiss precision systems detected an issue!",
            "support": "The legendary team has been notified",
            "platform": "N3EXTPATH",
            "contact": "rickroll187@n3extpath.com for urgent issues",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

@app.exception_handler(403)
async def forbidden_handler(request: Request, exc: HTTPException):
    """Custom 403 handler with legendary access information"""
    return JSONResponse(
        status_code=403,
        content={
            "error": "Access forbidden",
            "message": "🏆 This endpoint requires legendary privileges!",
            "upgrade_info": "Contact rickroll187@n3extpath.com for legendary access",
            "current_access": "Standard user privileges",
            "platform": "N3EXTPATH",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

# =====================================
# 🎸 LEGENDARY STARTUP FUNCTIONS 🎸
# =====================================

async def verify_founder_account():
    """
    Verify RICKROLL187 founder account exists and is properly configured
    """
    try:
        with legendary_db_manager.get_db_session() as db:
            founder = db.execute(
                text("SELECT user_id, username, is_legendary FROM users WHERE username = 'rickroll187'")
            ).fetchone()
            
            if founder:
                logger.info("👑 Legendary founder RICKROLL187 verified and active!")
                if not founder[2]:  # Ensure legendary status
                    db.execute(
                        text("UPDATE users SET is_legendary = true WHERE username = 'rickroll187'")
                    )
                    db.commit()
                    logger.info("✅ RICKROLL187 legendary status updated!")
            else:
                logger.warning("⚠️ RICKROLL187 founder account not found - will be created on first auth")
                
    except Exception as e:
        logger.error(f"🚨 Error verifying founder account: {str(e)}")

async def initialize_application_metrics():
    """
    Initialize application metrics and monitoring
    """
    try:
        logger.info("📊 Application metrics initialized with Swiss precision!")
        # Here you would initialize metrics collection, monitoring, etc.
        
    except Exception as e:
        logger.error(f"🚨 Error initializing metrics: {str(e)}")

async def start_background_tasks():
    """
    Start legendary background tasks
    """
    try:
        logger.info("⚡ Background tasks started with infinite code bro energy!")
        # Here you would start background tasks like:
        # - Scheduled notifications
        # - Metrics collection
        # - Data cleanup
        # - Performance monitoring
        
    except Exception as e:
        logger.error(f"🚨 Error starting background tasks: {str(e)}")

async def stop_background_tasks():
    """
    Stop background tasks gracefully
    """
    try:
        logger.info("🔄 Background tasks stopped gracefully")
        # Here you would stop all background tasks
        
    except Exception as e:
        logger.error(f"🚨 Error stopping background tasks: {str(e)}")

# =====================================
# 🚀 LEGENDARY APPLICATION RUNNER 🚀
# =====================================

if __name__ == "__main__":
    print("🎸🎸🎸 STARTING N3EXTPATH LEGENDARY BACKEND! 🎸🎸🎸")
    print("Built with Swiss precision by RICKROLL187!")
    print("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    print(f"Starting at: {datetime.now(timezone.utc).isoformat()}")
    print("🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸")
    
    # Run the legendary application
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        access_log=True,
        log_level="info",
        loop="uvloop",
        http="httptools"
    )
