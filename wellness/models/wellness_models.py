"""
LEGENDARY EMPLOYEE WELLNESS & MENTAL HEALTH MODELS 💚🧠
More caring than a Swiss therapist with a computer science degree!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

from ...core.database.base_models import BaseModel, Employee

class WellnessCategory(enum.Enum):
    """Wellness program categories - more organized than a Swiss spa menu!"""
    MENTAL_HEALTH = "mental_health"
    PHYSICAL_FITNESS = "physical_fitness"
    WORK_LIFE_BALANCE = "work_life_balance"
    STRESS_MANAGEMENT = "stress_management"
    NUTRITION = "nutrition"
    SLEEP_HYGIENE = "sleep_hygiene"
    MINDFULNESS = "mindfulness"
    SOCIAL_CONNECTION = "social_connection"
    FINANCIAL_WELLNESS = "financial_wellness"
    CAREER_DEVELOPMENT = "career_development"

class MoodRating(enum.Enum):
    """Daily mood ratings - more expressive than Swiss emojis!"""
    EXCELLENT = "excellent"      # 😄
    GOOD = "good"               # 😊
    NEUTRAL = "neutral"         # 😐
    LOW = "low"                 # 😔
    VERY_LOW = "very_low"       # 😰

class StressLevel(enum.Enum):
    """Stress level indicators - more precise than a Swiss stress meter!"""
    MINIMAL = "minimal"         # 1-2
    LOW = "low"                # 3-4
    MODERATE = "moderate"       # 5-6
    HIGH = "high"              # 7-8
    EXTREME = "extreme"        # 9-10

class SupportType(enum.Enum):
    """Types of mental health support - more comprehensive than a Swiss wellness center!"""
    COUNSELING = "counseling"
    THERAPY = "therapy"
    PEER_SUPPORT = "peer_support"
    MANAGER_SUPPORT = "manager_support"
    EAP_PROGRAM = "eap_program"
    WELLNESS_COACHING = "wellness_coaching"
    CRISIS_INTERVENTION = "crisis_intervention"

class PrivacyLevel(enum.Enum):
    """Privacy levels for wellness data - more secure than Swiss banking!"""
    PRIVATE = "private"                    # Only employee can see
    MANAGER_VISIBLE = "manager_visible"    # Manager can see aggregated data
    HR_VISIBLE = "hr_visible"             # HR can see for support purposes
    ANONYMOUS_AGGREGATE = "anonymous_aggregate"  # Anonymous aggregated data only

class WellnessProgram(BaseModel):
    """
    Wellness programs and initiatives!
    More beneficial than a Swiss health retreat with legendary benefits! 🏔️💚
    """
    __tablename__ = "wellness_programs"
    
    # Basic Information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(50), nullable=False, index=True)  # WellnessCategory enum
    
    # Program Details
    program_type = Column(String(50), nullable=False)  # workshop, course, ongoing, etc.
    duration_weeks = Column(Integer)
    max_participants = Column(Integer)
    current_participants = Column(Integer, default=0)
    
    # Scheduling
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    meeting_schedule = Column(JSON)  # Flexible scheduling data
    location = Column(String(200))  # Physical or virtual location
    
    # Resources
    facilitator = Column(String(200))
    materials_provided = Column(JSON)  # List of materials/resources
    external_resources = Column(JSON)  # External links, apps, etc.
    
    # Tracking
    is_active = Column(Boolean, default=True, index=True)
    requires_approval = Column(Boolean, default=False)
    cost_per_participant = Column(Float, default=0.0)
    
    # Relationships
    enrollments = relationship("WellnessEnrollment", back_populates="program")
    
    def __repr__(self):
        return f"<WellnessProgram(name='{self.name}', category='{self.category}')>"

class WellnessEnrollment(BaseModel):
    """
    Employee enrollment in wellness programs!
    More organized than a Swiss registration system! 📋✅
    """
    __tablename__ = "wellness_enrollments"
    
    # References
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    program_id = Column(Integer, ForeignKey("wellness_programs.id"), nullable=False, index=True)
    
    # Enrollment Details
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now())
    completion_date = Column(DateTime(timezone=True))
    withdrawal_date = Column(DateTime(timezone=True))
    withdrawal_reason = Column(Text)
    
    # Progress Tracking
    sessions_attended = Column(Integer, default=0)
    total_sessions = Column(Integer)
    completion_percentage = Column(Float, default=0.0)
    
    # Feedback
    satisfaction_rating = Column(Integer)  # 1-10 scale
    program_feedback = Column(Text)
    would_recommend = Column(Boolean)
    
    # Status
    status = Column(String(50), default="enrolled", index=True)  # enrolled, completed, withdrawn, paused
    
    # Relationships
    employee = relationship("Employee", back_populates="wellness_enrollments")
    program = relationship("WellnessProgram", back_populates="enrollments")
    
    def __repr__(self):
        return f"<WellnessEnrollment(employee_id={self.employee_id}, program_id={self.program_id})>"

class MentalHealthCheckIn(BaseModel):
    """
    Regular mental health check-ins!
    More supportive than a Swiss counselor with unlimited patience! 🧠💙
    """
    __tablename__ = "mental_health_checkins"
    
    # Reference
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Check-in Data
    checkin_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    mood_rating = Column(String(20), nullable=False, index=True)  # MoodRating enum
    stress_level = Column(String(20), nullable=False, index=True)  # StressLevel enum
    energy_level = Column(Integer)  # 1-10 scale
    sleep_quality = Column(Integer)  # 1-10 scale
    
    # Work-related Factors
    workload_manageable = Column(Boolean)
    work_satisfaction = Column(Integer)  # 1-10 scale
    team_support_felt = Column(Boolean)
    manager_support_felt = Column(Boolean)
    
    # Personal Factors
    work_life_balance = Column(Integer)  # 1-10 scale
    physical_health = Column(Integer)  # 1-10 scale
    social_connections = Column(Integer)  # 1-10 scale
    
    # Open Feedback
    what_going_well = Column(Text)
    main_challenges = Column(Text)
    support_needed = Column(Text)
    additional_comments = Column(Text)
    
    # Privacy and Follow-up
    privacy_level = Column(String(30), default="private", index=True)  # PrivacyLevel enum
    follow_up_requested = Column(Boolean, default=False)
    follow_up_urgency = Column(String(20))  # low, medium, high, urgent
    
    # System flags (for automated support)
    risk_indicators = Column(JSON)  # Automated risk assessment
    support_recommendations = Column(JSON)  # System-generated recommendations
    
    # Relationships
    employee = relationship("Employee", back_populates="mental_health_checkins")
    support_sessions = relationship("SupportSession", back_populates="checkin")
    
    def __repr__(self):
        return f"<MentalHealthCheckIn(employee_id={self.employee_id}, mood='{self.mood_rating}', date='{self.checkin_date}')>"

class SupportSession(BaseModel):
    """
    Mental health support sessions!
    More helpful than a Swiss life coach with a psychology degree! 🤝💚
    """
    __tablename__ = "support_sessions"
    
    # References
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    checkin_id = Column(Integer, ForeignKey("mental_health_checkins.id"), nullable=True, index=True)
    
    # Session Details
    session_date = Column(DateTime(timezone=True), nullable=False, index=True)
    session_type = Column(String(30), nullable=False, index=True)  # SupportType enum
    duration_minutes = Column(Integer)
    
    # Participants
    facilitator_name = Column(String(200))
    facilitator_type = Column(String(50))  # internal_counselor, external_therapist, peer_supporter, etc.
    session_format = Column(String(30))  # individual, group, virtual, in_person
    
    # Session Content (confidential)
    session_notes = Column(Text)  # Encrypted in production
    goals_discussed = Column(JSON)
    action_items = Column(JSON)
    resources_provided = Column(JSON)
    
    # Outcomes
    employee_satisfaction = Column(Integer)  # 1-10 scale
    perceived_helpfulness = Column(Integer)  # 1-10 scale
    follow_up_needed = Column(Boolean, default=False)
    follow_up_timeline = Column(String(50))
    
    # Privacy and Compliance
    privacy_level = Column(String(30), default="private", index=True)
    confidentiality_level = Column(String(30), default="high")  # high, medium, low
    
    # Status
    session_status = Column(String(30), default="scheduled")  # scheduled, completed, cancelled, no_show
    
    # Relationships
    employee = relationship("Employee", back_populates="support_sessions")
    checkin = relationship("MentalHealthCheckIn", back_populates="support_sessions")
    
    def __repr__(self):
        return f"<SupportSession(employee_id={self.employee_id}, type='{self.session_type}', date='{self.session_date}')>"

class WellnessMetric(BaseModel):
    """
    Aggregated wellness metrics and insights!
    More insightful than a Swiss data scientist with empathy! 📊💡
    """
    __tablename__ = "wellness_metrics"
    
    # Reference
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Time Period
    metric_date = Column(DateTime(timezone=True), nullable=False, index=True)
    metric_period = Column(String(20), nullable=False, index=True)  # daily, weekly, monthly, quarterly
    
    # Wellness Scores (calculated from check-ins)
    overall_wellness_score = Column(Float)  # 0-100 composite score
    mood_average = Column(Float)
    stress_average = Column(Float)
    energy_average = Column(Float)
    sleep_quality_average = Column(Float)
    work_satisfaction_average = Column(Float)
    work_life_balance_average = Column(Float)
    
    # Engagement Metrics
    checkin_frequency = Column(Float)  # check-ins per week
    program_participation = Column(Integer)  # number of active programs
    support_session_count = Column(Integer)
    
    # Trend Analysis
    mood_trend = Column(String(20))  # improving, stable, declining
    stress_trend = Column(String(20))
    engagement_trend = Column(String(20))
    
    # Risk Assessment
    risk_score = Column(Float)  # 0-100, higher = more risk
    risk_factors = Column(JSON)  # List of identified risk factors
    protective_factors = Column(JSON)  # List of protective factors
    
    # Recommendations
    recommended_programs = Column(JSON)
    recommended_interventions = Column(JSON)
    
    # Privacy
    privacy_level = Column(String(30), default="private", index=True)
    
    # Relationships
    employee = relationship("Employee", back_populates="wellness_metrics")
    
    def __repr__(self):
        return f"<WellnessMetric(employee_id={self.employee_id}, period='{self.metric_period}', score={self.overall_wellness_score})>"

class WellnessGoal(BaseModel):
    """
    Personal wellness goals and tracking!
    More motivating than a Swiss fitness coach with attitude! 🎯💪
    """
    __tablename__ = "wellness_goals"
    
    # Reference
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Goal Details
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False, index=True)  # WellnessCategory enum
    
    # Goal Metrics
    target_value = Column(Float)
    current_value = Column(Float, default=0.0)
    measurement_unit = Column(String(50))
    
    # Timeline
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    target_date = Column(DateTime(timezone=True))
    completion_date = Column(DateTime(timezone=True))
    
    # Progress
    progress_percentage = Column(Float, default=0.0)
    milestones = Column(JSON)  # List of milestone definitions and completion status
    
    # Tracking
    is_active = Column(Boolean, default=True, index=True)
    priority_level = Column(String(20), default="medium")  # low, medium, high
    
    # Support
    accountability_partner_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    coaching_support = Column(Boolean, default=False)
    
    # Privacy
    privacy_level = Column(String(30), default="private", index=True)
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="wellness_goals")
    accountability_partner = relationship("Employee", foreign_keys=[accountability_partner_id])
    progress_logs = relationship("WellnessGoalProgress", back_populates="goal")
    
    def __repr__(self):
        return f"<WellnessGoal(employee_id={self.employee_id}, title='{self.title}', progress={self.progress_percentage}%)>"

class WellnessGoalProgress(BaseModel):
    """
    Wellness goal progress tracking!
    More encouraging than a Swiss motivational speaker! 📈🎉
    """
    __tablename__ = "wellness_goal_progress"
    
    # References
    goal_id = Column(Integer, ForeignKey("wellness_goals.id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Progress Data
    log_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    progress_value = Column(Float, nullable=False)
    progress_notes = Column(Text)
    
    # Context
    activity_type = Column(String(100))  # exercise, meditation, sleep, etc.
    mood_before = Column(String(20))
    mood_after = Column(String(20))
    
    # Validation
    verified_by_partner = Column(Boolean, default=False)
    photo_evidence = Column(String(500))  # URL to photo if provided
    
    # Relationships
    goal = relationship("WellnessGoal", back_populates="progress_logs")
    employee = relationship("Employee")
    
    def __repr__(self):
        return f"<WellnessGoalProgress(goal_id={self.goal_id}, date='{self.log_date}', value={self.progress_value})>"

# Add relationships to Employee model (if not already added)
# Employee.wellness_enrollments = relationship("WellnessEnrollment", back_populates="employee")
# Employee.mental_health_checkins = relationship("MentalHealthCheckIn", back_populates="employee")
# Employee.support_sessions = relationship("SupportSession", back_populates="employee")
# Employee.wellness_metrics = relationship("WellnessMetric", back_populates="employee")
# Employee.wellness_goals = relationship("WellnessGoal", foreign_keys="WellnessGoal.employee_id", back_populates="employee")