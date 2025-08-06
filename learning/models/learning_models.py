"""
LEGENDARY EMPLOYEE LEARNING & DEVELOPMENT MODELS 📚🚀
More educational than a Swiss university with legendary knowledge!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

from ...core.database.base_models import BaseModel, Employee, User

class CourseStatus(enum.Enum):
    """Course status - more organized than a Swiss curriculum!"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    UNDER_REVIEW = "under_review"

class EnrollmentStatus(enum.Enum):
    """Enrollment status tracking"""
    ENROLLED = "enrolled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"
    DROPPED = "dropped"
    FAILED = "failed"

class SkillLevel(enum.Enum):
    """Skill proficiency levels - more precise than Swiss measurements!"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    MASTER = "master"

class LearningPathType(enum.Enum):
    """Learning path types for career progression"""
    ONBOARDING = "onboarding"
    CAREER_TRACK = "career_track"
    SKILL_DEVELOPMENT = "skill_development"
    LEADERSHIP = "leadership"
    COMPLIANCE = "compliance"
    CERTIFICATION = "certification"

class AssessmentType(enum.Enum):
    """Assessment types for measuring progress"""
    QUIZ = "quiz"
    PROJECT = "project"
    PEER_REVIEW = "peer_review"
    PRACTICAL_EXAM = "practical_exam"
    PORTFOLIO = "portfolio"
    PRESENTATION = "presentation"

class SkillCategory(BaseModel):
    """
    Skill categories for organized learning!
    More structured than a Swiss education system! 🎓📊
    """
    __tablename__ = "skill_categories"
    
    # Basic Information
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    icon = Column(String(50))  # Icon name/URL
    color = Column(String(20))  # Hex color code
    
    # Organization
    parent_category_id = Column(Integer, ForeignKey("skill_categories.id"), nullable=True)
    sort_order = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    parent_category = relationship("SkillCategory", remote_side="SkillCategory.id")
    sub_categories = relationship("SkillCategory", back_populates="parent_category")
    skills = relationship("Skill", back_populates="category")
    
    def __repr__(self):
        return f"<SkillCategory(name='{self.name}')>"

class Skill(BaseModel):
    """
    Individual skills that are more valuable than Swiss precision!
    More comprehensive than a legendary skill database! 💎🛠️
    """
    __tablename__ = "skills"
    
    # Basic Information
    name = Column(String(150), nullable=False, index=True)
    description = Column(Text)
    short_description = Column(String(300))
    
    # Organization
    category_id = Column(Integer, ForeignKey("skill_categories.id"), nullable=False, index=True)
    skill_code = Column(String(50), unique=True, index=True)  # Unique identifier
    
    # Skill Properties
    difficulty_level = Column(String(20), default="intermediate")  # SkillLevel enum
    estimated_hours = Column(Integer)  # Hours to master
    prerequisites = Column(JSON)  # List of prerequisite skill IDs
    
    # Validation & Certification
    is_certifiable = Column(Boolean, default=False)
    certification_authority = Column(String(200))
    certification_url = Column(String(500))
    
    # Trending & Popularity
    demand_score = Column(Float, default=0.0)  # Market demand (0-100)
    trending_score = Column(Float, default=0.0)  # Trending indicator
    
    # Metadata
    tags = Column(JSON)  # List of tags for searchability
    external_resources = Column(JSON)  # External learning resources
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    category = relationship("SkillCategory", back_populates="skills")
    employee_skills = relationship("EmployeeSkill", back_populates="skill")
    course_skills = relationship("CourseSkill", back_populates="skill")
    
    def __repr__(self):
        return f"<Skill(name='{self.name}', level='{self.difficulty_level}')>"

class EmployeeSkill(BaseModel):
    """
    Employee skill proficiencies and development tracking!
    More personalized than a Swiss learning profile! 👤📈
    """
    __tablename__ = "employee_skills"
    
    # References
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False, index=True)
    
    # Proficiency
    current_level = Column(String(20), default="beginner")  # SkillLevel enum
    target_level = Column(String(20))  # SkillLevel enum
    proficiency_score = Column(Float, default=0.0)  # 0-100 score
    
    # Assessment
    last_assessed_at = Column(DateTime(timezone=True))
    assessed_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    assessment_notes = Column(Text)
    
    # Progress Tracking
    hours_invested = Column(Float, default=0.0)
    courses_completed = Column(Integer, default=0)
    certifications_earned = Column(JSON)  # List of certification details
    
    # Goals & Development
    development_priority = Column(String(20), default="medium")  # high, medium, low
    target_completion_date = Column(DateTime(timezone=True))
    learning_plan_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=True)
    
    # Validation
    is_validated = Column(Boolean, default=False)
    validated_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    validated_at = Column(DateTime(timezone=True))
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    skill = relationship("Skill", back_populates="employee_skills")
    assessed_by = relationship("Employee", foreign_keys=[assessed_by_id])
    validated_by = relationship("Employee", foreign_keys=[validated_by_id])
    learning_plan = relationship("LearningPath", foreign_keys=[learning_plan_id])
    
    def __repr__(self):
        return f"<EmployeeSkill(employee_id={self.employee_id}, skill='{self.skill.name}', level='{self.current_level}')>"

class Course(BaseModel):
    """
    Learning courses that are more engaging than Swiss education!
    More comprehensive than a legendary educational experience! 🎓✨
    """
    __tablename__ = "courses"
    
    # Basic Information
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    short_description = Column(String(500))
    course_code = Column(String(50), unique=True, index=True)
    
    # Course Properties
    difficulty_level = Column(String(20), default="intermediate")  # SkillLevel enum
    estimated_duration_hours = Column(Float, nullable=False)
    max_participants = Column(Integer)
    min_participants = Column(Integer, default=1)
    
    # Content & Structure
    learning_objectives = Column(JSON)  # List of learning objectives
    course_outline = Column(JSON)  # Structured course content
    prerequisites = Column(JSON)  # Required skills or courses
    
    # Delivery
    delivery_method = Column(String(30), default="online")  # online, in_person, hybrid, self_paced
    instructor_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    external_instructor = Column(String(200))  # External instructor name
    
    # Scheduling
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    enrollment_deadline = Column(DateTime(timezone=True))
    
    # Resources
    materials = Column(JSON)  # Course materials and resources
    external_resources = Column(JSON)  # External links and resources
    platform_url = Column(String(500))  # LMS or external platform URL
    
    # Pricing & Cost
    cost_per_participant = Column(Float, default=0.0)
    is_free = Column(Boolean, default=True)
    budget_account = Column(String(100))  # Budget account for tracking
    
    # Certification
    provides_certification = Column(Boolean, default=False)
    certificate_template = Column(String(500))  # Path to certificate template
    certification_authority = Column(String(200))
    
    # Analytics
    enrollment_count = Column(Integer, default=0)
    completion_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    total_ratings = Column(Integer, default=0)
    
    # Status
    status = Column(String(20), default="draft", index=True)  # CourseStatus enum
    is_featured = Column(Boolean, default=False)
    
    # Relationships
    instructor = relationship("Employee", foreign_keys=[instructor_id])
    enrollments = relationship("CourseEnrollment", back_populates="course")
    skills = relationship("CourseSkill", back_populates="course")
    assessments = relationship("CourseAssessment", back_populates="course")
    
    def __repr__(self):
        return f"<Course(title='{self.title}', status='{self.status}')>"

class CourseSkill(BaseModel):
    """
    Skills associated with courses!
    More connected than Swiss networking with legendary precision! 🔗🎯
    """
    __tablename__ = "course_skills"
    
    # References
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False, index=True)
    
    # Skill Development
    skill_weight = Column(Float, default=1.0)  # Importance of this skill in the course
    expected_improvement = Column(Float)  # Expected skill level improvement (0-100)
    skill_focus = Column(String(20), default="primary")  # primary, secondary, supplementary
    
    # Relationships
    course = relationship("Course", back_populates="skills")
    skill = relationship("Skill", back_populates="course_skills")
    
    def __repr__(self):
        return f"<CourseSkill(course_id={self.course_id}, skill_id={self.skill_id})>"

class CourseEnrollment(BaseModel):
    """
    Course enrollments and progress tracking!
    More engaging than a Swiss student record system! 📋🎓
    """
    __tablename__ = "course_enrollments"
    
    # References
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Enrollment Details
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    enrolled_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)  # Manager or self
    enrollment_reason = Column(Text)
    
    # Progress Tracking
    status = Column(String(20), default="enrolled", index=True)  # EnrollmentStatus enum
    progress_percentage = Column(Float, default=0.0)
    last_accessed_at = Column(DateTime(timezone=True))
    
    # Completion
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    completion_certificate_url = Column(String(500))
    
    # Assessment
    final_score = Column(Float)  # 0-100 score
    grade = Column(String(10))  # Letter grade or pass/fail
    assessment_attempts = Column(Integer, default=0)
    
    # Feedback
    course_rating = Column(Integer)  # 1-5 star rating
    course_review = Column(Text)
    instructor_rating = Column(Integer)  # 1-5 star rating
    would_recommend = Column(Boolean)
    
    # Time Tracking
    total_time_spent_hours = Column(Float, default=0.0)
    estimated_completion_date = Column(DateTime(timezone=True))
    
    # Status Changes
    paused_at = Column(DateTime(timezone=True))
    paused_reason = Column(Text)
    dropped_at = Column(DateTime(timezone=True))
    drop_reason = Column(Text)
    
    # Relationships
    course = relationship("Course", back_populates="enrollments")
    employee = relationship("Employee")
    enrolled_by = relationship("Employee", foreign_keys=[enrolled_by_id])
    
    def __repr__(self):
        return f"<CourseEnrollment(course_id={self.course_id}, employee_id={self.employee_id}, status='{self.status}')>"

class LearningPath(BaseModel):
    """
    Structured learning paths for career development!
    More guided than a Swiss mountain trail with legendary direction! 🏔️🎯
    """
    __tablename__ = "learning_paths"
    
    # Basic Information
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    path_code = Column(String(50), unique=True, index=True)
    
    # Path Properties
    path_type = Column(String(30), nullable=False, index=True)  # LearningPathType enum
    difficulty_level = Column(String(20), default="intermediate")
    estimated_duration_weeks = Column(Integer)
    
    # Target Audience
    target_roles = Column(JSON)  # List of job titles/roles
    target_departments = Column(JSON)  # List of department names
    experience_level = Column(String(20))  # entry, mid, senior, executive
    
    # Path Structure
    learning_objectives = Column(JSON)  # Overall learning objectives
    milestones = Column(JSON)  # Key milestones and checkpoints
    completion_criteria = Column(JSON)  # Criteria for path completion
    
    # Certification
    provides_certification = Column(Boolean, default=False)
    certification_name = Column(String(200))
    certification_authority = Column(String(200))
    
    # Analytics
    enrollment_count = Column(Integer, default=0)
    completion_count = Column(Integer, default=0)
    average_completion_time_weeks = Column(Float)
    success_rate = Column(Float, default=0.0)  # Completion rate
    
    # Curation
    curator_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    last_updated_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False)
    
    # Relationships
    curator = relationship("Employee", foreign_keys=[curator_id])
    last_updated_by = relationship("Employee", foreign_keys=[last_updated_by_id])
    path_courses = relationship("LearningPathCourse", back_populates="learning_path")
    enrollments = relationship("LearningPathEnrollment", back_populates="learning_path")
    
    def __repr__(self):
        return f"<LearningPath(title='{self.title}', type='{self.path_type}')>"

class LearningPathCourse(BaseModel):
    """
    Courses within learning paths!
    More organized than a Swiss curriculum with legendary structure! 📚🗂️
    """
    __tablename__ = "learning_path_courses"
    
    # References
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    
    # Sequence & Requirements
    sequence_order = Column(Integer, nullable=False)
    is_required = Column(Boolean, default=True)
    is_prerequisite = Column(Boolean, default=False)
    
    # Prerequisites
    prerequisite_courses = Column(JSON)  # Course IDs that must be completed first
    prerequisite_skills = Column(JSON)  # Skill requirements
    
    # Timing
    suggested_start_week = Column(Integer)
    estimated_duration_weeks = Column(Integer)
    
    # Relationships
    learning_path = relationship("LearningPath", back_populates="path_courses")
    course = relationship("Course")
    
    def __repr__(self):
        return f"<LearningPathCourse(path_id={self.learning_path_id}, course_id={self.course_id}, order={self.sequence_order})>"

class LearningPathEnrollment(BaseModel):
    """
    Learning path enrollments and progress!
    More comprehensive than a Swiss academic record! 🎓📊
    """
    __tablename__ = "learning_path_enrollments"
    
    # References
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Enrollment Details
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    enrolled_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    enrollment_reason = Column(Text)
    
    # Progress Tracking
    status = Column(String(20), default="enrolled", index=True)  # EnrollmentStatus enum
    overall_progress_percentage = Column(Float, default=0.0)
    current_milestone = Column(Integer, default=0)
    
    # Completion
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    certification_earned = Column(Boolean, default=False)
    certification_url = Column(String(500))
    
    # Timeline
    estimated_completion_date = Column(DateTime(timezone=True))
    actual_completion_date = Column(DateTime(timezone=True))
    
    # Performance
    overall_score = Column(Float)  # Average score across all assessments
    courses_completed = Column(Integer, default=0)
    total_courses = Column(Integer)
    
    # Status Changes
    paused_at = Column(DateTime(timezone=True))
    paused_reason = Column(Text)
    
    # Relationships
    learning_path = relationship("LearningPath", back_populates="enrollments")
    employee = relationship("Employee")
    enrolled_by = relationship("Employee", foreign_keys=[enrolled_by_id])
    
    def __repr__(self):
        return f"<LearningPathEnrollment(path_id={self.learning_path_id}, employee_id={self.employee_id}, status='{self.status}')>"

class CourseAssessment(BaseModel):
    """
    Course assessments and evaluations!
    More comprehensive than Swiss examinations! 📝🎯
    """
    __tablename__ = "course_assessments"
    
    # References
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    
    # Assessment Details
    title = Column(String(200), nullable=False)
    description = Column(Text)
    assessment_type = Column(String(30), nullable=False)  # AssessmentType enum
    
    # Configuration
    max_attempts = Column(Integer, default=3)
    time_limit_minutes = Column(Integer)
    passing_score = Column(Float, default=70.0)  # Minimum score to pass
    
    # Content
    questions = Column(JSON)  # Assessment questions/content
    rubric = Column(JSON)  # Grading rubric
    resources_allowed = Column(JSON)  # Allowed resources during assessment
    
    # Timing
    available_from = Column(DateTime(timezone=True))
    available_until = Column(DateTime(timezone=True))
    
    # Weighting
    weight_percentage = Column(Float, default=100.0)  # Weight in final course grade
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    course = relationship("Course", back_populates="assessments")
    submissions = relationship("AssessmentSubmission", back_populates="assessment")
    
    def __repr__(self):
        return f"<CourseAssessment(title='{self.title}', type='{self.assessment_type}')>"

class AssessmentSubmission(BaseModel):
    """
    Assessment submissions and grading!
    More precise than Swiss grading with legendary accuracy! ✅📊
    """
    __tablename__ = "assessment_submissions"
    
    # References
    assessment_id = Column(Integer, ForeignKey("course_assessments.id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Submission Details
    attempt_number = Column(Integer, default=1)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    time_taken_minutes = Column(Integer)
    
    # Content
    answers = Column(JSON)  # Student answers/responses
    files_submitted = Column(JSON)  # Submitted files for projects/portfolios
    
    # Grading
    score = Column(Float)  # Raw score
    percentage_score = Column(Float)  # Percentage score
    grade = Column(String(10))  # Letter grade
    is_passing = Column(Boolean)
    
    # Review
    graded_at = Column(DateTime(timezone=True))
    graded_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    feedback = Column(Text)
    detailed_feedback = Column(JSON)  # Structured feedback per question/section
    
    # Status
    status = Column(String(20), default="submitted")  # submitted, graded, needs_review
    
    # Relationships
    assessment = relationship("CourseAssessment", back_populates="submissions")
    employee = relationship("Employee", foreign_keys=[employee_id])
    graded_by = relationship("Employee", foreign_keys=[graded_by_id])
    
    def __repr__(self):
        return f"<AssessmentSubmission(assessment_id={self.assessment_id}, employee_id={self.employee_id}, score={self.score})>"

# Add relationships to Employee model (if not already added)
# Employee.skills = relationship("EmployeeSkill", foreign_keys="EmployeeSkill.employee_id")
# Employee.course_enrollments = relationship("CourseEnrollment", foreign_keys="CourseEnrollment.employee_id")
# Employee.learning_path_enrollments = relationship("LearningPathEnrollment", foreign_keys="LearningPathEnrollment.employee_id")
# Employee.taught_courses = relationship("Course", foreign_keys="Course.instructor_id")
# Employee.curated_paths = relationship("LearningPath", foreign_keys="LearningPath.curator_id")