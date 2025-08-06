# File: backend/performance/legendary_performance_system.py
"""
📊🎸 N3EXTPATH - LEGENDARY PERFORMANCE MANAGEMENT SYSTEM 🎸📊
Professional performance reviews with AI-driven insights and Swiss precision
Built: 2025-08-05 22:26:18 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, BackgroundTasks
from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timezone, timedelta
from enum import Enum
import logging
from sqlalchemy.orm import Session
from sqlalchemy import text, func
import statistics
import uuid
import json

# Import dependencies
from auth.security import get_current_user, get_legendary_user, verify_rickroll187
from database.connection import get_db_session, db_utils
from config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)

# =====================================
# 🎸 LEGENDARY PERFORMANCE ROUTER 🎸
# =====================================

router = APIRouter(
    prefix="/performance",
    tags=["Legendary Performance Management"],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Insufficient privileges"},
        404: {"description": "Performance review not found"},
        422: {"description": "Validation error with Swiss precision"},
    }
)

# =====================================
# 📊 PERFORMANCE ENUMS & CONSTANTS 📊
# =====================================

class ReviewCycle(str, Enum):
    QUARTERLY = "quarterly"
    SEMI_ANNUAL = "semi_annual"
    ANNUAL = "annual"
    PROBATION = "probation"
    PROJECT_END = "project_end"

class ReviewStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    COMPLETED = "completed"
    APPROVED = "approved"

class PerformanceMetric(str, Enum):
    OVERALL = "overall_performance"
    TECHNICAL = "technical_skills"
    COMMUNICATION = "communication"
    LEADERSHIP = "leadership"
    COLLABORATION = "collaboration"
    INNOVATION = "innovation"
    RELIABILITY = "reliability"
    PROBLEM_SOLVING = "problem_solving"

# Swiss Precision Performance Standards
SWISS_PRECISION_THRESHOLDS = {
    "excellent": 4.5,
    "good": 4.0,
    "satisfactory": 3.5,
    "needs_improvement": 3.0,
    "unsatisfactory": 2.0
}

LEGENDARY_PERFORMANCE_MULTIPLIER = 1.2  # Legendary users get bonus consideration

# =====================================
# 📋 LEGENDARY PYDANTIC MODELS 📋
# =====================================

class PerformanceScores(BaseModel):
    """Performance scores with Swiss precision validation"""
    overall_performance: float = Field(..., ge=1.0, le=5.0, description="Overall performance (1-5)")
    technical_skills: float = Field(..., ge=1.0, le=5.0, description="Technical skills (1-5)")
    communication: float = Field(..., ge=1.0, le=5.0, description="Communication (1-5)")
    leadership: float = Field(..., ge=1.0, le=5.0, description="Leadership (1-5)")
    collaboration: float = Field(..., ge=1.0, le=5.0, description="Collaboration (1-5)")
    innovation: float = Field(..., ge=1.0, le=5.0, description="Innovation (1-5)")
    reliability: float = Field(..., ge=1.0, le=5.0, description="Reliability (1-5)")
    problem_solving: float = Field(..., ge=1.0, le=5.0, description="Problem solving (1-5)")

class PerformanceReviewRequest(BaseModel):
    """Create performance review request"""
    reviewee_id: str = Field(..., description="User being reviewed")
    review_period_start: datetime = Field(..., description="Review period start date")
    review_period_end: datetime = Field(..., description="Review period end date")
    review_cycle: ReviewCycle = Field(..., description="Review cycle type")
    scores: PerformanceScores = Field(..., description="Performance scores")
    
    # Narrative sections
    achievements: str = Field(..., min_length=50, description="Key achievements")
    strengths: str = Field(..., min_length=30, description="Areas of strength")
    improvement_areas: str = Field(..., min_length=30, description="Areas for improvement")
    goals_next_period: str = Field(..., min_length=50, description="Goals for next period")
    additional_comments: Optional[str] = Field(None, description="Additional comments")
    
    # Compensation and development
    salary_recommendation: Optional[float] = Field(None, ge=0, description="Salary recommendation")
    promotion_recommendation: Optional[str] = Field(None, description="Promotion recommendation")
    development_plan: Optional[str] = Field(None, description="Development plan")
    
    # Swiss precision and legendary features
    is_legendary_review: bool = Field(default=False, description="🎸 Legendary review status")
    swiss_precision_notes: Optional[str] = Field(None, description="Swiss precision observations")
    code_bro_energy_notes: Optional[str] = Field(None, description="Code bro energy assessment")

class PerformanceReviewUpdate(BaseModel):
    """Update performance review request"""
    scores: Optional[PerformanceScores] = Field(None, description="Updated performance scores")
    achievements: Optional[str] = Field(None, min_length=50, description="Updated achievements")
    strengths: Optional[str] = Field(None, min_length=30, description="Updated strengths")
    improvement_areas: Optional[str] = Field(None, min_length=30, description="Updated improvement areas")
    goals_next_period: Optional[str] = Field(None, min_length=50, description="Updated goals")
    additional_comments: Optional[str] = Field(None, description="Updated comments")
    salary_recommendation: Optional[float] = Field(None, ge=0, description="Updated salary recommendation")
    promotion_recommendation: Optional[str] = Field(None, description="Updated promotion recommendation")
    development_plan: Optional[str] = Field(None, description="Updated development plan")
    status: Optional[ReviewStatus] = Field(None, description="Review status")
    swiss_precision_notes: Optional[str] = Field(None, description="Updated Swiss precision notes")
    code_bro_energy_notes: Optional[str] = Field(None, description="Updated code bro energy notes")

class PerformanceReviewResponse(BaseModel):
    """Performance review response"""
    review_id: str
    reviewee_id: str
    reviewer_id: str
    reviewee_name: str
    reviewer_name: str
    review_period_start: datetime
    review_period_end: datetime
    review_cycle: str
    status: str
    scores: Dict[str, float]
    achievements: str
    strengths: str
    improvement_areas: str
    goals_next_period: str
    additional_comments: Optional[str]
    salary_recommendation: Optional[float]
    promotion_recommendation: Optional[str]
    development_plan: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    approved_at: Optional[datetime]
    approved_by: Optional[str]
    
    # Legendary metadata
    is_legendary_review: bool
    swiss_precision_score: Optional[float]
    code_bro_rating: Optional[int]
    ai_insights: Optional[Dict[str, Any]]

class PerformanceFeedbackRequest(BaseModel):
    """360-degree feedback request"""
    to_user_id: str = Field(..., description="User receiving feedback")
    feedback_type: str = Field(..., description="Type of feedback (peer, subordinate, manager)")
    rating: float = Field(..., ge=1.0, le=5.0, description="Overall rating (1-5)")
    feedback_text: str = Field(..., min_length=100, description="Detailed feedback")
    strengths: str = Field(..., min_length=50, description="Observed strengths")
    improvement_suggestions: str = Field(..., min_length=50, description="Improvement suggestions")
    anonymous: bool = Field(default=True, description="Anonymous feedback")
    legendary_recognition: bool = Field(default=False, description="🎸 Legendary performance recognition")

class PerformanceFeedbackResponse(BaseModel):
    """Performance feedback response"""
    feedback_id: str
    from_user_id: Optional[str]  # None if anonymous
    to_user_id: str
    from_user_name: Optional[str]  # None if anonymous
    to_user_name: str
    feedback_type: str
    rating: float
    feedback_text: str
    strengths: str
    improvement_suggestions: str
    anonymous: bool
    legendary_recognition: bool
    created_at: datetime

class PerformanceAnalyticsResponse(BaseModel):
    """Performance analytics response"""
    user_id: Optional[str]
    period_start: datetime
    period_end: datetime
    
    # Score analytics
    average_scores: Dict[str, float]
    score_trends: Dict[str, List[float]]
    performance_grade: str
    
    # Comparative analytics
    department_comparison: Optional[Dict[str, float]]
    role_comparison: Optional[Dict[str, float]]
    company_percentile: Optional[float]
    
    # Legendary analytics
    swiss_precision_score: Optional[float]
    code_bro_energy_level: Optional[str]
    legendary_achievements: int
    
    # AI insights
    ai_insights: Dict[str, Any]
    recommendations: List[str]

# =====================================
# 📊 PERFORMANCE REVIEW OPERATIONS 📊
# =====================================

@router.post("/reviews", response_model=PerformanceReviewResponse, summary="📝 Create Performance Review")
async def create_performance_review(
    review_data: PerformanceReviewRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Create performance review with Swiss precision and AI insights
    """
    try:
        reviewer_id = current_user.get("user_id")
        reviewer_role = current_user.get("role")
        reviewer_username = current_user.get("username")
        
        # Validate reviewer permissions
        if reviewer_role not in ["manager", "hr_manager", "admin", "founder"] and reviewer_username != "rickroll187":
            # Check if reviewing direct report
            if reviewer_role == "manager":
                direct_report = db.execute(
                    text("SELECT user_id FROM users WHERE user_id = :reviewee_id AND manager_id = :reviewer_id"),
                    {"reviewee_id": review_data.reviewee_id, "reviewer_id": reviewer_id}
                ).fetchone()
                
                if not direct_report:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Can only review direct reports"
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient privileges to create performance reviews"
                )
        
        # Validate reviewee exists
        reviewee = db.execute(
            text("""
                SELECT user_id, username, first_name, last_name, is_legendary, role, department
                FROM users WHERE user_id = :reviewee_id AND is_active = true
            """),
            {"reviewee_id": review_data.reviewee_id}
        ).fetchone()
        
        if not reviewee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reviewee not found or inactive"
            )
        
        reviewee_data = dict(reviewee._mapping)
        
        # Check for overlapping review periods
        existing_review = db.execute(
            text("""
                SELECT review_id FROM performance_reviews_enhanced 
                WHERE reviewee_id = :reviewee_id 
                  AND (review_period_start <= :period_end AND review_period_end >= :period_start)
                  AND status != 'draft'
            """),
            {
                "reviewee_id": review_data.reviewee_id,
                "period_start": review_data.review_period_start,
                "period_end": review_data.review_period_end
            }
        ).fetchone()
        
        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Overlapping review period exists"
            )
        
        # Calculate Swiss precision score and AI insights
        scores_dict = review_data.scores.dict()
        swiss_precision_score = calculate_swiss_precision_score(scores_dict, reviewee_data.get("is_legendary", False))
        ai_insights = generate_ai_performance_insights(scores_dict, review_data.dict(), reviewee_data)
        
        # Generate review ID
        review_id = str(uuid.uuid4())
        
        # Create performance review
        db.execute(
            text("""
                INSERT INTO performance_reviews_enhanced (
                    review_id, reviewee_id, reviewer_id, review_period_start, review_period_end,
                    review_cycle, status, overall_score, technical_skills, communication,
                    leadership, collaboration, innovation, reliability, problem_solving,
                    achievements, strengths, improvement_areas, goals_next_period,
                    additional_comments, salary_recommendation, promotion_recommendation,
                    development_plan, is_legendary, swiss_precision_score,
                    swiss_precision_notes, code_bro_energy_notes, ai_insights, created_at
                ) VALUES (
                    :review_id, :reviewee_id, :reviewer_id, :review_period_start, :review_period_end,
                    :review_cycle, 'in_progress', :overall_score, :technical_skills, :communication,
                    :leadership, :collaboration, :innovation, :reliability, :problem_solving,
                    :achievements, :strengths, :improvement_areas, :goals_next_period,
                    :additional_comments, :salary_recommendation, :promotion_recommendation,
                    :development_plan, :is_legendary, :swiss_precision_score,
                    :swiss_precision_notes, :code_bro_energy_notes, :ai_insights, :created_at
                )
            """),
            {
                "review_id": review_id,
                "reviewee_id": review_data.reviewee_id,
                "reviewer_id": reviewer_id,
                "review_period_start": review_data.review_period_start,
                "review_period_end": review_data.review_period_end,
                "review_cycle": review_data.review_cycle.value,
                "overall_score": scores_dict["overall_performance"],
                "technical_skills": scores_dict["technical_skills"],
                "communication": scores_dict["communication"],
                "leadership": scores_dict["leadership"],
                "collaboration": scores_dict["collaboration"],
                "innovation": scores_dict["innovation"],
                "reliability": scores_dict["reliability"],
                "problem_solving": scores_dict["problem_solving"],
                "achievements": review_data.achievements,
                "strengths": review_data.strengths,
                "improvement_areas": review_data.improvement_areas,
                "goals_next_period": review_data.goals_next_period,
                "additional_comments": review_data.additional_comments,
                "salary_recommendation": review_data.salary_recommendation,
                "promotion_recommendation": review_data.promotion_recommendation,
                "development_plan": review_data.development_plan,
                "is_legendary": review_data.is_legendary_review or reviewee_data.get("is_legendary", False),
                "swiss_precision_score": swiss_precision_score,
                "swiss_precision_notes": review_data.swiss_precision_notes,
                "code_bro_energy_notes": review_data.code_bro_energy_notes,
                "ai_insights": json.dumps(ai_insights),
                "created_at": datetime.now(timezone.utc)
            }
        )
        
        # Update legendary metrics if applicable
        if reviewee_data.get("is_legendary") or review_data.is_legendary_review:
            await update_legendary_metrics(review_data.reviewee_id, swiss_precision_score, scores_dict, db)
        
        db.commit()
        
        logger.info(f"📝 Performance review created: {review_id} for {reviewee_data['username']} by {reviewer_username}")
        
        # Return created review
        return await get_performance_review(review_id, current_user, db)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error creating performance review: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create performance review"
        )

