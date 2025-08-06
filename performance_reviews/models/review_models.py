"""
LEGENDARY PERFORMANCE REVIEW MODELS 🎯🏆
More comprehensive than a PhD dissertation with attitude!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum
from typing import Dict, List, Optional

from ...core.database.base_models import Base, LegendaryBaseMixin

class ReviewCycle(PyEnum):
    """Review cycle types - more organized than a Swiss schedule!"""
    ANNUAL = "annual"
    SEMI_ANNUAL = "semi_annual"
    QUARTERLY = "quarterly"
    MONTHLY = "monthly"
    PROJECT_BASED = "project_based"
    PROBATIONARY = "probationary"

class ReviewStatus(PyEnum):
    """Review status tracking - more precise than a GPS!"""
    NOT_STARTED = "not_started"
    SELF_ASSESSMENT = "self_assessment"
    MANAGER_REVIEW = "manager_review"
    PEER_REVIEW = "peer_review"
    CALIBRATION = "calibration"
    COMPLETED = "completed"
    APPROVED = "approved"
    ARCHIVED = "archived"

class RatingScale(PyEnum):
    """Rating scales - more balanced than a yoga instructor!"""
    EXCEEDS_EXPECTATIONS = "exceeds_expectations"
    MEETS_EXPECTATIONS = "meets_expectations"
    PARTIALLY_MEETS = "partially_meets"
    BELOW_EXPECTATIONS = "below_expectations"
    NEEDS_IMPROVEMENT = "needs_improvement"

class PerformanceReviewCycle(Base, LegendaryBaseMixin):
    """
    Performance review cycle management!
    More organized than a Swiss train schedule! 🚂📅
    """
    __tablename__ = "performance_review_cycles"
    
    # Basic cycle info
    name = Column(String(100), nullable=False)
    cycle_type = Column(Enum(ReviewCycle), nullable=False)
    
    # Timeline
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    self_assessment_deadline = Column(DateTime(timezone=True), nullable=False)
    manager_review_deadline = Column(DateTime(timezone=True), nullable=False)
    final_deadline = Column(DateTime(timezone=True), nullable=False)
    
    # Configuration
    enable_self_assessment = Column(Boolean, default=True)
    enable_peer_reviews = Column(Boolean, default=True)
    enable_360_feedback = Column(Boolean, default=False)
    min_peer_reviewers = Column(Integer, default=2)
    max_peer_reviewers = Column(Integer, default=5)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    
    # Jokes for motivation during review season
    cycle_jokes = Column(JSON, default=lambda: [
        "Why did the performance review go to comedy school? To improve its delivery! 🎭",
        "What's the difference between our reviews and a fair judge? Nothing - both are impartial! ⚖️",
        "Why don't performance reviews get stage fright? Because they're well-prepared! 🎯",
        "What do you call a review cycle that's always on time? LEGENDARY! 🏆"
    ])
    
    def __repr__(self):
        return f"<PerformanceReviewCycle(name='{self.name}', type='{self.cycle_type}')>"

class PerformanceReview(Base, LegendaryBaseMixin):
    """
    Individual performance review!
    More comprehensive than a life biography with metrics! 📊👤
    """
    __tablename__ = "performance_reviews"
    
    # Review identification
    review_cycle_id = Column(Integer, ForeignKey("performance_review_cycles.id"), nullable=False)
    review_cycle = relationship("PerformanceReviewCycle")
    
    # Employee being reviewed
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    employee = relationship("Employee", foreign_keys=[employee_id])
    
    # Primary reviewer (usually manager)
    reviewer_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    reviewer = relationship("Employee", foreign_keys=[reviewer_id])
    
    # Review status and timeline
    status = Column(Enum(ReviewStatus), default=ReviewStatus.NOT_STARTED)
    
    # Key dates
    self_assessment_submitted_at = Column(DateTime(timezone=True), nullable=True)
    manager_review_submitted_at = Column(DateTime(timezone=True), nullable=True)
    final_review_completed_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    approved_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    approved_by = relationship("Employee", foreign_keys=[approved_by_id])
    
    # Overall ratings
    overall_rating = Column(Enum(RatingScale), nullable=True)
    overall_score = Column(Float, nullable=True)  # 0-100 scale
    
    # Self assessment
    self_assessment_data = Column(JSON, default=dict)
    self_assessment_comments = Column(Text, nullable=True)
    
    # Manager review
    manager_assessment_data = Column(JSON, default=dict)
    manager_comments = Column(Text, nullable=True)
    strengths = Column(Text, nullable=True)
    areas_for_improvement = Column(Text, nullable=True)
    
    # Goals and development
    achievements = Column(JSON, default=list)
    goals_met = Column(JSON, default=list)
    goals_missed = Column(JSON, default=list)
    development_plan = Column(JSON, default=dict)
    
    # Promotion and compensation recommendations
    promotion_ready = Column(Boolean, default=False)
    promotion_timeline = Column(String(50), nullable=True)
    salary_increase_recommended = Column(Float, nullable=True)  # Percentage
    bonus_recommended = Column(Float, nullable=True)
    
    # Calibration data
    calibration_notes = Column(Text, nullable=True)
    calibration_adjustments = Column(JSON, default=dict)
    
    # Review quality metrics
    review_completeness_score = Column(Float, default=0.0)
    bias_detection_results = Column(JSON, default=dict)
    fairness_validation_passed = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<PerformanceReview(employee_id={self.employee_id}, cycle='{self.review_cycle.name if self.review_cycle else None}')>"

class ReviewGoal(Base, LegendaryBaseMixin):
    """
    Performance goals and objectives!
    More focused than a laser with ambition! 🎯🚀
    """
    __tablename__ = "review_goals"
    
    # Goal identification
    review_id = Column(Integer, ForeignKey("performance_reviews.id"), nullable=False)
    review = relationship("PerformanceReview", backref="goals")
    
    # Goal details
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)  # PERFORMANCE, DEVELOPMENT, BEHAVIORAL, STRATEGIC
    
    # Goal metrics
    target_value = Column(Float, nullable=True)
    actual_value = Column(Float, nullable=True)
    measurement_unit = Column(String(50), nullable=True)
    
    # Timeline
    target_date = Column(DateTime(timezone=True), nullable=True)
    completion_date = Column(DateTime(timezone=True), nullable=True)
    
    # Assessment
    self_rating = Column(Enum(RatingScale), nullable=True)
    manager_rating = Column(Enum(RatingScale), nullable=True)
    final_rating = Column(Enum(RatingScale), nullable=True)
    
    # Progress tracking
    progress_percentage = Column(Float, default=0.0)
    progress_notes = Column(Text, nullable=True)
    
    # Weighting
    weight = Column(Float, default=1.0)  # Goal importance weight
    
    def __repr__(self):
        return f"<ReviewGoal(title='{self.title}', category='{self.category}')>"

class PeerReview(Base, LegendaryBaseMixin):
    """
    Peer review feedback!
    More insightful than a wise sage with people skills! 👥💡
    """
    __tablename__ = "peer_reviews"
    
    # Review linkage
    performance_review_id = Column(Integer, ForeignKey("performance_reviews.id"), nullable=False)
    performance_review = relationship("PerformanceReview", backref="peer_reviews")
    
    # Reviewer information
    reviewer_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    reviewer = relationship("Employee")
    
    # Review relationship
    relationship_type = Column(String(50), nullable=False)  # PEER, DIRECT_REPORT, CROSS_FUNCTIONAL, CLIENT
    collaboration_frequency = Column(String(20), nullable=False)  # DAILY, WEEKLY, MONTHLY, OCCASIONALLY
    
    # Feedback categories
    collaboration_rating = Column(Enum(RatingScale), nullable=True)
    communication_rating = Column(Enum(RatingScale), nullable=True)
    leadership_rating = Column(Enum(RatingScale), nullable=True)
    technical_skills_rating = Column(Enum(RatingScale), nullable=True)
    reliability_rating = Column(Enum(RatingScale), nullable=True)
    
    # Detailed feedback
    strengths = Column(Text, nullable=True)
    areas_for_improvement = Column(Text, nullable=True)
    specific_examples = Column(Text, nullable=True)
    additional_comments = Column(Text, nullable=True)
    
    # Review status
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    is_anonymous = Column(Boolean, default=True)
    
    # Quality control
    feedback_quality_score = Column(Float, default=0.0)
    contains_bias_indicators = Column(Boolean, default=False)
    bias_analysis = Column(JSON, default=dict)
    
    def __repr__(self):
        return f"<PeerReview(reviewer_id={self.reviewer_id}, relationship='{self.relationship_type}')>"

class ReviewTemplate(Base, LegendaryBaseMixin):
    """
    Review templates for consistency!
    More standardized than ISO certification with personality! 📋✨
    """
    __tablename__ = "review_templates"
    
    # Template identification
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    template_type = Column(String(50), nullable=False)  # SELF_ASSESSMENT, MANAGER_REVIEW, PEER_REVIEW
    
    # Applicability
    role_level = Column(String(50), nullable=True)  # ENTRY, MID, SENIOR, EXECUTIVE
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department = relationship("Department")
    
    # Template structure
    sections = Column(JSON, nullable=False)  # Template sections and questions
    rating_scale = Column(JSON, nullable=False)  # Rating scale definition
    
    # Configuration
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    version = Column(String(10), default="1.0")
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<ReviewTemplate(name='{self.name}', type='{self.template_type}')>"

class ReviewCalibration(Base, LegendaryBaseMixin):
    """
    Review calibration for fairness!
    More balanced than a supreme court with math skills! ⚖️📊
    """
    __tablename__ = "review_calibrations"
    
    # Calibration session
    calibration_session_id = Column(String(50), nullable=False)
    session_date = Column(DateTime(timezone=True), nullable=False)
    
    # Participants
    facilitator_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    facilitator = relationship("Employee", foreign_keys=[facilitator_id])
    participant_ids = Column(JSON, nullable=False)  # List of participant employee IDs
    
    # Reviews being calibrated
    review_ids = Column(JSON, nullable=False)  # List of review IDs
    
    # Calibration results
    rating_adjustments = Column(JSON, default=dict)  # Original vs adjusted ratings
    consensus_reached = Column(Boolean, default=False)
    discussion_notes = Column(Text, nullable=True)
    
    # Fairness metrics
    rating_distribution_before = Column(JSON, default=dict)
    rating_distribution_after = Column(JSON, default=dict)
    bias_indicators_found = Column(JSON, default=list)
    
    # Session metadata
    duration_minutes = Column(Integer, nullable=True)
    reviews_calibrated_count = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<ReviewCalibration(session_id='{self.calibration_session_id}', date='{self.session_date}')>"