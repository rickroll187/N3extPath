"""
Pydantic Schemas for Hiring Process Service
Where recruitment schemas meet validation excellence! 🎯✨
Crafted with hiring precision by rickroll187 at 2025-08-03 18:38:13 UTC
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator, EmailStr

class JobPostingRequest(BaseModel):
    """Request for creating a job posting - the beacon for perfect candidates! 🎯"""
    job_title: str = Field(..., description="Position title")
    department: str = Field(..., description="Department or team")
    job_description: str = Field(..., description="Detailed job description")
    required_skills: List[str] = Field(..., description="Must-have skills")
    preferred_skills: Optional[List[str]] = Field(None, description="Nice-to-have skills")
    experience_level: str = Field(..., description="junior, mid, senior, expert")
    education_requirements: Optional[List[str]] = Field(None, description="Education criteria")
    salary_range: Optional[Dict[str, float]] = Field(None, description="Min/max salary")
    location: Optional[str] = Field(None, description="Job location")
    remote_options: str = Field("hybrid", description="remote, onsite, hybrid")
    employment_type: str = Field("full_time", description="full_time, part_time, contract")
    urgency_level: str = Field("normal", description="low, normal, high, urgent")
    team_size: Optional[int] = Field(None, description="Size of the team")
    growth_opportunities: Optional[List[str]] = Field(None, description="Career growth opportunities")
    company_culture_requirements: Optional[List[str]] = Field(None, description="Cultural fit requirements")
    positions_available: int = Field(1, ge=1, description="Number of open positions")
    closing_date: Optional[datetime] = Field(None, description="Application deadline")
    
    @validator('required_skills')
    def validate_required_skills(cls, v):
        if not v:
            raise ValueError("At least one required skill must be specified")
        return [skill.strip().lower() for skill in v if skill.strip()]
    
    @validator('job_title')
    def validate_job_title(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Job title must be at least 3 characters")
        return v.strip()

class JobPostingResponse(BaseModel):
    """Response from job posting creation"""
    job_posting_id: int
    job_title: str
    department: str
    posting_status: str
    bias_score: float = Field(..., ge=0, le=1, description="Bias detection score")
    fairness_certified: bool
    applications_expected: int = Field(..., description="Estimated number of applications")
    posting_optimization_suggestions: List[str] = Field(default_factory=list)
    posting_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class CandidateProfile(BaseModel):
    """Candidate profile information"""
    candidate_name: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    current_role: Optional[str] = None
    current_company: Optional[str] = None
    years_experience: Optional[float] = Field(None, ge=0)
    skills_profile: List[str] = Field(..., description="Self-reported skills")
    education_background: Optional[List[Dict[str, str]]] = None
    career_objectives: Optional[str] = None
    salary_expectations: Optional[Dict[str, float]] = None
    availability: Optional[str] = Field(None, description="immediate, 2_weeks, 1_month, etc.")
    work_preferences: Optional[Dict[str, Any]] = None
    portfolio_links: Optional[Dict[str, str]] = None

class CandidateEvaluationRequest(BaseModel):
    """Request for candidate evaluation - where science meets hiring! 🔬"""
    candidate_id: int
    job_posting_id: int
    evaluation_depth: str = Field("standard", description="quick, standard, comprehensive, deep_dive")
    include_technical_assessment: bool = Field(True)
    include_cultural_fit_analysis: bool = Field(True)
    include_potential_assessment: bool = Field(True)
    include_bias_check: bool = Field(True)
    evaluator_notes: Optional[str] = None
    interview_feedback: Optional[Dict[str, Any]] = None
    custom_criteria: Optional[Dict[str, float]] = Field(None, description="Custom evaluation criteria")
    
    @validator('evaluation_depth')
    def validate_evaluation_depth(cls, v):
        allowed_depths = ["quick", "standard", "comprehensive", "deep_dive"]
        if v not in allowed_depths:
            raise ValueError(f"Evaluation depth must be one of: {allowed_depths}")
        return v

class SkillAssessment(BaseModel):
    """Individual skill assessment result"""
    skill_name: str
    required_level: float = Field(..., ge=0, le=100, description="Required proficiency level")
    candidate_level: float = Field(..., ge=0, le=100, description="Candidate's proficiency level")
    match_score: float = Field(..., ge=0, le=100, description="How well candidate matches requirement")
    assessment_method: str = Field(..., description="self_reported, verified, tested, interview")
    confidence_level: float = Field(..., ge=0, le=1, description="Confidence in assessment")

class HiringDecisionResponse(BaseModel):
    """Response from candidate evaluation - the hiring crystal ball! 🔮"""
    evaluation_id: int
    candidate_id: int
    job_posting_id: int
    overall_fit_score: float = Field(..., ge=0, le=100, description="Overall candidate fit")
    skills_match_score: float = Field(..., ge=0, le=100, description="Skills compatibility")
    experience_match_score: float = Field(..., ge=0, le=100, description="Experience level fit")
    cultural_fit_score: Optional[float] = Field(None, ge=0, le=100, description="Cultural alignment")
    potential_score: Optional[float] = Field(None, ge=0, le=100, description="Growth potential")
    skill_assessments: List[SkillAssessment] = Field(default_factory=list)
    key_strengths: List[str] = Field(..., description="Candidate's top strengths")
    areas_of_concern: List[str] = Field(default_factory=list, description="Potential concerns")
    hiring_recommendation: str = Field(..., description="hire, reject, interview, hold")
    recommendation_confidence: float = Field(..., ge=0, le=1, description="Confidence in recommendation")
    competitive_ranking: Optional[int] = Field(None, description="Rank among candidates")
    next_steps: List[str] = Field(..., description="Recommended next actions")
    bias_metrics: Dict[str, float] = Field(..., description="Bias detection results")
    evaluation_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ResumeAnalysisRequest(BaseModel):
    """Request for resume analysis"""
    candidate_id: int
    job_posting_id: int
    analysis_depth: str = Field("comprehensive", description="quick, standard, comprehensive")
    extract_skills: bool = Field(True)
    extract_experience: bool = Field(True)
    extract_education: bool = Field(True)
    match_against_job: bool = Field(True)

class ResumeAnalysisResponse(BaseModel):
    """Response from resume analysis"""
    candidate_id: int
    job_posting_id: int
    extracted_skills: List[str]
    experience_summary: Dict[str, Any]
    education_summary: List[Dict[str, str]]
    job_match_score: float = Field(..., ge=0, le=100, description="How well resume matches job")
    key_achievements: List[str]
    recommended_interview_questions: List[str]
    red_flags: List[str] = Field(default_factory=list)
    analysis_confidence: float = Field(..., ge=0, le=1)
    processing_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class HiringDecisionRequest(BaseModel):
    """Request for making a hiring decision"""
    candidate_id: int
    job_posting_id: int
    decision: str = Field(..., description="hire, reject, interview, hold")
    decision_rationale: str = Field(..., description="Reasoning behind the decision")
    decision_maker: str = Field(..., description="Who made this decision")
    contributing_factors: Optional[List[str]] = None
    approval_required: bool = Field(False, description="Does this need additional approval")
    notification_preferences: Optional[Dict[str, bool]] = None
    
    @validator('decision')
    def validate_decision(cls, v):
        allowed_decisions = ["hire", "reject", "interview", "hold"]
        if v not in allowed_decisions:
            raise ValueError(f"Decision must be one of: {allowed_decisions}")
        return v

class BiasAuditReport(BaseModel):
    """Comprehensive bias audit report for hiring - the fairness certificate! ⚖️"""
    audit_timestamp: datetime
    audit_period_days: int
    total_applications_processed: int
    total_candidates_evaluated: int
    total_hiring_decisions: int
    demographic_fairness_metrics: Dict[str, Dict[str, float]]
    hiring_algorithm_bias_scores: Dict[str, float]
    decision_transparency_scores: Dict[str, float]
    appeal_and_feedback_metrics: Dict[str, int]
    corrective_actions_implemented: List[str]
    fairness_certification_status: str = Field(..., description="certified, provisional, needs_improvement")
    legal_compliance_score: float = Field(..., ge=0, le=1)
    equal_opportunity_metrics: Dict[str, float]
    adverse_impact_analysis: Dict[str, float]
    audit_recommendations: List[str]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class RecruitmentAnalytics(BaseModel):
    """Recruitment analytics and metrics"""
    analytics_period: str
    total_job_postings: int
    total_applications: int
    total_hires: int
    average_time_to_hire_days: float
    average_applications_per_posting: float
    conversion_rates: Dict[str, float] = Field(..., description="Application to hire conversion")
    most_demanded_skills: List[str]
    hiring_success_by_source: Dict[str, float]
    candidate_satisfaction_metrics: Dict[str, float]
    cost_per_hire_analysis: Dict[str, float]
    diversity_hiring_metrics: Dict[str, float]
    algorithm_performance_metrics: Dict[str, float]
    market_competitiveness_analysis: Dict[str, Any]
    
class InterviewScheduleRequest(BaseModel):
    """Request for scheduling interviews"""
    candidate_id: int
    job_posting_id: int
    interview_type: str = Field(..., description="phone, video, onsite, technical")
    interviewer_ids: List[str] = Field(..., description="List of interviewer IDs")
    preferred_dates: List[datetime] = Field(..., description="Candidate's preferred dates")
    duration_minutes: int = Field(60, ge=15, le=240)
    interview_focus_areas: List[str] = Field(..., description="Technical, behavioral, cultural, etc.")
    special_requirements: Optional[List[str]] = None

class BulkCandidateEvaluationRequest(BaseModel):
    """Request for bulk candidate evaluation"""
    job_posting_id: int
    candidate_ids: List[int] = Field(..., max_items=50

