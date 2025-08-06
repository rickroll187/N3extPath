"""
LEGENDARY PERFORMANCE REVIEW CRUD ENGINE 🔧🎯
More efficient than a Swiss machine with a computer science degree!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc
from sqlalchemy.exc import IntegrityError

from ..models.review_models import (
    PerformanceReviewCycle, PerformanceReview, ReviewGoal, 
    PeerReview, ReviewTemplate, ReviewCalibration,
    ReviewCycle, ReviewStatus, RatingScale
)
from ...core.auth.authorization import AuthContext, Permission
from ...core.database.base_models import Employee, User, Department, AuditLog

logger = logging.getLogger(__name__)

class LegendaryPerformanceCRUD:
    """
    The most badass performance review CRUD system in the galaxy!
    More reliable than a Swiss timepiece with attitude! ⏰💪
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # PERFORMANCE CRUD JOKES FOR SUNDAY MORNING MOTIVATION
        self.crud_jokes = [
            "Why did the CRUD operation go to therapy? It had commitment issues! 💾😄",
            "What's the difference between our CRUD and a reliable friend? Nothing - both always deliver! 🤝",
            "Why don't our operations ever fail? Because they have legendary error handling! 🛡️",
            "What do you call CRUD at 3 AM? Night shift with perfect performance! 🌙",
            "Why did the database become a comedian? It had great CRUD timing! ⏰"
        ]
        
        logger.info("🚀 Legendary Performance CRUD initialized - Ready to manage reviews!")
    
    # ===========================================
    # PERFORMANCE REVIEW CYCLE OPERATIONS
    # ===========================================
    
    def create_review_cycle(self, cycle_data: Dict[str, Any], 
                           auth_context: AuthContext) -> Dict[str, Any]:
        """
        Create new performance review cycle!
        More organized than a Swiss train schedule! 🚂📅
        """
        try:
            logger.info(f"🎯 Creating review cycle: {cycle_data.get('name', 'unknown')}")
            
            # Validate permissions
            if not auth_context.has_permission(Permission.PERFORMANCE_ADMIN):
                return {
                    "success": False,
                    "error": "Insufficient permissions to create review cycles"
                }
            
            # Validate input data
            validation_result = self._validate_cycle_data(cycle_data)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            # Check for overlapping cycles
            overlap_check = self._check_cycle_overlap(
                cycle_data["start_date"], 
                cycle_data["end_date"],
                cycle_data.get("cycle_type")
            )
            
            if overlap_check["has_overlap"]:
                return {
                    "success": False,
                    "error": f"Cycle overlaps with existing cycle: {overlap_check['conflicting_cycle']}"
                }
            
            # Create cycle
            new_cycle = PerformanceReviewCycle(
                name=cycle_data["name"],
                cycle_type=ReviewCycle(cycle_data["cycle_type"]),
                start_date=cycle_data["start_date"],
                end_date=cycle_data["end_date"],
                self_assessment_deadline=cycle_data["self_assessment_deadline"],
                manager_review_deadline=cycle_data["manager_review_deadline"],
                final_deadline=cycle_data["final_deadline"],
                enable_self_assessment=cycle_data.get("enable_self_assessment", True),
                enable_peer_reviews=cycle_data.get("enable_peer_reviews", True),
                enable_360_feedback=cycle_data.get("enable_360_feedback", False),
                min_peer_reviewers=cycle_data.get("min_peer_reviewers", 2),
                max_peer_reviewers=cycle_data.get("max_peer_reviewers", 5),
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(new_cycle)
            self.db.flush()
            
            # Auto-generate reviews for all active employees if requested
            if cycle_data.get("auto_generate_reviews", True):
                generation_result = self._auto_generate_reviews(new_cycle, auth_context)
                if not generation_result["success"]:
                    self.db.rollback()
                    return {
                        "success": False,
                        "error": f"Failed to generate reviews: {generation_result['error']}"
                    }
            
            self.db.commit()
            
            logger.info(f"✅ Review cycle created: {new_cycle.name} (ID: {new_cycle.id})")
            
            return {
                "success": True,
                "cycle_id": new_cycle.id,
                "cycle_name": new_cycle.name,
                "reviews_generated": generation_result.get("reviews_created", 0) if cycle_data.get("auto_generate_reviews") else 0,
                "legendary_joke": "Why did the review cycle become legendary? Because it was perfectly timed! ⏰🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Review cycle creation error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def get_review_cycles(self, filters: Optional[Dict[str, Any]] = None,
                         auth_context: AuthContext) -> Dict[str, Any]:
        """
        Get review cycles with filtering!
        More precise than a Swiss watchmaker's tools! 🔧⏰
        """
        try:
            # Build query
            query = self.db.query(PerformanceReviewCycle)
            
            # Apply filters
            if filters:
                if filters.get("is_active") is not None:
                    query = query.filter(PerformanceReviewCycle.is_active == filters["is_active"])
                
                if filters.get("cycle_type"):
                    query = query.filter(PerformanceReviewCycle.cycle_type == ReviewCycle(filters["cycle_type"]))
                
                if filters.get("start_date_from"):
                    query = query.filter(PerformanceReviewCycle.start_date >= filters["start_date_from"])
                
                if filters.get("end_date_to"):
                    query = query.filter(PerformanceReviewCycle.end_date <= filters["end_date_to"])
            
            # Order by start date descending
            query = query.order_by(desc(PerformanceReviewCycle.start_date))
            
            # Apply pagination
            page = filters.get("page", 1) if filters else 1
            per_page = filters.get("per_page", 50) if filters else 50
            offset = (page - 1) * per_page
            
            total_count = query.count()
            cycles = query.offset(offset).limit(per_page).all()
            
            # Format results
            cycle_list = []
            for cycle in cycles:
                cycle_dict = {
                    "id": cycle.id,
                    "name": cycle.name,
                    "cycle_type": cycle.cycle_type.value,
                    "start_date": cycle.start_date.isoformat(),
                    "end_date": cycle.end_date.isoformat(),
                    "self_assessment_deadline": cycle.self_assessment_deadline.isoformat(),
                    "manager_review_deadline": cycle.manager_review_deadline.isoformat(),
                    "final_deadline": cycle.final_deadline.isoformat(),
                    "is_active": cycle.is_active,
                    "is_locked": cycle.is_locked,
                    "enable_self_assessment": cycle.enable_self_assessment,
                    "enable_peer_reviews": cycle.enable_peer_reviews,
                    "enable_360_feedback": cycle.enable_360_feedback,
                    "created_at": cycle.created_at.isoformat()
                }
                cycle_list.append(cycle_dict)
            
            logger.info(f"📊 Retrieved {len(cycles)} review cycles")
            
            return {
                "success": True,
                "cycles": cycle_list,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_count": total_count,
                    "total_pages": (total_count + per_page - 1) // per_page
                }
            }
            
        except Exception as e:
            logger.error(f"💥 Review cycles retrieval error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    # ===========================================
    # INDIVIDUAL REVIEW OPERATIONS
    # ===========================================
    
    def create_performance_review(self, review_data: Dict[str, Any],
                                 auth_context: AuthContext) -> Dict[str, Any]:
        """
        Create individual performance review!
        More personalized than a custom-tailored suit! 👔✨
        """
        try:
            logger.info(f"📝 Creating performance review for employee: {review_data.get('employee_id')}")
            
            # Validate permissions
            if not auth_context.has_permission(Permission.PERFORMANCE_WRITE):
                return {
                    "success": False,
                    "error": "Insufficient permissions to create performance reviews"
                }
            
            # Check if review already exists for this cycle/employee
            existing_review = self.db.query(PerformanceReview).filter(
                and_(
                    PerformanceReview.review_cycle_id == review_data["review_cycle_id"],
                    PerformanceReview.employee_id == review_data["employee_id"]
                )
            ).first()
            
            if existing_review:
                return {
                    "success": False,
                    "error": "Review already exists for this employee and cycle"
                }
            
            # Validate employee and reviewer exist
            employee = self.db.query(Employee).filter(Employee.id == review_data["employee_id"]).first()
            reviewer = self.db.query(Employee).filter(Employee.id == review_data["reviewer_id"]).first()
            
            if not employee or not reviewer:
                return {
                    "success": False,
                    "error": "Invalid employee or reviewer ID"
                }
            
            # Create performance review
            new_review = PerformanceReview(
                review_cycle_id=review_data["review_cycle_id"],
                employee_id=review_data["employee_id"],
                reviewer_id=review_data["reviewer_id"],
                status=ReviewStatus.NOT_STARTED,
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(new_review)
            self.db.flush()
            
            # Create default goals if provided
            if review_data.get("default_goals"):
                for goal_data in review_data["default_goals"]:
                    goal = ReviewGoal(
                        review_id=new_review.id,
                        title=goal_data["title"],
                        description=goal_data["description"],
                        category=goal_data.get("category", "PERFORMANCE"),
                        target_date=goal_data.get("target_date"),
                        weight=goal_data.get("weight", 1.0),
                        created_by=auth_context.user_id,
                        updated_by=auth_context.user_id
                    )
                    self.db.add(goal)
            
            self.db.commit()
            
            logger.info(f"✅ Performance review created: {new_review.id}")
            
            return {
                "success": True,
                "review_id": new_review.id,
                "employee_name": f"{employee.user.first_name} {employee.user.last_name}",
                "reviewer_name": f"{reviewer.user.first_name} {reviewer.user.last_name}",
                "status": new_review.status.value,
                "legendary_joke": "Why did the performance review become a hit? Because it had great character development! 🎭🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Performance review creation error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def update_review_status(self, review_id: int, new_status: str,
                           auth_context: AuthContext) -> Dict[str, Any]:
        """
        Update review status with more precision than a Swiss watch!
        More reliable than a loyal friend with perfect timing! ⏰🤝
        """
        try:
            logger.info(f"🔄 Updating review status: {review_id} -> {new_status}")
            
            # Get review
            review = self.db.query(PerformanceReview).filter(
                PerformanceReview.id == review_id
            ).first()
            
            if not review:
                return {
                    "success": False,
                    "error": "Review not found"
                }
            
            # Check permissions
            can_update = (
                auth_context.has_permission(Permission.PERFORMANCE_ADMIN) or
                review.employee_id == auth_context.user_id or
                review.reviewer_id == auth_context.user_id
            )
            
            if not can_update:
                return {
                    "success": False,
                    "error": "Insufficient permissions to update this review"
                }
            
            # Validate status transition
            old_status = review.status
            try:
                new_status_enum = ReviewStatus(new_status)
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid status: {new_status}"
                }
            
            # Validate status transition logic
            valid_transition = self._validate_status_transition(old_status, new_status_enum)
            if not valid_transition["is_valid"]:
                return {
                    "success": False,
                    "error": valid_transition["error"]
                }
            
            # Update status
            review.status = new_status_enum
            review.updated_by = auth_context.user_id
            
            # Update timestamps based on status
            if new_status_enum == ReviewStatus.SELF_ASSESSMENT:
                review.self_assessment_submitted_at = datetime.utcnow()
            elif new_status_enum == ReviewStatus.MANAGER_REVIEW:
                review.manager_review_submitted_at = datetime.utcnow()
            elif new_status_enum == ReviewStatus.COMPLETED:
                review.final_review_completed_at = datetime.utcnow()
            elif new_status_enum == ReviewStatus.APPROVED:
                review.approved_at = datetime.utcnow()
                review.approved_by_id = auth_context.user_id
            
            self.db.commit()
            
            logger.info(f"✅ Review status updated: {old_status.value} -> {new_status}")
            
            return {
                "success": True,
                "old_status": old_status.value,
                "new_status": new_status,
                "updated_at": review.updated_at.isoformat(),
                "legendary_joke": "Why did the status update become legendary? Because it was perfectly timed! ⏰🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Review status update error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    # ===========================================
    # HELPER METHODS
    # ===========================================
    
    def _validate_cycle_data(self, cycle_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate review cycle data"""
        errors = []
        
        # Required fields
        required_fields = ["name", "cycle_type", "start_date", "end_date", 
                          "self_assessment_deadline", "manager_review_deadline", "final_deadline"]
        
        for field in required_fields:
            if not cycle_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Date validation
        if cycle_data.get("start_date") and cycle_data.get("end_date"):
            if cycle_data["start_date"] >= cycle_data["end_date"]:
                errors.append("Start date must be before end date")
        
        # Deadline validation
        if cycle_data.get("self_assessment_deadline") and cycle_data.get("end_date"):
            if cycle_data["self_assessment_deadline"] > cycle_data["end_date"]:
                errors.append("Self assessment deadline must be before cycle end date")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    def _check_cycle_overlap(self, start_date: datetime, end_date: datetime, 
                           cycle_type: Optional[str] = None) -> Dict[str, Any]:
        """Check for overlapping review cycles"""
        try:
            query = self.db.query(PerformanceReviewCycle).filter(
                and_(
                    PerformanceReviewCycle.is_active == True,
                    or_(
                        and_(
                            PerformanceReviewCycle.start_date <= start_date,
                            PerformanceReviewCycle.end_date >= start_date
                        ),
                        and_(
                            PerformanceReviewCycle.start_date <= end_date,
                            PerformanceReviewCycle.end_date >= end_date
                        ),
                        and_(
                            PerformanceReviewCycle.start_date >= start_date,
                            PerformanceReviewCycle.end_date <= end_date
                        )
                    )
                )
            )
            
            # Only check same cycle type if specified
            if cycle_type:
                query = query.filter(PerformanceReviewCycle.cycle_type == ReviewCycle(cycle_type))
            
            conflicting_cycle = query.first()
            
            return {
                "has_overlap": conflicting_cycle is not None,
                "conflicting_cycle": conflicting_cycle.name if conflicting_cycle else None
            }
            
        except Exception as e:
            logger.error(f"💥 Cycle overlap check error: {e}")
            return {"has_overlap": False, "conflicting_cycle": None}
    
    def _auto_generate_reviews(self, cycle: PerformanceReviewCycle, 
                             auth_context: AuthContext) -> Dict[str, Any]:
        """Auto-generate reviews for all active employees"""
        try:
            # Get all active employees
            employees = self.db.query(Employee).filter(
                Employee.employment_status == "ACTIVE"
            ).all()
            
            reviews_created = 0
            
            for employee in employees:
                # Determine reviewer (manager or HR if no manager)
                reviewer_id = employee.manager_id
                if not reviewer_id:
                    # Find HR manager or admin as fallback
                    hr_employee = self.db.query(Employee).join(User).filter(
                        User.is_hr_admin == True
                    ).first()
                    reviewer_id = hr_employee.id if hr_employee else auth_context.user_id
                
                # Create review
                review = PerformanceReview(
                    review_cycle_id=cycle.id,
                    employee_id=employee.id,
                    reviewer_id=reviewer_id,
                    status=ReviewStatus.NOT_STARTED,
                    created_by=auth_context.user_id,
                    updated_by=auth_context.user_id
                )
                
                self.db.add(review)
                reviews_created += 1
            
            logger.info(f"✅ Auto-generated {reviews_created} reviews for cycle: {cycle.name}")
            
            return {
                "success": True,
                "reviews_created": reviews_created
            }
            
        except Exception as e:
            logger.error(f"💥 Auto-generate reviews error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _validate_status_transition(self, old_status: ReviewStatus, 
                                  new_status: ReviewStatus) -> Dict[str, Any]:
        """Validate review status transitions"""
        valid_transitions = {
            ReviewStatus.NOT_STARTED: [ReviewStatus.SELF_ASSESSMENT, ReviewStatus.MANAGER_REVIEW],
            ReviewStatus.SELF_ASSESSMENT: [ReviewStatus.MANAGER_REVIEW, ReviewStatus.PEER_REVIEW],
            ReviewStatus.MANAGER_REVIEW: [ReviewStatus.PEER_REVIEW, ReviewStatus.CALIBRATION, ReviewStatus.COMPLETED],
            ReviewStatus.PEER_REVIEW: [ReviewStatus.CALIBRATION, ReviewStatus.COMPLETED],
            ReviewStatus.CALIBRATION: [ReviewStatus.COMPLETED],
            ReviewStatus.COMPLETED: [ReviewStatus.APPROVED, ReviewStatus.MANAGER_REVIEW],  # Allow revision
            ReviewStatus.APPROVED: [ReviewStatus.ARCHIVED],
            ReviewStatus.ARCHIVED: []  # No transitions from archived
        }
        
        allowed_transitions = valid_transitions.get(old_status, [])
        
        if new_status not in allowed_transitions:
            return {
                "is_valid": False,
                "error": f"Invalid status transition from {old_status.value} to {new_status.value}"
            }
        
        return {"is_valid": True}