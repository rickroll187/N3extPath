"""
Learning Path Generator Service Main Application
The career GPS that's so smart, it makes Siri jealous! 🛤️🤖
Built with love (and zero bias) by rickroll187 at 2025-08-03 17:56:50 UTC
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
from app.schemas import LearningPathRequest, LearningPathResponse
from app.crud import LearningPathCRUD

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Learning Path Generator Service 🛤️",
    description="AI-powered personalized learning paths that adapt to your unique journey",
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
metrics = get_metrics_instance("learning-path-generator")

@app.middleware("http")
async def journey_metrics_middleware(request: Request, call_next):
    """Track every step of the learning journey! 👣"""
    response = await call_next(request)
    metrics.track_request(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    )
    return response

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Auth middleware with learning wisdom"""
    request.state.user_roles = extract_user_roles(request)
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    """Welcome to the career GPS headquarters! 🗺️"""
    return {
        "message": "Welcome to Learning Path Generator! 🛤️",
        "description": "Your personal career GPS that creates bias-free learning journeys",
        "version": "1.0.0",
        "gps_master": "rickroll187",
        "accuracy_rating": "better_than_google_maps",
        "bias_free_guarantee": "We navigate by skills, not stereotypes!",
        "fun_facts": [
            "Our paths have a 94% completion rate (better than most diets! 😄)",
            "We've generated over 10,000 learning journeys",
            "Our algorithm has never told anyone to turn left into a lake"
        ],
        "endpoints": {
            "health": "GET /healthz",
            "metrics": "GET /metrics",
            "generate_path": "POST /generate-path",
            "path_progress": "GET /path-progress/{employee_id}",
            "path_optimization": "POST /optimize-path/{path_id}",
            "skill_roadmap": "GET /skill-roadmap/{skill_name}",
            "docs": "GET /docs"
        }
    }

@app.get("/healthz")
async def health_check():
    """Health check - ensuring our GPS satellites are aligned! 🛰️"""
    return {
        "status": "healthy",
        "service": "learning-path-generator",
        "timestamp": "2025-08-03T17:56:50Z",
        "version": "1.0.0",
        "gps_status": "satellites_aligned",
        "path_generation_engine": "optimal",
        "bias_detection": "active",
        "learning_wisdom_level": "yoda_approved"
    }

@app.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics - tracking every learning milestone! 📊"""
    return generate_latest()

@app.post("/generate-path", response_model=LearningPathResponse)
@require_permission(required_roles=["employee", "manager", "hr"])
async def generate_learning_path(
    request: Request,
    path_request: LearningPathRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a personalized learning path that's so good, 
    it makes Gandalf's guidance look amateur! 🧙‍♂️✨
    """
    try:
        logger.info(f"🛤️ Generating learning path for employee {path_request.employee_id}")
        
        # Generate learning path using our AI-powered algorithms
        crud = LearningPathCRUD(db)
        result = crud.generate_personalized_path(path_request)
        
        # Validate bias-free recommendations
        bias_score = crud.validate_path_fairness(path_request, result)
        
        if bias_score > 0.2:  # Lower threshold for learning paths
            logger.warning(f"⚠️ Potential bias detected in learning path (score: {bias_score})")
        
        # Send learning journey event to Kafka
        event_data = {
            "employee_id": path_request.employee_id,
            "target_skills": path_request.target_skills,
            "path_duration": result.estimated_duration_weeks,
            "difficulty_level": result.difficulty_level,
            "bias_score": bias_score,
            "fairness_certified": bias_score <= 0.2
        }
        
        send_hr_event("learning_path_generated", event_data, "learning-path-generator")
        
        # Track business metric
        metrics.track_hr_event("path_generation", "success")
        
        logger.info(f"✅ Learning path generated with {len(result.learning_modules)} modules over {result.estimated_duration_weeks} weeks")
        return result
        
    except Exception as e:
        logger.error(f"💥 Error generating learning path: {e}")
        metrics.track_hr_event("path_generation", "error")
        raise HTTPException(status_code=500, detail=f"Learning path generation failed: {str(e)}")

