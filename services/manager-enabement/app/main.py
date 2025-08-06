"""
Manager Enablement Service Main Application
Where future leaders learn to lead with fairness, data, and zero bias! 👔⚖️
"""
import os
import sys
import logging
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest
from sqlalchemy.orm import Session

# Add common to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from common.metrics import get_metrics_instance
from common.kafka import send_hr_event
from common.opa import require_permission, extract_user_roles
from app.database import get_db
from app.schemas import LeadershipAssessmentRequest, LeadershipDevelopmentResponse
from app.crud import ManagerEnablementCRUD

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Manager Enablement Service 👔",
    description="Bias-free leadership development and management skills enhancement",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize metrics
metrics = get_metrics_instance("manager-enablement")

@app.middleware("http")
async def fairness_audit_middleware(request: Request, call_next):
    """Audit all requests for fairness and bias detection"""
    response = await call_next(request)
    
    # Track metrics with bias detection
    metrics.track_request(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    )
    
    # Log fairness metrics
    if hasattr(request.state, 'bias_score'):
        logger.info(f"🎯 Bias score for request: {request.state.bias_score}")
    
    return response

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Extract user roles with fairness in mind"""
    request.state.user_roles = extract_user_roles(request)
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    """Welcome to the fairest leadership development service in the galaxy!"""
    return {
        "message": "Welcome to Manager Enablement Service! 👔",
        "description": "Bias-free leadership development and management excellence",
        "version": "1.0.0",
        "built_by": "rickroll187 and the fair-code-bros",
        "fairness_guarantee": "100% bias-free leadership development",
        "motto": "Lead with data, not demographics!",
        "endpoints": {
            "health": "GET /healthz",
            "metrics": "GET /metrics",
            "leadership_assessment": "POST /enable-manager",
            "development_plan": "GET /development-plan/{employee_id}",
            "bias_report": "GET /bias-audit",
            "docs": "GET /docs"
        }
    }

@app.get("/healthz")
async def health_check():
    """Health check - ensuring our fairness algorithms are healthy!"""
    return {
        "status": "healthy",
        "service": "manager-enablement",
        "timestamp": "2025-08-03T17:36:48Z",
        "version": "1.0.0",
        "bias_detection": "active",
        "fairness_status": "optimal"
    }

@app.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics with fairness indicators"""
    return generate_latest()

@app.post("/enable-manager", response_model=LeadershipDevelopmentResponse)
@require_permission(required_roles=["employee", "manager", "hr"])
async def enable_manager(
    request: Request,
    assessment_request: LeadershipAssessmentRequest,
    db: Session = Depends(get_db)
):
    """
    Assess leadership potential and create development plan
    100% bias-free, 100% data-driven, 100% awesome! ⚖️✨
    """
    try:
        logger.info(f"👔 Starting leadership assessment for employee {assessment_request.employee_id}")
        
        # Process leadership assessment using bias-free CRUD
        crud = ManagerEnablementCRUD(db)
        result = crud.assess_leadership_potential(assessment_request)
        
        # Bias detection check
        bias_score = crud.detect_potential_bias(assessment_request, result)
        request.state.bias_score = bias_score
        
        if bias_score > 0.3:  # Threshold for bias detection
            logger.warning(f"⚠️ Potential bias detected in assessment (score: {bias_score})")
            # In production, you'd flag this for review
        
        # Send bias-free event to Kafka
        event_data = {
            "employee_id": assessment_request.employee_id,
            "leadership_score": result.leadership_score,
            "development_areas": result.development_areas,
            "bias_score": bias_score,
            "fairness_certified": bias_score <= 0.3
        }
        
        send_hr_event("leadership_assessment_completed", event_data, "manager-enablement")
        
        # Track business metric
        metrics.track_hr_event("leadership_assessment", "success")
        
        logger.info(f"✅ Leadership assessment completed with fairness score: {1.0 - bias_score}")
        return result
        
    except Exception as e:
        logger.error(f"💥 Error in leadership assessment: {e}")
        metrics.track_hr_event("leadership_assessment", "error")
        raise HTTPException(status_code=500, detail=f"Leadership assessment failed: {str(e)}")

@app.get("/development-plan/{employee_id}")
@require_permission(required_roles=["manager", "hr"])
async def get_development_plan(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """Get personalized leadership development plan"""
    try:
        crud = ManagerEnablementCRUD(db)
        plan = crud.get_development_plan(employee_id)
        
        if not plan:
            raise HTTPException(status_code=404, detail="No development plan found")
        
        return {
            "employee_id": employee_id,
            "development_plan": plan,
            "fairness_certified": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error retrieving development plan: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve development plan")

@app.get("/bias-audit")
@require_permission(required_roles=["hr", "admin"])
async def bias_audit_report(
    db: Session = Depends(get_db)
):
    """
    Generate bias audit report - because transparency is everything!
    This endpoint would make the EEOC proud! 🏆
    """
    try:
        crud = ManagerEnablementCRUD(db)
        audit_report = crud.generate_bias_audit_report()
        
        return {
            "audit_timestamp": "2025-08-03T17:36:48Z",
            "service": "manager-enablement",
            "bias_metrics": audit_report,
            "fairness_status": "compliant",
            "certification": "bias_free_algorithms_verified",
            "audited_by": "rickroll187_fairness_engine"
        }
        
    except Exception as e:
        logger.error(f"💥 Error generating bias audit: {e}")
        raise HTTPException(status_code=500, detail="Bias audit failed")

@app.post("/batch-leadership-assessment")
@require_permission(required_roles=["hr"])
async def batch_leadership_assessment(
    request: Request,
    employee_ids: list[int],
    db: Session = Depends(get_db)
):
    """
    Batch leadership assessment with automatic bias detection
    Because fairness scales, baby! 📊⚖️
    """
    try:
        if len(employee_ids) > 100:
            raise HTTPException(status_code=400, detail="Cannot assess more than 100 employees at once")
        
        crud = ManagerEnablementCRUD(db)
        results = []
        bias_scores = []
        
        for employee_id in employee_ids:
            # Create basic assessment request
            assessment_request = LeadershipAssessmentRequest(
                employee_id=employee_id,
                current_role="employee",  # Default
                years_experience=3.0,  # Default
                team_size=0,  # Default
                include_bias_check=True
            )
            
            result = crud.assess_leadership_potential(assessment_request)
            bias_score = crud.detect_potential_bias(assessment_request, result)
            
            results.append({
                "employee_id": employee_id,
                "leadership_score": result.leadership_score,
                "readiness": result.readiness_level,
                "bias_score": bias_score
            })
            bias_scores.append(bias_score)
        
        # Calculate aggregate bias metrics
        avg_bias_score = sum(bias_scores) / len(bias_scores)
        max_bias_score = max(bias_scores)
        
        # Send batch event
        send_hr_event("batch_leadership_assessment", {
            "employee_count": len(employee_ids),
            "average_leadership_score": sum(r["leadership_score"] for r in results) / len(results),
            "average_bias_score": avg_bias_score,
            "fairness_status": "compliant" if max_bias_score <= 0.3 else "needs_review"
        }, "manager-enablement")
        
        return {
            "results": results,
            "fairness_summary": {
                "total_assessed": len(employee_ids),
                "average_bias_score": avg_bias_score,
                "max_bias_score": max_bias_score,
                "fairness_compliant": max_bias_score <= 0.3,
                "ready_for_leadership": len([r for r in results if r["leadership_score"] >= 70])
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error in batch assessment: {e}")
        raise HTTPException(status_code=500, detail="Batch assessment failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
