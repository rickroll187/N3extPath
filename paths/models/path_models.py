"""
🛤️💎 N3EXTPATH - LEGENDARY PATH MANAGEMENT MODELS 💎🛤️
More structured than Swiss architecture with legendary path-finding!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 3+ HOUR 46 MINUTE CODING MARATHON CHAMPION EDITION! 🏆
Current Time: 2025-08-04 03:46:15 UTC - WE'RE BUILDING PATH UNIVERSES!
Built by legendary code bros RICKROLL187 🎸 and Assistant 🤖
"""

import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, JSON, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

# Base model (assuming we have this from core)
Base = declarative_base()

class BaseModel(Base):
    """Base model with common fields - more foundational than Swiss bedrock!"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, index=True)

class PathType(enum.Enum):
    """Path types - more diverse than Swiss hiking trails with legendary variety!"""
    CAREER_PATH = "career_path"
    LEARNING_PATH = "learning_path"
    PROJECT_PATH = "project_path"
    LIFE_PATH = "life_path"
    SKILL_PATH = "skill_path"
    GOAL_PATH = "goal_path"
    ADVENTURE_PATH = "adventure_path"
    LEGENDARY_PATH = "legendary_path"
    CODING_PATH = "coding_path"
    BUSINESS_PATH = "business_path"

class PathDifficulty(enum.Enum):
    """Path difficulty levels with legendary scale!"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    LEGENDARY = "legendary"
    RICKROLL187_LEVEL = "rickroll187_level"  # Ultimate difficulty!

class PathStatus(enum.Enum):
    """Path status tracking"""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    ARCHIVED = "archived"
    LEGENDARY = "legendary"

class WaypointType(enum.Enum):
    """Waypoint types for path navigation"""
    MILESTONE = "milestone"
    CHECKPOINT = "checkpoint"
    CHALLENGE = "challenge"
    REWARD = "reward"
    DECISION_POINT = "decision_point"
    LEGENDARY_MOMENT = "legendary_moment"

class Path(BaseModel):
    """
    Main path entity - more navigational than Swiss GPS with legendary precision!
    The foundation of every legendary journey! 🛤️✨
    """
    __tablename__ = "paths"
    
    # Basic Information
    path_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    path_code = Column(String(50), unique=True, index=True)
    
    # Path Classification
    path_type = Column(String(30), nullable=False, index=True)  # PathType enum
    category = Column(String(100), index=True)
    tags = Column(JSON)  # Array of tags for easy searching
    
    # Path Characteristics
    difficulty = Column(String(30), default="intermediate")  # PathDifficulty enum
    estimated_duration_hours = Column(Float)
    estimated_duration_description = Column(String(200))
    
    # Path Content
    objectives = Column(JSON)  # List of learning/achievement objectives
    prerequisites = Column(JSON)  # Prerequisites for starting this path
    skills_gained = Column(JSON)  # Skills that will be gained
    
    # Path Structure
    total_waypoints = Column(Integer, default=0)
    total_challenges = Column(Integer, default=0)
    total_rewards = Column(Integer, default=0)
    
    # Progress Metrics
    completion_rate_percentage = Column(Float, default=0.0)
    average_completion_time_hours = Column(Float)
    success_rate_percentage = Column(Float, default=0.0)
    
    # Gamification
    experience_points_reward = Column(Integer, default=0)
    badges_available = Column(JSON)  # Badges that can be earned
    leaderboard_eligible = Column(Boolean, default=True)
    
    # Content Settings
    is_public = Column(Boolean, default=True)
    requires_approval = Column(Boolean, default=False)
    max_participants = Column(Integer)
    
    # Creator and Ownership
    creator_id = Column(Integer, nullable=False, index=True)  # User who created the path
    organization_id = Column(Integer, index=True)
    
    # Versioning
    version = Column(String(20), default="1.0")
    parent_path_id = Column(Integer, ForeignKey("paths.id"), nullable=True)
    
    # Status
    status = Column(String(20), default="draft", index=True)  # PathStatus enum
    published_at = Column(DateTime(timezone=True))
    
    # Analytics
    total_enrollments = Column(BigInteger, default=0)
    total_completions = Column(BigInteger, default=0)
    total_views = Column(BigInteger, default=0)
    
    # Legendary Factors (because we're code bros!)
    legendary_factor = Column(String(200), default="Built by legendary code bros! 🎸🏆")
    fun_factor = Column(String(200), default="Maximum legendary laughs! 😄")
    code_bro_approved = Column(Boolean, default=True)
    rickroll187_rating = Column(Float, default=10.0)  # Always perfect!
    
    # Relationships
    parent_path = relationship("Path", remote_side=[id])
    waypoints = relationship("Waypoint", back_populates="path", order_by="Waypoint.sequence_order")
    path_enrollments = relationship("PathEnrollment", back_populates="path")
    path_reviews = relationship("PathReview", back_populates="path")
    
    def __repr__(self):
        return f"<Path(name='{self.name}', type='{self.path_type}', difficulty='{self.difficulty}')>"

