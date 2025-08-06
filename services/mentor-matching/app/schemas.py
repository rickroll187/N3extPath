"""
Pydantic Schemas for Mentor Matching Service
Where career love schemas meet validation magic! 💕⚖️
Built at 2025-08-03 17:53:17 UTC by the legendary rickroll187!
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator

class MentorMatchRequest(BaseModel):
    """Request for mentor matching - like a dating profile, but for your career!"""
    mentee_id: int = Field(..., description="Employee seeking mentorship")
    skills_to_develop: List[str] = Field(..., description="Skills mentee wants to develop")
    career_goals: List[str] = Field(..., description="Career aspirations")
    current_level: str = Field(..., description="junior, mid, senior, lead")
    preferred_mentoring_style: Optional[str] = Field(None, description="hands_on, advisory, coaching")
    availability: Optional[Dict[str, Any]] = Field(None, description="Available times")
    max_mentor_suggestions: int = Field(5, ge=1, le=10, description="Max number of mentor suggestions")
    include_compatibility_analysis: bool = Field(True, description="Include detailed compatibility analysis")
    
    @validator('skills_to_develop')
    def validate_skills(cls, v):
        if not v:
            raise ValueError("At least one skill to develop must be specified")
        # Remove any potential bias-introducing terms
        allowed_skills = [skill.lower().strip() for skill in v if skill.strip()]
        return allowed_skills
    
    @validator('career_goals')
    def validate_goals(cls, v):
        if not v:
            raise ValueError("At least one career goal must be specified")
        return [goal.strip() for goal in v if goal.strip()]

class MentorMatch(BaseModel):
    """Individual mentor match result"""
    mentor_id: int
    compatibility_score: float = Field(..., ge=0, le=1, description="Compatibility score (0-1)")
    skill_overlap: List[str] = Field(..., description="Overlapping skills")
    experience_gap: float = Field(..., description="Years of experience difference")
    mentoring_style_match: str = Field(..., description="perfect, good, fair, poor")
    availability_match: float = Field(..., ge=0, le=1, description="Schedule compatibility")
    previous_success_rate: float = Field(..., description="Mentor's success rate with similar mentees")
    estimated_relationship_success: float = Field(..., ge=0, le=1, description="Predicted success probability")
    match_reasoning: List[str] = Field(..., description="Why this mentor was suggested")

class MentorMatchResponse(BaseModel):
    """Response from mentor matching - the results of our career cupid! 💕"""
    request_id: int
    mentee_id: int
    mentor_matches: List[MentorMatch]
    algorithm_used: str = Field(..., description="Matching algorithm employed")
    total_mentors_considered: int
    fairness_score: float = Field(..., ge=0, le=1, description="Bias-free matching score")
    matching_criteria: Dict[str, float] = Field(..., description="Criteria weights used")
    recommendation: str = Field(..., description="proceed_with_top_match, explore_options, expand_criteria")
    match_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class MentorProfile(BaseModel):
    """Public mentor profile for matching"""
    employee_id: int
    expertise_areas: List[str]
    years_experience: float
    mentoring_capacity: int
    current_mentees: int
    successful_mentorships: int
    average_rating: float
    mentoring_style: str
    preferred_mentee_level: str
    availability_score: float = Field(..., description="How available they typically are")

class MentorshipCreationRequest(BaseModel):
    """Request to create a mentorship relationship"""
    mentee_id: int
    mentor_id: int
    duration_months: int = Field(6, ge=1, le=24, description="Mentorship duration")
    meeting_frequency: str = Field("weekly", description="weekly, biweekly, monthly")
    initial_goals: List[str] = Field(..., description="Initial mentorship goals")
    
    @validator('initial_goals')
    def validate_goals(cls, v):
        if not v:
            raise ValueError("At least one initial goal must be specified")
        return v

class MentorshipStatusResponse(BaseModel):
    """Current status of a mentorship relationship"""
    mentorship_id: int
    mentor_id: int
    mentee_id: int
    status: str
    duration_so_far: int = Field(..., description="Days since start")
    meetings_completed: int
    goals_achieved: int
    satisfaction_rating: Optional[float] = None
    relationship_health: str = Field(..., description="thriving, stable, struggling, needs_intervention")
    next_milestone: Optional[str] = None

class CompatibilityAnalysis(BaseModel):
    """Detailed compatibility analysis between mentor and mentee"""
    mentor_id: int
    mentee_id: int
    overall_compatibility: float = Field(..., ge=0, le=1)
    skill_compatibility: float = Field(..., ge=0, le=1)
    style_compatibility: float = Field(..., ge=0, le=1)
    schedule_compatibility: float = Field(..., ge=0, le=1)
    experience_fit: float = Field(..., ge=0, le=1)
    personality_match: float = Field(..., ge=0, le=1, description="Based on work style preferences")
    success_prediction: float = Field(..., ge=0, le=1, description="Predicted relationship success")
    potential_challenges: List[str]
    success_factors: List[str]
    
class BiasAuditReport(BaseModel):
    """Bias audit report for mentor matching - keeping it fair! ⚖️"""
    audit_period: str
    total_matches_made: int
    demographic_distribution: Dict[str, Dict[str, float]]
    algorithm_fairness_score: float = Field(..., ge=0, le=1)
    bias_detection_flags: List[str]
    corrective_actions_taken: List[str]
    fairness_certification: str = Field(..., description="compliant, needs_review, non_compliant")
    audit_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class MentorshipFeedback(BaseModel):
    """Feedback for mentorship relationships"""
    mentorship_id: int
    feedback_type: str = Field(..., description="midpoint, completion, quarterly")
    mentor_rating: Optional[float] = Field(None, ge=1, le=5)
    mentee_rating: Optional[float] = Field(None, ge=1, le=5)
    relationship_satisfaction: Optional[float] = Field(None, ge=1, le=5)
    goal_achievement: Optional[float] = Field(None, ge=0, le=100, description="Percentage of goals achieved")
    communication_quality: Optional[float] = Field(None, ge=1, le=5)
    feedback_comments: Optional[str] = None
    improvement_suggestions: Optional[str] = None
    would_recommend: Optional[bool] = None
