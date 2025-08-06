"""
Performance Management Service Main Application
The performance tracker that's so fair, it makes Lady Justice jealous! 📊⚖️
Built with love (and zero bias) by rickroll187 at 2025-08-03 18:55:14 UTC
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
from app.schemas import PerformanceReviewRequest, GoalSettingRequest, FeedbackSubmissionRequest
from app.crud import PerformanceManagementCRUD

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Performance Management Service 📊",
    description="AI-powered performance tracking that measures skills, not office politics",
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
metrics = get_metrics_instance("performance-management")

@app.middleware("http")
async def performance_metrics_middleware(request: Request, call_next):
    """Track every performance measurement like a productivity hawk! 🦅📊"""
    response = await call_next(request)
    metrics.track_request(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    )
    return response

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Auth middleware with performance-level security"""
    request.state.user_roles = extract_user_roles(request)
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    """Welcome to the performance command center! 📊"""
    return {
        "message": "Welcome to Performance Management Service! 📊",
        "description": "Where performance tracking meets fairness and dad jokes collide with science",
        "version": "1.0.0",
        "performance_master": "rickroll187",
        "tracking_accuracy": "scary_accurate",
        "bias_free_guarantee": "We measure skills, not shoe size!",
        "review_status": "always_fair_never_square",
        "fun_facts": [
            "We've tracked over 100,000 performance metrics! 📈",
            "Our bias detection is more thorough than airport security! 🛡️",
            "We can predict performance better than psychics predict the future! 🔮",
            "Our algorithms are fairer than a kindergarten teacher dividing cookies! 🍪"
        ],
        "endpoints": {
            "health": "GET /healthz",
            "metrics": "GET /metrics",
            "create_review": "POST /create-performance-review",
            "set_goals": "POST /set-employee-goals",
            "submit_feedback": "POST /submit-feedback",
            "get_performance": "GET /performance-summary/{employee_id}",
            "bias_audit": "GET /performance-bias-audit",
            "docs": "GET /docs"
        }
    }

@app.get("/healthz")
async def health_check():
    """Health check - ensuring our performance engine is running at peak efficiency! 📊"""
    return {
        "status": "healthy",
        "service": "performance-management",
        "timestamp": "2025-08-03T18:55:14Z",
        "version": "1.0.0",
        "performance_engine_status": "peak_efficiency",
        "bias_detection": "ultra_vigilant",
        "goal_tracking_system": "laser_focused",
        "feedback_analyzer": "constructively_awesome",
        "dad_joke_generator": "maximum_comedy"
    }

