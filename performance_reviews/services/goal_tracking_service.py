"""
LEGENDARY GOAL TRACKING SERVICE 🎯🚀
More ambitious than a startup CEO with a PhD in success!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc
from dataclasses import dataclass
import statistics
from enum import Enum

from ..models.review_models import (
    ReviewGoal, PerformanceReview, PerformanceReviewCycle,
    RatingScale
)
from ...core.auth.authorization import AuthContext, Permission
from ...core.database.base_models import Employee, User, AuditLog

logger = logging.getLogger(__name__)

class GoalStatus(Enum):
    """Goal status tracking - more organized than a Swiss agenda!"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    EXCEEDED = "exceeded"
    CANCELLED = "cancelled"

class GoalPriority(Enum):
    """Goal priority levels - more focused than a laser with ambition!"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class GoalAnalytics:
    """
    Goal analytics that are more insightful than a wise sage!
    More comprehensive than a PhD thesis on success! 📊🎯
    """
    total_goals: int
    completed_goals: int
    in_progress_goals: int
    at_risk_goals: int
    completion_rate: float
    average_progress: float
    goals_by_category: Dict[str, int]
    goals_by_status: Dict[str, int]
    overdue_goals: int
    upcoming_deadlines: int

class LegendaryGoalTracker:
    """
    The most ambitious goal tracking system in the galaxy!
    More focused than a Swiss watchmaker with OCD! 🎯⏰
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # GOAL TRACKING JOKES FOR SUNDAY MORNING MOTIVATION
        self.goal_jokes = [
            "Why did the goal go to therapy? It had commitment issues! 🎯😄",
            "What's the difference between our goals and a Swiss schedule? Both are perfectly timed! ⏰",
            "Why don't our goals ever give up? Because they have legendary persistence! 💪",
            "What do you call goal tracking at 3 AM? Night shift ambition with style! 🌙",
            "Why did the goal become a comedian? It had perfect timing for success! 🎭"
        ]
        
        # Goal categories and their weights
        self.goal_categories = {
            "PERFORMANCE": {"weight": 1.0, "description": "Core job performance goals"},
            "DEVELOPMENT": {"weight": 0.8, "description": "Skill and career development"},
            "BEHAVIORAL": {"weight": 0.7, "description": "Behavioral and soft skills"},
            "STRATEGIC": {"weight": 1.2, "description": "Strategic and business impact"},
            "INNOVATION": {"weight": 1.1, "description": "Innovation and improvement"},
            "LEADERSHIP": {"weight": 1.0, "description": "Leadership and team goals"},
            "COLLABORATION": {"weight": 0.9, "description": "Cross-team collaboration"}
        }
        
        # Progress calculation weights
        self.progress_weights = {
            "time_factor": 0.3,      # How much time has passed
            "milestone_factor": 0.4,  # Milestone completion
            "self_assessment": 0.3    # Self-reported progress
        }
        
        logger.info("🎯 Legendary Goal Tracker initialized - Ready to make dreams reality!")
    
    def create_goal(self, goal_data: Dict[str, Any], 
                   auth_context: AuthContext) -> Dict[str, Any]:
        """
        Create new performance goal!
        More ambitious than a startup pitch with a guaranteed success plan! 🚀💡
        """
        try:
            logger.info(f"🎯 Creating goal: {goal_data.get('title', 'unknown')}")
            
            # Validate permissions
            if not auth_context.has_permission(Permission.PERFORMANCE_WRITE):
                return {
                    "success": False,
                    "error": "Insufficient permissions to create goals"
                }
            
            # Validate goal data
            validation_result = self._validate_goal_data(goal_data)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            # Check if review exists
            review = self.db.query(PerformanceReview).filter(
                PerformanceReview.id == goal_data["review_id"]
            ).first()
            
            if not review:
                return {
                    "success": False,
                    "error": "Performance review not found"
                }
            
            # Create goal
            new_goal = ReviewGoal(
                review_id=goal_data["review_id"],
                title=goal_data["title"],
                description=goal_data["description"],
                category=goal_data.get("category", "PERFORMANCE"),
                target_value=goal_data.get("target_value"),
                measurement_unit=goal_data.get("measurement_unit"),
                target_date=goal_data.get("target_date"),
                weight=goal_data.get("weight", 1.0),
                progress_percentage=0.0,
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(new_goal)
            self.db.flush()
            
            # Calculate initial goal metrics
            initial_metrics = self._calculate_goal_metrics(new_goal)
            
            # Log goal creation
            self._log_goal_action("GOAL_CREATED", new_goal.id, auth_context, {
                "title": new_goal.title,
                "category": new_goal.category,
                "target_date": new_goal.target_date.isoformat() if new_goal.target_date else None,
                "initial_metrics": initial_metrics
            })
            
            self.db.commit()
            
            logger.info(f"✅ Goal created successfully: {new_goal.title} (ID: {new_goal.id})")
            
            return {
                "success": True,
                "goal_id": new_goal.id,
                "title": new_goal.title,
                "category": new_goal.category,
                "initial_status": self._determine_goal_status(new_goal),
                "metrics": initial_metrics,
                "legendary_joke": "Why did the goal become legendary? Because it was perfectly planned! 🎯🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Goal creation error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def update_goal_progress(self, goal_id: int, progress_data: Dict[str, Any],
                           auth_context: AuthContext) -> Dict[str, Any]:
        """
        Update goal progress with more precision than a Swiss timepiece!
        More accurate than a mathematician with OCD! 📊⏰
        """
        try:
            logger.info(f"📈 Updating goal progress: {goal_id}")
            
            # Get goal
            goal = self.db.query(ReviewGoal).filter(ReviewGoal.id == goal_id).first()
            
            if not goal:
                return {
                    "success": False,
                    "error": "Goal not found"
                }
            
            # Check permissions
            can_update = self._check_goal_update_permissions(goal, auth_context)
            if not can_update:
                return {
                    "success": False,
                    "error": "Insufficient permissions to update this goal"
                }
            
            # Store previous progress for comparison
            previous_progress = goal.progress_percentage
            previous_status = self._determine_goal_status(goal)
            
            # Update progress fields
            if "progress_percentage" in progress_data:
                progress_pct = max(0.0, min(100.0, progress_data["progress_percentage"]))
                goal.progress_percentage = progress_pct
            
            if "progress_notes" in progress_data:
                goal.progress_notes = progress_data["progress_notes"]
            
            if "actual_value" in progress_data:
                goal.actual_value = progress_data["actual_value"]
            
            if "completion_date" in progress_data and progress_data["completion_date"]:
                goal.completion_date = progress_data["completion_date"]
                if goal.progress_percentage < 100.0:
                    goal.progress_percentage = 100.0  # Auto-complete if date is set
            
            # Auto-calculate progress if we have target and actual values
            if goal.target_value and goal.actual_value:
                calculated_progress = min(100.0, (goal.actual_value / goal.target_value) * 100.0)
                goal.progress_percentage = calculated_progress
            
            # Update timestamp
            goal.updated_by = auth_context.user_id
            
            # Determine new status
            new_status = self._determine_goal_status(goal)
            
            # Calculate updated metrics
            updated_metrics = self._calculate_goal_metrics(goal)
            
            # Check for significant changes
            progress_change = goal.progress_percentage - previous_progress
            status_changed = new_status != previous_status
            
            # Log progress update
            self._log_goal_action("GOAL_PROGRESS_UPDATED", goal.id, auth_context, {
                "previous_progress": previous_progress,
                "new_progress": goal.progress_percentage,
                "progress_change": progress_change,
                "previous_status": previous_status,
                "new_status": new_status,
                "status_changed": status_changed,
                "updated_metrics": updated_metrics
            })
            
            # Generate notifications for significant changes
            notifications = []
            if progress_change >= 25.0:
                notifications.append("Significant progress made - great work!")
            if status_changed and new_status in ["COMPLETED", "EXCEEDED"]:
                notifications.append("Goal achieved - congratulations!")
            elif status_changed and new_status == "AT_RISK":
                notifications.append("Goal at risk - may need additional support")
            
            self.db.commit()
            
            logger.info(f"✅ Goal progress updated: {goal.title} -> {goal.progress_percentage}%")
            
            return {
                "success": True,
                "goal_id": goal.id,
                "title": goal.title,
                "previous_progress": previous_progress,
                "new_progress": goal.progress_percentage,
                "progress_change": progress_change,
                "status": new_status,
                "status_changed": status_changed,
                "metrics": updated_metrics,
                "notifications": notifications,
                "legendary_joke": "Why did the progress update become legendary? Because it moved mountains! 🏔️🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Goal progress update error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def get_employee_goals(self, employee_id: int, filters: Optional[Dict[str, Any]] = None,
                          auth_context: AuthContext) -> Dict[str, Any]:
        """
        Get employee goals with more organization than a Swiss filing system!
        More comprehensive than a life planner with attitude! 📋🎯
        """
        try:
            logger.info(f"📊 Getting goals for employee: {employee_id}")
            
            # Build base query
            query = self.db.query(ReviewGoal).join(PerformanceReview).filter(
                PerformanceReview.employee_id == employee_id
            )
            
            # Apply filters
            if filters:
                if filters.get("category"):
                    query = query.filter(ReviewGoal.category == filters["category"])
                
                if filters.get("review_cycle_id"):
                    query = query.filter(PerformanceReview.review_cycle_id == filters["review_cycle_id"])
                
                if filters.get("status"):
                    # Status filtering requires calculation - we'll filter after retrieval
                    pass
                
                if filters.get("target_date_from"):
                    query = query.filter(ReviewGoal.target_date >= filters["target_date_from"])
                
                if filters.get("target_date_to"):
                    query = query.filter(ReviewGoal.target_date <= filters["target_date_to"])
            
            # Order by priority (weight desc) and target date
            query = query.order_by(desc(ReviewGoal.weight), asc(ReviewGoal.target_date))
            
            # Execute query
            goals = query.all()
            
            # Filter by status if requested (post-query filtering)
            if filters and filters.get("status"):
                requested_status = filters["status"]
                goals = [goal for goal in goals if self._determine_goal_status(goal) == requested_status]
            
            # Calculate analytics
            analytics = self._calculate_goals_analytics(goals)
            
            # Format goals data
            goals_data = []
            for goal in goals:
                goal_status = self._determine_goal_status(goal)
                goal_metrics = self._calculate_goal_metrics(goal)
                
                goal_dict = {
                    "id": goal.id,
                    "title": goal.title,
                    "description": goal.description,
                    "category": goal.category,
                    "target_value": goal.target_value,
                    "actual_value": goal.actual_value,
                    "measurement_unit": goal.measurement_unit,
                    "target_date": goal.target_date.isoformat() if goal.target_date else None,
                    "completion_date": goal.completion_date.isoformat() if goal.completion_date else None,
                    "progress_percentage": goal.progress_percentage,
                    "progress_notes": goal.progress_notes,
                    "weight": goal.weight,
                    "status": goal_status,
                    "metrics": goal_metrics,
                    "self_rating": goal.self_rating.value if goal.self_rating else None,
                    "manager_rating": goal.manager_rating.value if goal.manager_rating else None,
                    "final_rating": goal.final_rating.value if goal.final_rating else None,
                    "created_at": goal.created_at.isoformat(),
                    "updated_at": goal.updated_at.isoformat()
                }
                goals_data.append(goal_dict)
            
            logger.info(f"📈 Retrieved {len(goals)} goals for employee {employee_id}")
            
            return {
                "success": True,
                "employee_id": employee_id,
                "goals": goals_data,
                "analytics": analytics,
                "total_goals": len(goals),
                "legendary_joke": "Why did the goal list become legendary? Because it was perfectly organized! 📋🏆"
            }
            
        except Exception as e:
            logger.error(f"💥 Employee goals retrieval error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def _validate_goal_data(self, goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate goal input data with Swiss precision"""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ["review_id", "title", "description"]
        for field in required_fields:
            if not goal_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Title validation
        if goal_data.get("title"):
            title = goal_data["title"]
            if len(title) < 5:
                errors.append("Goal title must be at least 5 characters long")
            elif len(title) > 200:
                errors.append("Goal title must be no more than 200 characters long")
        
        # Description validation
        if goal_data.get("description"):
            description = goal_data["description"]
            if len(description) < 10:
                warnings.append("Goal description is quite brief - consider adding more detail")
            elif len(description) > 1000:
                errors.append("Goal description must be no more than 1000 characters long")
        
        # Category validation
        if goal_data.get("category"):
            category = goal_data["category"]
            if category not in self.goal_categories:
                valid_categories = list(self.goal_categories.keys())
                errors.append(f"Invalid category. Must be one of: {valid_categories}")
        
        # Target value validation
        if goal_data.get("target_value") is not None:
            try:
                target_value = float(goal_data["target_value"])
                if target_value <= 0:
                    errors.append("Target value must be positive")
            except (ValueError, TypeError):
                errors.append("Target value must be a valid number")
        
        # Weight validation
        if goal_data.get("weight") is not None:
            try:
                weight = float(goal_data["weight"])
                if weight < 0 or weight > 5:
                    errors.append("Goal weight must be between 0 and 5")
            except (ValueError, TypeError):
                errors.append("Goal weight must be a valid number")
        
        # Target date validation
        if goal_data.get("target_date"):
            target_date = goal_data["target_date"]
            if isinstance(target_date, str):
                try:
                    target_date = datetime.fromisoformat(target_date.replace('Z', '+00:00'))
                except ValueError:
                    errors.append("Invalid target date format")
            
            if isinstance(target_date, datetime):
                if target_date <= datetime.utcnow():
                    warnings.append("Target date is in the past or very soon")
                elif target_date > datetime.utcnow() + timedelta(days=730):  # 2 years
                    warnings.append("Target date is quite far in the future")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _determine_goal_status(self, goal: ReviewGoal) -> str:
        """Determine current goal status based on progress and timeline"""
        try:
            # Check if completed
            if goal.completion_date or goal.progress_percentage >= 100.0:
                if goal.actual_value and goal.target_value and goal.actual_value > goal.target_value:
                    return GoalStatus.EXCEEDED.value
                return GoalStatus.COMPLETED.value
            
            # Check if not started
            if goal.progress_percentage <= 0.0:
                return GoalStatus.NOT_STARTED.value
            
            # Calculate time-based status
            if goal.target_date:
                now = datetime.utcnow()
                if now > goal.target_date:
                    # Overdue
                    return GoalStatus.AT_RISK.value
                
                # Calculate expected progress based on time
                total_duration = (goal.target_date - goal.created_at).total_seconds()
                elapsed_duration = (now - goal.created_at).total_seconds()
                
                if total_duration > 0:
                    expected_progress = (elapsed_duration / total_duration) * 100.0
                    actual_progress = goal.progress_percentage
                    
                    # Determine status based on progress vs timeline
                    if actual_progress >= expected_progress * 1.1:  # 10% ahead
                        return GoalStatus.ON_TRACK.value
                    elif actual_progress >= expected_progress * 0.8:  # Within 20% of expected
                        return GoalStatus.IN_PROGRESS.value
                    else:
                        return GoalStatus.AT_RISK.value
            
            # Default status based on progress only
            if goal.progress_percentage >= 80.0:
                return GoalStatus.ON_TRACK.value
            elif goal.progress_percentage >= 20.0:
                return GoalStatus.IN_PROGRESS.value
            else:
                return GoalStatus.AT_RISK.value
                
        except Exception as e:
            logger.error(f"💥 Goal status determination error: {e}")
            return GoalStatus.IN_PROGRESS.value
        """
LEGENDARY GOAL TRACKING SERVICE - CONTINUATION 🎯🚀
More ambitious than a startup CEO with a PhD in success!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

    def _calculate_goal_metrics(self, goal: ReviewGoal) -> Dict[str, Any]:
        """
        Calculate comprehensive goal metrics!
        More analytical than a Swiss mathematician with OCD! 📊🔢
        """
        try:
            metrics = {}
            
            # Basic progress metrics
            metrics["progress_percentage"] = goal.progress_percentage
            metrics["is_completed"] = goal.progress_percentage >= 100.0 or goal.completion_date is not None
            
            # Time-based metrics
            if goal.target_date:
                now = datetime.utcnow()
                created_at = goal.created_at
                
                # Total timeline
                total_days = (goal.target_date - created_at).days
                elapsed_days = (now - created_at).days
                remaining_days = (goal.target_date - now).days
                
                metrics["total_timeline_days"] = total_days
                metrics["elapsed_days"] = elapsed_days
                metrics["remaining_days"] = remaining_days
                metrics["is_overdue"] = remaining_days < 0
                
                # Timeline progress
                if total_days > 0:
                    timeline_progress = min(100.0, (elapsed_days / total_days) * 100.0)
                    metrics["timeline_progress_percentage"] = timeline_progress
                    
                    # Progress vs timeline comparison
                    progress_vs_timeline = goal.progress_percentage - timeline_progress
                    metrics["progress_vs_timeline_delta"] = progress_vs_timeline
                    
                    if progress_vs_timeline > 10:
                        metrics["pace_status"] = "AHEAD_OF_SCHEDULE"
                    elif progress_vs_timeline > -10:
                        metrics["pace_status"] = "ON_SCHEDULE"
                    else:
                        metrics["pace_status"] = "BEHIND_SCHEDULE"
                else:
                    metrics["timeline_progress_percentage"] = 100.0
                    metrics["pace_status"] = "COMPLETED"
            
            # Value-based metrics
            if goal.target_value and goal.actual_value is not None:
                completion_ratio = goal.actual_value / goal.target_value
                metrics["value_completion_ratio"] = completion_ratio
                metrics["value_completion_percentage"] = min(100.0, completion_ratio * 100.0)
                
                if completion_ratio >= 1.1:
                    metrics["value_performance"] = "EXCEEDING"
                elif completion_ratio >= 0.9:
                    metrics["value_performance"] = "MEETING"
                elif completion_ratio >= 0.7:
                    metrics["value_performance"] = "APPROACHING"
                else:
                    metrics["value_performance"] = "BELOW_TARGET"
            
            # Category weight factor
            category_info = self.goal_categories.get(goal.category, {"weight": 1.0})
            metrics["category_weight"] = category_info["weight"]
            metrics["weighted_progress"] = goal.progress_percentage * category_info["weight"]
            
            # Priority calculation
            urgency_score = 0.0
            importance_score = category_info["weight"]
            
            if goal.target_date:
                days_remaining = (goal.target_date - datetime.utcnow()).days
                if days_remaining <= 0:
                    urgency_score = 1.0
                elif days_remaining <= 7:
                    urgency_score = 0.8
                elif days_remaining <= 30:
                    urgency_score = 0.6
                elif days_remaining <= 90:
                    urgency_score = 0.4
                else:
                    urgency_score = 0.2
            
            priority_score = (urgency_score + importance_score) / 2
            if priority_score >= 0.8:
                metrics["priority_level"] = GoalPriority.CRITICAL.value
            elif priority_score >= 0.6:
                metrics["priority_level"] = GoalPriority.HIGH.value
            elif priority_score >= 0.4:
                metrics["priority_level"] = GoalPriority.MEDIUM.value
            else:
                metrics["priority_level"] = GoalPriority.LOW.value
            
            metrics["priority_score"] = priority_score
            
            return metrics
            
        except Exception as e:
            logger.error(f"💥 Goal metrics calculation error: {e}")
            return {"error": "Failed to calculate metrics"}
    
    def _calculate_goals_analytics(self, goals: List[ReviewGoal]) -> GoalAnalytics:
        """
        Calculate comprehensive analytics across multiple goals!
        More insightful than a data scientist with a crystal ball! 🔮📊
        """
        try:
            if not goals:
                return GoalAnalytics(
                    total_goals=0,
                    completed_goals=0,
                    in_progress_goals=0,
                    at_risk_goals=0,
                    completion_rate=0.0,
                    average_progress=0.0,
                    goals_by_category={},
                    goals_by_status={},
                    overdue_goals=0,
                    upcoming_deadlines=0
                )
            
            # Basic counts
            total_goals = len(goals)
            completed_goals = 0
            in_progress_goals = 0
            at_risk_goals = 0
            overdue_goals = 0
            upcoming_deadlines = 0
            
            # Category and status tracking
            goals_by_category = {}
            goals_by_status = {}
            
            # Progress tracking
            total_progress = 0.0
            
            # Analyze each goal
            now = datetime.utcnow()
            upcoming_threshold = now + timedelta(days=7)  # 7 days ahead
            
            for goal in goals:
                # Progress
                total_progress += goal.progress_percentage
                
                # Status analysis
                status = self._determine_goal_status(goal)
                goals_by_status[status] = goals_by_status.get(status, 0) + 1
                
                if status in [GoalStatus.COMPLETED.value, GoalStatus.EXCEEDED.value]:
                    completed_goals += 1
                elif status in [GoalStatus.IN_PROGRESS.value, GoalStatus.ON_TRACK.value]:
                    in_progress_goals += 1
                elif status == GoalStatus.AT_RISK.value:
                    at_risk_goals += 1
                
                # Category analysis
                category = goal.category
                goals_by_category[category] = goals_by_category.get(category, 0) + 1
                
                # Timeline analysis
                if goal.target_date:
                    if goal.target_date < now:
                        overdue_goals += 1
                    elif goal.target_date <= upcoming_threshold:
                        upcoming_deadlines += 1
            
            # Calculate rates
            completion_rate = (completed_goals / total_goals) * 100.0 if total_goals > 0 else 0.0
            average_progress = total_progress / total_goals if total_goals > 0 else 0.0
            
            return GoalAnalytics(
                total_goals=total_goals,
                completed_goals=completed_goals,
                in_progress_goals=in_progress_goals,
                at_risk_goals=at_risk_goals,
                completion_rate=completion_rate,
                average_progress=average_progress,
                goals_by_category=goals_by_category,
                goals_by_status=goals_by_status,
                overdue_goals=overdue_goals,
                upcoming_deadlines=upcoming_deadlines
            )
            
        except Exception as e:
            logger.error(f"💥 Goals analytics calculation error: {e}")
            return GoalAnalytics(
                total_goals=0, completed_goals=0, in_progress_goals=0, at_risk_goals=0,
                completion_rate=0.0, average_progress=0.0, goals_by_category={},
                goals_by_status={}, overdue_goals=0, upcoming_deadlines=0
            )
    
    def _check_goal_update_permissions(self, goal: ReviewGoal, auth_context: AuthContext) -> bool:
        """Check if user can update this goal"""
        try:
            # Performance admins can update any goal
            if auth_context.has_permission(Permission.PERFORMANCE_ADMIN):
                return True
            
            # Get the review to check employee and reviewer
            review = goal.review
            if not review:
                return False
            
            # Employee can update their own goals
            if review.employee_id == auth_context.user_id:
                return True
            
            # Reviewer (manager) can update goals
            if review.reviewer_id == auth_context.user_id:
                return True
            
            # HR can update goals
            if auth_context.has_permission(Permission.HR_ADMIN):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"💥 Goal permission check error: {e}")
            return False
    
    def _log_goal_action(self, action: str, goal_id: int, auth_context: AuthContext, 
                        details: Dict[str, Any]):
        """Log goal-related actions for audit trail"""
        try:
            audit_log = AuditLog(
                user_id=auth_context.user_id,
                action=action,
                resource_type="GOAL",
                resource_id=goal_id,
                details=details,
                ip_address=getattr(auth_context, 'ip_address', None),
                user_agent=getattr(auth_context, 'user_agent', None)
            )
            self.db.add(audit_log)
            
        except Exception as e:
            logger.error(f"💥 Goal action logging error: {e}")
    
    def get_team_goal_dashboard(self, manager_id: int, 
                               auth_context: AuthContext) -> Dict[str, Any]:
        """
        Get team goal dashboard for managers!
        More comprehensive than a NASA mission control! 🚀📊
        """
        try:
            logger.info(f"📊 Getting team goal dashboard for manager: {manager_id}")
            
            # Check permissions
            if not (auth_context.user_id == manager_id or 
                   auth_context.has_permission(Permission.PERFORMANCE_ADMIN)):
                return {
                    "success": False,
                    "error": "Insufficient permissions to view team dashboard"
                }
            
            # Get all team members (direct reports)
            team_members = self.db.query(Employee).filter(
                Employee.manager_id == manager_id
            ).all()
            
            if not team_members:
                return {
                    "success": True,
                    "team_dashboard": {
                        "team_size": 0,
                        "total_goals": 0,
                        "team_analytics": {},
                        "member_summaries": [],
                        "recommendations": ["No team members found"]
                    }
                }
            
            # Collect all goals for team members
            all_team_goals = []
            member_summaries = []
            
            for member in team_members:
                # Get member's goals
                member_goals_result = self.get_employee_goals(
                    member.id, filters=None, auth_context=auth_context
                )
                
                if member_goals_result["success"]:
                    member_goals = member_goals_result["goals"]
                    member_analytics = member_goals_result["analytics"]
                    
                    all_team_goals.extend([
                        goal for goal in member_goals 
                        if goal  # Filter out None values
                    ])
                    
                    # Create member summary
                    member_summary = {
                        "employee_id": member.id,
                        "employee_name": f"{member.user.first_name} {member.user.last_name}",
                        "total_goals": len(member_goals),
                        "completed_goals": member_analytics.completed_goals,
                        "at_risk_goals": member_analytics.at_risk_goals,
                        "completion_rate": member_analytics.completion_rate,
                        "average_progress": member_analytics.average_progress,
                        "overdue_goals": member_analytics.overdue_goals,
                        "upcoming_deadlines": member_analytics.upcoming_deadlines
                    }
                    member_summaries.append(member_summary)
            
            # Calculate team-wide analytics
            team_analytics = self._calculate_team_analytics(all_team_goals, member_summaries)
            
            # Generate team recommendations
            recommendations = self._generate_team_recommendations(team_analytics, member_summaries)
            
            # Create dashboard
            dashboard = {
                "team_size": len(team_members),
                "total_goals": len(all_team_goals),
                "team_analytics": team_analytics,
                "member_summaries": member_summaries,
                "recommendations": recommendations,
                "dashboard_generated_at": datetime.utcnow().isoformat(),
                "legendary_status": "TEAM DASHBOARD LOADED WITH LEGENDARY PRECISION! 🚀🏆"
            }
            
            logger.info(f"📈 Team dashboard generated for {len(team_members)} members with {len(all_team_goals)} goals")
            
            return {
                "success": True,
                "team_dashboard": dashboard
            }
            
        except Exception as e:
            logger.error(f"💥 Team goal dashboard error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def _calculate_team_analytics(self, all_goals: List[Dict[str, Any]], 
                                member_summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate team-wide goal analytics"""
        try:
            if not all_goals:
                return {
                    "overall_completion_rate": 0.0,
                    "overall_progress": 0.0,
                    "team_goals_by_status": {},
                    "team_goals_by_category": {},
                    "performance_distribution": {},
                    "risk_analysis": {}
                }
            
            # Overall metrics
            total_goals = len(all_goals)
            completed_goals = sum(1 for goal in all_goals if goal.get("status") in ["COMPLETED", "EXCEEDED"])
            total_progress = sum(goal.get("progress_percentage", 0) for goal in all_goals)
            
            overall_completion_rate = (completed_goals / total_goals) * 100.0
            overall_progress = total_progress / total_goals
            
            # Goals by status
            goals_by_status = {}
            for goal in all_goals:
                status = goal.get("status", "UNKNOWN")
                goals_by_status[status] = goals_by_status.get(status, 0) + 1
            
            # Goals by category
            goals_by_category = {}
            for goal in all_goals:
                category = goal.get("category", "UNKNOWN")
                goals_by_category[category] = goals_by_category.get(category, 0) + 1
            
            # Performance distribution
            high_performers = sum(1 for summary in member_summaries if summary["completion_rate"] >= 80)
            solid_performers = sum(1 for summary in member_summaries if 60 <= summary["completion_rate"] < 80)
            struggling_performers = sum(1 for summary in member_summaries if summary["completion_rate"] < 60)
            
            performance_distribution = {
                "high_performers": high_performers,
                "solid_performers": solid_performers,
                "struggling_performers": struggling_performers,
                "high_performer_percentage": (high_performers / len(member_summaries)) * 100.0 if member_summaries else 0
            }
            
            # Risk analysis
            total_at_risk = sum(summary["at_risk_goals"] for summary in member_summaries)
            total_overdue = sum(summary["overdue_goals"] for summary in member_summaries)
            upcoming_deadlines = sum(summary["upcoming_deadlines"] for summary in member_summaries)
            
            risk_analysis = {
                "total_at_risk_goals": total_at_risk,
                "total_overdue_goals": total_overdue,
                "upcoming_deadlines": upcoming_deadlines,
                "risk_percentage": (total_at_risk / total_goals) * 100.0 if total_goals > 0 else 0,
                "members_with_overdue": sum(1 for summary in member_summaries if summary["overdue_goals"] > 0)
            }
            
            return {
                "overall_completion_rate": overall_completion_rate,
                "overall_progress": overall_progress,
                "team_goals_by_status": goals_by_status,
                "team_goals_by_category": goals_by_category,
                "performance_distribution": performance_distribution,
                "risk_analysis": risk_analysis
            }
            
        except Exception as e:
            logger.error(f"💥 Team analytics calculation error: {e}")
            return {}
    
    def _generate_team_recommendations(self, team_analytics: Dict[str, Any],
                                     member_summaries: List[Dict[str, Any]]) -> List[str]:
        """Generate actionable recommendations for team performance"""
        recommendations = []
        
        try:
            # Overall performance recommendations
            completion_rate = team_analytics.get("overall_completion_rate", 0)
            if completion_rate < 60:
                recommendations.append("Team completion rate is below 60% - consider reviewing goal setting and support processes")
            elif completion_rate >= 90:
                recommendations.append("Excellent team performance! Consider setting more stretch goals")
            
            # Risk-based recommendations
            risk_analysis = team_analytics.get("risk_analysis", {})
            
            if risk_analysis.get("total_overdue_goals", 0) > 0:
                recommendations.append(f"Address {risk_analysis['total_overdue_goals']} overdue goals - schedule goal review sessions")
            
            if risk_analysis.get("risk_percentage", 0) > 25:
                recommendations.append("High percentage of at-risk goals - implement weekly check-ins")
            
            if risk_analysis.get("upcoming_deadlines", 0) > 5:
                recommendations.append("Multiple upcoming deadlines - prioritize and provide additional support")
            
            # Performance distribution recommendations
            perf_dist = team_analytics.get("performance_distribution", {})
            
            if perf_dist.get("struggling_performers", 0) > 0:
                recommendations.append("Provide additional coaching for team members with low completion rates")
            
            if perf_dist.get("high_performer_percentage", 0) < 30:
                recommendations.append("Consider goal calibration - may need more achievable or clearer objectives")
            
            # Member-specific recommendations
            members_needing_attention = [
                summary for summary in member_summaries 
                if summary["completion_rate"] < 50 or summary["overdue_goals"] > 2
            ]
            
            if members_needing_attention:
                names = [member["employee_name"] for member in members_needing_attention[:3]]
                recommendations.append(f"Schedule 1:1 sessions with: {', '.join(names)}")
            
            # Category-based recommendations
            goals_by_category = team_analytics.get("team_goals_by_category", {})
            if "DEVELOPMENT" in goals_by_category and goals_by_category["DEVELOPMENT"] < len(member_summaries):
                recommendations.append("Consider adding development goals for team members without them")
            
            # Default recommendations if none generated
            if not recommendations:
                recommendations = [
                    "Team performance looks good - continue current practices",
                    "Regular goal check-ins recommended to maintain momentum",
                    "Consider celebrating recent achievements to boost morale"
                ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"💥 Team recommendations generation error: {e}")
            return ["Review team goal performance and provide support as needed"]

class GoalTemplateManager:
    """
    Goal template management for consistency!
    More organized than a Swiss blueprint library! 📋🏗️
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # Default goal templates
        self.default_templates = {
            "PERFORMANCE": {
                "sales_target": {
                    "title": "Achieve Sales Target",
                    "description": "Meet or exceed quarterly sales targets",
                    "measurement_unit": "dollars",
                    "category": "PERFORMANCE",
                    "weight": 1.2
                },
                "customer_satisfaction": {
                    "title": "Improve Customer Satisfaction",
                    "description": "Achieve target customer satisfaction score",
                    "measurement_unit": "percentage",
                    "category": "PERFORMANCE",
                    "weight": 1.0
                }
            },
            "DEVELOPMENT": {
                "skill_certification": {
                    "title": "Complete Professional Certification",
                    "description": "Obtain relevant professional certification",
                    "measurement_unit": "completion",
                    "category": "DEVELOPMENT",
                    "weight": 0.8
                },
                "training_completion": {
                    "title": "Complete Training Program",
                    "description": "Successfully complete assigned training program",
                    "measurement_unit": "percentage",
                    "category": "DEVELOPMENT",
                    "weight": 0.7
                }
            },
            "LEADERSHIP": {
                "team_development": {
                    "title": "Develop Team Members",
                    "description": "Support team member growth and development",
                    "measurement_unit": "team_members",
                    "category": "LEADERSHIP",
                    "weight": 1.1
                },
                "process_improvement": {
                    "title": "Lead Process Improvement",
                    "description": "Identify and implement process improvements",
                    "measurement_unit": "improvements",
                    "category": "LEADERSHIP",
                    "weight": 1.0
                }
            }
        }
    
    def get_templates_by_category(self, category: str) -> Dict[str, Any]:
        """Get goal templates for specific category"""
        return self.default_templates.get(category, {})
    
    def create_goal_from_template(self, template_key: str, category: str, 
                                 customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Create goal data from template with customizations"""
        try:
            template = self.default_templates.get(category, {}).get(template_key)
            if not template:
                return {"success": False, "error": "Template not found"}
            
            # Start with template
            goal_data = template.copy()
            
            # Apply customizations
            goal_data.update(customizations)
            
            return {"success": True, "goal_data": goal_data}
            
        except Exception as e:
            return {"success": False, "error": f"Template creation error: {str(e)}"}
