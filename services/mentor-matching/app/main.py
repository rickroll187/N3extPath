"""
Mentor Matching Service Main Application
The career cupid that matches based on skills, not similarities! 🤝💕
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
from app.schemas import MentorMatchRequest, MentorMatchResponse
from app.crud import MentorMatchingCRUD

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Mentor Matching Service 🤝",
    description="AI-powered mentor-mentee matching based on skills and growth potential",
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
metrics = get_metrics_instance("mentor-matching")

@app.middleware("http")
async def love_metrics_middleware(request: Request, call_next):
    """Track all the career love connections! 💕"""
    response = await call_next(request)
    metrics.track_request(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    )
    return response

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Auth middleware with extra love"""
    request.state.user_roles = extract_user_roles(request)
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    """Welcome to the career cupid headquarters!"""
    return {
        "message": "Welcome to Mentor Matching Service! 🤝",
        "description": "Where career relationships bloom based on skills and potential",
        "version": "1.0.0",
        "career_cupid": "rickroll187",
        "success_rate": "better_than_eharmony",
        "bias_free_guarantee": "We match minds, not demographics!",
        "fun_fact": "Our algorithm has a 97% compatibility rate (citation needed 😄)",
        "endpoints": {
            "health": "GET /healthz",
            "metrics": "GET /metrics",
            "find_mentor": "POST /match-mentor",
            "mentor_profile": "GET /mentor-profile/{employee_id}",
            "relationship_status": "GET /mentorship-status/{mentorship_id}",
            "breakup": "POST /end-mentorship/{mentorship_id}",
            "docs": "GET /docs"
        }
    }

@app.get("/healthz")
async def health_check():
    """Health check - ensuring cupid's arrows are sharp!"""
    return {
        "status": "healthy",
        "service": "mentor-matching",
        "timestamp": "2025-08-03T17:45:00Z",
        "version": "1.0.0",
        "cupid_status": "ready_to_match",
        "love_algorithm_status": "optimized_for_fairness"
    }

