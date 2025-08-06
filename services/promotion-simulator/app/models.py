"""
Database Models for Promotion Simulator Service
Where promotion predictions become permanent records!
"""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from app.database import Base

class PromotionSimulation(Base):
    """Model for storing promotion simulation results"""
    __tablename__ = "promotion_simulations"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True, nullable=False)
    target_position = Column(String(100), nullable=False)
    current_performance_score = Column(Float, nullable=False)
    years_in_current_role = Column(Float, nullable=False)
    years_with_company = Column(Float, nullable=True)
    promotion_probability = Column(Float, nullable=False)
    recommendation = Column(String(50), nullable=False)  # promote, develop, maintain
    factors_analysis = Column(JSON, nullable=True)
    development_plan = Column(JSON, nullable=True)
    simulation_algorithm = Column(String(50), default="monte_carlo")
    simulation_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PromotionSimulation(employee_id={self.employee_id}, probability={self.promotion_probability}%)>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "target_position": self.target_position,
            "current_performance_score": self.current_performance_score,
            "years_in_current_role": self.years_in_current_role,
            "years_with_company": self.years_with_company,
            "promotion_probability": self.promotion_probability,
            "recommendation": self.recommendation,
            "factors_analysis": self.factors_analysis,
            "development_plan": self.development_plan,
            "simulation_algorithm": self.simulation_algorithm,
            "simulation_date": self.simulation_date.isoformat(),
            "created_at": self.created_at.isoformat()
        }

class PromotionCriteria(Base):
    """Model for storing promotion criteria by position"""
    __tablename__ = "promotion_criteria"
    
    id = Column(Integer, primary_key=True, index=True)
    position_title = Column(String(100), unique=True, nullable=False)
    department = Column(String(50), nullable=False)
    minimum_performance_score = Column(Float, default=70.0)
    minimum_years_experience = Column(Float, default=2.0)
    required_skills = Column(JSON, nullable=False)
    preferred_skills = Column(JSON, nullable=True)
    leadership_requirements = Column(JSON, nullable=True)
    success_factors = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "position_title": self.position_title,
            "department": self.department,
            "minimum_performance_score": self.minimum_performance_score,
            "minimum_years_experience": self.minimum_years_experience,
            "required_skills": self.required_skills,
            "preferred_skills": self.preferred_skills,
            "leadership_requirements": self.leadership_requirements,
            "success_factors": self.success_factors,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class EmployeeProfile(Base):
    """Model for storing employee profiles for simulation"""
    __tablename__ = "employee_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, unique=True, nullable=False)
    current_position = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    hire_date = Column(DateTime, nullable=False)
    last_promotion_date = Column(DateTime, nullable=True)
    performance_history = Column(JSON, nullable=True)
    skills_assessment = Column(JSON, nullable=True)
    leadership_experience = Column(JSON, nullable=True)
    education = Column(JSON, nullable=True)
    certifications = Column(JSON, nullable=True)
    career_aspirations = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "current_position": self.current_position,
            "department": self.department,
            "hire_date": self.hire_date.isoformat() if self.hire_date else None,
            "last_promotion_date": self.last_promotion_date.isoformat() if self.last_promotion_date else None,
            "performance_history": self.performance_history,
            "skills_assessment": self.skills_assessment,
            "leadership_experience": self.leadership_experience,
            "education": self.education,
            "certifications": self.certifications,
            "career_aspirations": self.career_aspirations,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class PromotionBenchmark(Base):
    """Model for storing promotion benchmarks and success rates"""
    __tablename__ = "promotion_benchmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    from_position = Column(String(100), nullable=False)
    to_position = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    average_time_to_promotion = Column(Float, nullable=False)  # in years
    success_rate = Column(Float, nullable=False)  # percentage
    key_success_factors = Column(JSON, nullable=True)
    common_development_areas = Column(JSON, nullable=True)
    sample_size = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "from_position": self.from_position,
            "to_position": self.to_position,
            "department": self.department,
            "average_time_to_promotion": self.average_time_to_promotion,
            "success_rate": self.success_rate,
            "key_success_factors": self.key_success_factors,
            "common_development_areas": self.common_development_areas,
            "sample_size": self.sample_size,
            "last_updated": self.last_updated.isoformat()
        }