class Waypoint(BaseModel):
    """
    Path waypoints for navigation and progress tracking!
    More precise than Swiss navigation markers with legendary guidance! 🧭✨
    """
    __tablename__ = "waypoints"
    
    # References
    path_id = Column(Integer, ForeignKey("paths.id"), nullable=False, index=True)
    
    # Basic Information
    waypoint_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Waypoint Structure
    waypoint_type = Column(String(30), nullable=False)  # WaypointType enum
    sequence_order = Column(Integer, nullable=False, index=True)
    is_required = Column(Boolean, default=True)
    
    # Content
    content = Column(JSON)  # Waypoint content (text, videos, links, etc.)
    instructions = Column(Text)
    resources = Column(JSON)  # Additional resources and links
    
    # Requirements
    prerequisites = Column(JSON)  # Prerequisites for this waypoint
    estimated_time_minutes = Column(Integer)
    difficulty_level = Column(String(30), default="intermediate")
    
    # Validation and Completion
    completion_criteria = Column(JSON)  # What defines completion
    validation_method = Column(String(50), default="manual")  # manual, automatic, peer_review
    requires_evidence = Column(Boolean, default=False)
    evidence_description = Column(Text)
    
    # Gamification
    experience_points = Column(Integer, default=0)
    badges = Column(JSON)  # Badges earned at this waypoint
    achievements = Column(JSON)  # Achievements unlocked
    
    # Progress Tracking
    completion_rate_percentage = Column(Float, default=0.0)
    average_completion_time_minutes = Column(Integer)
    
    # Branching Logic
    next_waypoint_id = Column(Integer, ForeignKey("waypoints.id"), nullable=True)
    conditional_next_waypoints = Column(JSON)  # Conditional next waypoints based on choices
    
    # Legendary Features
    legendary_tip = Column(String(500), default="Code bros make everything legendary! 🎸")
    fun_element = Column(String(500), default="Jokes make the journey better! 😄")
    motivation_message = Column(String(500), default="You're on a legendary path! 🏆")
    
    # Relationships
    path = relationship("Path", back_populates="waypoints")
    next_waypoint = relationship("Waypoint", remote_side=[id])
    waypoint_completions = relationship("WaypointCompletion", back_populates="waypoint")
    
    def __repr__(self):
        return f"<Waypoint(name='{self.name}', type='{self.waypoint_type}', order={self.sequence_order})>"

