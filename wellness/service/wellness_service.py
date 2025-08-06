"""
LEGENDARY WELLNESS SERVICE ENGINE 💚🧠
More caring than a Swiss therapist with a computer science degree!
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
import numpy as np
from collections import defaultdict, Counter

from ..models.wellness_models import (
    WellnessProgram, WellnessEnrollment, MentalHealthCheckIn, SupportSession,
    WellnessMetric, WellnessGoal, WellnessGoalProgress,
    WellnessCategory, MoodRating, StressLevel, SupportType, PrivacyLevel
)
from ...core.auth.authorization import AuthContext, Permission
from ...core.database.base_models import Employee, User, AuditLog

logger = logging.getLogger(__name__)

class WellnessRiskLevel(Enum):
    """Wellness risk assessment levels - more precise than a Swiss health monitor!"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class WellnessInsights:
    """
    Wellness insights that are more helpful than a Swiss life coach!
    More supportive than a therapy session with unlimited time! 🧠💙
    """
    overall_wellness_score: float
    risk_level: str
    primary_concerns: List[str]
    positive_trends: List[str]
    recommended_programs: List[str]
    immediate_actions: List[str]
    support_recommendations: List[str]

class LegendaryWellnessService:
    """
    The most caring wellness service in the galaxy!
    More supportive than a Swiss wellness retreat with unlimited hugs! 💚🤗
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # WELLNESS SERVICE JOKES FOR SUNDAY MORNING MOTIVATION
        self.wellness_jokes = [
            "Why did the wellness program go to therapy? It wanted to feel better about itself! 💚😄",
            "What's the difference between our wellness service and a spa? Both make you feel legendary! 🧘‍♀️",
            "Why don't our wellness programs ever stress out? Because they practice what they preach! 🧠",
            "What do you call wellness at 3 AM? Night shift self-care with attitude! 🌙",
            "Why did the mental health check-in become a comedian? It had perfect emotional timing! 🎭"
        ]
        
        # Wellness scoring weights
        self.wellness_weights = {
            "mood": 0.25,
            "stress": 0.20,
            "energy": 0.15,
            "sleep": 0.15,
            "work_satisfaction": 0.10,
            "work_life_balance": 0.10,
            "social_connections": 0.05
        }
        
        # Risk assessment thresholds
        self.risk_thresholds = {
            "critical_mood_days": 3,      # Days of very low mood
            "high_stress_days": 5,        # Days of high/extreme stress
            "low_energy_threshold": 3.0,  # Energy level threshold
            "poor_sleep_threshold": 4.0,  # Sleep quality threshold
            "support_request_weight": 2.0  # Weight for support requests
        }
        
        # Wellness program recommendations
        self.program_recommendations = {
            "high_stress": ["stress_management", "mindfulness", "work_life_balance"],
            "low_mood": ["mental_health", "social_connection", "physical_fitness"],
            "poor_sleep": ["sleep_hygiene", "stress_management", "mindfulness"],
            "low_energy": ["physical_fitness", "nutrition", "sleep_hygiene"],
            "work_dissatisfaction": ["career_development", "work_life_balance", "stress_management"]
        }
        
        logger.info("💚 Legendary Wellness Service initialized - Ready to spread wellness and joy!")
    
    def submit_mental_health_checkin(self, checkin_data: Dict[str, Any],
                                   auth_context: AuthContext) -> Dict[str, Any]:
        """
        Submit mental health check-in with more care than a Swiss nurse!
        More supportive than a best friend with psychology training! 🧠💙
        """
        try:
            logger.info(f"🧠 Processing mental health check-in for employee: {checkin_data.get('employee_id', auth_context.user_id)}")
            
            # Use current user if no employee_id specified
            employee_id = checkin_data.get('employee_id', auth_context.user_id)
            
            # Check permissions (employees can only submit their own check-ins)
            if employee_id != auth_context.user_id and not auth_context.has_permission(Permission.HR_ADMIN):
                return {
                    "success": False,
                    "error": "You can only submit your own mental health check-ins"
                }
            
            # Validate check-in data
            validation_result = self._validate_checkin_data(checkin_data)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            # Create mental health check-in
            checkin = MentalHealthCheckIn(
                employee_id=employee_id,
                mood_rating=checkin_data["mood_rating"],
                stress_level=checkin_data["stress_level"],
                energy_level=checkin_data.get("energy_level"),
                sleep_quality=checkin_data.get("sleep_quality"),
                workload_manageable=checkin_data.get("workload_manageable"),
                work_satisfaction=checkin_data.get("work_satisfaction"),
                team_support_felt=checkin_data.get("team_support_felt"),
                manager_support_felt=checkin_data.get("manager_support_felt"),
                work_life_balance=checkin_data.get("work_life_balance"),
                physical_health=checkin_data.get("physical_health"),
                social_connections=checkin_data.get("social_connections"),
                what_going_well=checkin_data.get("what_going_well"),
                main_challenges=checkin_data.get("main_challenges"),
                support_needed=checkin_data.get("support_needed"),
                additional_comments=checkin_data.get("additional_comments"),
                privacy_level=checkin_data.get("privacy_level", "private"),
                follow_up_requested=checkin_data.get("follow_up_requested", False),
                follow_up_urgency=checkin_data.get("follow_up_urgency"),
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(checkin)
            self.db.flush()
            
            # Perform risk assessment
            risk_assessment = self._assess_wellness_risk(employee_id, checkin)
            
            # Update check-in with risk indicators
            checkin.risk_indicators = risk_assessment["risk_indicators"]
            checkin.support_recommendations = risk_assessment["support_recommendations"]
            
            # Auto-schedule support if high risk
            support_scheduled = False
            if risk_assessment["risk_level"] in ["HIGH", "CRITICAL"]:
                support_result = self._auto_schedule_support(checkin, risk_assessment)
                support_scheduled = support_result.get("scheduled", False)
            
            # Generate wellness insights
            insights = self._generate_wellness_insights(employee_id)
            
            # Log check-in submission
            self._log_wellness_action("MENTAL_HEALTH_CHECKIN", checkin.id, auth_context, {
                "mood": checkin.mood_rating,
                "stress": checkin.stress_level,
                "risk_level": risk_assessment["risk_level"],
                "support_scheduled": support_scheduled,
                "follow_up_requested": checkin.follow_up_requested
            })
            
            self.db.commit()
            
            logger.info(f"✅ Mental health check-in submitted: ID {checkin.id}")
            
            return {
                "success": True,
                "checkin_id": checkin.id,
                "submission_time": checkin.checkin_date.isoformat(),
                "risk_assessment": {
                    "risk_level": risk_assessment["risk_level"],
                    "immediate_concerns": risk_assessment.get("immediate_concerns", []),
                    "support_scheduled": support_scheduled
                },
                "wellness_insights": insights,
                "motivational_message": self._get_motivational_message(checkin),
                "legendary_joke": "Why did the check-in become legendary? Because it showed you care about yourself! 💚🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Mental health check-in error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def enroll_in_wellness_program(self, program_id: int, employee_id: Optional[int] = None,
                                 auth_context: AuthContext) -> Dict[str, Any]:
        """
        Enroll employee in wellness program!
        More exciting than joining a Swiss health club with legendary benefits! 🏋️‍♀️💚
        """
        try:
            # Use current user if no employee_id specified
            target_employee_id = employee_id or auth_context.user_id
            
            logger.info(f"📝 Enrolling employee {target_employee_id} in wellness program {program_id}")
            
            # Check permissions
            if target_employee_id != auth_context.user_id and not auth_context.has_permission(Permission.HR_ADMIN):
                return {
                    "success": False,
                    "error": "You can only enroll yourself in wellness programs"
                }
            
            # Get wellness program
            program = self.db.query(WellnessProgram).filter(
                WellnessProgram.id == program_id
            ).first()
            
            if not program:
                return {
                    "success": False,
                    "error": "Wellness program not found"
                }
            
            # Check if program is active
            if not program.is_active:
                return {
                    "success": False,
                    "error": "This wellness program is no longer active"
                }
            
            # Check capacity
            if program.max_participants and program.current_participants >= program.max_participants:
                return {
                    "success": False,
                    "error": "This wellness program is currently full"
                }
            
            # Check if already enrolled
            existing_enrollment = self.db.query(WellnessEnrollment).filter(
                and_(
                    WellnessEnrollment.employee_id == target_employee_id,
                    WellnessEnrollment.program_id == program_id,
                    WellnessEnrollment.status.in_(["enrolled", "paused"])
                )
            ).first()
            
            if existing_enrollment:
                return {
                    "success": False,
                    "error": "Already enrolled in this wellness program"
                }
            
            # Create enrollment
            enrollment = WellnessEnrollment(
                employee_id=target_employee_id,
                program_id=program_id,
                total_sessions=self._calculate_total_sessions(program),
                status="enrolled",
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(enrollment)
            
            # Update program participant count
            program.current_participants += 1
            
            # Log enrollment
            self._log_wellness_action("WELLNESS_ENROLLMENT", enrollment.id, auth_context, {
                "program_name": program.name,
                "program_category": program.category,
                "employee_id": target_employee_id
            })
            
            self.db.commit()
            
            logger.info(f"✅ Wellness program enrollment successful: {enrollment.id}")
            
            return {
                "success": True,
                "enrollment_id": enrollment.id,
                "program_name": program.name,
                "program_category": program.category,
                "start_date": program.start_date.isoformat() if program.start_date else None,
                "duration_weeks": program.duration_weeks,
                "next_steps": self._get_program_next_steps(program),
                "legendary_joke": "Why did the wellness enrollment become legendary? Because it's the first step to feeling amazing! 🌟💚"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Wellness enrollment error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def create_wellness_goal(self, goal_data: Dict[str, Any],
                           auth_context: AuthContext) -> Dict[str, Any]:
        """
        Create personal wellness goal!
        More motivating than a Swiss personal trainer with unlimited enthusiasm! 🎯💪
        """
        try:
            # Use current user if no employee_id specified
            employee_id = goal_data.get('employee_id', auth_context.user_id)
            
            logger.info(f"🎯 Creating wellness goal for employee: {employee_id}")
            
            # Check permissions
            if employee_id != auth_context.user_id and not auth_context.has_permission(Permission.HR_ADMIN):
                return {
                    "success": False,
                    "error": "You can only create your own wellness goals"
                }
            
            # Validate goal data
            validation_result = self._validate_goal_data(goal_data)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            # Create wellness goal
            goal = WellnessGoal(
                employee_id=employee_id,
                title=goal_data["title"],
                description=goal_data.get("description"),
                category=goal_data["category"],
                target_value=goal_data.get("target_value"),
                measurement_unit=goal_data.get("measurement_unit"),
                target_date=goal_data.get("target_date"),
                priority_level=goal_data.get("priority_level", "medium"),
                accountability_partner_id=goal_data.get("accountability_partner_id"),
                coaching_support=goal_data.get("coaching_support", False),
                privacy_level=goal_data.get("privacy_level", "private"),
                milestones=goal_data.get("milestones", []),
                created_by=auth_context.user_id,
                updated_by=auth_context.user_id
            )
            
            self.db.add(goal)
            self.db.flush()
            
            # Create initial progress log
            initial_progress = WellnessGoalProgress(
                goal_id=goal.id,
                employee_id=employee_id,
                progress_value=goal.current_value or 0.0,
                progress_notes="Goal created",
                activity_type="goal_creation"
            )
            
            self.db.add(initial_progress)
            
            # Generate goal recommendations
            recommendations = self._generate_goal_recommendations(goal)
            
            # Log goal creation
            self._log_wellness_action("WELLNESS_GOAL_CREATED", goal.id, auth_context, {
                "title": goal.title,
                "category": goal.category,
                "target_date": goal.target_date.isoformat() if goal.target_date else None,
                "has_accountability_partner": goal.accountability_partner_id is not None
            })
            
            self.db.commit()
            
            logger.info(f"✅ Wellness goal created: {goal.title} (ID: {goal.id})")
            
            return {
                "success": True,
                "goal_id": goal.id,
                "title": goal.title,
                "category": goal.category,
                "target_date": goal.target_date.isoformat() if goal.target_date else None,
                "recommendations": recommendations,
                "motivational_message": f"You've got this! Every step towards {goal.title} is a step towards a better you! 💪✨",
                "legendary_joke": "Why did the wellness goal become legendary? Because it turned dreams into reality, one step at a time! 🎯🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Wellness goal creation error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def get_wellness_dashboard(self, employee_id: Optional[int] = None,
                             auth_context: AuthContext) -> Dict[str, Any]:
        """
        Get comprehensive wellness dashboard!
        More insightful than a Swiss wellness consultant with X-ray vision! 📊💚
        """
        try:
            # Use current user if no employee_id specified
            target_employee_id = employee_id or auth_context.user_id
            
            logger.info(f"📊 Generating wellness dashboard for employee: {target_employee_id}")
            
            # Check permissions
            if target_employee_id != auth_context.user_id and not auth_context.has_permission(Permission.HR_ADMIN):
                return {
                    "success": False,
                    "error": "You can only view your own wellness dashboard"
                }
            
            # Get recent check-ins (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_checkins = self.db.query(MentalHealthCheckIn).filter(
                and_(
                    MentalHealthCheckIn.employee_id == target_employee_id,
                    MentalHealthCheckIn.checkin_date >= thirty_days_ago
                )
            ).order_by(desc(MentalHealthCheckIn.checkin_date)).all()
            
            # Get active wellness goals
            active_goals = self.db.query(WellnessGoal).filter(
                and_(
                    WellnessGoal.employee_id == target_employee_id,
                    WellnessGoal.is_active == True,
                    or_(
                        WellnessGoal.target_date.is_(None),
                        WellnessGoal.target_date >= datetime.utcnow()
                    )
                )
            ).all()
            
            # Get active program enrollments
            active_enrollments = self.db.query(WellnessEnrollment).join(WellnessProgram).filter(
                and_(
                    WellnessEnrollment.employee_id == target_employee_id,
                    WellnessEnrollment.status == "enrolled",
                    WellnessProgram.is_active == True
                )
            ).all()
            
            # Calculate wellness metrics
            wellness_metrics = self._calculate_wellness_metrics(recent_checkins)
            
            # Generate insights
            insights = self._generate_wellness_insights(target_employee_id)
            
            # Get recommended programs
            recommended_programs = self._get_recommended_programs(target_employee_id, insights)
            
            # Format dashboard data
            dashboard = {
                "employee_id": target_employee_id,
                "dashboard_date": datetime.utcnow().isoformat(),
                "wellness_overview": {
                    "overall_wellness_score": wellness_metrics.get("overall_score", 0),
                    "recent_checkins_count": len(recent_checkins),
                    "active_goals_count": len(active_goals),
                    "active_programs_count": len(active_enrollments),
                    "last_checkin_date": recent_checkins[0].checkin_date.isoformat() if recent_checkins else None
                },
                "wellness_trends": {
                    "mood_trend": wellness_metrics.get("mood_trend", "stable"),
                    "stress_trend": wellness_metrics.get("stress_trend", "stable"),
                    "energy_trend": wellness_metrics.get("energy_trend", "stable"),
                    "sleep_trend": wellness_metrics.get("sleep_trend", "stable")
                },
                "current_goals": [
                    {
                        "id": goal.id,
                        "title": goal.title,
                        "category": goal.category,
                        "progress": goal.progress_percentage,
                        "target_date": goal.target_date.isoformat() if goal.target_date else None,
                        "priority": goal.priority_level
                    }
                    for goal in active_goals
                ],
                "active_programs": [
                    {
                        "id": enrollment.program.id,
                        "name": enrollment.program.name,
                        "category": enrollment.program.category,
                        "progress": enrollment.completion_percentage,
                        "sessions_attended": enrollment.sessions_attended,
                        "total_sessions": enrollment.total_sessions
                    }
                    for enrollment in active_enrollments
                ],
                "wellness_insights": insights,
                "recommended_programs": recommended_programs,
                "motivational_message": self._get_dashboard_motivational_message(wellness_metrics),
                "legendary_status": "WELLNESS DASHBOARD LOADED WITH LEGENDARY CARE! 💚🏆"
            }
            
            logger.info(f"📈 Wellness dashboard generated for employee {target_employee_id}")
            
            return {
                "success": True,
                "wellness_dashboard": dashboard
            }
            
        except Exception as e:
            logger.error(f"💥 Wellness dashboard error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def _validate_checkin_data(self, checkin_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate mental health check-in data"""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ["mood_rating", "stress_level"]
        for field in required_fields:
            if not checkin_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Validate enum values
        try:
            if checkin_data.get("mood_rating"):
                MoodRating(checkin_data["mood_rating"])
        except ValueError:
            errors.append("Invalid mood rating value")
        
        try:
            if checkin_data.get("stress_level"):
                StressLevel(checkin_data["stress_level"])
        except ValueError:
            errors.append("Invalid stress level value")
        
        # Validate numeric fields (1-10 scale)
        numeric_fields = ["energy_level", "sleep_quality", "work_satisfaction", 
                         "work_life_balance", "physical_health", "social_connections"]
        
        for field in numeric_fields:
            value = checkin_data.get(field)
            if value is not None:
                try:
                    numeric_value = float(value)
                    if not 1 <= numeric_value <= 10:
                        errors.append(f"{field} must be between 1 and 10")
                except (ValueError, TypeError):
                    errors.append(f"{field} must be a valid number")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    """
LEGENDARY WELLNESS SERVICE ENGINE - CONTINUATION 💚🧠
More caring than a Swiss therapist with a computer science degree!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

    def _assess_wellness_risk(self, employee_id: int, 
                             checkin: MentalHealthCheckIn) -> Dict[str, Any]:
        """
        Assess wellness risk with more precision than a Swiss health monitor!
        More caring than a concerned best friend with medical training! 🏥💙
        """
        try:
            risk_indicators = []
            immediate_concerns = []
            support_recommendations = []
            risk_score = 0.0
            
            # Analyze current check-in
            mood_numeric = self._mood_to_numeric(checkin.mood_rating)
            stress_numeric = self._stress_to_numeric(checkin.stress_level)
            
            # Current check-in risk factors
            if mood_numeric <= 2:  # very_low or low mood
                risk_score += 25
                risk_indicators.append("low_mood_current")
                if mood_numeric == 1:  # very_low
                    immediate_concerns.append("Very low mood reported")
                    support_recommendations.append("Immediate mental health support recommended")
            
            if stress_numeric >= 4:  # high or extreme stress
                risk_score += 20
                risk_indicators.append("high_stress_current")
                if stress_numeric == 5:  # extreme
                    immediate_concerns.append("Extreme stress level reported")
                    support_recommendations.append("Urgent stress management intervention needed")
            
            # Work-related risk factors
            if checkin.workload_manageable is False:
                risk_score += 15
                risk_indicators.append("workload_unmanageable")
                support_recommendations.append("Workload assessment and adjustment needed")
            
            if checkin.work_satisfaction and checkin.work_satisfaction <= 3:
                risk_score += 10
                risk_indicators.append("low_work_satisfaction")
                support_recommendations.append("Career satisfaction discussion recommended")
            
            if checkin.team_support_felt is False:
                risk_score += 10
                risk_indicators.append("lack_team_support")
                support_recommendations.append("Team dynamics intervention may be helpful")
            
            if checkin.manager_support_felt is False:
                risk_score += 12
                risk_indicators.append("lack_manager_support")
                support_recommendations.append("Manager-employee relationship support needed")
            
            # Personal well-being factors
            if checkin.energy_level and checkin.energy_level <= 3:
                risk_score += 8
                risk_indicators.append("low_energy")
                support_recommendations.append("Energy and vitality assessment recommended")
            
            if checkin.sleep_quality and checkin.sleep_quality <= 4:
                risk_score += 8
                risk_indicators.append("poor_sleep")
                support_recommendations.append("Sleep hygiene program recommended")
            
            if checkin.work_life_balance and checkin.work_life_balance <= 3:
                risk_score += 10
                risk_indicators.append("poor_work_life_balance")
                support_recommendations.append("Work-life balance coaching suggested")
            
            if checkin.social_connections and checkin.social_connections <= 3:
                risk_score += 8
                risk_indicators.append("low_social_connections")
                support_recommendations.append("Social connection activities recommended")
            
            # Support request indicators
            if checkin.support_needed:
                risk_score += 15
                risk_indicators.append("support_requested")
                immediate_concerns.append("Employee has requested support")
            
            if checkin.follow_up_requested:
                risk_score += 10
                risk_indicators.append("follow_up_requested")
                
                if checkin.follow_up_urgency == "urgent":
                    risk_score += 20
                    immediate_concerns.append("Urgent follow-up requested")
                elif checkin.follow_up_urgency == "high":
                    risk_score += 10
            
            # Historical pattern analysis (last 14 days)
            two_weeks_ago = datetime.utcnow() - timedelta(days=14)
            recent_checkins = self.db.query(MentalHealthCheckIn).filter(
                and_(
                    MentalHealthCheckIn.employee_id == employee_id,
                    MentalHealthCheckIn.checkin_date >= two_weeks_ago,
                    MentalHealthCheckIn.id != checkin.id  # Exclude current check-in
                )
            ).order_by(desc(MentalHealthCheckIn.checkin_date)).limit(10).all()
            
            if recent_checkins:
                # Count consecutive concerning days
                low_mood_days = sum(1 for c in recent_checkins if self._mood_to_numeric(c.mood_rating) <= 2)
                high_stress_days = sum(1 for c in recent_checkins if self._stress_to_numeric(c.stress_level) >= 4)
                
                if low_mood_days >= self.risk_thresholds["critical_mood_days"]:
                    risk_score += 25
                    risk_indicators.append("persistent_low_mood")
                    immediate_concerns.append(f"Low mood for {low_mood_days} days in past 2 weeks")
                
                if high_stress_days >= self.risk_thresholds["high_stress_days"]:
                    risk_score += 20
                    risk_indicators.append("persistent_high_stress")
                    immediate_concerns.append(f"High stress for {high_stress_days} days in past 2 weeks")
                
                # Trend analysis
                recent_moods = [self._mood_to_numeric(c.mood_rating) for c in recent_checkins[:5]]
                if len(recent_moods) >= 3:
                    mood_trend = np.polyfit(range(len(recent_moods)), recent_moods, 1)[0]
                    if mood_trend < -0.3:  # Declining mood trend
                        risk_score += 15
                        risk_indicators.append("declining_mood_trend")
                        support_recommendations.append("Mood trend monitoring and intervention recommended")
            
            # Determine risk level
            if risk_score >= 80:
                risk_level = WellnessRiskLevel.CRITICAL.value
            elif risk_score >= 60:
                risk_level = WellnessRiskLevel.HIGH.value
            elif risk_score >= 30:
                risk_level = WellnessRiskLevel.MODERATE.value
            else:
                risk_level = WellnessRiskLevel.LOW.value
            
            # Add general support recommendations based on risk level
            if risk_level == "critical":
                support_recommendations.insert(0, "Immediate mental health professional consultation required")
                support_recommendations.append("Consider crisis intervention protocols")
            elif risk_level == "high":
                support_recommendations.insert(0, "Schedule mental health support session within 24-48 hours")
                support_recommendations.append("Implement daily check-in process")
            elif risk_level == "moderate":
                support_recommendations.insert(0, "Schedule wellness coaching session within 1 week")
                support_recommendations.append("Explore appropriate wellness programs")
            
            return {
                "risk_level": risk_level,
                "risk_score": risk_score,
                "risk_indicators": risk_indicators,
                "immediate_concerns": immediate_concerns,
                "support_recommendations": support_recommendations,
                "historical_context": {
                    "recent_checkins_count": len(recent_checkins),
                    "low_mood_days": low_mood_days if recent_checkins else 0,
                    "high_stress_days": high_stress_days if recent_checkins else 0
                }
            }
            
        except Exception as e:
            logger.error(f"💥 Wellness risk assessment error: {e}")
            return {
                "risk_level": "moderate",
                "risk_score": 50,
                "risk_indicators": ["assessment_error"],
                "immediate_concerns": ["Risk assessment system error"],
                "support_recommendations": ["Manual wellness review recommended"]
            }
    
    def _generate_wellness_insights(self, employee_id: int) -> WellnessInsights:
        """
        Generate comprehensive wellness insights!
        More insightful than a Swiss wellness guru with data science superpowers! 🔮📊
        """
        try:
            # Get recent wellness data (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            recent_checkins = self.db.query(MentalHealthCheckIn).filter(
                and_(
                    MentalHealthCheckIn.employee_id == employee_id,
                    MentalHealthCheckIn.checkin_date >= thirty_days_ago
                )
            ).order_by(desc(MentalHealthCheckIn.checkin_date)).all()
            
            if not recent_checkins:
                return WellnessInsights(
                    overall_wellness_score=50.0,
                    risk_level="unknown",
                    primary_concerns=["No recent wellness data available"],
                    positive_trends=[],
                    recommended_programs=["stress_management", "mindfulness"],
                    immediate_actions=["Complete wellness check-in"],
                    support_recommendations=["Regular wellness monitoring recommended"]
                )
            
            # Calculate wellness metrics
            wellness_metrics = self._calculate_wellness_metrics(recent_checkins)
            
            # Identify trends
            positive_trends = []
            primary_concerns = []
            
            # Mood analysis
            mood_trend = wellness_metrics.get("mood_trend", "stable")
            if mood_trend == "improving":
                positive_trends.append("Mood has been improving recently")
            elif mood_trend == "declining":
                primary_concerns.append("Mood has been declining")
            
            # Stress analysis
            stress_trend = wellness_metrics.get("stress_trend", "stable")
            if stress_trend == "improving":
                positive_trends.append("Stress levels have been decreasing")
            elif stress_trend == "declining":
                primary_concerns.append("Stress levels have been increasing")
            
            # Energy analysis
            avg_energy = wellness_metrics.get("avg_energy", 5.0)
            if avg_energy >= 7:
                positive_trends.append("Maintaining good energy levels")
            elif avg_energy <= 4:
                primary_concerns.append("Low energy levels reported")
            
            # Sleep analysis
            avg_sleep = wellness_metrics.get("avg_sleep_quality", 5.0)
            if avg_sleep >= 7:
                positive_trends.append("Good sleep quality maintained")
            elif avg_sleep <= 4:
                primary_concerns.append("Poor sleep quality reported")
            
            # Work satisfaction analysis
            avg_work_satisfaction = wellness_metrics.get("avg_work_satisfaction", 5.0)
            if avg_work_satisfaction >= 7:
                positive_trends.append("High work satisfaction reported")
            elif avg_work_satisfaction <= 4:
                primary_concerns.append("Low work satisfaction reported")
            
            # Generate program recommendations
            recommended_programs = []
            for concern in primary_concerns:
                if "stress" in concern.lower():
                    recommended_programs.extend(self.program_recommendations["high_stress"])
                elif "mood" in concern.lower():
                    recommended_programs.extend(self.program_recommendations["low_mood"])
                elif "sleep" in concern.lower():
                    recommended_programs.extend(self.program_recommendations["poor_sleep"])
                elif "energy" in concern.lower():
                    recommended_programs.extend(self.program_recommendations["low_energy"])
                elif "work satisfaction" in concern.lower():
                    recommended_programs.extend(self.program_recommendations["work_dissatisfaction"])
            
            # Remove duplicates and limit recommendations
            recommended_programs = list(set(recommended_programs))[:5]
            
            # Generate immediate actions
            immediate_actions = []
            latest_checkin = recent_checkins[0]
            
            if self._mood_to_numeric(latest_checkin.mood_rating) <= 2:
                immediate_actions.append("Consider speaking with a mental health professional")
            
            if self._stress_to_numeric(latest_checkin.stress_level) >= 4:
                immediate_actions.append("Practice stress reduction techniques today")
            
            if latest_checkin.energy_level and latest_checkin.energy_level <= 3:
                immediate_actions.append("Focus on rest and energy restoration")
            
            if latest_checkin.sleep_quality and latest_checkin.sleep_quality <= 4:
                immediate_actions.append("Implement better sleep hygiene practices")
            
            if not immediate_actions:
                immediate_actions = ["Continue current wellness practices", "Regular wellness check-ins"]
            
            # Support recommendations
            support_recommendations = []
            risk_level = wellness_metrics.get("risk_level", "low")
            
            if risk_level in ["high", "critical"]:
                support_recommendations.append("Professional mental health support recommended")
                support_recommendations.append("Manager notification (with privacy considerations)")
            elif risk_level == "moderate":
                support_recommendations.append("Wellness coaching session recommended")
                support_recommendations.append("Peer support group participation")
            else:
                support_recommendations.append("Continue preventive wellness activities")
                support_recommendations.append("Regular wellness monitoring")
            
            return WellnessInsights(
                overall_wellness_score=wellness_metrics.get("overall_score", 50.0),
                risk_level=risk_level,
                primary_concerns=primary_concerns[:5],  # Limit to top 5
                positive_trends=positive_trends[:5],    # Limit to top 5
                recommended_programs=recommended_programs,
                immediate_actions=immediate_actions[:3], # Limit to top 3
                support_recommendations=support_recommendations[:3] # Limit to top 3
            )
            
        except Exception as e:
            logger.error(f"💥 Wellness insights generation error: {e}")
            return WellnessInsights(
                overall_wellness_score=50.0,
                risk_level="unknown",
                primary_concerns=["Wellness analysis temporarily unavailable"],
                positive_trends=[],
                recommended_programs=["mindfulness", "stress_management"],
                immediate_actions=["Regular wellness check-ins"],
                support_recommendations=["Manual wellness review recommended"]
            )
    
    def _calculate_wellness_metrics(self, checkins: List[MentalHealthCheckIn]) -> Dict[str, Any]:
        """Calculate comprehensive wellness metrics from check-ins"""
        try:
            if not checkins:
                return {"overall_score": 50.0, "risk_level": "unknown"}
            
            # Convert ratings to numeric values
            mood_values = [self._mood_to_numeric(c.mood_rating) for c in checkins]
            stress_values = [self._stress_to_numeric(c.stress_level) for c in checkins]
            
            # Energy and sleep (if available)
            energy_values = [c.energy_level for c in checkins if c.energy_level]
            sleep_values = [c.sleep_quality for c in checkins if c.sleep_quality]
            work_satisfaction_values = [c.work_satisfaction for c in checkins if c.work_satisfaction]
            work_life_balance_values = [c.work_life_balance for c in checkins if c.work_life_balance]
            
            # Calculate averages
            avg_mood = statistics.mean(mood_values)
            avg_stress = statistics.mean(stress_values)
            avg_energy = statistics.mean(energy_values) if energy_values else 5.0
            avg_sleep = statistics.mean(sleep_values) if sleep_values else 5.0
            avg_work_satisfaction = statistics.mean(work_satisfaction_values) if work_satisfaction_values else 5.0
            avg_work_life_balance = statistics.mean(work_life_balance_values) if work_life_balance_values else 5.0
            
            # Calculate trends (last 5 vs previous 5)
            mood_trend = self._calculate_trend(mood_values, "higher_better")
            stress_trend = self._calculate_trend(stress_values, "lower_better")
            energy_trend = self._calculate_trend(energy_values, "higher_better") if len(energy_values) >= 3 else "stable"
            sleep_trend = self._calculate_trend(sleep_values, "higher_better") if len(sleep_values) >= 3 else "stable"
            
            # Calculate overall wellness score
            mood_score = (avg_mood / 5.0) * 100  # Convert to 0-100 scale
            stress_score = ((6 - avg_stress) / 5.0) * 100  # Inverted for stress
            energy_score = (avg_energy / 10.0) * 100
            sleep_score = (avg_sleep / 10.0) * 100
            work_satisfaction_score = (avg_work_satisfaction / 10.0) * 100
            work_life_balance_score = (avg_work_life_balance / 10.0) * 100
            
            # Weighted overall score
            overall_score = (
                mood_score * self.wellness_weights["mood"] +
                stress_score * self.wellness_weights["stress"] +
                energy_score * self.wellness_weights["energy"] +
                sleep_score * self.wellness_weights["sleep"] +
                work_satisfaction_score * self.wellness_weights["work_satisfaction"] +
                work_life_balance_score * self.wellness_weights["work_life_balance"]
            )
            
            # Determine risk level based on score and recent patterns
            if overall_score < 40 or avg_mood <= 2 or avg_stress >= 4:
                risk_level = "high"
            elif overall_score < 60 or avg_mood <= 3 or avg_stress >= 3.5:
                risk_level = "moderate"
            else:
                risk_level = "low"
            
            return {
                "overall_score": overall_score,
                "avg_mood": avg_mood,
                "avg_stress": avg_stress,
                "avg_energy": avg_energy,
                "avg_sleep_quality": avg_sleep,
                "avg_work_satisfaction": avg_work_satisfaction,
                "avg_work_life_balance": avg_work_life_balance,
                "mood_trend": mood_trend,
                "stress_trend": stress_trend,
                "energy_trend": energy_trend,
                "sleep_trend": sleep_trend,
                "risk_level": risk_level,
                "checkins_count": len(checkins)
            }
            
        except Exception as e:
            logger.error(f"💥 Wellness metrics calculation error: {e}")
            return {"overall_score": 50.0, "risk_level": "unknown"}
    
    def _calculate_trend(self, values: List[float], trend_type: str) -> str:
        """Calculate trend direction for wellness metrics"""
        try:
            if len(values) < 4:
                return "stable"
            
            # Split into recent and previous periods
            mid_point = len(values) // 2
            recent_avg = statistics.mean(values[:mid_point])
            previous_avg = statistics.mean(values[mid_point:])
            
            difference = recent_avg - previous_avg
            threshold = 0.3  # Minimum difference to consider a trend
            
            if trend_type == "higher_better":
                if difference > threshold:
                    return "improving"
                elif difference < -threshold:
                    return "declining"
            else:  # lower_better (for stress)
                if difference < -threshold:
                    return "improving"
                elif difference > threshold:
                    return "declining"
            
            return "stable"
            
        except Exception:
            return "stable"
    
    def _mood_to_numeric(self, mood: str) -> int:
        """Convert mood rating to numeric value"""
        mood_map = {
            MoodRating.EXCELLENT.value: 5,
            MoodRating.GOOD.value: 4,
            MoodRating.NEUTRAL.value: 3,
            MoodRating.LOW.value: 2,
            MoodRating.VERY_LOW.value: 1
        }
        return mood_map.get(mood, 3)
    
    def _stress_to_numeric(self, stress: str) -> int:
        """Convert stress level to numeric value"""
        stress_map = {
            StressLevel.MINIMAL.value: 1,
            StressLevel.LOW.value: 2,
            StressLevel.MODERATE.value: 3,
            StressLevel.HIGH.value: 4,
            StressLevel.EXTREME.value: 5
        }
        return stress_map.get(stress, 3)
    
    def _get_motivational_message(self, checkin: MentalHealthCheckIn) -> str:
        """Get personalized motivational message based on check-in"""
        mood_numeric = self._mood_to_numeric(checkin.mood_rating)
        stress_numeric = self._stress_to_numeric(checkin.stress_level)
        
        if mood_numeric >= 4 and stress_numeric <= 2:
            return "You're doing amazing! Keep up the great work and remember to celebrate your wins! 🌟✨"
        elif mood_numeric >= 3 and stress_numeric <= 3:
            return "You're on a good path! Small steps every day lead to big changes. You've got this! 💪😊"
        elif mood_numeric <= 2 or stress_numeric >= 4:
            return "Remember, it's okay to have tough days. You're stronger than you know, and support is here when you need it. 💙🤗"
        else:
            return "Every day is a new opportunity to take care of yourself. You matter, and your wellness matters too! 💚🌈"
    
    def _get_dashboard_motivational_message(self, wellness_metrics: Dict[str, Any]) -> str:
        """Get motivational message for wellness dashboard"""
        overall_score = wellness_metrics.get("overall_score", 50)
        
        if overall_score >= 80:
            return "You're absolutely crushing your wellness goals! Your commitment to self-care is legendary! 🏆🌟"
        elif overall_score >= 60:
            return "Great progress on your wellness journey! Keep up the momentum - you're doing fantastic! 💪✨"
        elif overall_score >= 40:
            return "Every step forward counts! You're building positive habits that will serve you well. Keep going! 🌱💚"
        else:
            return "Remember, seeking support is a sign of strength. You're taking important steps by engaging with wellness resources! 💙🤝"
    
    def _auto_schedule_support(self, checkin: MentalHealthCheckIn, 
                              risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-schedule support for high-risk situations"""
        try:
            # In a real implementation, this would integrate with scheduling systems
            # For now, we'll create a support session record
            
            session = SupportSession(
                employee_id=checkin.employee_id,
                checkin_id=checkin.id,
                session_date=datetime.utcnow() + timedelta(hours=24),  # Schedule within 24 hours
                session_type=SupportType.COUNSELING.value if risk_assessment["risk_level"] == "CRITICAL" else SupportType.WELLNESS_COACHING.value,
                facilitator_type="auto_scheduled",
                session_format="to_be_determined",
                session_status="scheduled",
                privacy_level="private"
            )
            
            self.db.add(session)
            
            return {"scheduled": True, "session_id": session.id}
            
        except Exception as e:
            logger.error(f"💥 Auto-schedule support error: {e}")
            return {"scheduled": False, "error": str(e)}
    
    def _log_wellness_action(self, action: str, resource_id: int, 
                           auth_context: AuthContext, details: Dict[str, Any]):
        """Log wellness-related actions for audit trail"""
        try:
            audit_log = AuditLog(
                user_id=auth_context.user_id,
                action=action,
                resource_type="WELLNESS",
                resource_id=resource_id,
                details=details,
                ip_address=getattr(auth_context, 'ip_address', None),
                user_agent=getattr(auth_context, 'user_agent', None)
            )
            self.db.add(audit_log)
            
        except Exception as e:
            logger.error(f"💥 Wellness action logging error: {e}")

