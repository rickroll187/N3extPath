"""
Pydantic Schemas for Learning Path Generator Service
Where learning request schemas meet validation wizardry! 🛤️✨
Crafted with precision by rickroll187 at 2025-08-03 18:06:49 UTC
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator

class LearningPathRequest(BaseModel):
    """Request for learning path generation - your ticket to career greatness! 🎫"""
    employee_id: int = Field(..., description="Employee seeking enlightenment")
    target_skills: List[str] = Field(..., description="Skills to master")
    current_skill_level: str = Field(..., description="beginner, intermediate, advanced, expert")
    learning_style: str = Field("mixed", description="visual, auditory, kinesthetic, mixed")
    time_commitment_hours_per_week: float = Field(5.0, ge=1, le=40, description="Weekly time investment")
    preferred_difficulty: Optional[str] = Field("adaptive", description="easy, medium, hard, adaptive")
    deadline_weeks: Optional[int] = Field(None, ge=1, le=52, description="Target completion time")
    learning_preferences: Optional[Dict[str, Any]] = Field(None, description="Additional preferences")
    include_certifications: bool = Field(True, description="Include certification opportunities")
    include_practical_projects: bool = Field(True, description="Include hands-on projects")
    include_bias_check: bool = Field(True, description="Include bias detection analysis")
    
    @validator('target_skills')
    def validate_skills(cls, v):
        if not v:
            raise ValueError("At least one target skill must be specified")
        # Ensure bias-free skill names
        return [skill.lower().strip() for skill in v if skill.strip()]
    
    @validator('time_commitment_hours_per_week')
    def validate_time_commitment(cls, v):
        if v <= 0:
            raise ValueError("Time commitment must be positive")
        return v

class LearningModule(BaseModel):
    """Individual learning module in the path"""
    module_id: int
    module_name: str
    module_type: str = Field(..., description="course, video, book, practice, project, certification")
    skill_focus: str
    difficulty_level: str
    estimated_hours: float
    sequence_order: int
    prerequisites: List[str] = Field(default_factory=list)
    content_provider: Optional[str] = None
    content_url: Optional[str] = None
    description: Optional[str] = None
    learning_objectives: List[str] = Field(default_factory=list)
    assessment_criteria: Optional[Dict[str, Any]] = None

class LearningPathResponse(BaseModel):
    """Response from learning path generation - your personalized journey map! 🗺️"""
    path_id: int
    employee_id: int
    path_name: str
    target_skills: List[str]
    difficulty_level: str
    learning_style: str
    estimated_duration_weeks: int
    time_commitment_hours_per_week: float
    learning_modules: List[LearningModule]
    milestones: List[Dict[str, Any]] = Field(..., description="Key milestones in the journey")
    personalization_factors: Dict[str, Any] = Field(..., description="Factors used for personalization")
    bias_score: float = Field(..., ge=0, le=1, description="Bias detection score")
    fairness_certified: bool = Field(..., description="Certified as bias-free")
    completion_criteria: Dict[str, Any] = Field(..., description="How to measure success")
    estimated_outcomes: List[str] = Field(..., description="Expected learning outcomes")
    path_generation_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class LearningProgressUpdate(BaseModel):
    """Update learning progress"""
    learning_path_id: int
    module_id: Optional[int] = None
    completion_status: str = Field(..., description="not_started, in_progress, completed, skipped")
    time_spent_hours: float = Field(0.0, ge=0)
    completion_score: Optional[float] = Field(None, ge=0, le=100)
    engagement_score: Optional[float] = Field(None, ge=1, le=10)
    difficulty_rating: Optional[float] = Field(None, ge=1, le=10)
    satisfaction_score: Optional[float] = Field(None, ge=1, le=10)
    notes: Optional[str] = None
    skill_improvements: Optional[Dict[str, float]] = None

class LearningProgressResponse(BaseModel):
    """Learning progress tracking response"""
    employee_id: int
    learning_path_id: int
    overall_completion_percentage: float = Field(..., ge=0, le=100)
    modules_completed: int
    total_modules: int
    hours_invested: float
    current_module: Optional[Dict[str, Any]] = None
    next_milestone: Optional[Dict[str, Any]] = None
    skill_progress: Dict[str, float] = Field(..., description="Skill improvement tracking")
    engagement_trends: List[Dict[str, Any]] = Field(..., description="Engagement over time")
    estimated_completion_date: Optional[datetime] = None
    performance_insights: List[str] = Field(..., description="AI insights on performance")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SkillRoadmapRequest(BaseModel):
    """Request for skill roadmap generation"""
    skill_name: str
    current_level: str = Field("beginner", description="beginner, intermediate, advanced, expert")
    target_level: str = Field("advanced", description="beginner, intermediate, advanced, expert")
    learning_style: str = Field("mixed", description="visual, auditory, kinesthetic, mixed")
    time_budget_hours_per_week: float = Field(5.0, ge=1, le=20)
    include_certifications: bool = Field(True)
    include_practical_experience: bool = Field(True)

class SkillRoadmapResponse(BaseModel):
    """Skill roadmap response"""
    skill_name: str
    current_level: str
    target_level: str
    learning_phases: List[Dict[str, Any]] = Field(..., description="Phases of learning")
    total_duration_weeks: int
    key_milestones: List[Dict[str, Any]]
    recommended_resources: List[Dict[str, Any]]
    assessment_checkpoints: List[Dict[str, Any]]
    career_impact: Dict[str, Any] = Field(..., description="How this skill impacts career")
    market_relevance: Dict[str, Any] = Field(..., description="Market demand and trends")

class PathOptimizationRequest(BaseModel):
    """Request for learning path optimization"""
    learning_path_id: int
    performance_data: Dict[str, Any] = Field(..., description="Performance metrics and feedback")
    optimization_goals: List[str] = Field(..., description="What to optimize for")
    constraints: Optional[Dict[str, Any]] = Field(None, description="Any constraints to consider")

class PathOptimizationResponse(BaseModel):
    """Path optimization response"""
    path_id: int
    optimization_type: str
    changes_made: List[Dict[str, Any]] = Field(..., description="What was changed")
    expected_improvements: Dict[str, float] = Field(..., description="Expected performance gains")
    time_savings_hours: float = Field(..., description="Expected time savings")
    engagement_boost_percentage: float = Field(..., description="Expected engagement improvement")
    optimization_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BiasAuditReport(BaseModel):
    """Bias audit report for learning path generation - keeping it fair! ⚖️"""
    audit_period: str
    total_paths_generated: int
    demographic_distribution: Dict[str, Dict[str, float]]
    algorithm_fairness_score: float = Field(..., ge=0, le=1)
    bias_detection_flags: List[str]
    skill_recommendation_fairness: Dict[str, float]
    corrective_actions_taken: List[str]
    fairness_certification: str = Field(..., description="compliant, needs_review, non_compliant")
    audit_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class LearningRecommendation(BaseModel):
    """AI-generated learning recommendation"""
    recommendation_id: int
    employee_id: int
    recommendation_type: str = Field(..., description="skill_gap, career_advancement, trending, peer_based")
    recommended_skills: List[str]
    reasoning: str
    priority_score: float = Field(..., ge=1, le=10)
    confidence_score: float = Field(..., ge=0, le=1)
    market_alignment: float = Field(..., ge=0, le=1)
    estimated_learning_time: int = Field(..., description="Estimated weeks to complete")
    expected_career_impact: str = Field(..., description="high, medium, low")
    recommendation_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BulkPathGenerationRequest(BaseModel):
    """Request for bulk learning path generation"""
    employee_ids: List[int] = Field(..., description="List of employee IDs")
    common_target_skills: List[str] = Field(..., description="Skills for all employees")
    team_learning_goals: Optional[List[str]] = Field(None, description="Team-specific goals")
    synchronized_timeline: bool = Field(False, description="Should all paths finish together?")
    include_team_projects: bool = Field(True, description="Include collaborative learning")
    
    @validator('employee_ids')
    def validate_employee_ids(cls, v):
        if not v:
            raise ValueError("At least one employee ID must be provided")
        if len(v) > 50:
            raise ValueError("Cannot generate paths for more than 50 employees at once")
        return v