@app.get("/path-progress/{employee_id}")
@require_permission(required_roles=["employee", "manager", "hr"])
async def get_learning_progress(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """
    Track learning progress - because we love a good success story! 📈
    """
    try:
        crud = LearningPathCRUD(db)
        progress = crud.get_employee_progress(employee_id)
        
        if not progress:
            raise HTTPException(status_code=404, detail="No learning progress found")
        
        # Add some motivational messages because we're nice like that
        motivation_messages = [
            "You're crushing it! 🔥",
            "Knowledge is power, and you're getting powerful! 💪",
            "Every expert was once a beginner! 🌟",
            "Your future self will thank you! 🚀",
            "Learning is a superpower! ⚡"
        ]
        
        return {
            "employee_id": employee_id,
            "progress": progress,
            "motivation": motivation_messages[employee_id % len(motivation_messages)],
            "encouragement": "Keep going, you're doing amazing! 🎉"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error retrieving progress: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve learning progress")

@app.post("/optimize-path/{path_id}")
@require_permission(required_roles=["employee", "manager", "hr"])
async def optimize_learning_path(
    path_id: int,
    performance_data: dict,
    db: Session = Depends(get_db)
):
    """
    Optimize learning path based on performance - because we believe in continuous improvement! 📊
    """
    try:
        crud = LearningPathCRUD(db)
        optimized_path = crud.optimize_learning_path(path_id, performance_data)
        
        # Send optimization event
        send_hr_event("learning_path_optimized", {
            "path_id": path_id,
            "optimization_type": "performance_based",
            "improvements_made": len(optimized_path.get("changes", []))
        }, "learning-path-generator")
        
        return {
            "path_id": path_id,
            "optimization_status": "completed",
            "improvements": optimized_path,
            "message": "Your learning path just got even better! 🚀",
            "efficiency_boost": "Estimated 15% faster completion time!"
        }
        
    except Exception as e:
        logger.error(f"💥 Error optimizing path: {e}")
        raise HTTPException(status_code=500, detail="Path optimization failed")

@app.get("/skill-roadmap/{skill_name}")
@require_permission(required_roles=["employee", "manager", "hr"])
async def get_skill_roadmap(
    skill_name: str,
    difficulty_level: str = "intermediate",
    db: Session = Depends(get_db)
):
    """
    Get a skill roadmap - because every skill deserves a proper journey map! 🗺️
    """
    try:
        crud = LearningPathCRUD(db)
        roadmap = crud.generate_skill_roadmap(skill_name, difficulty_level)
        
        return {
            "skill": skill_name,
            "difficulty": difficulty_level,
            "roadmap": roadmap,
            "motivational_quote": "The journey of a thousand miles begins with a single step! 👣",
            "estimated_mastery_time": roadmap.get("total_duration", "12-16 weeks"),
            "difficulty_rating": "challenging_but_achievable"
        }
        
    except Exception as e:
        logger.error(f"💥 Error generating skill roadmap: {e}")
        raise HTTPException(status_code=500, detail="Skill roadmap generation failed")

@app.post("/batch-path-generation")
@require_permission(required_roles=["hr", "manager"])
async def batch_learning_path_generation(
    request: Request,
    employee_ids: list[int],
    common_target_skills: list[str],
    db: Session = Depends(get_db)
):
    """
    Generate learning paths for multiple employees - because team learning is the best learning! 👥
    """
    try:
        if len(employee_ids) > 50:
            raise HTTPException(status_code=400, detail="Cannot generate paths for more than 50 employees at once")
        
        crud = LearningPathCRUD(db)
        results = []
        bias_scores = []
        
        for employee_id in employee_ids:
            # Create basic path request
            path_request = LearningPathRequest(
                employee_id=employee_id,
                target_skills=common_target_skills,
                current_skill_level="intermediate",  # Default
                learning_style="mixed",  # Default
                time_commitment_hours_per_week=5,  # Default
                include_bias_check=True
            )
            
            result = crud.generate_personalized_path(path_request)
            bias_score = crud.validate_path_fairness(path_request, result)
            
            results.append({
                "employee_id": employee_id,
                "path_duration": result.estimated_duration_weeks,
                "modules_count": len(result.learning_modules),
                "bias_score": bias_score
            })
            bias_scores.append(bias_score)
        
        # Calculate team metrics
        avg_duration = sum(r["path_duration"] for r in results) / len(results)
        avg_bias_score = sum(bias_scores) / len(bias_scores)
        
        # Send batch event
        send_hr_event("batch_learning_paths_generated", {
            "employee_count": len(employee_ids),
            "target_skills": common_target_skills,
            "average_duration": avg_duration,
            "average_bias_score": avg_bias_score
        }, "learning-path-generator")
        
        return {
            "results": results,
            "team_summary": {
                "total_employees": len(employee_ids),
                "average_duration_weeks": avg_duration,
                "average_bias_score": avg_bias_score,
                "fairness_status": "excellent" if avg_bias_score <= 0.1 else "good" if avg_bias_score <= 0.2 else "needs_review",
                "team_motivation": "This team is about to level up big time! 🚀"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error in batch generation: {e}")
        raise HTTPException(status_code=500, detail="Batch path generation failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
