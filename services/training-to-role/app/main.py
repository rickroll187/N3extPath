"""
Training-to-Role Service Main Application
The skill gap analyzer that HR departments dream about!
"""
import os
import sys
import logging
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from sqlalchemy.orm import Session

# Add common to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from common.metrics import get_metrics_instance, metrics_middleware
from common.kafka import send_hr_event
from common.opa import require_permission, extract_user_roles
from app.database import get_db
from app.schemas import SkillMatchRequest, SkillMatchResponse
from app.crud import SkillMatchCRUD

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Training-to-Role Service 🎯",
    description="Intelligent skill matching and training recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize metrics
metrics = get_metrics_instance("training-to-role")

@app.middleware("http")
async def custom_metrics_middleware(request: Request, call_next):
    """Custom metrics middleware"""
    response = await call_next(request)
    
    # Track metrics
    metrics.track_request(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    )
    
    return response

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Extract user roles for authorization"""
    request.state.user_roles = extract_user_roles(request)
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    """Welcome endpoint - because first impressions matter!"""
    return {
        "message": "Welcome to Training-to-Role Service! 🎯",
        "description": "Intelligent skill matching and career development",
        "version": "1.0.0",
        "built_by": "rickroll187",
        "endpoints": {
            "health": "GET /healthz",
            "metrics": "GET /metrics",
            "skill_match": "POST /skill-match",
            "docs": "GET /docs"
        }
    }

@app.get("/healthz")
async def health_check():
    """Health check endpoint - keeping the service healthy!"""
    return {
        "status": "healthy",
        "service": "training-to-role",
        "timestamp": "2025-08-03T14:48:32Z",
        "version": "1.0.0"
    }

@app.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics endpoint"""
    return generate_latest()

@app.post("/skill-match", response_model=SkillMatchResponse)
@require_permission(required_roles=["employee", "manager", "hr"])
async def skill_match(
    request: Request,
    skill_request: SkillMatchRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze skill gaps and recommend training paths
    The magic happens here, bro! ✨
    """
    try:
        logger.info(f"🎯 Processing skill match for employee {skill_request.employee_id}")
        
        # Process skill matching using CRUD
        crud = SkillMatchCRUD(db)
        result = crud.analyze_skills(skill_request)
        
        # Send event to Kafka
        event_data = {
            "employee_id": skill_request.employee_id,
            "current_skills": skill_request.current_skills,
            "target_role": skill_request.target_role,
            "skill_gaps": result.skill_gaps,
            "match_score": result.match_score
        }
        
        send_hr_event("skill_analysis_completed", event_data, "training-to-role")
        
        # Track business metric
        metrics.track_hr_event("skill_match", "success")
        
        logger.info(f"✅ Skill match completed for employee {skill_request.employee_id}")
        return result
        
    except Exception as e:
        logger.error(f"💥 Error processing skill match: {e}")
        metrics.track_hr_event("skill_match", "error")
        raise HTTPException(status_code=500, detail=f"Skill matching failed: {str(e)}")

@app.get("/skill-match/{employee_id}")
@require_permission(required_roles=["manager", "hr"])
async def get_skill_analysis(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """Get existing skill analysis for an employee"""
    try:
        crud = SkillMatchCRUD(db)
        analyses = crud.get_employee_analyses(employee_id)
        
        if not analyses:
            raise HTTPException(status_code=404, detail="No skill analyses found")
        
        return {"employee_id": employee_id, "analyses": analyses}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error retrieving skill analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve skill analysis")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
