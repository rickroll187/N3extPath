"""
Database Models for Mentor Matching Service
Where mentor-mentee relationships are stored with love! 💕📊
"""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class MentorProfile(Base):
    """Model for mentor profiles - the dating profile for career mentors!"""
    __tablename__ = "mentor_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, unique=True, nullable=False)
    expertise_areas = Column(JSON, nullable=False)  # List of expertise areas
    mentoring_capacity = Column(Integer, default=3)  # Max mentees at once
    current_mentees = Column(Integer, default=0)
    mentoring_style = Column(String(50), nullable=True)  # hands_on, advisory, coaching
    availability = Column(JSON, nullable=True)  # Available times/days
    preferred_mentee_level = Column(String(50), nullable=True)  # junior, mid, senior
    years_experience = Column(Float, nullable=False)
    successful_mentorships = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    mentorships = relationship("MentorshipRelationship", back_populates="mentor", foreign_keys="MentorshipRelationship.mentor_id")
    
    def __repr__(self):
        return f"<MentorProfile(employee_id={self.employee_id}, expertise={self.expertise_areas[:2]})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "expertise_areas": self.expertise_areas,
            "mentoring_capacity": self.mentoring_capacity,
            "current_mentees": self.current_mentees,
            "mentoring_style": self.mentoring_style,
            "availability": self.availability,
            "preferred_mentee_level": self.preferred_mentee_level,
            "years_experience": self.years_experience,
            "successful_mentorships": self.successful_mentorships,
            "average_rating": self.average_rating,
            "bio": self.bio,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class MenteeProfile(Base):
    """Model for mentee profiles - the other half of our career love story!"""
    __tablename__ = "mentee_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, unique=True, nullable=False)
    career_goals = Column(JSON, nullable=False)  # List of career goals
    skills_to_develop = Column(JSON, nullable=False)  # Skills they want to learn
    current_level = Column(String(50), nullable=False)  # junior, mid, senior
    preferred_mentoring_style = Column(String(50), nullable=True)
    availability = Column(JSON, nullable=True)
    previous_mentorships = Column(Integer, default=0)
    learning_style = Column(String(50), nullable=True)  # visual, auditory, kinesthetic
    motivation_level = Column(Float, default=5.0)  # 1-10 scale
    bio = Column(Text, nullable=True)
    is_seeking_mentor = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    mentorships = relationship("MentorshipRelationship", back_populates="mentee", foreign_keys="MentorshipRelationship.mentee_id")
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "career_goals": self.career_goals,
            "skills_to_develop": self.skills_to_develop,
            "current_level": self.current_level,
            "preferred_mentoring_style": self.preferred_mentoring_style,
            "availability": self.availability,
            "previous_mentorships": self.previous_mentorships,
            "learning_style": self.learning_style,
            "motivation_level": self.motivation_level,
            "bio": self.bio,
            "is_seeking_mentor": self.is_seeking_mentor,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class MentorshipRelationship(Base):
    """Model for mentorship relationships - where the magic happens!"""
    __tablename__ = "mentorship_relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    mentor_id = Column(Integer, ForeignKey('mentor_profiles.employee_id'), nullable=False)
    mentee_id = Column(Integer, ForeignKey('mentee_profiles.employee_id'), nullable=False)
    status = Column(String(20), default="active")  # active, completed, paused, terminated
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    duration_months = Column(Integer, default=6)
    meeting_frequency = Column(String(20), default="weekly")  # weekly, biweekly, monthly
    goals = Column(JSON, nullable=True)  # Mentorship goals
    progress_notes = Column(JSON, nullable=True)  # Progress tracking
    meetings_completed = Column(Integer, default=0)
    satisfaction_rating = Column(Float, nullable=True)  # 1-5 scale
    success_metrics = Column(JSON, nullable=True)
    completion_reason = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    mentor = relationship("MentorProfile", back_populates="mentorships", foreign_keys=[mentor_id])
    mentee = relationship("MenteeProfile", back_populates="mentorships", foreign_keys=[mentee_id])
    
    def to_dict(self):
        return {
            "id": self.id,
            "mentor_id": self.mentor_id,
            "mentee_id": self.mentee_id,
            "status": self.status,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "duration_months": self.duration_months,
            "meeting_frequency": self.meeting_frequency,
            "goals": self.goals,
            "progress_notes": self.progress_notes,
            "meetings_completed": self.meetings_completed,
            "satisfaction_rating": self.satisfaction_rating,
            "success_metrics": self.success_metrics,
            "completion_reason": self.completion_reason,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class MatchingHistory(Base):
    """Model for tracking matching history and algorithm performance"""
    __tablename__ = "matching_history"
    
    id = Column(Integer, primary_key=True, index=True)
    mentee_id = Column(Integer, nullable=False)
    potential_mentors = Column(JSON, nullable=False)  # List of suggested mentors
    algorithm_used = Column(String(50), nullable=False)
    matching_criteria = Column(JSON, nullable=False)
    compatibility_scores = Column(JSON, nullable=False)
    selected_mentor_id = Column(Integer, nullable=True)
    selection_date = Column(DateTime, nullable=True)
    fairness_metrics = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "mentee_id": self.mentee_id,
            "potential_mentors": self.potential_mentors,
            "algorithm_used": self.algorithm_used,
            "matching_criteria": self.matching_criteria,
            "compatibility_scores": self.compatibility_scores,
            "selected_mentor_id": self.selected_mentor_id,
            "selection_date": self.selection_date.isoformat() if self.selection_date else None,
            "fairness_metrics": self.fairness_metrics,
            "created_at": self.created_at.isoformat()
        }

class MentorshipFeedback(Base):
    """Model for mentorship feedback and ratings"""
    __tablename__ = "mentorship_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    mentorship_id = Column(Integer, ForeignKey('mentorship_relationships.id'), nullable=False)
    feedback_type = Column(String(20), nullable=False)  # midpoint, completion, quarterly
    mentor_rating = Column(Float, nullable=True)  # 1-5 scale
    mentee_rating = Column(Float, nullable=True)  # 1-5 scale
    relationship_satisfaction = Column(Float, nullable=True)  # 1-5 scale
    goal_achievement = Column(Float, nullable=True)  # 1-5 scale (percentage)
    communication_quality = Column(Float, nullable=True)  # 1-5 scale
    feedback_comments = Column(Text, nullable=True)
    improvement_suggestions = Column(Text, nullable=True)
    would_recommend = Column(Boolean, nullable=True)
    feedback_date = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "mentorship_id": self.mentorship_id,
            "feedback_type": self.feedback_type,
            "mentor_rating": self.mentor_rating,
            "mentee_rating": self.mentee_rating,
            "relationship_satisfaction": self.relationship_satisfaction,
            "goal_achievement": self.goal_achievement,
            "communication_quality": self.communication_quality,
            "feedback_comments": self.feedback_comments,
            "improvement_suggestions": self.improvement_suggestions,
            "would_recommend": self.would_recommend,
            "feedback_date": self.feedback_date.isoformat()
        }