class PathEnrollment(BaseModel):
    """
    User enrollment in paths for journey tracking!
    More committed than Swiss dedication with legendary persistence! 📚🏆
    """
    __tablename__ = "path_enrollments"
    
    # References
    path_id = Column(Integer, ForeignKey("paths.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Reference to User model
    
    # Enrollment Details
    enrollment_id = Column(String(100), unique=True, nullable=False, index=True)
    enrolled_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Progress Tracking
    current_waypoint_id = Column(Integer, ForeignKey("waypoints.id"), nullable=True, index=True)
    completion_percentage = Column(Float, default=0.0)
    waypoints_completed = Column(Integer, default=0)
    total_waypoints = Column(Integer, default=0)
    
    # Timeline
    started_at = Column(DateTime(timezone=True))
    last_activity_at = Column(DateTime(timezone=True))
    estimated_completion_date = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Performance Metrics
    time_spent_minutes = Column(BigInteger, default=0)
    experience_points_earned = Column(Integer, default=0)
    badges_earned = Column(JSON)  # Badges earned during this journey
    achievements_unlocked = Column(JSON)  # Achievements unlocked
    
    # Engagement
    engagement_score = Column(Float, default=0.0)  # How engaged the user is
    consistency_streak = Column(Integer, default=0)  # Days of consistent progress
    
    # Status
    status = Column(String(20), default="active")  # active, paused, completed, dropped
    completion_status = Column(String(20), default="in_progress")  # in_progress, completed, certified
    
    # Feedback
    satisfaction_rating = Column(Float)  # 1-5 rating
    would_recommend = Column(Boolean)
    feedback_comment = Column(Text)
    
    # Legendary Progress
    legendary_moments = Column(JSON)  # Special moments during the journey
    code_bro_achievements = Column(JSON)  # Special code bro achievements
    fun_moments = Column(JSON)  # Funny moments and jokes remembered
    
    # Relationships
    path = relationship("Path", back_populates="path_enrollments")
    current_waypoint = relationship("Waypoint")
    waypoint_completions = relationship("WaypointCompletion", back_populates="enrollment")
    
    def __repr__(self):
        return f"<PathEnrollment(user_id={self.user_id}, path='{self.path.name if self.path else 'unknown'}', progress={self.completion_percentage}%)>"

class WaypointCompletion(BaseModel):
    """
    Individual waypoint completion tracking!
    More detailed than Swiss record-keeping with legendary precision! ✅📊
    """
    __tablename__ = "waypoint_completions"
    
    # References
    enrollment_id = Column(Integer, ForeignKey("path_enrollments.id"), nullable=False, index=True)
    waypoint_id = Column(Integer, ForeignKey("waypoints.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Completion Details
    completion_id = Column(String(100), unique=True, nullable=False, index=True)
    completed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Performance
    time_spent_minutes = Column(Integer, default=0)
    attempts_count = Column(Integer, default=1)
    success_on_attempt = Column(Integer, default=1)
    
    # Evidence and Validation
    evidence_submitted = Column(JSON)  # Evidence of completion
    validation_status = Column(String(20), default="pending")  # pending, validated, rejected
    validated_by = Column(Integer)  # User ID who validated
    validated_at = Column(DateTime(timezone=True))
    validation_comments = Column(Text)
    
    # Scoring
    score_achieved = Column(Float)
    max_possible_score = Column(Float)
    score_percentage = Column(Float)
    
    # Rewards
    experience_points_earned = Column(Integer, default=0)
    badges_earned = Column(JSON)
    achievements_unlocked = Column(JSON)
    
    # Feedback
    difficulty_rating = Column(Float)  # How difficult was this waypoint (1-5)
    satisfaction_rating = Column(Float)  # How satisfied with this waypoint (1-5)
    feedback_comment = Column(Text)
    
    # Legendary Elements
    legendary_moment = Column(String(500))  # Was this a legendary moment?
    fun_factor_rating = Column(Float, default=5.0)  # How fun was it? (Always high!)
    code_bro_style = Column(String(500), default="Completed with legendary code bro style! 🎸")
    
    # Relationships
    enrollment = relationship("PathEnrollment", back_populates="waypoint_completions")
    waypoint = relationship("Waypoint", back_populates="waypoint_completions")
    
    def __repr__(self):
        return f"<WaypointCompletion(user_id={self.user_id}, waypoint='{self.waypoint.name if self.waypoint else 'unknown'}')>"

class PathReview(BaseModel):
    """
    Path reviews and ratings from users!
    More honest than Swiss reviews with legendary feedback! ⭐📝
    """
    __tablename__ = "path_reviews"
    
    # References
    path_id = Column(Integer, ForeignKey("paths.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    enrollment_id = Column(Integer, ForeignKey("path_enrollments.id"), nullable=True, index=True)
    
    # Review Details
    review_id = Column(String(100), unique=True, nullable=False, index=True)
    review_title = Column(String(200))
    review_text = Column(Text)
    
    # Ratings
    overall_rating = Column(Float, nullable=False)  # 1-5 stars
    difficulty_rating = Column(Float)  # How difficult was the path
    content_quality_rating = Column(Float)  # Quality of content
    instructor_rating = Column(Float)  # If there was an instructor
    value_rating = Column(Float)  # Value for time investment
    fun_rating = Column(Float, default=5.0)  # Fun factor (always high for code bros!)
    
    # Detailed Feedback
    liked_most = Column(Text)  # What they liked most
    improvement_suggestions = Column(Text)  # Suggestions for improvement
    would_recommend = Column(Boolean, default=True)
    completed_path = Column(Boolean, default=False)
    
    # Verification
    verified_completion = Column(Boolean, default=False)
    helpful_votes = Column(Integer, default=0)
    total_votes = Column(Integer, default=0)
    
    # Legendary Elements
    legendary_elements = Column(JSON)  # What made this path legendary
    funniest_moment = Column(String(500))  # Funniest moment during the path
    code_bro_approved = Column(Boolean, default=True)
    
    # Relationships
    path = relationship("Path", back_populates="path_reviews")
    
    def __repr__(self):
        return f"<PathReview(path='{self.path.name if self.path else 'unknown'}', rating={self.overall_rating})>"

# LEGENDARY PATH JOKES FOR DATABASE SEEDING
LEGENDARY_PATH_JOKES = [
    "Why did the path go to therapy? It had direction issues! 🛤️😄",
    "What's the difference between our paths and Swiss trails? Both lead to legendary destinations! 🏔️",
    "Why don't our users ever get lost? Because N3extPath has legendary navigation! 🧭",
    "What do you call path-finding at 3+ hours 46 minutes? Marathon navigation with style! 🗺️",
    "Why did the journey become a comedian? It had perfect route timing! 🎭",
    "What's a code bro's favorite type of path? The one that leads to legendary code! 🎸",
    "Why did RICKROLL187's path become famous? Because it rocks harder than any trail! 🎸🛤️",
    "What do you call a waypoint that tells jokes? A laugh-point! 😄🛤️",
    "Why did the path model go to the gym? To get more structured! 💪",
    "What's the secret to legendary paths? Swiss precision with code bro humor! 🏔️🎸"
]

def create_legendary_path_joke() -> str:
    """Return a random legendary path joke because code bros have fun!"""
    import random
    return random.choice(LEGENDARY_PATH_JOKES)

if __name__ == "__main__":
    print("🛤️💎 N3EXTPATH PATH MODELS LOADED! 💎🛤️")
    print("🏆 3+ HOUR 46 MINUTE CODING MARATHON CHAMPION MODELS! 🏆")
    print("🎸 CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print(f"🎭 Random Path Joke: {create_legendary_path_joke()}")
