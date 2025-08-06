"""
Pydantic Schemas for Performance Management Service
Where performance schemas meet validation excellence! 📊✨
Crafted with performance precision by rickroll187 at 2025-08-03 19:10:09 UTC
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator

class PerformanceReviewRequest(BaseModel):
    """Request for creating a performance review - the report card for grown-ups! 📊"""
    employee_id: int = Field(..., description="Employee being reviewed")
    reviewer_id: int = Field(..., description="Person conducting the review")
    review_period_start: datetime = Field(..., description="Start of review period")
    review_period_end: datetime = Field(..., description="End of review period")
    review_type: str = Field("annual", description="annual, quarterly, mid_year, probation")
    competency_scores: Dict[str, float] = Field(..., description="Scores for each competency")
    goal_achievement_score: float = Field(..., ge=1, le=10, description="Goal achievement rating")
    strengths: List[str] = Field(..., description="Identified strengths")
    areas_for_improvement: List[str] = Field(..., description="Growth opportunities")
    reviewer_comments: Optional[str] = Field(None, description="Reviewer's detailed comments")
    employee_self_assessment: Optional[Dict[str, Any]] = Field(None, description="Employee's self-evaluation")
    development_plan: Optional[List[str]] = Field(None, description="Future development goals")
    career_aspirations: Optional[str] = Field(None, description="Employee's career goals")
    promotion_readiness: Optional[str] = Field(None, description="ready, developing, not_ready")
    
    @validator('competency_scores')
    def validate_competency_scores(cls, v):
        for competency, score in v.items():
            if not (1 <= score <= 10):
                raise ValueError(f"Competency score for {competency} must be between 1 and 10")
        return v
    
    @validator('review_type')
    def validate_review_type(cls, v):
        allowed_types = ["annual", "quarterly", "mid_year", "probation", "special"]
        if v not in allowed_types:
            raise ValueError(f"Review type must be one of: {allowed_types}")
        return v

class PerformanceReviewResponse(BaseModel):
    """Response from performance review creation"""
    review_id: int
    employee_id: int
    reviewer_id: int
    overall_score: float = Field(..., ge=1, le=10)
    performance_trend: str
    bias_score: float = Field(..., ge=0, le=1, description="Bias detection score")
    fairness_certified: bool
    next_review_date: datetime
    development_recommendations: List[str]
    review_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class GoalSettingRequest(BaseModel):
    """Request for setting employee goals - the roadmap to greatness! 🎯"""
    employee_id: int = Field(..., description="Employee setting the goal")
    goal_title: str = Field(..., min_length=3, max_length=200)
    goal_description: str = Field(..., description="Detailed goal description")
    goal_category: str = Field(..., description="performance, learning, project, behavioral")
    priority_level: str = Field("medium", description="low, medium, high, critical")
    target_completion_date: datetime = Field(..., description="Target completion date")
    success_criteria: Dict[str, Any] = Field(..., description="SMART criteria for success")
    key_milestones: Optional[List[Dict[str, Any]]] = Field(None, description="Intermediate checkpoints")
    measurement_method: str = Field(..., description="How success will be measured")
    resources_needed: Optional[List[str]] = Field(None, description="Required resources/support")
    impact_on_role: str = Field(..., description="high, medium, low")
    skill_development_areas: Optional[List[str]] = Field(None, description="Skills this goal develops")
    alignment_with_company_goals: str = Field("medium", description="high, medium, low")
    goal_setter_id: int = Field(..., description="Who is setting this goal")
    
    @validator('goal_category')
    def validate_goal_category(cls, v):
        allowed_categories = ["performance", "learning", "project", "behavioral", "career"]
        if v not in allowed_categories:
            raise ValueError(f"Goal category must be one of: {allowed_categories}")
        return v
    
    @validator('target_completion_date')
    def validate_target_date(cls, v):
        if v <= datetime.now():
            raise ValueError("Target completion date must be in the future")
        return v

class GoalSettingResponse(BaseModel):
    """Response from goal setting"""
    goal_id: int
    employee_id: int
    goal_title: str
    goal_status: str
    smart_analysis: Dict[str, bool] = Field(..., description="SMART criteria analysis")
    achievability_score: float = Field(..., ge=0, le=1)
    estimated_effort_hours: float
    milestone_schedule: List[Dict[str, Any]]
    success_probability: float = Field(..., ge=0, le=1)
    goal_creation_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class FeedbackSubmissionRequest(BaseModel):
    """Request for submitting feedback - where constructive meets constructive! 💬"""
    giver_id: int = Field(..., description="Person giving feedback")
    receiver_id: int = Field(..., description="Person receiving feedback")
    feedback_type: str = Field(..., description="peer, upward, downward, self, 360")
    feedback_category: str = Field(..., description="technical, communication, leadership, collaboration")
    feedback_content: str = Field(..., min_length=10, description="The actual feedback content")
    feedback_rating: Optional[float] = Field(None, ge=1, le=10, description="Optional numerical rating")
    specific_examples: Optional[List[str]] = Field(None, description="Concrete examples")
    suggested_improvements: Optional[str] = Field(None, description="Specific improvement suggestions")
    positive_reinforcement: Optional[str] = Field(None, description="What to keep doing")
    development_suggestions: Optional[List[str]] = Field(None, description="Development ideas")
    feedback_context: Optional[str] = Field(None, description="Project or situation context")
    anonymity_level: str = Field("identified", description="anonymous, semi_anonymous, identified")
    
    @validator('feedback_type')
    def validate_feedback_type(cls, v):
        allowed_types = ["peer", "upward", "downward", "self", "360"]
        if v not in allowed_types:
            raise ValueError(f"Feedback type must be one of: {allowed_types}")
        return v
    
    @validator('giver_id', 'receiver_id')
    def validate_ids(cls, v):
        if v <= 0:
            raise ValueError("Employee IDs must be positive integers")
        return v

class FeedbackSubmissionResponse(BaseModel):
    """Response from feedback submission"""
    feedback_id: int
    giver_id: int
    receiver_id: int
    feedback_type: str
    sentiment_analysis: Dict[str, float] = Field(..., description="AI-analyzed sentiment")
    constructiveness_score: float = Field(..., ge=0, le=1)
    actionability_score: float = Field(..., ge=0, le=1)
    bias_detection_results: Dict[str, float]
    suggested_follow_up_actions: List[str]
    feedback_quality_score: float = Field(..., ge=0, le=1)
    submission_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PerformanceMetricRequest(BaseModel):
    """Request for adding performance metrics"""
    employee_id: int
    metric_name: str = Field(..., max_length=100)
    metric_category: str = Field(..., description="productivity, quality, efficiency, collaboration")
    metric_value: float
    metric_unit: str = Field(..., max_length=20, description="percentage, count, hours, rating")
    target_value: Optional[float] = None
    measurement_period: str = Field(..., description="daily, weekly, monthly, quarterly")
    data_source: str = Field(..., description="system, manual, survey, observation")
    collection_method: str = Field(..., description="automated, self_reported, manager_assessed")
    contextual_factors: Optional[Dict[str, Any]] = None
    
    @validator('metric_value')
    def validate_metric_value(cls, v):
        if v < 0:
            raise ValueError("Metric value cannot be negative")
        return v

class PerformanceSummaryResponse(BaseModel):
    """Comprehensive performance summary"""
    employee_id: int
    current_overall_score: float = Field(..., ge=1, le=10)
    performance_trend: str = Field(..., description="improving, stable, declining, excellent")
    goal_completion_rate: float = Field(..., ge=0, le=100, description="Percentage of goals completed")
    recent_feedback_summary: Dict[str, Any]
    key_strengths: List[str]
    development_areas: List[str]
    performance_metrics_summary: Dict[str, float]
    career_progression_indicators: Dict[str, Any]
    peer_comparison: Dict[str, float] = Field(..., description="How performance compares to peers")
    manager_notes: List[str]
    recommended_next_steps: List[str]
    performance_trajectory_prediction: Dict[str, Any]
    last_review_date: Optional[datetime] = None
    next_review_date: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BiasAuditReport(BaseModel):
    """Bias audit report for performance management - the fairness certificate! ⚖️"""
    audit_timestamp: datetime
    audit_period_days: int
    total_reviews_audited: int
    total_feedback_entries_audited: int
    demographic_fairness_metrics: Dict[str, Dict[str, float]]
    review_bias_scores: Dict[str, float]
    feedback_bias_scores: Dict[str, float]
    manager_calibration_analysis: Dict[str, float]
    goal_setting_fairness: Dict[str, float]
    corrective_actions_taken: List[str]
    fairness_certification_status: str = Field(..., description="certified, provisional, needs_improvement")
    statistical_significance: float = Field(..., ge=0, le=1)
    audit_recommendations: List[str]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class GoalProgressUpdate(BaseModel):
    """Update goal progress"""
    goal_id: int
    progress_percentage: float = Field(..., ge=0, le=100)
    milestone_updates: Optional[Dict[str, Any]] = None
    obstacles_encountered: Optional[List[str]] = None
    resources_used: Optional[List[str]] = None
    lessons_learned: Optional[str] = None
    manager_support_needed: Optional[str] = None
    estimated_completion_date: Optional[datetime] = None

class TeamPerformanceAnalytics(BaseModel):
    """Team-level performance analytics"""
    team_id: int
    analysis_period: str
    team_average_score: float = Field(..., ge=1, le=10)
    performance_distribution: Dict[str, int]
    top_performers: List[Dict[str, Any]]
    improvement_candidates: List[Dict[str, Any]]
    team_strengths: List[str]
    team_development_areas: List[str]
    goal_completion_trends: Dict[str, float]
    feedback_culture_score: float = Field(..., ge=0, le=10)
    manager_effectiveness_score: float = Field(..., ge=0, le=10)
    team_collaboration_metrics: Dict[str, float]
    predictive_insights: Dict[str, Any]
    recommended_team_interventions: List[str]

class PerformanceCalibrationSession(BaseModel):
    """Performance review calibration session"""
    session_id: int
    session_date: datetime
    participating_managers: List[int]
    reviews_calibrated: List[int]
    calibration_guidelines: Dict[str, Any]
    pre_calibration_variance: float
    post_calibration_variance: float
    consensus_scores: Dict[int, float]  # employee_id -> calibrated_score
    discussion_notes: List[str]
    calibration_effectiveness: float = Field(..., ge=0, le=1)
    follow_up_actions: List[str]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
