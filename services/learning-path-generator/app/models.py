"""
Database Models for Learning Path Generator Service
Where learning data structures meet career enlightenment! 🛤️📊
Built at 2025-08-03 18:06:49 UTC by the legendary path master rickroll187
"""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class LearningPath(Base):
    """Model for learning paths - the GPS route for your career! 🗺️"""
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True, nullable=False)
    path_name = Column(String(200), nullable=False)
    target_skills = Column(JSON, nullable=False)  # List of skills to acquire
    current_skill_levels = Column(JSON, nullable=False)  # Current proficiency levels
    difficulty_level = Column(String(20), default="intermediate")  # beginner, intermediate, advanced, expert
    learning_style = Column(String(50), nullable=True)  # visual, auditory, kinesthetic, mixed
    estimated_duration_weeks = Column(Integer, nullable=False)
    time_commitment_hours_per_week = Column(Float, default=5.0)
    path_status = Column(String(20), default="active")  # active, completed, paused, abandoned
    completion_percentage = Column(Float, default=0.0)
    personalization_factors = Column(JSON, nullable=True)  # Factors used for personalization
    bias_score = Column(Float, default=0.0)  # Bias detection score
    algorithm_version = Column(String(20), default="v2.0")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    modules = relationship("LearningModule", back_populates="learning_path", cascade="all, delete-orphan")
    progress_records = relationship("LearningProgress", back_populates="learning_path", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<LearningPath(employee_id={self.employee_id}, path='{self.path_name}', progress={self.completion_percentage}%)>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "path_name": self.path_name,
            "target_skills": self.target_skills,
            "current_skill_levels": self.current_skill_levels,
            "difficulty_level": self.difficulty_level,
            "learning_style": self.learning_style,
            "estimated_duration_weeks": self.estimated_duration_weeks,
            "time_commitment_hours_per_week": self.time_commitment_hours_per_week,
            "path_status": self.path_status,
            "completion_percentage": self.completion_percentage,
            "personalization_factors": self.personalization_factors,
            "bias_score": self.bias_score,
            "algorithm_version": self.algorithm_version,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

class LearningModule(Base):
    """Model for individual learning modules - the stepping stones to greatness! 🪨"""
    __tablename__ = "learning_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey('learning_paths.id'), nullable=False)
    module_name = Column(String(200), nullable=False)
    module_type = Column(String(50), nullable=False)  # course, video, book, practice, project, certification
    skill_focus = Column(String(100), nullable=False)  # Primary skill this module addresses
    difficulty_level = Column(String(20), nullable=False)
    estimated_hours = Column(Float, nullable=False)
    sequence_order = Column(Integer, nullable=False)  # Order in the learning path
    prerequisites = Column(JSON, nullable=True)  # Required prior modules/skills
    content_provider = Column(String(100), nullable=True)  # Coursera, Udemy, internal, etc.
    content_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    learning_objectives = Column(JSON, nullable=True)  # What you'll learn
    assessment_criteria = Column(JSON, nullable=True)  # How success is measured
    completion_status = Column(String(20), default="not_started")  # not_started, in_progress, completed, skipped
    completion_score = Column(Float, nullable=True)  # Score achieved (if applicable)
    time_spent_hours = Column(Float, default=0.0)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    learning_path = relationship("LearningPath", back_populates="modules")
    
    def __repr__(self):
        return f"<LearningModule(name='{self.module_name}', skill='{self.skill_focus}', status='{self.completion_status}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "learning_path_id": self.learning_path_id,
            "module_name": self.module_name,
            "module_type": self.module_type,
            "skill_focus": self.skill_focus,
            "difficulty_level": self.difficulty_level,
            "estimated_hours": self.estimated_hours,
            "sequence_order": self.sequence_order,
            "prerequisites": self.prerequisites,
            "content_provider": self.content_provider,
            "content_url": self.content_url,
            "description": self.description,
            "learning_objectives": self.learning_objectives,
            "assessment_criteria": self.assessment_criteria,
            "completion_status": self.completion_status,
            "completion_score": self.completion_score,
            "time_spent_hours": self.time_spent_hours,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat()
        }

class LearningProgress(Base):
    """Model for tracking detailed learning progress - because every step counts! 👣"""
    __tablename__ = "learning_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey('learning_paths.id'), nullable=False)
    employee_id = Column(Integer, index=True, nullable=False)
    progress_date = Column(DateTime, default=datetime.utcnow)
    modules_completed = Column(Integer, default=0)
    total_modules = Column(Integer, nullable=False)
    hours_invested = Column(Float, default=0.0)
    skill_improvements = Column(JSON, nullable=True)  # Skill level changes
    performance_metrics = Column(JSON, nullable=True)  # Assessment scores, etc.
    engagement_score = Column(Float, nullable=True)  # How engaged the learner is (1-10)
    difficulty_rating = Column(Float, nullable=True)  # How difficult they find it (1-10)
    satisfaction_score = Column(Float, nullable=True)  # How satisfied they are (1-10)
    notes = Column(Text, nullable=True)  # Personal notes or reflections
    milestone_achieved = Column(String(100), nullable=True)  # If any milestone was reached
    
    # Relationships
    learning_path = relationship("LearningPath", back_populates="progress_records")
    
    def to_dict(self):
        return {
            "id": self.id,
            "learning_path_id": self.learning_path_id,
            "employee_id": self.employee_id,
            "progress_date": self.progress_date.isoformat(),
            "modules_completed": self.modules_completed,
            "total_modules": self.total_modules,
            "hours_invested": self.hours_invested,
            "skill_improvements": self.skill_improvements,
            "performance_metrics": self.performance_metrics,
            "engagement_score": self.engagement_score,
            "difficulty_rating": self.difficulty_rating,
            "satisfaction_score": self.satisfaction_score,
            "notes": self.notes,
            "milestone_achieved": self.milestone_achieved
        }

