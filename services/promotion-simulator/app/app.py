"""
Promotion Simulator Service Main Application
The crystal ball for career advancement that HR never knew they needed!
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
from app.schemas import PromotionSimulationRequest, PromotionSimulationResponse
from app.crud import PromotionSimulatorCRUD

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Promotion Simulator Service 🔮",
    description="AI-powered promotion readiness and career path simulation",
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
metrics = get_metrics_instance("promotion-simulator")

@app.middleware("http")
async def custom_metrics_middleware(request: Request, call_next):
    """Track all the things!"""
    response = await call_next(request)
    metrics.track_request(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    )
    return response

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Extract user roles because security is sexy"""
    request.state.user_roles = extract_user_roles(request)
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    """Welcome to the promotion fortune teller!"""
    return {
        "message": "Welcome to Promotion Simulator! 🔮",
        "description": "AI-powered promotion readiness analysis and career simulation",
        "version": "1.0.0",
        "fortune_teller": "rickroll187",
        "disclaimer": "No crystal balls were harmed in the making of this service",
        "endpoints": {
            "health": "GET /healthz",
            "metrics": "GET /metrics",
            "simulate": "POST /simulate-promotion",
            "history": "GET /simulation-history/{employee_id}",
            "docs": "GET /docs"
        }
    }

@app.get("/healthz")
async def health_check():
    """Health check - keeping the fortune teller healthy!"""
    return {
        "status": "healthy",
        "service": "promotion-simulator",
        "timestamp": "2025-08-03T17:16:15Z",
        "version": "1.0.0",
        "crystal_ball_status": "crystal_clear"
    }

@app.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics - because data is beautiful"""
    return generate_latest()

@app.post("/simulate-promotion", response_model=PromotionSimulationResponse)
@require_permission(required_roles=["employee", "manager", "hr"])
async def simulate_promotion(
    request: Request,
    simulation_request: PromotionSimulationRequest,
    db: Session = Depends(get_db)
):
    """
    Simulate promotion readiness - the magic happens here! ✨
    Using advanced algorithms that would make Fortune 500 companies jealous
    """
    try:
        logger.info(f"🔮 Starting promotion simulation for employee {simulation_request.employee_id}")
        
        # Process simulation using our AI-powered CRUD
        crud = PromotionSimulatorCRUD(db)
        result = crud.simulate_promotion(simulation_request)
        
        # Send event to Kafka because everyone needs to know about potential promotions
        event_data = {
            "employee_id": simulation_request.employee_id,
            "target_position": simulation_request.target_position,
            "current_performance_score": simulation_request.current_performance_score,
            "promotion_probability": result.promotion_probability,
            "recommendation": result.recommendation
        }
        
        send_hr_event("promotion_simulation_completed", event_data, "promotion-simulator")
        
        # Track business metric
        metrics.track_hr_event("promotion_simulation", "success")
        
        logger.info(f"✅ Promotion simulation completed with {result.promotion_probability}% probability")
        return result
        
    except Exception as e:
        logger.error(f"💥 Error in promotion simulation: {e}")
        metrics.track_hr_event("promotion_simulation", "error")
        raise HTTPException(status_code=500, detail=f"Promotion simulation failed: {str(e)}")

@app.get("/simulation-history/{employee_id}")
@require_permission(required_roles=["manager", "hr"])
async def get_simulation_history(
    employee_id: int,
    db: Session = Depends(get_db)
):
    """Get promotion simulation history for an employee"""
    try:
        crud = PromotionSimulatorCRUD(db)
        history = crud.get_employee_simulation_history(employee_id)
        
        if not history:
            raise HTTPException(status_code=404, detail="No simulation history found")
        
        return {
            "employee_id": employee_id,
            "simulations": history,
            "total_simulations": len(history)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error retrieving simulation history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve simulation history")

@app.post("/batch-simulate")
@require_permission(required_roles=["hr", "manager"])
async def batch_promotion_simulation(
    request: Request,
    employee_ids: list[int],
    target_position: str,
    db: Session = Depends(get_db)
):
    """
    Batch promotion simulation for multiple employees
    Because HR loves efficiency almost as much as they love spreadsheets
    """
    try:
        if len(employee_ids) > 50:  # Reasonable limit
            raise HTTPException(status_code=400, detail="Cannot simulate more than 50 employees at once")
        
        crud = PromotionSimulatorCRUD(db)
        results = []
        
        for employee_id in employee_ids:
            # Create a basic simulation request
            sim_request = PromotionSimulationRequest(
                employee_id=employee_id,
                target_position=target_position,
                current_performance_score=75.0,  # Default
                years_in_current_role=2.0,  # Default
                include_development_plan=False
            )
            
            result = crud.simulate_promotion(sim_request)
            results.append({
                "employee_id": employee_id,
                "promotion_probability": result.promotion_probability,
                "recommendation": result.recommendation
            })
        
        # Send batch event
        send_hr_event("batch_promotion_simulation", {
            "employee_count": len(employee_ids),
            "target_position": target_position,
            "average_probability": sum(r["promotion_probability"] for r in results) / len(results)
        }, "promotion-simulator")
        
        return {
            "results": results,
            "summary": {
                "total_employees": len(employee_ids),
                "average_probability": sum(r["promotion_probability"] for r in results) / len(results),
                "ready_for_promotion": len([r for r in results if r["promotion_probability"] >= 70])
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error in batch simulation: {e}")
        raise HTTPException(status_code=500, detail="Batch simulation failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
