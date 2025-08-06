"""
Pydantic Schemas for Training-to-Role Service
Where data validation meets career dreams!
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator

class SkillLevel(BaseModel):
    """Individual skill with proficiency level"""
    name: str = Field(..., description="Skill name")
    level: str = Field(..., description="Proficiency level (beginner, intermediate, advanced, expert)")
    years_experience: Optional[float] = Field(None, description="Years of experience with this skill")

class SkillMatchRequest(BaseModel):
    """Request for skill matching analysis"""
    employee_id: int = Field(..., description="Employee identifier")
    current_skills: List[SkillLevel] = Field(..., description="Current skills and levels")
    target_role: str = Field(..., description="Target role for career development")
    include_training_recommendations: bool = Field(True, description="Include training recommendations")
    
    @validator('current_skills')
    def validate_skills(cls, v):
        if not v:
            raise ValueError("At least one current skill must be provided")
        return v
    
    @validator('target_role')
    def validate_target_role(cls, v):
        if not v.strip():
            raise ValueError("Target role cannot be empty")
        return v.strip()

class SkillGap(BaseModel):
    """Represents a skill gap between current and required"""
    skill_name: str
    current_level: Optional[str] = None
    required_level: str
    gap_severity: str = Field(..., description="low, medium, high, critical")
    training_priority: str = Field(..., description="low, medium, high")

class TrainingRecommendation(BaseModel):
    """Training recommendation for a skill"""
    skill_name: str
    recommended_courses: List[str]
    estimated_duration_hours: int
    priority: str
    learning_path: List[str]

class SkillMatchResponse(BaseModel):
    """Response from skill matching analysis"""
    analysis_id: int
    employee_id: int
    target_role: str
    match_score: float = Field(..., description="Overall match score (0-100)")
    skill_gaps: List[SkillGap]
    training_recommendations: Optional[List[TrainingRecommendation]] = None
    estimated_training_time: Optional[int] = Field(None, description="Total estimated training time in hours")
    career_readiness: str = Field(..., description="ready, needs_development, significant_gaps")
    analysis_timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class RoleRequirementsRequest(BaseModel):
    """Request to get role requirements"""
    role_title: str
    department: Optional[str] = None
    level: Optional[str] = None

class RoleRequirementsResponse(BaseModel):
    """Response with role requirements"""
    role_title: str
    department: str
    level: str
    required_skills: List[SkillLevel]
    preferred_skills: Optional[List[SkillLevel]] = None
    description: Optional[str] = None
    
class SkillAnalysisHistory(BaseModel):
    """Historical skill analysis data"""
    analysis_id: int
    analysis_date: datetime
    target_role: str
    match_score: float
    improvements_since_last: Optional[Dict[str, Any]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BulkSkillAnalysisRequest(BaseModel):
    """Request for bulk skill analysis"""
    employee_ids: List[int] = Field(..., description="List of employee IDs to analyze")
    target_role: str = Field(..., description="Target role for all employees")
    include_training_recommendations: bool = Field(True)
    
    @validator('employee_ids')
    def validate_employee_ids(cls, v):
        if not v:
            raise ValueError("At least one employee ID must be provided")
        if len(v) > 100:  # Reasonable limit
            raise ValueError("Cannot process more than 100 employees at once")
        return v
