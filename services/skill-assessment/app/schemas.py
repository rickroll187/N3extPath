"""
Pydantic Schemas for Skill Assessment Service
Where skill schemas meet validation excellence and dad jokes meet pedagogy! 🎓✨
Crafted with academic precision by rickroll187 at 2025-08-03 19:25:29 UTC
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator, EmailStr

class SkillAssessmentRequest(BaseModel):
    """Request for skill assessment - the entrance exam for excellence! 🎓"""
    employee_id: int = Field(..., description="Employee being assessed")
    skills_to_assess: List[str] = Field(..., description="List of skills to evaluate")
    assessment_type: str = Field("comprehensive", description="self, peer, manager, technical, comprehensive")
    assessment_method: str = Field("multi_modal", description="practical, theoretical, portfolio, interview, multi_modal")
    assessor_id: Optional[int] = Field(None, description="Who is conducting the assessment")
    target_role: Optional[str] = Field(None, description="Role being assessed for")
    include_market_analysis: bool = Field(True, description="Include market relevance analysis")
    include_future_skills: bool = Field(True, description="Include emerging skills assessment")
    include_bias_check: bool = Field(True, description="Include bias detection")
    assessment_depth: str = Field("standard", description="quick, standard, comprehensive, deep_dive")
    evidence_requirements: Optional[List[str]] = Field(None, description="Required evidence types")
    time_limit_minutes: Optional[int] = Field(None, description="Assessment time limit")
    
    @validator('skills_to_assess')
    def validate_skills_list(cls, v):
        if not v:
            raise ValueError("At least one skill must be specified for assessment")
        if len(v) > 20:
            raise ValueError("Cannot assess more than 20 skills at once")
        return [skill.strip().lower() for skill in v if skill.strip()]
    
    @validator('assessment_type')
    def validate_assessment_type(cls, v):
        allowed_types = ["self", "peer", "manager", "technical", "comprehensive", "360"]
        if v not in allowed_types:
            raise ValueError(f"Assessment type must be one of: {allowed_types}")
        return v
    
    @validator('assessment_depth')
    def validate_assessment_depth(cls, v):
        allowed_depths = ["quick", "standard", "comprehensive", "deep_dive"]
        if v not in allowed_depths:
            raise ValueError(f"Assessment depth must be one of: {allowed_depths}")
        return v

class SkillProficiency(BaseModel):
    """Individual skill proficiency result"""
    skill_name: str
    skill_category: str
    proficiency_level: float = Field(..., ge=0, le=100, description="Skill proficiency score")
    competency_level: str = Field(..., description="beginner, intermediate, advanced, expert")
    assessment_confidence: float = Field(..., ge=0, le=1, description="Confidence in assessment")
    market_demand_level: str = Field(..., description="low, medium, high, critical")
    skill_currency: str = Field(..., description="current, emerging, declining, obsolete")
    evidence_strength: float = Field(..., ge=0, le=1, description="Strength of evidence")
    peer_validation: Optional[float] = Field(None, ge=0, le=100, description="Peer validation score")
    recommended_actions: List[str] = Field(default_factory=list)

class SkillAssessmentResponse(BaseModel):
    """Response from skill assessment - the report card of excellence! 📊"""
    assessment_id: int
    employee_id: int
    assessor_id: Optional[int] = None
    assessment_type: str
    assessment_date: datetime
    overall_proficiency_score: float = Field(..., ge=0, le=100, description="Overall skill score")
    skill_proficiencies: List[SkillProficiency] = Field(..., description="Individual skill scores")
    strengths_identified: List[str] = Field(..., description="Key strengths discovered")
    improvement_areas: List[str] = Field(..., description="Areas needing development")
    market_relevance_score: float = Field(..., ge=0, le=100, description="Market alignment score")
    future_skill_potential: float = Field(..., ge=0, le=100, description="Growth potential")
    recommended_learning_paths: List[str] = Field(default_factory=list)
    certification_recommendations: List[str] = Field(default_factory=list)
    bias_metrics: Dict[str, float] = Field(..., description="Bias detection results")
    confidence_interval: float = Field(..., ge=0, le=1, description="Statistical confidence")
    next_assessment_date: Optional[datetime] = None
    assessment_summary: str = Field(..., description="Executive summary of assessment")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class CertificationTrackingRequest(BaseModel):
    """Request for tracking certifications - the hall of fame entry! 🏆"""
    employee_id: int = Field(..., description="Employee earning certification")
    certification_name: str = Field(..., min_length=3, max_length=200)
    certification_provider: str = Field(..., description="Organization providing certification")
    certification_type: str = Field(..., description="technical, professional, academic, vendor")
    certification_level: Optional[str] = Field(None, description="foundation, associate, professional, expert")
    certification_id: Optional[str] = Field(None, description="Certificate ID/number")
    issue_date: datetime = Field(..., description="When certification was issued")
    expiration_date: Optional[datetime] = Field(None, description="When certification expires")
    verification_url: Optional[str] = Field(None, description="Digital verification link")
    skills_covered: List[str] = Field(..., description="Skills this certification validates")
    study_hours_invested: Optional[float] = Field(None, ge=0, description="Hours spent preparing")
    exam_score: Optional[float] = Field(None, ge=0, le=100, description="Exam score if applicable")
    digital_badge_url: Optional[str] = Field(None, description="Digital badge image URL")
    
    @validator('certification_type')
    def validate_certification_type(cls, v):
        allowed_types = ["technical", "professional", "academic", "vendor", "industry"]
        if v not in allowed_types:
            raise ValueError(f"Certification type must be one of: {allowed_types}")
        return v
    
    @validator('issue_date')
    def validate_issue_date(cls, v):
        if v > datetime.now():
            raise ValueError("Issue date cannot be in the future")
        return v

class CertificationTrackingResponse(BaseModel):
    """Response from certification tracking"""
    certification_id: int
    employee_id: int
    certification_name: str
    certification_status: str
    market_value_score: float = Field(..., ge=0, le=100, description="Market value of certification")
    salary_impact_estimate: float = Field(..., description="Estimated salary impact percentage")
    career_advancement_value: float = Field(..., ge=0, le=100, description="Career progression value")
    skill_enhancement_score: float = Field(..., ge=0, le=100, description="How much this enhances skills")
    industry_recognition: str = Field(..., description="high, medium, low")
    renewal_timeline: Optional[str] = None
    recommended_next_certifications: List[str] = Field(default_factory=list)
    tracking_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SkillGapAnalysisRequest(BaseModel):
    """Request for skill gap analysis - the roadmap to excellence! 🗺️"""
    employee_id: int = Field(..., description="Employee for gap analysis")
    target_role: Optional[str] = Field(None, description="Target role to analyze against")
    target_department: Optional[str] = Field(None, description="Target department")
    analysis_scope: str = Field("individual", description="individual, team, department, organization")
    current_role: Optional[str] = Field(None, description="Current employee role")
    career_timeline: str = Field("1_year", description="6_months, 1_year, 2_years, 5_years")
    include_emerging_skills: bool = Field(True, description="Include future skill requirements")
    include_market_trends: bool = Field(True, description="Include market demand analysis")
    priority_focus: Optional[str] = Field(None, description="technical, leadership, domain, soft_skills")
    budget_constraints: Optional[float] = Field(None, ge=0, description="Budget for development")
    time_constraints: Optional[str] = Field(None, description="Time available for development")
    
    @validator('analysis_scope')
    def validate_analysis_scope(cls, v):
        allowed_scopes = ["individual", "team", "department", "organization"]
        if v not in allowed_scopes:
            raise ValueError(f"Analysis scope must be one of: {allowed_scopes}")
        return v
    
    @validator('career_timeline')
    def validate_career_timeline(cls, v):
        allowed_timelines = ["6_months", "1_year", "2_years", "5_years"]
        if v not in allowed_timelines:
            raise ValueError(f"Career timeline must be one of: {allowed_timelines}")
        return v

class SkillGap(BaseModel):
    """Individual skill gap identified"""
    skill_name: str
    current_level: float = Field(..., ge=0, le=100)
    required_level: float = Field(..., ge=0, le=100)
    gap_severity: str = Field(..., description="low, medium, high, critical")
    development_priority: int = Field(..., ge=1, le=10, description="Priority ranking")
    estimated_development_time: str = Field(..., description="Time to close gap")
    recommended_approach: List[str] = Field(..., description="How to develop this skill")
    resource_requirements: List[str] = Field(default_factory=list)
    success_metrics: List[str] = Field(default_factory=list)

class SkillGapAnalysisResponse(BaseModel):
    """Response from skill gap analysis"""
    analysis_id: int
    employee_id: int
    target_role: Optional[str] = None
    analysis_date: datetime
    identified_gaps: List[SkillGap] = Field(..., description="All skill gaps identified")
    critical_gaps: List[str] = Field(..., description="Most important gaps to address")
    quick_wins: List[str] = Field(..., description="Skills that can be developed quickly")
    long_term_development: List[str] = Field(..., description="Skills requiring significant time")
    recommended_learning_path: Dict[str, Any] = Field(..., description="Structured development plan")
    estimated_timeline: str = Field(..., description="Timeline to close all gaps")
    budget_estimate: Optional[float] = Field(None, description="Estimated development cost")
    roi_projection: Dict[str, float] = Field(..., description="Expected return on investment")
    market_urgency: Dict[str, str] = Field(..., description="Market demand urgency for skills")
    success_probability: float = Field(..., ge=0, le=1, description="Probability of successful development")
    analysis_confidence: float = Field(..., ge=0, le=1, description="Confidence in analysis")
    next_review_date: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SkillEvidenceSubmission(BaseModel):
    """Skill evidence submission"""
    employee_id: int
    skill_name: str
    evidence_type: str = Field(..., description="portfolio, project, certification, endorsement")
    evidence_title: str = Field(..., min_length=3, max_length=200)
    evidence_description: str = Field(..., description="Detailed description of evidence")
    evidence_url: Optional[str] = Field(None, description="Link to evidence")
    skill_level_demonstrated: str = Field(..., description="beginner, intermediate, advanced, expert")
    project_duration: Optional[str] = Field(None, description="Duration of project/work")
    team_size: Optional[int] = Field(None, ge=1, description="Size of team involved")
    role_in_project: Optional[str] = Field(None, description="Person's role in the project")
    technology_stack: Optional[List[str]] = Field(None, description="Technologies used")
    challenges_overcome: Optional[List[str]] = Field(None, description="Challenges faced and solved")
    impact_metrics: Optional[Dict[str, Any]] = Field(None, description="Measurable impact")
    visibility_level: str = Field("team", description="team, department, organization, public")
    
    @validator('evidence_type')
    def validate_evidence_type(cls, v):
        allowed_types = ["portfolio", "project", "certification", "endorsement", "achievement", "publication"]
        if v not in allowed_types:
            raise ValueError(f"Evidence type must be one of: {allowed_types}")
        return v

class SkillProfileSummary(BaseModel):
    """Comprehensive skill profile summary"""
    employee_id: int
    profile_completeness: float = Field(..., ge=0, le=100, description="How complete the profile is")
    total_skills_assessed: int = Field(..., description="Number of skills evaluated")
    average_proficiency: float = Field(..., ge=0, le=100, description="Average skill level")
    skill_categories: Dict[str, float] = Field(..., description="Proficiency by category")
    top_skills: List[str] = Field(..., description="Highest proficiency skills")
    emerging_skills: List[str] = Field(..., description="Skills being developed")
    certifications_earned: int = Field(..., description="Number of certifications")
    certifications_pending: int = Field(..., description="Certifications in progress")
    market_competitiveness: float = Field(..., ge=0, le=100, description="Market positioning")
    career_trajectory: str = Field(..., description="ascending, stable, developing")
    learning_velocity: float = Field(..., ge=0, le=10, description="Rate of skill development")
    skill_diversity_score: float = Field(..., ge=0, le=100, description="Breadth of skills")
    specialization_depth: float = Field(..., ge=0, le=100, description="Depth in core areas")
    future_readiness: float = Field(..., ge=0, le=100, description="Readiness for emerging trends")
    development_recommendations: List[str] = Field(..., description="Next steps for growth")
    last_assessment_date: Optional[datetime] = None
    next_assessment_due: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class MarketSkillAnalysis(BaseModel):
    """Market-wide skill analysis"""
    skill_name: str
    market_demand_level: str = Field(..., description="low, medium, high, critical")
    demand_trend: str = Field(..., description="increasing, stable, declining")
    average_salary_impact: float = Field(..., description="Percentage impact on salary")
    job_posting_frequency: int = Field(..., description="Times mentioned in job postings")
    skill_shortage_indicator: float = Field(..., ge=0, le=1, description="Supply vs demand ratio")
    geographic_demand: Dict[str, str] = Field(..., description="Demand by location")
    industry_relevance: Dict[str, float] = Field(..., description="Relevance by industry")
    career_advancement_value: float = Field(..., ge=0, le=100, description="Career progression value")
    automation_risk: float = Field(..., ge=0, le=1, description="Risk of automation")
    future_viability: str = Field(..., description="growing, stable, declining, obsolete")
    related_skills: List[str] = Field(..., description="Complementary skills")
    certification_providers: List[str] = Field(..., description="Who provides training")
    learning_resources: List[str] = Field(..., description="Where to develop this skill")

class TeamSkillAnalytics(BaseModel):
    """Team-level skill analytics"""
    team_id: int
    analysis_period: str
    team_average_proficiency: float = Field(..., ge=0, le=100)
    skill_distribution: Dict[str, Dict[str, int]] = Field(..., description="Skills by level")
    team_strengths: List[str] = Field(..., description="Collective strong skills")
    team_gaps: List[str] = Field(..., description="Skills missing from team")
    skill_coverage_percentage: float = Field(..., ge=0, le=100)
    cross_training_opportunities: List[Dict[str, Any]] = Field(..., description="Internal skill sharing")
    external_training_needs: List[str] = Field(..., description="Skills needing external development")
    skill_redundancy_analysis: Dict[str, int] = Field(..., description="Skills with multiple experts")
    succession_planning_readiness: float = Field(..., ge=0, le=100)
    innovation_potential: float = Field(..., ge=0, le=100)
    market_competitiveness: float = Field(..., ge=0, le=100)
    recommended_hires: List[str] = Field(..., description="Skills to hire for")
    team_development_priority: List[str] = Field(..., description="Priority skills to develop")

class SkillAssessmentCalibration(BaseModel):
    """Skill assessment calibration session"""
    calibration_id: int
    calibration_date: datetime
    participating_assessors: List[int]
    skills_calibrated: List[str]
    assessment_samples: List[int]  # Assessment IDs used for calibration
    pre_calibration_variance: float = Field(..., description="Variance before calibration")
    post_calibration_variance: float = Field(..., description="Variance after calibration")
    inter_rater_reliability: float = Field(..., ge=0, le=1, description="Agreement between assessors")
    calibration_effectiveness: float = Field(..., ge=0, le=1, description="How well calibration worked")
    consensus_scores: Dict[int, float] = Field(..., description="Agreed upon scores")
    outlier_assessments: List[int] = Field(..., description="Assessments needing review")
    calibration_notes: List[str] = Field(..., description="Discussion notes")
    follow_up_actions: List[str] = Field(..., description="Actions needed post-calibration")
    next_calibration_date: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BiasAuditReport(BaseModel):
    """Comprehensive bias audit for skill assessments - the fairness PhD thesis! ⚖️"""
    audit_timestamp: datetime
    audit_period_days: int
    total_assessments_audited: int
    demographic_fairness_metrics: Dict[str, Dict[str, float]]
    assessment_bias_scores: Dict[str, float]
    assessor_calibration_analysis: Dict[str, float]
    skill_category_bias_analysis: Dict[str, float]
    evidence_evaluation_fairness: Dict[str, float]
    certification_tracking_bias: Dict[str, float]
    corrective_actions_implemented: List[str]
    fairness_certification_status: str = Field(..., description="certified, provisional, needs_improvement")
    statistical_significance: float = Field(..., ge=0, le=1)
    equal_opportunity_metrics: Dict[str, float]
    adverse_impact_analysis: Dict[str, float]
    algorithmic_fairness_score: float = Field(..., ge=0, le=1)
    audit_recommendations: List[str]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BulkSkillAssessmentRequest(BaseModel):
    """Bulk skill assessment request"""
    employee_ids: List[int] = Field(..., max_items=100)
    skills_to_assess: List[str] = Field(..., max_items=20)
    assessment_type: str = Field("comprehensive")
    assessment_method: str = Field("multi_modal")
    include_market_analysis: bool = Field(True)
    include_team_analysis: bool = Field(False)
    priority_level: str = Field("standard", description="low, standard, high, urgent")
    
    @validator('employee_ids')
    def validate_employee_ids(cls, v):
        if not v:
            raise ValueError("At least one employee ID must be provided")
        if len(v) > 100:
            raise ValueError("Cannot assess more than 100 employees at once")
        return list(set(v))  # Remove duplicates

class SkillTrendAnalysis(BaseModel):
    """Skill trend analysis over time"""
    analysis_period: str
    skill_emergence_trends: Dict[str, float] = Field(..., description="New skills appearing")
    skill_decline_trends: Dict[str, float] = Field(..., description="Skills becoming less relevant")
    proficiency_improvement_trends: Dict[str, float] = Field(..., description="Skills getting better")
    market_alignment_trends: Dict[str, float] = Field(..., description="How skills align with market")
    certification_completion_trends: Dict[str, float] = Field(..., description="Certification rates")
    learning_velocity_trends: Dict[str, float] = Field(..., description="Speed of skill development")
    cross_skill_correlation: Dict[str, Dict[str, float]] = Field(..., description="Skills that develop together")
    predictive_skill_needs: Dict[str, float] = Field(..., description="Future skill requirements")
    competitive_positioning: Dict[str, str] = Field(..., description="Org vs market positioning")
    investment_roi_trends: Dict[str, float] = Field(..., description="ROI on skill development")
