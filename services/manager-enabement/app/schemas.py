"""
Pydantic Schemas for Manager Enablement Service
Where leadership schemas meet fairness validation! 👔⚖️
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator

class LeadershipAssessmentRequest(BaseModel):
    """Request for leadership potential assessment - bias-free guaranteed!"""
    employee_id: int = Field(..., description="Employee identifier")
    current_role: str = Field(..., description="Current role/position")
    years_experience: float = Field(..., ge=0, description="Total years of experience")
    team_size: int = Field(0, ge=0, description="Current team size managed")
    previous_leadership_roles: Optional[List[str]] = Field(None, description="Previous leadership experience")
    leadership_training_completed: Optional[List[str]] = Field(None, description="Completed leadership training")
    performance_metrics: Optional[Dict[str, float]] = Field(None, description="Performance data (bias-free)")
    include_development_plan: bool = Field(True, description="Include personalized development plan")
    include_bias_check: bool = Field(True, description="Include bias detection analysis")
    
    @validator('current_role')
    def validate_current_role(cls, v):
        if not v.strip():
            raise ValueError("Current role cannot be empty")
        return v.strip()
    
    @validator('years_experience')
    def validate_experience(cls, v):
        if v < 0:
            raise ValueError("Years of experience must be non-negative")
        return v

class LeadershipCompetency(BaseModel):
    """Individual leadership competency assessment"""
    competency_name: str
    current_score: float = Field(..., ge=0, le=100, description="Current competency score (0-100)")
    target_score: float = Field(..., ge=0, le=100, description="Target competency score")
    development_priority: str = Field(..., description="low, medium, high, critical")
    improvement_recommendations: List[str]

class DevelopmentAction(BaseModel):
    """Specific development action for leadership growth"""
    action_type: str = Field(..., description="training, mentoring, experience, project")
    description: str
    priority: str = Field(..., description="low, medium, high, critical")
    estimated_duration: str
    success_metrics: List[str]
    resources_required: List[str]

class BiasMetrics(BaseModel):
    """Bias detection metrics for fairness validation"""
    bias_score: float = Field(..., ge=0, le=1, description="Overall bias score (0=no bias, 1=high bias)")
    demographic_parity: float = Field(..., description="Demographic parity metric")
    equalized_odds: float = Field(..., description="Equalized odds metric")
    statistical_parity: float = Field(..., description="Statistical parity metric")
    fairness_status: str = Field(..., description="compliant, needs_review, non_compliant")
    bias_factors: List[str] = Field(..., description="Factors contributing to bias if any")

class LeadershipDevelopmentResponse(BaseModel):
    """Response from leadership assessment - certified bias-free!"""
    assessment_id: int
    employee_id: int
    leadership_score: float = Field(..., ge=0, le=100, description="Overall leadership potential score")
    readiness_level: str = Field(..., description="not_ready, developing, ready, advanced")
    competency_breakdown: List[LeadershipCompetency]
    development_plan: Optional[List[DevelopmentAction]] = None
    estimated_development_time: Optional[str] = Field(None, description="Estimated time to leadership readiness")
    leadership_track_recommendations: List[str] = Field(..., description="Recommended leadership tracks")
    bias_metrics: Optional[BiasMetrics] = None
    assessment_timestamp: datetime
    fairness_certified: bool = Field(True, description="Certified as bias-free assessment")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class LeadershipTrainingProgram(BaseModel):
    """Leadership training program recommendation"""
    program_name: str
    program_type: str = Field(..., description="online, in_person, hybrid, mentoring")
    duration: str
    competencies_addressed: List[str]
    target_audience: str
    cost_estimate: Optional[float] = None
    provider: str
    effectiveness_rating: float = Field(..., ge=0, le=5, description="Program effectiveness rating")

class ManagerEnablementMetrics(BaseModel):
    """Metrics for manager enablement programs"""
    period: str = Field(..., description="monthly, quarterly, yearly")
    assessments_completed: int
    leadership_ready_count: int
    average_development_time: float
    program_effectiveness: float
    bias_compliance_rate: float = Field(..., ge=0, le=1, description="Rate of bias-compliant assessments")
    demographic_representation: Dict[str, float] = Field(..., description="Representation metrics")

class BiasAuditReport(BaseModel):
    """Comprehensive bias audit report"""
    audit_period: str
    total_assessments: int
    bias_compliance_rate: float
    demographic_breakdown: Dict[str, Dict[str, float]]
    fairness_metrics: Dict[str, float]
    recommended_actions: List[str]
    certification_status: str = Field(..., description="compliant, needs_improvement, non_compliant")
    audit_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BulkAssessmentRequest(BaseModel):
    """Request for bulk leadership assessment"""
    employee_ids: List[int] = Field(..., description="List of employee IDs")
    assessment_type: str = Field("standard", description="standard, comprehensive, quick")
    include_development_plans: bool = Field(True)
    include_bias_analysis: bool = Field(True)
    
    @validator('employee_ids')
    def validate_employee_ids(cls, v):
        if not v:
            raise ValueError("At least one employee ID must be provided")
        if len(v) > 100:
            raise ValueError("Cannot assess more than 100 employees at once")
        return v
