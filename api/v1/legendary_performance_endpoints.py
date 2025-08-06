"""
📊🎸 N3EXTPATH - LEGENDARY PERFORMANCE REVIEW API ENDPOINTS 🎸📊
More evaluative than Swiss precision with legendary performance API mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Next order API time: 2025-08-05 13:02:30 UTC
Built by legendary next order RICKROLL187 🎸📱
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from core.response_middleware import legendary_response_middleware
from core.auth import get_current_user
from users.models.user_models import LegendaryUser
from core.legendary_performance_review_system import (
    legendary_performance_review_system, 
    create_legendary_review, 
    submit_legendary_self_assessment,
    submit_legendary_manager_review
)

# Create legendary performance review router
legendary_performance_router = APIRouter(
    prefix="/api/v1/performance",
    tags=["📊 Legendary Performance Reviews"]
)

@legendary_performance_router.post("/reviews/create")
async def create_performance_review(
    review_data: Dict[str, Any],
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    📊 CREATE LEGENDARY PERFORMANCE REVIEW! 📊
    More thorough than Swiss evaluations with next order review creation! 🎸📊
    """
    # Check permissions - only managers and above can create reviews
    if current_user.role not in ['manager', 'admin', 'hr', 'rickroll187']:
        raise HTTPException(
            status_code=403,
            detail="Manager level access required to create performance reviews!"
        )
    
    # Add manager context
    review_data["manager_id"] = current_user.user_id
    review_data["manager_name"] = current_user.full_name or current_user.username
    
    # Create the review
    result = await create_legendary_review(review_data)
    
    processing_time = 0.456  # Performance review creation processing time
    return legendary_response_middleware.add_legendary_polish(
        result, request, processing_time
    )

