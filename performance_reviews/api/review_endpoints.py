"""
LEGENDARY PERFORMANCE REVIEW API ENDPOINTS 🌐🎯
More responsive than a Swiss customer service with attitude!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator

from ...core.database.connection import get_db
from ...core.auth.authentication import get_current_user
from ...core.auth.authorization import AuthContext, Permission
from ..services.performance_crud import LegendaryPerformanceCRUD
from ..services.review_fairness_engine import LegendaryFairnessEngine
from ..models.review_models import ReviewCycle, ReviewStatus, RatingScale

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/performance", tags=["performance_reviews"])

# ===========================================
# PYDANTIC MODELS FOR API
# ===========================================

class ReviewCycleCreate(BaseModel):
    """
    Review cycle creation model!
    More structured than a Swiss blueprint! 🏗️📋
    """
    name: str = Field(..., min_length=3, max_length=100, description="Cycle name")
    cycle_type: str = Field(..., description="Type of review cycle")
    start_date: datetime = Field(..., description="Cycle start date")
    end_date: datetime = Field(..., description="Cycle end date")
    self_assessment_deadline: datetime = Field(..., description="Self assessment deadline")
    manager_review_deadline: datetime = Field(..., description="Manager review deadline")
    final_deadline: datetime = Field(..., description="Final submission deadline")
    enable_self_assessment: bool = Field(True, description="Enable self assessments")
    enable_peer_reviews: bool = Field(True, description="Enable peer reviews")
    enable_360_feedback: bool = Field(False, description="Enable 360 feedback")
    min_peer_reviewers: int = Field(2, ge=0, le=10, description="Minimum peer reviewers")
    max_peer_reviewers: int = Field(5, ge=1, le=20, description="Maximum peer reviewers")
    auto_generate_reviews: bool = Field(True, description="Auto-generate reviews for all employees")
    
    @validator('end_date')
    def end_date_after_start(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v
    
    @validator('cycle_type')
    def validate_cycle_type(cls, v):
        valid_types = [cycle.value for cycle in ReviewCycle]
        if v not in valid_types:
            raise ValueError(f'Invalid cycle type. Must be one of: {valid_types}')
        return v

class PerformanceReviewCreate(BaseModel):
    """
    Performance review creation model!
    More detailed than a biography with metrics! 📊👤
    """
    review_cycle_id: int = Field(..., description="Review cycle ID")
    employee_id: int = Field(..., description="Employee being reviewed")
    reviewer_id: int = Field(..., description="Primary reviewer (manager)")
    default_goals: Optional[List[Dict[str, Any]]] = Field(None, description="Default goals to create")

class ReviewStatusUpdate(BaseModel):
    """
    Review status update model!
    More precise than a Swiss timepiece! ⏰✨
    """
    status: str = Field(..., description="New review status")
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = [status.value for status in ReviewStatus]
        if v not in valid_statuses:
            raise ValueError(f'Invalid status. Must be one of: {valid_statuses}')
        return v

class ReviewAssessmentUpdate(BaseModel):
    """
    Review assessment update model!
    More comprehensive than a doctoral thesis! 🎓📋
    """
    overall_rating: Optional[str] = Field(None, description="Overall performance rating")
    overall_score: Optional[float] = Field(None, ge=0, le=100, description="Overall score (0-100)")
    manager_comments: Optional[str] = Field(None, description="Manager comments")
    strengths: Optional[str] = Field(None, description="Employee strengths")
    areas_for_improvement: Optional[str] = Field(None, description="Areas for improvement")
    achievements: Optional[List[str]] = Field(None, description="Key achievements")
    goals_met: Optional[List[str]] = Field(None, description="Goals successfully met")
    goals_missed: Optional[List[str]] = Field(None, description="Goals not achieved")
    development_plan: Optional[Dict[str, Any]] = Field(None, description="Development plan")
    promotion_ready: Optional[bool] = Field(None, description="Ready for promotion")
    promotion_timeline: Optional[str] = Field(None, description="Promotion timeline")
    salary_increase_recommended: Optional[float] = Field(None, ge=0, le=100, description="Salary increase %")
    bonus_recommended: Optional[float] = Field(None, ge=0, description="Bonus amount")
    
    @validator('overall_rating')
    def validate_rating(cls, v):
        if v is not None:
            valid_ratings = [rating.value for rating in RatingScale]
            if v not in valid_ratings:
                raise ValueError(f'Invalid rating. Must be one of: {valid_ratings}')
        return v

# ===========================================
# DEPENDENCY FUNCTIONS
# ===========================================

async def get_performance_crud(db: Session = Depends(get_db)) -> LegendaryPerformanceCRUD:
    """Get performance CRUD instance"""
    return LegendaryPerformanceCRUD(db)

async def get_fairness_engine(db: Session = Depends(get_db)) -> LegendaryFairnessEngine:
    """Get fairness engine instance"""
    return LegendaryFairnessEngine(db)

# ===========================================
# REVIEW CYCLE ENDPOINTS
# ===========================================

@router.post("/cycles", response_model=Dict[str, Any])
async def create_review_cycle(
    cycle_data: ReviewCycleCreate,
    current_user: AuthContext = Depends(get_current_user),
    crud: LegendaryPerformanceCRUD = Depends(get_performance_crud)
):
    """
    Create new performance review cycle!
    More organized than a Swiss train schedule! 🚂📅
    """
    try:
        logger.info(f"🎯 API: Creating review cycle - {cycle_data.name}")
        
        # Convert Pydantic model to dict
        cycle_dict = cycle_data.dict()
        
        # Create cycle
        result = crud.create_review_cycle(cycle_dict, current_user)
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "success": True,
                    "message": "Review cycle created successfully! 🎯",
                    "data": result,
                    "legendary_quote": "Another legendary cycle begins! CODE BROS CREATE THE BEST! 🏆"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to create review cycle")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 API: Review cycle creation error - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during cycle creation"
        )

@router.get("/cycles", response_model=Dict[str, Any])
async def get_review_cycles(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    cycle_type: Optional[str] = Query(None, description="Filter by cycle type"),
    start_date_from: Optional[datetime] = Query(None, description="Filter by start date from"),
    end_date_to: Optional[datetime] = Query(None, description="Filter by end date to"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Items per page"),
    current_user: AuthContext = Depends(get_current_user),
    crud: LegendaryPerformanceCRUD = Depends(get_performance_crud)
):
    """
    Get review cycles with filtering!
    More organized than a Swiss library! 📚🎯
    """
    try:
        logger.info(f"📊 API: Getting review cycles - Page {page}")
        
        # Build filters
        filters = {
            "page": page,
            "per_page": per_page
        }
        
        if is_active is not None:
            filters["is_active"] = is_active
        if cycle_type:
            filters["cycle_type"] = cycle_type
        if start_date_from:
            filters["start_date_from"] = start_date_from
        if end_date_to:
            filters["end_date_to"] = end_date_to
        
        # Get cycles
        result = crud.get_review_cycles(filters, current_user)
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "message": f"Retrieved {len(result['cycles'])} review cycles! 📊",
                    "data": result,
                    "legendary_quote": "Cycles retrieved with Swiss precision! CODE BROS DELIVER! 🎯"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to retrieve review cycles")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 API: Review cycles retrieval error - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during cycles retrieval"
        )

@router.get("/cycles/{cycle_id}", response_model=Dict[str, Any])
async def get_review_cycle(
    cycle_id: int = Path(..., description="Review cycle ID"),
    current_user: AuthContext = Depends(get_current_user),
    crud: LegendaryPerformanceCRUD = Depends(get_performance_crud)
):
    """
    Get specific review cycle!
    More detailed than a Swiss manual! 📋✨
    """
    try:
        logger.info(f"🔍 API: Getting review cycle - {cycle_id}")
        
        # Get cycle (implement this method in CRUD)
        # For now, return a placeholder response
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": f"Review cycle {cycle_id} retrieved! 🎯",
                "data": {"cycle_id": cycle_id, "placeholder": "Implementation pending"},
                "legendary_quote": "Cycle details delivered with legendary precision! 🏆"
            }
        )
        
    except Exception as e:
        logger.error(f"💥 API: Review cycle retrieval error - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during cycle retrieval"
        )

# ===========================================
# INDIVIDUAL REVIEW ENDPOINTS
# ===========================================

@router.post("/reviews", response_model=Dict[str, Any])
async def create_performance_review(
    review_data: PerformanceReviewCreate,
    current_user: AuthContext = Depends(get_current_user),
    crud: LegendaryPerformanceCRUD = Depends(get_performance_crud)
):
    """
    Create individual performance review!
    More personalized than a custom-tailored suit! 👔✨
    """
    try:
        logger.info(f"📝 API: Creating performance review - Employee {review_data.employee_id}")
        
        # Convert Pydantic model to dict
        review_dict = review_data.dict()
        
        # Create review
        result = crud.create_performance_review(review_dict, current_user)
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "success": True,
                    "message": "Performance review created successfully! 📝",
                    "data": result,
                    "legendary_quote": "Another legendary review begins! CODE BROS ASSESS THE BEST! 🏆"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to create performance review")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 API: Performance review creation error - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during review creation"
        )

@router.patch("/reviews/{review_id}/status", response_model=Dict[str, Any])
async def update_review_status(
    review_id: int = Path(..., description="Review ID"),
    status_update: ReviewStatusUpdate = None,
    current_user: AuthContext = Depends(get_current_user),
    crud: LegendaryPerformanceCRUD = Depends(get_performance_crud)
):
    """
    Update review status!
    More precise than a Swiss timepiece! ⏰🎯
    """
    try:
        logger.info(f"🔄 API: Updating review status - {review_id} -> {status_update.status}")
        
        # Update status
        result = crud.update_review_status(review_id, status_update.status, current_user)
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "message": f"Review status updated to {status_update.status}! 🔄",
                    "data": result,
                    "legendary_quote": "Status updated with legendary precision! CODE BROS DELIVER! ⏰"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to update review status")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 API: Review status update error - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during status update"
        )

# ===========================================
# FAIRNESS ANALYSIS ENDPOINTS
# ===========================================

@router.get("/reviews/{review_id}/fairness", response_model=Dict[str, Any])
async def analyze_review_fairness(
    review_id: int = Path(..., description="Review ID"),
    current_user: AuthContext = Depends(get_current_user),
    fairness_engine: LegendaryFairnessEngine = Depends(get_fairness_engine)
):
    """
    Analyze individual review for fairness!
    More thorough than a Supreme Court investigation! ⚖️🔍
    """
    try:
        logger.info(f"⚖️ API: Analyzing review fairness - {review_id}")
        
        # Analyze fairness
        result = fairness_engine.analyze_review_fairness(review_id, current_user)
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "message": "Fairness analysis completed! ⚖️",
                    "data": result,
                    "legendary_quote": "Justice delivered with legendary precision! CODE BROS ENSURE FAIRNESS! 🏛️"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to analyze review fairness")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 API: Review fairness analysis error - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during fairness analysis"
        )

@router.get("/cycles/{cycle_id}/fairness", response_model=Dict[str, Any])
async def analyze_cycle_fairness(
    cycle_id: int = Path(..., description="Review cycle ID"),
    current_user: AuthContext = Depends(get_current_user),
    fairness_engine: LegendaryFairnessEngine = Depends(get_fairness_engine)
):
    """
    Analyze entire review cycle for fairness!
    More comprehensive than a federal investigation! 📊⚖️
    """
    try:
        logger.info(f"📊 API: Analyzing cycle fairness - {cycle_id}")
        
        # Analyze cycle fairness
        result = fairness_engine.analyze_cycle_fairness(cycle_id, current_user)
        
        if result["success"]:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "success": True,
                    "message": "Cycle fairness analysis completed! 📊",
                    "data": result,
                    "legendary_quote": "Cycle justice delivered with Swiss precision! CODE BROS ENSURE BALANCE! ⚖️"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to analyze cycle fairness")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 API: Cycle fairness analysis error - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during cycle fairness analysis"
        )

# ===========================================
# HEALTH CHECK ENDPOINT
# ===========================================

@router.get("/health", response_model=Dict[str, Any])
async def performance_health_check():
    """
    Performance review system health check!
    More reliable than a Swiss timepiece! ⏰✅
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "performance_reviews",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "legendary_status": "PERFORMANCE REVIEW SYSTEM RUNNING LIKE A LEGENDARY MACHINE! 🏆",
            "code_bros_motto": "CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 😄💪"
        }
    )