@app.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics - tracking all the career love!"""
    return generate_latest()

@app.post("/match-mentor", response_model=MentorMatchResponse)
@require_permission(required_roles=["employee", "manager", "hr"])
async def match_mentor(
    request: Request,
    match_request: MentorMatchRequest,
    db: Session = Depends(get_db)
):
    """
    Find the perfect mentor match based on skills and growth needs
    Better than dating apps, but for your career! 💕✨
    """
    try:
        logger.info(f"🤝 Starting mentor matching for employee {match_request.mentee_id}")
        
        # Process mentor matching using our bias-free algorithms
        crud = MentorMatchingCRUD(db)
        result = crud.find_mentor_matches(match_request)
        
        # Validate fairness of matches
        fairness_score = crud.validate_match_fairness(match_request, result)
        
        if fairness_score < 0.8:  # Fairness threshold
            logger.warning(f"⚠️ Match fairness below threshold: {fairness_score}")
        
        # Send love event to Kafka (career love, that is!)
        event_data = {
            "mentee_id": match_request.mentee_id,
            "mentor_matches": [match.mentor_id for match in result.mentor_matches],
            "matching_algorithm": result.algorithm_used,
            "fairness_score": fairness_score,
            "skills_matched": match_request.skills_to_develop
        }
        
        send_hr_event("mentor_matching_completed", event_data, "mentor-matching")
        
        # Track business metric
        metrics.track_hr_event("mentor_matching", "success")
        
        logger.info(f"✅ Found {len(result.mentor_matches)} mentor matches with fairness score: {fairness_score}")
        return result
        
    except Exception as e:
        logger.error(f"💥 Error in mentor matching: {e}")
        metrics.track_hr_event("mentor_matching", "error")
        raise HTTPException(status_code=500, detail=f"Mentor matching failed: {str(e)}")

@app.post("/create-mentorship")
@require_permission(required_roles=["employee", "manager", "hr"])
async def create_mentorship(
    request: Request,
    mentee_id: int,
    mentor_id: int,
    duration_months: int = 6,
    db: Session = Depends(get_db)
):
    """
    Create a mentorship relationship - it's official! 💍
    (But for careers, not marriage... although both can be life-changing!)
    """
    try:
        crud = MentorMatchingCRUD(db)
        mentorship = crud.create_mentorship_relationship(mentee_id, mentor_id, duration_months)
        
        # Send the good news to Kafka
        event_data = {
            "mentorship_id": mentorship.id,
            "mentee_id": mentee_id,
            "mentor_id": mentor_id,
            "duration_months": duration_months,
            "relationship_status": "newly_matched"
        }
        
        send_hr_event("mentorship_created", event_data, "mentor-matching")
        
        return {
            "mentorship_id": mentorship.id,
            "status": "relationship_created",
            "message": "Congratulations! A beautiful mentorship has begun! 💕",
            "mentee_id": mentee_id,
            "mentor_id": mentor_id,
            "duration": f"{duration_months} months",
            "relationship_advice": "Communication is key! (Just like in real relationships 😄)"
        }
        
    except Exception as e:
        logger.error(f"💥 Error creating mentorship: {e}")
        raise HTTPException(status_code=500, detail="Failed to create mentorship relationship")

@app.get("/mentorship-status/{mentorship_id}")
@require_permission(required_roles=["employee", "manager", "hr"])
async def get_mentorship_status(
    mentorship_id: int,
    db: Session = Depends(get_db)
):
    """Check the relationship status - like Facebook, but for mentorship!"""
    try:
        crud = MentorMatchingCRUD(db)
        status = crud.get_mentorship_status(mentorship_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Mentorship not found")
        
        return {
            "mentorship_id": mentorship_id,
            "status": status,
            "relationship_health": "thriving" if status.get("meetings_completed", 0) > 2 else "developing",
            "facebook_status_equivalent": "It's Complicated" if status.get("status") == "active" else "Single"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error getting mentorship status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get mentorship status")

@app.post("/end-mentorship/{mentorship_id}")
@require_permission(required_roles=["employee", "manager", "hr"])
async def end_mentorship(
    mentorship_id: int,
    reason: str = "completed_successfully",
    db: Session = Depends(get_db)
):
    """
    End a mentorship relationship - sometimes good things come to an end! 💔
    (But hopefully on good terms!)
    """
    try:
        crud = MentorMatchingCRUD(db)
        result = crud.end_mentorship_relationship(mentorship_id, reason)
        
        # Send breakup... err, completion event
        event_data = {
            "mentorship_id": mentorship_id,
            "end_reason": reason,
            "relationship_duration": result.get("duration_days", 0),
            "success_rating": result.get("success_rating", "unknown")
        }
        
        send_hr_event("mentorship_ended", event_data, "mentor-matching")
        
        return {
            "mentorship_id": mentorship_id,
            "status": "relationship_ended",
            "message": "Thanks for the memories! Hope you both learned something! 🎓",
            "reason": reason,
            "relationship_counselor_note": "Remember, every ending is a new beginning! 🌟"
        }
        
    except Exception as e:
        logger.error(f"💥 Error ending mentorship: {e}")
        raise HTTPException(status_code=500, detail="Failed to end mentorship")

@app.get("/mentor-compatibility/{mentee_id}/{mentor_id}")
@require_permission(required_roles=["employee", "manager", "hr"])
async def check_compatibility(
    mentee_id: int,
    mentor_id: int,
    db: Session = Depends(get_db)
):
    """
    Check compatibility between potential mentor and mentee
    Like a pre-relationship compatibility test! 💕
    """
    try:
        crud = MentorMatchingCRUD(db)
        compatibility = crud.calculate_compatibility(mentee_id, mentor_id)
        
        compatibility_level = "Perfect Match! 💕" if compatibility > 0.9 else \
                            "Great Match! 😍" if compatibility > 0.7 else \
                            "Good Match! 😊" if compatibility > 0.5 else \
                            "It's Complicated 🤔"
        
        return {
            "mentee_id": mentee_id,
            "mentor_id": mentor_id,
            "compatibility_score": compatibility,
            "compatibility_level": compatibility_level,
            "relationship_forecast": "Sunny with a chance of career growth! ☀️",
            "recommended_action": "Go for it!" if compatibility > 0.6 else "Maybe keep looking..."
        }
        
    except Exception as e:
        logger.error(f"💥 Error checking compatibility: {e}")
        raise HTTPException(status_code=500, detail="Compatibility check failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