@legendary_performance_router.get("/reviews")
async def get_performance_reviews(
    request: Request,
    status: Optional[str] = None,
    employee_id: Optional[str] = None,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    📋 GET PERFORMANCE REVIEWS! 📋
    More organized than Swiss documentation with next order review listing! 🎸📋
    """
    # Filter reviews based on user role and permissions
    all_reviews = list(legendary_performance_review_system.performance_reviews.values())
    user_reviews = []
    
    for review in all_reviews:
        # Users can see their own reviews
        if review.employee_id == current_user.user_id:
            user_reviews.append(review)
        # Managers can see their team's reviews
        elif review.manager_id == current_user.user_id:
            user_reviews.append(review)
        # HR and admins can see all reviews
        elif current_user.role in ['admin', 'hr', 'rickroll187']:
            user_reviews.append(review)
    
    # Apply filters
    if status:
        user_reviews = [r for r in user_reviews if r.status.value == status]
    
    if employee_id:
        user_reviews = [r for r in user_reviews if r.employee_id == employee_id]
    
    reviews_data = {
        "reviews_count": len(user_reviews),
        "reviews": [
            {
                "review_id": review.review_id,
                "employee_id": review.employee_id,
                "employee_name": review.employee_name,
                "manager_name": review.manager_name,
                "review_type": review.review_type.value,
                "status": review.status.value,
                "review_period": f"{review.review_period_start.strftime('%Y-%m-%d')} to {review.review_period_end.strftime('%Y-%m-%d')}",
                "due_date": review.due_date.isoformat(),
                "completed_date": review.completed_date.isoformat() if review.completed_date else None,
                "final_rating": review.final_rating_overall,
                "final_rating_label": review.final_rating_normalized,
                "self_assessment_completed": review.self_assessment_completed,
                "peer_feedback_count": len(review.peer_feedback),
                "okr_reviews_count": len(review.okr_reviews),
                "promotion_recommended": review.promotion_recommended,
                "high_performer": review.high_performer,
                "legendary_factor": review.legendary_factor,
                "rickroll187_approved": review.rickroll187_approved
            }
            for review in user_reviews
        ],
        "status_filter": status,
        "employee_filter": employee_id,
        "retrieved_by": current_user.username,
        "retrieved_at": "2025-08-05 13:02:30 UTC",
        "retrieved_from": "RICKROLL187's Legendary Performance Review API 🎸📊"
    }
    
    processing_time = 0.234  # Reviews retrieval processing time
    return legendary_response_middleware.add_legendary_polish(
        reviews_data, request, processing_time
    )

@legendary_performance_router.get("/reviews/{review_id}")
async def get_performance_review_details(
    review_id: str,
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🔍 GET DETAILED PERFORMANCE REVIEW! 🔍
    More detailed than Swiss documentation with next order review details! 🎸📊
    """
    if review_id not in legendary_performance_review_system.performance_reviews:
        raise HTTPException(
            status_code=404,
            detail="Performance review not found in our legendary system!"
        )
    
    review = legendary_performance_review_system.performance_reviews[review_id]
    
    # Check permissions
    has_access = False
    if review.employee_id == current_user.user_id:  # Employee's own review
        has_access = True
    elif review.manager_id == current_user.user_id:  # Manager's review of their report
        has_access = True
    elif current_user.role in ['admin', 'hr', 'rickroll187']:  # Admin access
        has_access = True
    elif current_user.user_id in [pf.reviewer_id for pf in review.peer_feedback]:  # Peer reviewer
        has_access = True
    
    if not has_access:
        raise HTTPException(
            status_code=403,
            detail="Access denied to this legendary performance review!"
        )
    
    review_details = {
        "review_id": review.review_id,
        "employee_id": review.employee_id,
        "employee_name": review.employee_name,
        "manager_id": review.manager_id,
        "manager_name": review.manager_name,
        "review_type": review.review_type.value,
        "status": review.status.value,
        "review_period": {
            "start_date": review.review_period_start.isoformat(),
            "end_date": review.review_period_end.isoformat()
        },
        "due_date": review.due_date.isoformat(),
        "completed_date": review.completed_date.isoformat() if review.completed_date else None,
        
        # Self Assessment
        "self_assessment": {
            "completed": review.self_assessment_completed,
            "overall_rating": review.self_rating_overall,
            "comments": review.self_assessment_comments if has_access else "*** CONFIDENTIAL ***"
        },
        
        # Competency Ratings
        "competency_ratings": [
            {
                "competency": cr.competency.value,
                "rating": cr.rating,
                "weight": cr.weight,
                "comments": cr.comments if has_access else "*** CONFIDENTIAL ***",
                "examples": cr.examples if has_access else [],
                "improvement_areas": cr.improvement_areas if has_access else []
            }
            for cr in review.competency_ratings
        ],
        
        # OKR Reviews
        "okr_reviews": [
            {
                "objective_id": okr.objective_id,
                "objective_name": okr.objective_name,
                "completion_percentage": okr.completion_percentage,
                "quality_rating": okr.quality_rating,
                "impact_rating": okr.impact_rating,
                "learnings": okr.learnings,
                "challenges_overcome": okr.challenges_overcome,
                "manager_comments": okr.manager_comments if has_access else "*** CONFIDENTIAL ***"
            }
            for okr in review.okr_reviews
        ],
        
        # Peer Feedback (anonymized for employee)
        "peer_feedback": [
            {
                "feedback_id": pf.feedback_id,
                "reviewer_name": pf.reviewer_name if current_user.user_id != review.employee_id else "Anonymous Colleague",
                "relationship": pf.relationship,
                "collaboration_rating": pf.collaboration_rating,
                "communication_rating": pf.communication_rating,
                "reliability_rating": pf.reliability_rating,
                "strengths": pf.strengths,
                "improvement_areas": pf.improvement_areas,
                "overall_comments": pf.overall_comments,
                "submitted_at": pf.submitted_at.isoformat()
            }
            for pf in review.peer_feedback
        ],
        
        # Manager Assessment (visible based on permissions)
        "manager_assessment": {
            "overall_rating": review.manager_rating_overall,
            "comments": review.manager_comments if has_access else "*** CONFIDENTIAL ***",
            "strengths": review.manager_strengths if has_access else [],
            "improvement_areas": review.manager_improvement_areas if has_access else []
        } if current_user.user_id != review.employee_id or review.status.value == "completed" else None,
        
        # Final Results (only if completed)
        "final_results": {
            "overall_rating": review.final_rating_overall,
            "rating_label": review.final_rating_normalized,
            "promotion_recommended": review.promotion_recommended,
            "salary_increase_recommended": review.salary_increase_recommended,
            "high_performer": review.high_performer,
            "retention_risk": review.retention_risk,
            "pip_recommended": review.pip_recommended
        } if review.status.value == "completed" else None,
        
        # Development Plan
        "development_plan": {
            "development_goals": review.development_plan.development_goals,
            "skill_gaps": review.development_plan.skill_gaps,
            "training_recommendations": review.development_plan.training_recommendations,
            "stretch_assignments": review.development_plan.stretch_assignments,
            "mentoring_opportunities": review.development_plan.mentoring_opportunities,
            "timeline": review.development_plan.timeline,
            "success_metrics": review.development_plan.success_metrics
        } if review.development_plan else None,
        
        # Metadata
        "created_at": review.created_at.isoformat(),
        "updated_at": review.updated_at.isoformat(),
        "legendary_factor": review.legendary_factor,
        "rickroll187_approved": review.rickroll187_approved,
        "retrieved_by": current_user.username,
        "retrieved_at": "2025-08-05 13:02:30 UTC"
    }
    
    processing_time = 0.345  # Review details processing time
    return legendary_response_middleware.add_legendary_polish(
        review_details, request, processing_time
    )

@legendary_performance_router.post("/reviews/{review_id}/self-assessment")
async def submit_self_assessment(
    review_id: str,
    assessment_data: Dict[str, Any],
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🪞 SUBMIT SELF ASSESSMENT! 🪞
    More reflective than Swiss introspection with next order self-evaluation! 🎸🪞
    """
    if review_id not in legendary_performance_review_system.performance_reviews:
        raise HTTPException(
            status_code=404,
            detail="Performance review not found!"
        )
    
    review = legendary_performance_review_system.performance_reviews[review_id]
    
    # Check if user can submit self assessment
    if review.employee_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only submit self-assessment for your own review!"
        )
    
    if review.self_assessment_completed:
        raise HTTPException(
            status_code=400,
            detail="Self-assessment has already been completed!"
        )
    
    # Submit the self assessment
    result = await submit_legendary_self_assessment(review_id, assessment_data)
    
    processing_time = 0.278  # Self assessment processing time
    return legendary_response_middleware.add_legendary_polish(
        result, request, processing_time
    )

@legendary_performance_router.post("/reviews/{review_id}/manager-review")
async def submit_manager_review(
    review_id: str,
    manager_assessment: Dict[str, Any],
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    👨‍💼 SUBMIT MANAGER REVIEW! 👨‍💼
    More insightful than Swiss evaluation with next order manager assessment! 🎸👨‍💼
    """
    if review_id not in legendary_performance_review_system.performance_reviews:
        raise HTTPException(
            status_code=404,
            detail="Performance review not found!"
        )
    
    review = legendary_performance_review_system.performance_reviews[review_id]
    
    # Check if user can submit manager review
    if review.manager_id != current_user.user_id and current_user.role not in ['admin', 'rickroll187']:
        raise HTTPException(
            status_code=403,
            detail="You can only submit manager review for your direct reports!"
        )
    
    if review.status.value == "completed":
        raise HTTPException(
            status_code=400,
            detail="Manager review has already been completed!"
        )
    
    # Submit the manager review
    result = await submit_legendary_manager_review(review_id, manager_assessment)
    
    processing_time = 0.567  # Manager review processing time
    return legendary_response_middleware.add_legendary_polish(
        result, request, processing_time
    )

@legendary_performance_router.post("/reviews/{review_id}/peer-feedback")
async def add_peer_feedback(
    review_id: str,
    peer_feedback_data: Dict[str, Any],
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    🤝 ADD PEER FEEDBACK! 🤝
    More collaborative than Swiss teamwork with next order peer evaluation! 🎸🤝
    """
    if review_id not in legendary_performance_review_system.performance_reviews:
        raise HTTPException(
            status_code=404,
            detail="Performance review not found!"
        )
    
    review = legendary_performance_review_system.performance_reviews[review_id]
    
    # Add reviewer context
    peer_feedback_data["reviewer_id"] = current_user.user_id
    peer_feedback_data["reviewer_name"] = current_user.full_name or current_user.username
    
    # Check if user is reviewing themselves (not allowed)
    if review.employee_id == current_user.user_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot provide peer feedback for your own review!"
        )
    
    # Add the peer feedback
    result = await legendary_performance_review_system.add_peer_feedback(review_id, peer_feedback_data)
    
    processing_time = 0.189  # Peer feedback processing time
    return legendary_response_middleware.add_legendary_polish(
        result, request, processing_time
    )

@legendary_performance_router.get("/analytics/summary")
async def get_performance_analytics(
    request: Request,
    timeframe: Optional[str] = "quarter",
    department: Optional[str] = None,
    current_user: LegendaryUser = Depends(get_current_user)
):
    """
    📈 GET PERFORMANCE ANALYTICS! 📈
    More analytical than Swiss precision with next order performance insights! 🎸📈
    """
    # Check analytics access
    if current_user.role not in ['admin', 'hr', 'manager', 'rickroll187']:
        raise HTTPException(
            status_code=403,
            detail="Analytics access requires manager level or higher!"
        )
    
    # Get all completed reviews for analytics
    completed_reviews = [
        review for review in legendary_performance_review_system.performance_reviews.values()
        if review.status.value == "completed"
    ]
    
    # Filter by department if specified
    if department:
        # This would integrate with employee department data
        pass  # Simplified for demo
    
    analytics_summary = {
        "analytics_title": f"🏆 LEGENDARY PERFORMANCE ANALYTICS SUMMARY 🏆",
        "timeframe": timeframe,
        "department_filter": department,
        "generated_for": current_user.username,
        "generated_at": "2025-08-05 13:02:30 UTC",
        
        "review_metrics": {
            "total_reviews": len(completed_reviews),
            "average_rating": round(sum([r.final_rating_overall for r in completed_reviews if r.final_rating_overall]) / len(completed_reviews), 2) if completed_reviews else 0,
            "high_performers": len([r for r in completed_reviews if r.high_performer]),
            "promotion_recommendations": len([r for r in completed_reviews if r.promotion_recommended]),
            "salary_increase_recommendations": len([r for r in completed_reviews if r.salary_increase_recommended]),
            "retention_risks": len([r for r in completed_reviews if r.retention_risk])
        },
        
        "rating_distribution": {
            "exceptional": len([r for r in completed_reviews if r.final_rating_overall and r.final_rating_overall >= 4.5]),
            "exceeds_expectations": len([r for r in completed_reviews if r.final_rating_overall and 3.5 <= r.final_rating_overall < 4.5]),
            "meets_expectations": len([r for r in completed_reviews if r.final_rating_overall and 2.5 <= r.final_rating_overall < 3.5]),
            "below_expectations": len([r for r in completed_reviews if r.final_rating_overall and 1.5 <= r.final_rating_overall < 2.5]),
            "does_not_meet": len([r for r in completed_reviews if r.final_rating_overall and r.final_rating_overall < 1.5])
        },
        
        "competency_insights": [
            "🎯 Technical skills consistently rated highest across teams",
            "💬 Communication shows strong correlation with overall performance",
            "🚀 Leadership competency correlates with promotion recommendations",
            "⚡ Time management is key differentiator for high performers"
        ],
        
        "recommendations": [
            "🎓 Invest in leadership development for high performers",
            "💪 Focus on communication training for emerging talent",
            "🏆 Recognize and retain high performers with competitive packages",
            "📈 Address retention risks proactively with career development"
        ],
        
        "rickroll187_insights": {
            "legendary_reviews": len([r for r in completed_reviews if r.rickroll187_approved]),
            "founder_note": "🎸 Performance reviews are driving legendary talent development across the organization! 🎸"
        },
        
        "generated_by": "RICKROLL187's Legendary Performance Analytics 🎸📈"
    }
    
    processing_time = 0.678  # Analytics processing time
    return legendary_response_middleware.add_legendary_polish(
        analytics_summary, request, processing_time
    )

if __name__ == "__main__":
    print("📊🎸📱 N3EXTPATH LEGENDARY PERFORMANCE REVIEW API LOADED! 📱🎸📊")
    print("🏆 LEGENDARY NEXT ORDER PERFORMANCE API CHAMPION EDITION! 🏆")
    print(f"⏰ Next Order API Time: 2025-08-05 13:02:30 UTC")
    print("📱 NEXT ORDER CODED API BY LEGENDARY RICKROLL187! 📱")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("📊 PERFORMANCE API POWERED BY NEXT ORDER RICKROLL187 WITH SWISS EVALUATION PRECISION! 📊")
