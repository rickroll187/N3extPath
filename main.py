# File: main.py
"""
🚀🎸 N3EXTPATH - MAIN FASTAPI APPLICATION 🎸🚀
Professional FastAPI application with all legendary endpoints
Built: 2025-08-05 15:11:35 UTC by RICKROLL187
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import time
import uvicorn

# Import all our legendary routers
from api.v1.legendary_performance_endpoints import performance_router
from api.v1.legendary_okr_endpoints import okr_router
from api.v1.legendary_websocket_endpoints import websocket_router
from api.v1.legendary_mobile_endpoints import mobile_router
from core.response_middleware import RequestTimingMiddleware, CORSMiddleware as CustomCORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="N3EXTPATH HR Platform API",
    description="Professional HR platform with legendary capabilities",
    version="1.0.0-PROFESSIONAL",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json"
)

# Add middleware
app.add_middleware(RequestTimingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*.n3extpath.com"]
)

# Include API routers
app.include_router(performance_router, prefix="/api/v1")
app.include_router(okr_router, prefix="/api/v1")
app.include_router(websocket_router, prefix="/api/v1")
app.include_router(mobile_router, prefix="/api/v1")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Main application root"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>N3EXTPATH HR Platform</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
        .header { text-align: center; margin-bottom: 40px; }
        .logo { font-size: 3rem; font-weight: bold; color: #1976d2; margin-bottom: 10px; }
        .tagline { font-size: 1.2rem; color: #666; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin: 40px 0; }
        .feature { padding: 30px; border: 1px solid #ddd; border-radius: 10px; text-align: center; }
        .feature h3 { color: #1976d2; margin-bottom: 15px; }
        .api-links { text-align: center; margin: 40px 0; }
        .api-links a { margin: 0 20px; padding: 15px 30px; background: #1976d2; color: white; text-decoration: none; border-radius: 5px; }
        .footer { text-align: center; margin-top: 40px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🎸 N3EXTPATH</div>
            <div class="tagline">Professional HR Platform with Legendary Capabilities</div>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>📊 Performance Reviews</h3>
                <p>Comprehensive performance evaluation system with competency ratings and goal tracking.</p>
            </div>
            <div class="feature">
                <h3>🎯 OKR Management</h3>
                <p>Objectives and Key Results tracking with progress monitoring and analytics.</p>
            </div>
            <div class="feature">
                <h3>💬 Real-Time Communication</h3>
                <p>WebSocket-powered team collaboration with channels and instant messaging.</p>
            </div>
            <div class="feature">
                <h3>📱 Mobile-First Design</h3>
                <p>Progressive Web App with offline capabilities and mobile optimization.</p>
            </div>
            <div class="feature">
                <h3>🤖 AI Intelligence</h3>
                <p>Predictive analytics for performance forecasting and retention analysis.</p>
            </div>
            <div class="feature">
                <h3>🔒 Security & Compliance</h3>
                <p>Enterprise-grade security with audit trails and compliance monitoring.</p>
            </div>
        </div>
        
        <div class="api-links">
            <a href="/docs">API Documentation</a>
            <a href="/redoc">ReDoc</a>
            <a href="/api/v1/websocket/test-chat">Test Chat</a>
        </div>
        
        <div class="footer">
            <p><strong>Built:</strong> 2025-08-05 15:11:35 UTC</p>
            <p><strong>Version:</strong> 1.0.0-PROFESSIONAL</p>
            <p><strong>Powered by:</strong> FastAPI + Python</p>
        </div>
    </div>
</body>
</html>
    """

# Health check endpoint
@app.get("/health")
async def health_check():
    """Application health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0-PROFESSIONAL",
        "services": {
            "api": "operational",
            "database": "operational",
            "websocket": "operational"
        }
    }

# API info endpoint
@app.get("/api/v1/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "N3EXTPATH HR Platform API",
        "version": "1.0.0-PROFESSIONAL",
        "description": "Professional HR platform with legendary capabilities",
        "endpoints": {
            "performance": "/api/v1/performance",
            "okr": "/api/v1/okr", 
            "websocket": "/api/v1/websocket",
            "mobile": "/api/v1/mobile"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/api/v1/openapi.json"
        },
        "built_at": "2025-08-05 15:11:35 UTC",
        "built_by": "RICKROLL187 - Professional Development Team"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