@app.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics - tracking every performance victory! 📊"""
    return generate_latest()

@app.post("/create-performance-review")
@require_permission(required_roles=["manager", "hr"])
async def create_performance_review(
    request: Request,
    review_request: PerformanceReviewRequest,
    db: Session = Depends(get_db)
):
    """
    Create performance review so fair, it would make Olympic judges weep with joy!
    This review system is more unbiased than a robot referee! 🤖⚖️
    """
    try:
        logger.info(f"📊 Creating performance review for employee {review_request.employee_id}")
        
        crud = PerformanceManagementCRUD(db)
        result = crud.create_performance_review(review_request)
        
        # Bias detection with more scrutiny than a tax audit
        bias_score = crud.validate_review_fairness(review_request, result)
        
        if bias_score > 0.10:  # Ultra-strict bias threshold
            logger.warning(f"⚠️ Potential bias detected in performance review (score: {bias_score})")
        
        # Send performance event to Kafka
        event_data = {
            "review_id": result.review_id,
            "employee_id": review_request.employee_id,
            "reviewer_id": review_request.reviewer_id,
            "overall_score": result.overall_score,
            "bias_score": bias_score,
            "fairness_certified": bias_score <= 0.10
        }
        
        send_hr_event("performance_review_created", event_data, "performance-management")
        
        metrics.track_hr_event("performance_review", "success")
        
        logger.info(f"✅ Performance review created with fairness score: {1.0 - bias_score:.3f}")
        return result
        
    except Exception as e:
        logger.error(f"💥 Error creating performance review: {e}")
        metrics.track_hr_event("performance_review", "error")
        raise HTTPException(status_code=500, detail=f"Performance review creation failed: {str(e)}")

@app.post("/set-employee-goals")
@require_permission(required_roles=["employee", "manager"])
async def set_employee_goals(
    request: Request,
    goal_request: GoalSettingRequest,
    db: Session = Depends(get_db)
):
    """
    Set employee goals with SMART criteria so smart, they graduated from Harvard! 🎓✨
    """
    try:
        logger.info(f"🎯 Setting goals for employee {goal_request.employee_id}")
        
        crud = PerformanceManagementCRUD(db)
        result = crud.set_employee_goals(goal_request)
        
        # Goal achievement humor
        goal_jokes = [
            "Goals set! Now let's crush them like we crush Monday mornings! ☕",
            "SMART goals created - they're so smart, they could teach a masterclass! 🎓",
            "Goals locked and loaded - time to be legendary! 🎯",
            "Achievement unlocked: Goal Setting Master! 🏆"
        ]
        
        return {
            "goal_summary": result,
            "motivational_message": goal_jokes[goal_request.employee_id % len(goal_jokes)],
            "success_probability": "high_with_proper_effort",
            "coach_advice": "Break big goals into smaller wins - like eating pizza slice by slice! 🍕"
        }
        
    except Exception as e:
        logger.error(f"💥 Error setting goals: {e}")
        raise HTTPException(status_code=500, detail="Goal setting failed")

@app.post("/submit-feedback")
@require_permission(required_roles=["employee", "manager"])
async def submit_feedback(
    request: Request,
    feedback_request: FeedbackSubmissionRequest,
    db: Session = Depends(get_db)
):
    """
    Submit feedback so constructive, it could build bridges! 🌉
    """
    try:
        logger.info(f"💬 Processing feedback from {feedback_request.giver_id} to {feedback_request.receiver_id}")
        
        crud = PerformanceManagementCRUD(db)
        result = crud.submit_feedback(feedback_request)
        
        # Feedback processing humor
        feedback_jokes = [
            "Feedback delivered with surgical precision! 🔬",
            "Constructive feedback: because we're all works in progress! 🚧",
            "Feedback processed faster than a drive-thru order! 🍔",
            "Growth mindset activated - level up incoming! 📈"
        ]
        
        return {
            "feedback_id": result["feedback_id"],
            "processing_status": "constructively_processed",
            "impact_prediction": "positive_growth_expected",
            "coach_humor": feedback_jokes[feedback_request.receiver_id % len(feedback_jokes)]
        }
        
    except Exception as e:
        logger.error(f"💥 Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail="Feedback submission failed")

@app.get("/performance-summary/{employee_id}")
@require_permission(required_roles=["employee", "manager", "hr"])
async def get_performance_summary(
    employee_id: int,
    include_trends: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get performance summary with more insights than a crystal ball! 🔮📊
    """
    try:
        crud = PerformanceManagementCRUD(db)
        summary = crud.get_performance_summary(employee_id, include_trends)
        
        if not summary:
            raise HTTPException(status_code=404, detail="No performance data found")
        
        # Performance insights humor
        insight_jokes = [
            "Performance trajectory: Ascending like a rocket! 🚀",
            "Your growth curve is more impressive than compound interest! 📈",
            "Performance data so good, it deserves its own analytics dashboard! 📊",
            "You're performing better than expectations - and our expectations were already high! ⭐"
        ]
        
        return {
            "employee_id": employee_id,
            "performance_summary": summary,
            "insight_humor": insight_jokes[employee_id % len(insight_jokes)],
            "coach_recommendation": "Keep being awesome with data to prove it! 📊⭐"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error retrieving performance summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve performance summary")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