@router.get("/reviews/{review_id}", response_model=PerformanceReviewResponse, summary="📋 Get Performance Review")
async def get_performance_review(
    review_id: str = Path(..., description="Review ID"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get performance review with Swiss precision details
    """
    try:
        current_user_id = current_user.get("user_id")
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Get review with user details
        result = db.execute(
            text("""
                SELECT pr.*, 
                       reviewee.username as reviewee_username,
                       reviewee.first_name as reviewee_first_name,
                       reviewee.last_name as reviewee_last_name,
                       reviewer.username as reviewer_username,
                       reviewer.first_name as reviewer_first_name,
                       reviewer.last_name as reviewer_last_name,
                       approver.username as approver_username,
                       COALESCE(lm.code_bro_rating, 5) as code_bro_rating
                FROM performance_reviews_enhanced pr
                JOIN users reviewee ON pr.reviewee_id = reviewee.user_id
                JOIN users reviewer ON pr.reviewer_id = reviewer.user_id
                LEFT JOIN users approver ON pr.approved_by = approver.user_id
                LEFT JOIN legendary_metrics lm ON pr.reviewee_id = lm.user_id
                WHERE pr.review_id = :review_id
            """),
            {"review_id": review_id}
        ).fetchone()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Performance review not found"
            )
        
        review_data = dict(result._mapping)
        
        # Check access permissions
        if (str(current_user_id) not in [str(review_data["reviewee_id"]), str(review_data["reviewer_id"])] and
            current_role not in ["hr_manager", "admin", "founder"] and
            current_username != "rickroll187"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges to view this review"
            )
        
        # Parse AI insights
        ai_insights = None
        if review_data.get("ai_insights"):
            try:
                ai_insights = json.loads(review_data["ai_insights"])
            except json.JSONDecodeError:
                ai_insights = {"error": "Failed to parse AI insights"}
        
        # Build response
        response = PerformanceReviewResponse(
            review_id=review_data["review_id"],
            reviewee_id=str(review_data["reviewee_id"]),
            reviewer_id=str(review_data["reviewer_id"]),
            reviewee_name=f"{review_data['reviewee_first_name']} {review_data['reviewee_last_name']}",
            reviewer_name=f"{review_data['reviewer_first_name']} {review_data['reviewer_last_name']}",
            review_period_start=review_data["review_period_start"],
            review_period_end=review_data["review_period_end"],
            review_cycle=review_data["review_cycle"],
            status=review_data["status"],
            scores={
                "overall_performance": review_data["overall_score"],
                "technical_skills": review_data["technical_skills"],
                "communication": review_data["communication"],
                "leadership": review_data["leadership"],
                "collaboration": review_data["collaboration"],
                "innovation": review_data["innovation"],
                "reliability": review_data["reliability"],
                "problem_solving": review_data["problem_solving"]
            },
            achievements=review_data["achievements"],
            strengths=review_data["strengths"],
            improvement_areas=review_data["improvement_areas"],
            goals_next_period=review_data["goals_next_period"],
            additional_comments=review_data.get("additional_comments"),
            salary_recommendation=review_data.get("salary_recommendation"),
            promotion_recommendation=review_data.get("promotion_recommendation"),
            development_plan=review_data.get("development_plan"),
            created_at=review_data["created_at"],
            updated_at=review_data.get("updated_at"),
            approved_at=review_data.get("approved_at"),
            approved_by=review_data.get("approver_username"),
            is_legendary_review=review_data.get("is_legendary", False),
            swiss_precision_score=review_data.get("swiss_precision_score"),
            code_bro_rating=review_data.get("code_bro_rating"),
            ai_insights=ai_insights
        )
        
        logger.info(f"📋 Performance review retrieved: {review_id} by {current_username}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error getting performance review: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve performance review"
        )

@router.get("/reviews", summary="📊 List Performance Reviews")
async def list_performance_reviews(
    reviewee_id: Optional[str] = Query(None, description="Filter by reviewee"),
    reviewer_id: Optional[str] = Query(None, description="Filter by reviewer"),
    status: Optional[ReviewStatus] = Query(None, description="Filter by status"),
    review_cycle: Optional[ReviewCycle] = Query(None, description="Filter by review cycle"),
    start_date: Optional[datetime] = Query(None, description="Filter by period start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by period end date"),
    is_legendary: Optional[bool] = Query(None, description="Filter by legendary status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    List performance reviews with filtering and pagination
    """
    try:
        current_user_id = current_user.get("user_id")
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Build base query
        base_query = """
            FROM performance_reviews_enhanced pr
            JOIN users reviewee ON pr.reviewee_id = reviewee.user_id
            JOIN users reviewer ON pr.reviewer_id = reviewer.user_id
            LEFT JOIN legendary_metrics lm ON pr.reviewee_id = lm.user_id
            WHERE 1=1
        """
        
        query_params = {}
        
        # Access control - limit based on role
        if current_role not in ["hr_manager", "admin", "founder"] and current_username != "rickroll187":
            # Regular users and managers can only see their own reviews or reviews they conducted
            base_query += " AND (pr.reviewee_id = :current_user_id OR pr.reviewer_id = :current_user_id"
            query_params["current_user_id"] = current_user_id
            
            # Managers can also see their direct reports' reviews
            if current_role == "manager":
                base_query += " OR reviewee.manager_id = :current_user_id"
            
            base_query += ")"
        
        # Apply filters
        if reviewee_id:
            base_query += " AND pr.reviewee_id = :reviewee_id"
            query_params["reviewee_id"] = reviewee_id
        
        if reviewer_id:
            base_query += " AND pr.reviewer_id = :reviewer_id"
            query_params["reviewer_id"] = reviewer_id
        
        if status:
            base_query += " AND pr.status = :status"
            query_params["status"] = status.value
        
        if review_cycle:
            base_query += " AND pr.review_cycle = :review_cycle"
            query_params["review_cycle"] = review_cycle.value
        
        if start_date:
            base_query += " AND pr.review_period_start >= :start_date"
            query_params["start_date"] = start_date
        
        if end_date:
            base_query += " AND pr.review_period_end <= :end_date"
            query_params["end_date"] = end_date
        
        if is_legendary is not None:
            base_query += " AND pr.is_legendary = :is_legendary"
            query_params["is_legendary"] = is_legendary
        
        # Get total count
        count_query = f"SELECT COUNT(*) {base_query}"
        total_count = db.execute(text(count_query), query_params).scalar()
        
        # Calculate pagination
        total_pages = (total_count + page_size - 1) // page_size
        offset = (page - 1) * page_size
        
        # Get reviews with pagination
        reviews_query = f"""
            SELECT pr.review_id, pr.reviewee_id, pr.reviewer_id, pr.review_period_start,
                   pr.review_period_end, pr.review_cycle, pr.status, pr.overall_score,
                   pr.is_legendary, pr.swiss_precision_score, pr.created_at, pr.updated_at,
                   reviewee.username as reviewee_username,
                   reviewee.first_name as reviewee_first_name,
                   reviewee.last_name as reviewee_last_name,
                   reviewer.username as reviewer_username,
                   reviewer.first_name as reviewer_first_name,
                   reviewer.last_name as reviewer_last_name,
                   COALESCE(lm.code_bro_rating, 5) as code_bro_rating
            {base_query}
            ORDER BY pr.created_at DESC
            LIMIT :limit OFFSET :offset
        """
        
        query_params.update({
            "limit": page_size,
            "offset": offset
        })
        
        reviews_result = db.execute(text(reviews_query), query_params).fetchall()
        
        # Build response
        reviews = []
        for review in reviews_result:
            review_dict = dict(review._mapping)
            reviews.append({
                "review_id": review_dict["review_id"],
                "reviewee_id": str(review_dict["reviewee_id"]),
                "reviewer_id": str(review_dict["reviewer_id"]),
                "reviewee_name": f"{review_dict['reviewee_first_name']} {review_dict['reviewee_last_name']}",
                "reviewer_name": f"{review_dict['reviewer_first_name']} {review_dict['reviewer_last_name']}",
                "review_period_start": review_dict["review_period_start"].isoformat(),
                "review_period_end": review_dict["review_period_end"].isoformat(),
                "review_cycle": review_dict["review_cycle"],
                "status": review_dict["status"],
                "overall_score": review_dict["overall_score"],
                "is_legendary": review_dict.get("is_legendary", False),
                "swiss_precision_score": review_dict.get("swiss_precision_score"),
                "code_bro_rating": review_dict.get("code_bro_rating"),
                "created_at": review_dict["created_at"].isoformat(),
                "updated_at": review_dict["updated_at"].isoformat() if review_dict.get("updated_at") else None
            })
        
        response = {
            "reviews": reviews,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1
            }
        }
        
        logger.info(f"📊 Performance reviews listed by: {current_username} - Page {page}/{total_pages}")
        
        return response
        
    except Exception as e:
        logger.error(f"🚨 Error listing performance reviews: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list performance reviews"
        )

# =====================================
# 🔄 360-DEGREE FEEDBACK SYSTEM 🔄
# =====================================

@router.post("/feedback", response_model=PerformanceFeedbackResponse, summary="💬 Submit 360 Feedback")
async def submit_performance_feedback(
    feedback_data: PerformanceFeedbackRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Submit 360-degree performance feedback with legendary recognition
    """
    try:
        from_user_id = current_user.get("user_id")
        from_username = current_user.get("username")
        
        # Validate to_user exists
        to_user = db.execute(
            text("SELECT username, first_name, last_name FROM users WHERE user_id = :user_id"),
            {"user_id": feedback_data.to_user_id}
        ).fetchone()
        
        if not to_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target user not found"
            )
        
        to_user_data = dict(to_user._mapping)
        
        # Check if feedback already exists from this user in the last 30 days
        existing_feedback = db.execute(
            text("""
                SELECT feedback_id FROM performance_feedback 
                WHERE from_user_id = :from_user_id 
                  AND to_user_id = :to_user_id 
                  AND created_at >= NOW() - INTERVAL '30 days'
            """),
            {
                "from_user_id": from_user_id,
                "to_user_id": feedback_data.to_user_id
            }
        ).fetchone()
        
        if existing_feedback:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Feedback already submitted for this user in the last 30 days"
            )
        
        # Generate feedback ID
        feedback_id = str(uuid.uuid4())
        
        # Create feedback record
        db.execute(
            text("""
                INSERT INTO performance_feedback (
                    feedback_id, from_user_id, to_user_id, feedback_type, rating,
                    feedback_text, strengths, improvement_suggestions, anonymous,
                    legendary_recognition, created_at
                ) VALUES (
                    :feedback_id, :from_user_id, :to_user_id, :feedback_type, :rating,
                    :feedback_text, :strengths, :improvement_suggestions, :anonymous,
                    :legendary_recognition, :created_at
                )
            """),
            {
                "feedback_id": feedback_id,
                "from_user_id": from_user_id if not feedback_data.anonymous else None,
                "to_user_id": feedback_data.to_user_id,
                "feedback_type": feedback_data.feedback_type,
                "rating": feedback_data.rating,
                "feedback_text": feedback_data.feedback_text,
                "strengths": feedback_data.strengths,
                "improvement_suggestions": feedback_data.improvement_suggestions,
                "anonymous": feedback_data.anonymous,
                "legendary_recognition": feedback_data.legendary_recognition,
                "created_at": datetime.now(timezone.utc)
            }
        )
        
        db.commit()
        
        # Build response
        response = PerformanceFeedbackResponse(
            feedback_id=feedback_id,
            from_user_id=str(from_user_id) if not feedback_data.anonymous else None,
            to_user_id=feedback_data.to_user_id,
            from_user_name=f"{current_user.get('first_name')} {current_user.get('last_name')}" if not feedback_data.anonymous else None,
            to_user_name=f"{to_user_data['first_name']} {to_user_data['last_name']}",
            feedback_type=feedback_data.feedback_type,
            rating=feedback_data.rating,
            feedback_text=feedback_data.feedback_text,
            strengths=feedback_data.strengths,
            improvement_suggestions=feedback_data.improvement_suggestions,
            anonymous=feedback_data.anonymous,
            legendary_recognition=feedback_data.legendary_recognition,
            created_at=datetime.now(timezone.utc)
        )
        
        logger.info(f"💬 360 feedback submitted by {from_username} for {to_user_data['username']}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error submitting performance feedback: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit performance feedback"
        )

# =====================================
# 📈 PERFORMANCE ANALYTICS 📈
# =====================================

@router.get("/analytics/{user_id}", response_model=PerformanceAnalyticsResponse, summary="📈 Performance Analytics")
async def get_performance_analytics(
    user_id: str = Path(..., description="User ID for analytics"),
    period_start: Optional[datetime] = Query(None, description="Analysis period start"),
    period_end: Optional[datetime] = Query(None, description="Analysis period end"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get comprehensive performance analytics with Swiss precision insights
    """
    try:
        current_user_id = current_user.get("user_id")
        current_role = current_user.get("role")
        current_username = current_user.get("username")
        
        # Set default period if not provided
        if not period_end:
            period_end = datetime.now(timezone.utc)
        if not period_start:
            period_start = period_end - timedelta(days=365)  # Last year
        
        # Check access permissions
        if (str(current_user_id) != user_id and
            current_role not in ["hr_manager", "admin", "founder"] and
            current_username != "rickroll187"):
            # Managers can view their direct reports
            if current_role == "manager":
                direct_report = db.execute(
                    text("SELECT user_id FROM users WHERE user_id = :user_id AND manager_id = :manager_id"),
                    {"user_id": user_id, "manager_id": current_user_id}
                ).fetchone()
                
                if not direct_report:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient privileges to view analytics for this user"
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient privileges to view analytics for this user"
                )
        
        # Get user info
        user_info = db.execute(
            text("""
                SELECT username, first_name, last_name, role, department, is_legendary
                FROM users WHERE user_id = :user_id
            """),
            {"user_id": user_id}
        ).fetchone()
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_data = dict(user_info._mapping)
        
        # Get performance reviews in period
        reviews = db.execute(
            text("""
                SELECT * FROM performance_reviews_enhanced
                WHERE reviewee_id = :user_id
                  AND review_period_start >= :period_start
                  AND review_period_end <= :period_end
                  AND status = 'completed'
                ORDER BY review_period_start
            """),
            {
                "user_id": user_id,
                "period_start": period_start,
                "period_end": period_end
            }
        ).fetchall()
        
        if not reviews:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No completed reviews found in the specified period"
            )
        
        # Calculate average scores
        score_fields = [
            "overall_score", "technical_skills", "communication", "leadership",
            "collaboration", "innovation", "reliability", "problem_solving"
        ]
        
        average_scores = {}
        score_trends = {}
        
        for field in score_fields:
            scores = [getattr(review, field) for review in reviews if getattr(review, field) is not None]
            if scores:
                average_scores[field] = round(statistics.mean(scores), 2)
                score_trends[field] = scores
            else:
                average_scores[field] = 0.0
                score_trends[field] = []
        
        # Determine performance grade
        overall_avg = average_scores.get("overall_score", 0.0)
        if overall_avg >= SWISS_PRECISION_THRESHOLDS["excellent"]:
            performance_grade = "A+ (Excellent)"
        elif overall_avg >= SWISS_PRECISION_THRESHOLDS["good"]:
            performance_grade = "A (Good)"
        elif overall_avg >= SWISS_PRECISION_THRESHOLDS["satisfactory"]:
            performance_grade = "B (Satisfactory)"
        elif overall_avg >= SWISS_PRECISION_THRESHOLDS["needs_improvement"]:
            performance_grade = "C (Needs Improvement)"
        else:
            performance_grade = "D (Unsatisfactory)"
        
        # Get comparative analytics
        department_comparison = None
        role_comparison = None
        company_percentile = None
        
        if user_data.get("department"):
            dept_avg = db.execute(
                text("""
                    SELECT AVG(pr.overall_score) as avg_score
                    FROM performance_reviews_enhanced pr
                    JOIN users u ON pr.reviewee_id = u.user_id
                    WHERE u.department = :department
                      AND pr.review_period_start >= :period_start
                      AND pr.review_period_end <= :period_end
                      AND pr.status = 'completed'
                """),
                {
                    "department": user_data["department"],
                    "period_start": period_start,
                    "period_end": period_end
                }
            ).scalar()
            
            if dept_avg:
                department_comparison = {
                    "department": user_data["department"],
                    "user_average": overall_avg,
                    "department_average": round(float(dept_avg), 2),
                    "difference": round(overall_avg - float(dept_avg), 2)
                }
        
        if user_data.get("role"):
            role_avg = db.execute(
                text("""
                    SELECT AVG(pr.overall_score) as avg_score
                    FROM performance_reviews_enhanced pr
                    JOIN users u ON pr.reviewee_id = u.user_id
                    WHERE u.role = :role
                      AND pr.review_period_start >= :period_start
                      AND pr.review_period_end <= :period_end
                      AND pr.status = 'completed'
                """),
                {
                    "role": user_data["role"],
                    "period_start": period_start,
                    "period_end": period_end
                }
            ).scalar()
            
            if role_avg:
                role_comparison = {
                    "role": user_data["role"],
                    "user_average": overall_avg,
                    "role_average": round(float(role_avg), 2),
                    "difference": round(overall_avg - float(role_avg), 2)
                }
        
        # Calculate company percentile
        all_scores = db.execute(
            text("""
                SELECT pr.overall_score
                FROM performance_reviews_enhanced pr
                WHERE pr.review_period_start >= :period_start
                  AND pr.review_period_end <= :period_end
                  AND pr.status = 'completed'
                  AND pr.overall_score IS NOT NULL
            """),
            {
                "period_start": period_start,
                "period_end": period_end
            }
        ).fetchall()
        
        if all_scores:
            all_scores_list = [score[0] for score in all_scores]
            scores_below = len([s for s in all_scores_list if s < overall_avg])
            company_percentile = round((scores_below / len(all_scores_list)) * 100, 1)
        
        # Get legendary metrics
        legendary_metrics = db.execute(
            text("SELECT * FROM legendary_metrics WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).fetchone()
        
        swiss_precision_score = None
        code_bro_energy_level = "standard"
        
        if legendary_metrics:
            legendary_data = dict(legendary_metrics._mapping)
            swiss_precision_score = legendary_data.get("swiss_precision_score")
            code_bro_energy_level = legendary_data.get("code_bro_energy_level", "standard")
        
        # Get legendary achievements
        achievements_count = db.execute(
            text("SELECT COUNT(*) FROM legendary_achievements WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).scalar() or 0
        
        # Generate AI insights
        ai_insights = generate_analytics_ai_insights(average_scores, score_trends, user_data, reviews)
        
        # Generate recommendations
        recommendations = generate_performance_recommendations(average_scores, user_data, ai_insights)
        
        # Build response
        response = PerformanceAnalyticsResponse(
            user_id=user_id,
            period_start=period_start,
            period_end=period_end,
            average_scores=average_scores,
            score_trends=score_trends,
            performance_grade=performance_grade,
            department_comparison=department_comparison,
            role_comparison=role_comparison,
            company_percentile=company_percentile,
            swiss_precision_score=swiss_precision_score,
            code_bro_energy_level=code_bro_energy_level,
            legendary_achievements=achievements_count,
            ai_insights=ai_insights,
            recommendations=recommendations
        )
        
        logger.info(f"📈 Performance analytics generated for {user_data['username']} by {current_username}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error generating performance analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate performance analytics"
        )

# =====================================
# 🎸 LEGENDARY PERFORMANCE FUNCTIONS 🎸
# =====================================

def calculate_swiss_precision_score(scores: Dict[str, float], is_legendary: bool = False) -> float:
    """
    Calculate Swiss precision score with legendary adjustments
    """
    try:
        # Base score calculation
        weights = {
            "overall_performance": 0.25,
            "technical_skills": 0.15,
            "communication": 0.15,
            "leadership": 0.15,
            "collaboration": 0.15,
            "innovation": 0.10,
            "reliability": 0.15,
            "problem_solving": 0.10
        }
        
        weighted_score = sum(scores.get(metric, 0) * weight for metric, weight in weights.items())
        
        # Convert to 100-point scale
        swiss_precision_score = (weighted_score / 5.0) * 100
        
        # Apply legendary multiplier
        if is_legendary:
            swiss_precision_score *= LEGENDARY_PERFORMANCE_MULTIPLIER
        
        # Cap at 100
        return min(swiss_precision_score, 100.0)
        
    except Exception as e:
        logger.error(f"🚨 Error calculating Swiss precision score: {str(e)}")
        return 0.0

def generate_ai_performance_insights(
    scores: Dict[str, float], 
    review_data: Dict[str, Any], 
    user_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate AI-driven performance insights with Swiss precision
    """
    try:
        insights = {
            "overall_assessment": "",
            "key_strengths": [],
            "improvement_areas": [],
            "career_recommendations": [],
            "swiss_precision_analysis": {},
            "code_bro_energy_assessment": "",
            "legendary_potential": False
        }
        
        # Overall assessment
        overall_score = scores.get("overall_performance", 0)
        if overall_score >= 4.5:
            insights["overall_assessment"] = "🏆 Exceptional performance with Swiss precision execution"
        elif overall_score >= 4.0:
            insights["overall_assessment"] = "⭐ Strong performance with room for legendary growth"
        elif overall_score >= 3.5:
            insights["overall_assessment"] = "✅ Solid performance meeting expectations"
        elif overall_score >= 3.0:
            insights["overall_assessment"] = "⚠️ Performance needs focused improvement"
        else:
            insights["overall_assessment"] = "🚨 Performance requires immediate attention"
        
        # Identify strengths (scores >= 4.0)
        for metric, score in scores.items():
            if score >= 4.0:
                metric_name = metric.replace("_", " ").title()
                insights["key_strengths"].append(f"{metric_name}: {score}/5.0")
        
        # Identify improvement areas (scores < 3.5)
        for metric, score in scores.items():
            if score < 3.5:
                metric_name = metric.replace("_", " ").title()
                insights["improvement_areas"].append(f"{metric_name}: {score}/5.0")
        
        # Career recommendations
        if scores.get("leadership", 0) >= 4.0 and scores.get("technical_skills", 0) >= 4.0:
            insights["career_recommendations"].append("Consider technical leadership roles")
        
        if scores.get("communication", 0) >= 4.5:
            insights["career_recommendations"].append("Excellent candidate for client-facing roles")
        
        if scores.get("innovation", 0) >= 4.0:
            insights["career_recommendations"].append("Consider R&D or innovation projects")
        
        # Swiss precision analysis
        consistency_score = min(scores.values()) / max(scores.values()) if max(scores.values()) > 0 else 1.0
        insights["swiss_precision_analysis"] = {
            "consistency_score": round(consistency_score, 2),
            "precision_rating": "High" if consistency_score >= 0.8 else "Medium" if consistency_score >= 0.6 else "Low",
            "quality_metrics": {
                "attention_to_detail": scores.get("reliability", 0),
                "execution_excellence": scores.get("technical_skills", 0),
                "process_adherence": (scores.get("reliability", 0) + scores.get("problem_solving", 0)) / 2
            }
        }
        
        # Code bro energy assessment
        collaboration_score = scores.get("collaboration", 0)
        communication_score = scores.get("communication", 0)
        team_energy = (collaboration_score + communication_score) / 2
        
        if team_energy >= 4.5:
            insights["code_bro_energy_assessment"] = "🎸 Infinite code bro energy - ultimate team player!"
        elif team_energy >= 4.0:
            insights["code_bro_energy_assessment"] = "⚡ High code bro energy - great team collaboration"
        elif team_energy >= 3.5:
            insights["code_bro_energy_assessment"] = "💪 Good code bro energy - solid team member"
        else:
            insights["code_bro_energy_assessment"] = "📈 Code bro energy needs enhancement - focus on teamwork"
        
        # Legendary potential
        avg_score = sum(scores.values()) / len(scores) if scores else 0
        insights["legendary_potential"] = (
            avg_score >= 4.2 and 
            scores.get("innovation", 0) >= 4.0 and 
            scores.get("collaboration", 0) >= 4.0
        )
        
        return insights
        
    except Exception as e:
        logger.error(f"🚨 Error generating AI insights: {str(e)}")
        return {"error": "Failed to generate AI insights"}

def generate_analytics_ai_insights(
    average_scores: Dict[str, float],
    score_trends: Dict[str, List[float]],
    user_data: Dict[str, Any],
    reviews: List[Any]
) -> Dict[str, Any]:
    """
    Generate AI insights for performance analytics
    """
    try:
        insights = {
            "trend_analysis": {},
            "performance_trajectory": "",
            "strengths_over_time": [],
            "areas_of_growth": [],
            "swiss_precision_evolution": {},
            "legendary_readiness": False
        }
        
        # Trend analysis
        for metric, scores in score_trends.items():
            if len(scores) >= 2:
                trend = "improving" if scores[-1] > scores[0] else "declining" if scores[-1] < scores[0] else "stable"
                change = scores[-1] - scores[0]
                insights["trend_analysis"][metric] = {
                    "trend": trend,
                    "change": round(change, 2),
                    "consistency": round(statistics.stdev(scores) if len(scores) > 1 else 0, 2)
                }
        
        # Performance trajectory
        overall_trend = insights["trend_analysis"].get("overall_score", {}).get("trend", "stable")
        if overall_trend == "improving":
            insights["performance_trajectory"] = "📈 Upward trajectory - consistent improvement over time"
        elif overall_trend == "declining":
            insights["performance_trajectory"] = "📉 Downward trend - requires attention and support"
        else:
            insights["performance_trajectory"] = "📊 Stable performance - maintaining consistent level"
        
        # Swiss precision evolution
        if len(reviews) >= 2:
            latest_swiss_score = getattr(reviews[-1], "swiss_precision_score", 0) or 0
            earliest_swiss_score = getattr(reviews[0], "swiss_precision_score", 0) or 0
            swiss_improvement = latest_swiss_score - earliest_swiss_score
            
            insights["swiss_precision_evolution"] = {
                "improvement": round(swiss_improvement, 2),
                "current_level": "Maximum" if latest_swiss_score >= 90 else "High" if latest_swiss_score >= 80 else "Standard",
                "trajectory": "Ascending" if swiss_improvement > 5 else "Stable" if abs(swiss_improvement) <= 5 else "Needs Focus"
            }
        
        # Legendary readiness assessment
        avg_overall = average_scores.get("overall_score", 0)
        avg_innovation = average_scores.get("innovation", 0)
        avg_collaboration = average_scores.get("collaboration", 0)
        
        insights["legendary_readiness"] = (
            avg_overall >= 4.3 and
            avg_innovation >= 4.0 and
            avg_collaboration >= 4.0 and
            len([t for t in insights["trend_analysis"].values() if t.get("trend") == "improving"]) >= 3
        )
        
        return insights
        
    except Exception as e:
        logger.error(f"🚨 Error generating analytics AI insights: {str(e)}")
        return {"error": "Failed to generate analytics insights"}

def generate_performance_recommendations(
    average_scores: Dict[str, float],
    user_data: Dict[str, Any],
    ai_insights: Dict[str, Any]
) -> List[str]:
    """
    Generate personalized performance recommendations
    """
    try:
        recommendations = []
        
        # Score-based recommendations
        if average_scores.get("technical_skills", 0) < 3.5:
            recommendations.append("📚 Focus on technical skill development through training and certification")
        
        if average_scores.get("communication", 0) < 3.5:
            recommendations.append("💬 Improve communication skills through workshops and practice")
        
        if average_scores.get("leadership", 0) < 3.5:
            recommendations.append("👨‍💼 Develop leadership capabilities through mentoring and leadership programs")
        
        if average_scores.get("innovation", 0) < 3.5:
            recommendations.append("💡 Enhance innovation through creative thinking workshops and cross-functional projects")
        
        # Strength-based recommendations
        if average_scores.get("technical_skills", 0) >= 4.5:
            recommendations.append("🎯 Consider technical mentoring roles to share expertise with team members")
        
        if average_scores.get("leadership", 0) >= 4.5:
            recommendations.append("👑 Excellent leadership potential - consider management track opportunities")
        
        # Swiss precision recommendations
        swiss_analysis = ai_insights.get("swiss_precision_analysis", {})
        if swiss_analysis.get("consistency_score", 0) < 0.7:
            recommendations.append("⚙️ Focus on consistency across all performance areas for Swiss precision excellence")
        
        # Code bro energy recommendations
        if average_scores.get("collaboration", 0) >= 4.5:
            recommendations.append("🎸 Maximum code bro energy - consider team lead or culture ambassador roles")
        elif average_scores.get("collaboration", 0) < 3.5:
            recommendations.append("🤝 Enhance team collaboration and code bro energy through team building activities")
        
        # Legendary potential recommendations
        if ai_insights.get("legendary_potential", False):
            recommendations.append("🏆 Demonstrates legendary potential - recommend for advanced leadership opportunities")
        
        # Role-specific recommendations
        if user_data.get("role") == "employee" and average_scores.get("overall_performance", 0) >= 4.0:
            recommendations.append("📈 Strong performance indicates readiness for increased responsibilities")
        
        return recommendations
        
    except Exception as e:
        logger.error(f"🚨 Error generating recommendations: {str(e)}")
        return ["Unable to generate recommendations at this time"]

async def update_legendary_metrics(
    user_id: str,
    swiss_precision_score: float,
    scores: Dict[str, float],
    db: Session
):
    """
    Update legendary metrics for legendary users
    """
    try:
        # Calculate code bro rating
        collaboration_score = scores.get("collaboration", 0)
        communication_score = scores.get("communication", 0)
        code_bro_rating = min(10, int((collaboration_score + communication_score) / 2 * 2))
        
        # Update or insert legendary metrics
        db.execute(
            text("""
                INSERT INTO legendary_metrics (
                    user_id, swiss_precision_score, code_bro_rating, updated_at
                ) VALUES (
                    :user_id, :swiss_precision_score, :code_bro_rating, :updated_at
                ) ON CONFLICT (user_id) DO UPDATE SET
                    swiss_precision_score = :swiss_precision_score,
                    code_bro_rating = :code_bro_rating,
                    updated_at = :updated_at
            """),
            {
                "user_id": user_id,
                "swiss_precision_score": swiss_precision_score,
                "code_bro_rating": code_bro_rating,
                "updated_at": datetime.now(timezone.utc)
            }
        )
        
        logger.info(f"🎸 Legendary metrics updated for user: {user_id}")
        
    except Exception as e:
        logger.error(f"🚨 Error updating legendary metrics: {str(e)}")

# =====================================
# 🎸 LEGENDARY EXPORTS 🎸
# =====================================

__all__ = ["router"]

# =====================================
# 🎸 LEGENDARY COMPLETION MESSAGE 🎸
# =====================================

if __name__ == "__main__":
    print("🎸🎸🎸 LEGENDARY PERFORMANCE MANAGEMENT SYSTEM LOADED! 🎸🎸🎸")
    print("Built with Swiss precision by RICKROLL187!")
    print("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    print(f"Performance management system loaded at: 2025-08-05 22:26:18 UTC")
    print("📊 AI-driven performance reviews: ACTIVE")
    print("🎸 Swiss precision scoring: MAXIMUM")
    print("💬 360-degree feedback system: ENABLED")
    print("📈 Advanced performance analytics: OPERATIONAL")
    print("⚡ Code bro energy assessment: INFINITE")
    print("🏆 Legendary potential detection: ACTIVATED")
    print("🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸")
