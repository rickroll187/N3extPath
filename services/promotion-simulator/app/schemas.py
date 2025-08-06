"""
Pydantic Schemas for Promotion Simulator Service
Where promotion requests meet validation magic!
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator

class PromotionSimulationRequest(BaseModel):
    """Request for promotion simulation"""
    employee_id: int = Field(..., description="Employee identifier")
    target_position: str = Field(..., description="Target position for promotion")
    current_performance_score: float = Field(..., ge=0, le=100, description="Current performance score (0-100)")
    years_in_current_role: float = Field(..., ge=0, description="Years in current role")
    years_with_company: Optional[float] = Field(None, ge=0, description="Total years with company")
    skills_assessment: Optional[Dict[str, Any]] = Field(None, description="Current skills assessment")
    include_development_plan: bool = Field(True, description="Include development plan in response")
    simulation_algorithm: Optional[str] = Field("monte_carlo", description="Simulation algorithm to use")
    
    @validator('target_position')
    def validate_target_position(cls, v):
        if not v.strip():
            raise ValueError("Target position cannot be empty")
        return v.strip()
    
    @validator('current_performance_score')
    def validate_performance_score(cls, v):
        if v < 0 or v > 100:
            raise ValueError("Performance score must be between 0 and 100")
        return v

class PromotionFactor(BaseModel):
    """Individual factor affecting promotion probability"""
    factor_name: str
    current_value: float
    target_value: float
    weight: float = Field(..., description="Weight in overall calculation (0-1)")
    impact_score: float = Field(..., description="How this factor impacts promotion probability")
    improvement_needed: str = Field(..., description="none, low, medium, high, critical")

class DevelopmentAction(BaseModel):
    """Specific development action recommendation"""
    action_type: str = Field(..., description="skill, experience, leadership, certification")
    description: str
    priority: str = Field(..., description="low, medium, high, critical")
    estimated_timeline: str
    success_metrics: List[str]

class PromotionSimulationResponse(BaseModel):
    """Response from promotion simulation"""
    simulation_id: int
    employee_id: int
    target_position: str
    promotion_probability: float = Field(..., ge=0, le=100, description="Probability of promotion success (0-100)")
    recommendation: str = Field(..., description="promote, develop, maintain")
    confidence_level: str = Field(..., description="low, medium, high")
    factors_analysis: List[PromotionFactor]
    development_plan: Optional[List[DevelopmentAction]] = None
    estimated_readiness_timeline: Optional[str] = Field(None, description="When employee might be ready")
    benchmark_comparison: Dict[str, Any] = Field(..., description="How employee compares to successful promotions")
    simulation_algorithm: str
    simulation_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PromotionCriteriaRequest(BaseModel):
    """Request to get or update promotion criteria"""
    position_title: str
    department: str
    minimum_performance_score: Optional[float] = Field(70.0, ge=0, le=100)
    minimum_years_experience: Optional[float] = Field(2.0, ge=0)
    required_skills: List[str]
    preferred_skills: Optional[List[str]] = None
    leadership_requirements: Optional[Dict[str, Any]] = None

class BulkSimulationRequest(BaseModel):
    """Request for bulk promotion simulation"""
    employee_ids: List[int] = Field(..., description="List of employee IDs")
    target_position: str = Field(..., description="Target position for all employees")
    include_development_plans: bool = Field(False, description="Include development plans")
    
    @validator('employee_ids')
    def validate_employee_ids(cls, v):
        if not v:
            raise ValueError("At least one employee ID must be provided")
        if len(v) > 50:
            raise ValueError("Cannot simulate more than 50 employees at once")
        return v

class PromotionBenchmarkResponse(BaseModel):
    """Response with promotion benchmark data"""
    from_position: str
    to_position: str
    department: str
    average_time_to_promotion: float
    success_rate: float
    key_success_factors: List[str]
    common_development_areas: List[str]
    sample_size: int
    
class PromotionTrend(BaseModel):
    """Promotion trend analysis"""
    period: str = Field(..., description="monthly, quarterly, yearly")
    promotions_count: int
    success_rate: float
    average_timeline: float
    top_promoting_departments: List[Dict[str, Any]]
    trending_skills: List[str]