# WELLNESS UTILITIES
class WellnessReportGenerator:
    """
    Generate comprehensive wellness reports!
    More insightful than a Swiss wellness retreat with data superpowers! 📊🏔️
    """
    
    @staticmethod
    def generate_wellness_summary(employee_wellness_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive wellness summary"""
        
        overall_score = employee_wellness_data.get("overall_wellness_score", 0)
        risk_level = employee_wellness_data.get("risk_level", "unknown")
        
        # Determine wellness status
        if overall_score >= 80:
            status = "THRIVING"
            status_emoji = "🌟"
        elif overall_score >= 60:
            status = "GOOD"
            status_emoji = "😊"
        elif overall_score >= 40:
            status = "MANAGING"
            status_emoji = "😐"
        else:
            status = "NEEDS_SUPPORT"
            status_emoji = "💙"
        
        return {
            "wellness_status": status,
            "status_emoji": status_emoji,
            "overall_score": overall_score,
            "risk_level": risk_level,
            "primary_strengths": employee_wellness_data.get("positive_trends", [])[:3],
            "areas_for_focus": employee_wellness_data.get("primary_concerns", [])[:3],
            "recommended_next_steps": employee_wellness_data.get("immediate_actions", [])[:3],
            "support_available": employee_wellness_data.get("support_recommendations", [])[:3],
            "legendary_status": "WELLNESS ANALYZED WITH LEGENDARY CARE! 💚🏆"
        }
