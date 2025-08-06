"""
Pydantic Schemas for Talent Genome Service
Where talent request schemas meet genetic validation! 🧬✨
Crafted with DNA-level precision by rickroll187 at 2025-08-03 18:22:04 UTC
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator

class TalentAnalysisRequest(BaseModel):
    """Request for talent genome analysis - your DNA test for career success! 🧬"""
    employee_id: int = Field(..., description="Employee seeking genetic career analysis")
    analysis_depth: str = Field("comprehensive", description="quick, standard, comprehensive, deep_dive")
    include_career_predictions: bool = Field(True, description="Include future career trajectory")
    include_skill_recommendations: bool = Field(True, description="Include skill development suggestions")
    include_peer_comparisons: bool = Field(False, description="Compare with similar genetic profiles")
    prediction_horizon_years: int = Field(5, ge=1, le=10, description="Years to predict into future")
    benchmark_against_role: Optional[str] = Field(None, description="Specific role to benchmark against")
    include_market_factors: bool = Field(True, description="Include market trend analysis")
    include_bias_check: bool = Field(True, description="Include bias detection analysis")
    privacy_level: str = Field("standard", description="minimal, standard, comprehensive")
    
    @validator('analysis_depth')
    def validate_analysis_depth(cls, v):
        allowed_depths = ["quick", "standard", "comprehensive", "deep_dive"]
        if v not in allowed_depths:
            raise ValueError(f"Analysis depth must be one of: {allowed_depths}")
        return v

class TalentTrait(BaseModel):
    """Individual talent trait in the genetic profile"""
    trait_name: str
    trait_category: str = Field(..., description="cognitive, behavioral, technical, soft")
    expression_level: float = Field(..., ge=0, le=100, description="Strength of trait expression")
    dominance: str = Field(..., description="dominant, recessive, co_dominant")
    development_potential: float = Field(..., ge=0, le=100, description="Growth potential for this trait")
    market_relevance: float = Field(..., ge=0, le=100, description="Current market value")
    measurement_confidence: float = Field(..., ge=0, le=1, description="Statistical confidence")

class CareerPrediction(BaseModel):
    """Career trajectory prediction"""
    prediction_horizon_years: int
    predicted_roles: List[str] = Field(..., description="Likely future roles")
    success_probability: float = Field(..., ge=0, le=1, description="Probability of career success")
    growth_velocity: float = Field(..., description="Expected rate of career progression")
    leadership_emergence_probability: float = Field(..., ge=0, le=1)
    entrepreneurial_potential: float = Field(..., ge=0, le=1)
    skill_evolution_path: Dict[str, List[str]] = Field(..., description="How skills will evolve")
    risk_factors: List[str] = Field(default_factory=list)
    opportunity_indicators: List[str] = Field(default_factory=list)
    confidence_score: float = Field(..., ge=0, le=1)

class TalentGenomeResponse(BaseModel):
    """Response from talent genome analysis - your career DNA report! 🧬📊"""
    analysis_id: int
    employee_id: int
    genome_version: str
    overall_talent_score: float = Field(..., ge=0, le=100, description="Overall talent rating")
    genetic_markers: Dict[str, float] = Field(..., description="Key talent indicators")
    talent_traits: List[TalentTrait]
    key_strengths: List[str] = Field(..., description="Top genetic advantages")
    growth_areas: List[str] = Field(..., description="Areas for genetic enhancement")
    growth_potential: str = Field(..., description="low, medium, high, exceptional")
    learning_adaptability: float = Field(..., ge=0, le=100, description="Learning speed and flexibility")
    innovation_potential: float = Field(..., ge=0, le=100, description="Creative problem-solving ability")
    collaboration_score: float = Field(..., ge=0, le=100, description="Team synergy factor")
    leadership_genome: Optional[Dict[str, Any]] = None
    predicted_career_trajectory: Optional[CareerPrediction] = None
    skill_recommendations: List[str] = Field(default_factory=list)
    peer_comparison: Optional[Dict[str, Any]] = None
    bias_metrics: Dict[str, float] = Field(..., description="Bias detection results")
    confidence_interval: float = Field(..., ge=0, le=1, description="Statistical confidence")
    analysis_timestamp: datetime
    next_sequencing_recommended: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TalentComparisonRequest(BaseModel):
    """Request for talent genome comparison"""
    primary_employee_id: int
    comparison_employee_ids: List[int] = Field(..., max_items=10)
    comparison_criteria: List[str] = Field(default=["skills", "performance", "potential", "traits"])
    include_statistical_analysis: bool = Field(True)
    anonymize_results: bool = Field(True, description="Hide identities in comparison")
    
    @validator('comparison_employee_ids')
    def validate_comparison_ids(cls, v):
        if not v:
            raise ValueError("At least one comparison employee must be provided")
        if len(set(v)) != len(v):
            raise ValueError("Duplicate employee IDs in comparison list")
        return v

class TalentComparisonResponse(BaseModel):
    """Response from talent comparison analysis"""
    comparison_id: int
    primary_employee_id: int
    comparison_summary: Dict[str, Any]
    genetic_distance_scores: Dict[str, float] = Field(..., description="Similarity scores with each compared talent")
    shared_traits: List[str]
    unique_advantages: List[str]
    competitive_positioning: Dict[str, Any]
    development_insights: List[str]
    peer_ranking: int = Field(..., description="Rank among compared talents")
    statistical_significance: float = Field(..., ge=0, le=1)
    comparison_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class CareerTrajectoryRequest(BaseModel):
    """Request for career trajectory prediction"""
    employee_id: int
    prediction_horizon_years: int = Field(5, ge=1, le=10)
    include_market_factors: bool = Field(True)
    include_skill_evolution: bool = Field(True)
    target_roles: Optional[List[str]] = Field(None, description="Specific roles to evaluate")
    risk_tolerance: str = Field("medium", description="low, medium, high")

class SkillEvolutionAnalysis(BaseModel):
    """Skill evolution analysis over time"""
    skill_name: str
    current_level: float = Field(..., ge=0, le=100)
    growth_trajectory: str = Field(..., description="ascending, stable, declining, variable")
    growth_rate: float = Field(..., description="Rate of improvement per year")
    future_relevance: float = Field(..., ge=0, le=100, description="Market relevance in 5 years")
    investment_recommendation: str = Field(..., description="grow, maintain, pivot, deprecate")
    plateau_risk: float = Field(..., ge=0, le=1, description="Risk of skill stagnation")

class TalentBenchmarkRequest(BaseModel):
    """Request for talent benchmarking"""
    employee_id: int
    benchmark_role: str
    experience_level: str = Field(..., description="junior, mid, senior, expert")
    include_market_percentiles: bool = Field(True)
    include_development_gaps: bool = Field(True)

class TalentBenchmarkResponse(BaseModel):
    """Response from talent benchmarking"""
    employee_id: int
    benchmark_role: str
    overall_match_score: float = Field(..., ge=0, le=100)
    trait_gap_analysis: Dict[str, Dict[str, float]]
    market_percentile: float = Field(..., ge=0, le=100, description="Performance vs market")
    development_priorities: List[str]
    readiness_assessment: str = Field(..., description="ready, developing, needs_significant_development")
    time_to_readiness_months: Optional[int] = None
    benchmark_confidence: float = Field(..., ge=0, le=1)
    
class BiasAuditReport(BaseModel):
    """Comprehensive bias audit report for talent analysis - the fairness certificate! ⚖️"""
    audit_timestamp: datetime
    audit_period_days: int
    total_analyses_conducted: int
    demographic_fairness_metrics: Dict[str, Dict[str, float]]
    algorithm_bias_scores: Dict[str, float]
    trait_measurement_fairness: Dict[str, float]
    prediction_accuracy_by_group: Dict[str, float]
    recommendation_bias_detection: Dict[str, float]
    corrective_actions_implemented: List[str]
    fairness_certification_status: str = Field(..., description="certified, provisional, needs_improvement")
    statistical_parity_score: float = Field(..., ge=0, le=1)
    equalized_odds_score: float = Field(..., ge=0, le=1)
    individual_fairness_score: float = Field(..., ge=0, le=1)
    audit_recommendations: List[str]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BulkTalentAnalysisRequest(BaseModel):
    """Request for bulk talent analysis"""
    employee_ids: List[int] = Field(..., max_items=100)
    analysis_depth: str = Field("standard", description="quick, standard, comprehensive")
    include_comparisons: bool = Field(True, description="Include peer comparisons")
    include_benchmarking: bool = Field(True, description="Include role benchmarking")
    batch_processing_priority: str = Field("normal", description="low, normal, high, urgent")
    
    @validator('employee_ids')
    def validate_employee_ids(cls, v):
        if not v:
            raise ValueError("At least one employee ID must be provided")
        if len(v) > 100:
            raise ValueError("Cannot analyze more than 100 employees at once")
        return list(set(v))  # Remove duplicates

class TalentInsightResponse(BaseModel):
    """Advanced talent insights response"""
    employee_id: int
    insight_type: str = Field(..., description="strength, opportunity, risk, trend")
    insight_description: str
    supporting_data: Dict[str, Any]
    confidence_level: float = Field(..., ge=0, le=1)
    actionability_score: float = Field(..., ge=0, le=10, description="How actionable this insight is")
    priority_level: str = Field(..., description="low, medium, high, critical")
    recommended_actions: List[str]
    timeline_relevance: str = Field(..., description="immediate, short_term, medium_term, long_term")