class SkillDefinition(Base):
    """Model for skill definitions and learning resources - the knowledge encyclopedia! 📚"""
    __tablename__ = "skill_definitions"
    
    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(100), unique=True, nullable=False)
    skill_category = Column(String(50), nullable=False)  # technical, soft, domain, certification
    description = Column(Text, nullable=True)
    proficiency_levels = Column(JSON, nullable=False)  # beginner, intermediate, advanced, expert
    learning_resources = Column(JSON, nullable=True)  # Available courses, books, etc.
    assessment_methods = Column(JSON, nullable=True)  # How to test proficiency
    related_skills = Column(JSON, nullable=True)  # Skills that often go together
    market_demand = Column(String(20), default="medium")  # high, medium, low
    difficulty_to_learn = Column(String(20), default="medium")  # easy, medium, hard, expert
    average_learning_time_hours = Column(Float, nullable=True)
    prerequisites = Column(JSON, nullable=True)  # Skills needed before learning this
    career_impact_score = Column(Float, default=5.0)  # How much this skill impacts career (1-10)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "skill_name": self.skill_name,
            "skill_category": self.skill_category,
            "description": self.description,
            "proficiency_levels": self.proficiency_levels,
            "learning_resources": self.learning_resources,
            "assessment_methods": self.assessment_methods,
            "related_skills": self.related_skills,
            "market_demand": self.market_demand,
            "difficulty_to_learn": self.difficulty_to_learn,
            "average_learning_time_hours": self.average_learning_time_hours,
            "prerequisites": self.prerequisites,
            "career_impact_score": self.career_impact_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class LearningRecommendation(Base):
    """Model for AI-generated learning recommendations - the wise oracle speaks! 🔮"""
    __tablename__ = "learning_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True, nullable=False)
    recommendation_type = Column(String(50), nullable=False)  # skill_gap, career_advancement, trending, peer_based
    recommended_skills = Column(JSON, nullable=False)
    reasoning = Column(Text, nullable=True)  # Why this was recommended
    priority_score = Column(Float, default=5.0)  # How important this recommendation is (1-10)
    confidence_score = Column(Float, default=0.7)  # How confident the AI is (0-1)
    market_alignment = Column(Float, default=0.5)  # How well this aligns with market trends (0-1)
    personalization_factors = Column(JSON, nullable=True)  # Factors used in recommendation
    expiration_date = Column(DateTime, nullable=True)  # When this recommendation becomes stale
    acceptance_status = Column(String(20), default="pending")  # pending, accepted, rejected, expired
    feedback_score = Column(Float, nullable=True)  # User feedback on recommendation quality
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "recommendation_type": self.recommendation_type,
            "recommended_skills": self.recommended_skills,
            "reasoning": self.reasoning,
            "priority_score": self.priority_score,
            "confidence_score": self.confidence_score,
            "market_alignment": self.market_alignment,
            "personalization_factors": self.personalization_factors,
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            "acceptance_status": self.acceptance_status,
            "feedback_score": self.feedback_score,
            "created_at": self.created_at.isoformat()
        }

class PathOptimization(Base):
    """Model for tracking path optimizations - because we believe in continuous improvement! 📈"""
    __tablename__ = "path_optimizations"
    
    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey('learning_paths.id'), nullable=False)
    optimization_trigger = Column(String(50), nullable=False)  # performance, time, engagement, completion
    original_path_config = Column(JSON, nullable=False)  # What the path looked like before
    optimized_path_config = Column(JSON, nullable=False)  # What it looks like after
    optimization_algorithm = Column(String(50), default="adaptive_learning_v2")
    performance_improvement = Column(Float, nullable=True)  # Expected improvement percentage
    time_savings_hours = Column(Float, nullable=True)  # Expected time savings
    engagement_boost = Column(Float, nullable=True)  # Expected engagement improvement
    optimization_date = Column(DateTime, default=datetime.utcnow)
    success_metrics = Column(JSON, nullable=True)  # How to measure if optimization worked
    
    def to_dict(self):
        return {
            "id": self.id,
            "learning_path_id": self.learning_path_id,
            "optimization_trigger": self.optimization_trigger,
            "original_path_config": self.original_path_config,
            "optimized_path_config": self.optimized_path_config,
            "optimization_algorithm": self.optimization_algorithm,
            "performance_improvement": self.performance_improvement,
            "time_savings_hours": self.time_savings_hours,
            "engagement_boost": self.engagement_boost,
            "optimization_date": self.optimization_date.isoformat(),
            "success_metrics": self.success_metrics
        }
