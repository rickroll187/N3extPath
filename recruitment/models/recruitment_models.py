"""
LEGENDARY EMPLOYEE RECRUITMENT & ONBOARDING MODELS 👨‍💼🚀
More efficient than a Swiss recruitment agency with legendary talent acquisition!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 2+ HOUR CODING MARATHON CHAMPION EDITION! 🏆
Current Time: 2025-08-04 02:13:12 UTC - WE'RE RECRUITING LEGENDS!
"""

import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

from ...core.database.base_models import BaseModel, Employee, User

class JobPostingStatus(enum.Enum):
    """Job posting status - more organized than a Swiss career board!"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    FILLED = "filled"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class ApplicationStatus(enum.Enum):
    """Application status tracking"""
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    PHONE_SCREEN = "phone_screen"
    TECHNICAL_INTERVIEW = "technical_interview"
    PANEL_INTERVIEW = "panel_interview"
    FINAL_INTERVIEW = "final_interview"
    REFERENCE_CHECK = "reference_check"
    OFFER_EXTENDED = "offer_extended"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_DECLINED = "offer_declined"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class InterviewType(enum.Enum):
    """Interview types for comprehensive evaluation"""
    PHONE_SCREEN = "phone_screen"
    VIDEO_CALL = "video_call"
    IN_PERSON = "in_person"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    PANEL = "panel"
    PRESENTATION = "presentation"
    CODING_CHALLENGE = "coding_challenge"
    WHITEBOARD = "whiteboard"

class OnboardingStatus(enum.Enum):
    """Onboarding progress tracking"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    CANCELLED = "cancelled"

class JobPosting(BaseModel):
    """
    Job postings that attract legendary talent!
    More appealing than a Swiss career opportunity! 💼✨
    """
    __tablename__ = "job_postings"
    
    # Basic Information
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    short_description = Column(String(500))
    job_code = Column(String(50), unique=True, index=True)
    
    # Job Details
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    location = Column(String(200), nullable=False)
    employment_type = Column(String(30), nullable=False)  # full_time, part_time, contract, internship
    work_arrangement = Column(String(30), default="hybrid")  # remote, hybrid, on_site
    experience_level = Column(String(30), nullable=False)  # entry, mid, senior, executive
    
    # Compensation
    salary_min = Column(Float)
    salary_max = Column(Float)
    salary_currency = Column(String(10), default="USD")
    compensation_type = Column(String(30), default="annual")  # annual, hourly, project
    benefits_summary = Column(Text)
    
    # Requirements
    required_skills = Column(JSON)  # List of required skills
    preferred_skills = Column(JSON)  # List of preferred skills
    required_experience_years = Column(Integer)
    education_requirements = Column(JSON)  # List of education requirements
    certifications_required = Column(JSON)  # List of required certifications
    
    # Job Responsibilities
    key_responsibilities = Column(JSON)  # List of key responsibilities
    success_metrics = Column(JSON)  # List of success metrics
    reporting_structure = Column(Text)
    team_size = Column(Integer)
    
    # Posting Management
    hiring_manager_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    recruiter_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    created_by_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Timeline
    application_deadline = Column(DateTime(timezone=True))
    target_start_date = Column(DateTime(timezone=True))
    posted_date = Column(DateTime(timezone=True))
    filled_date = Column(DateTime(timezone=True))
    
    # Posting Settings
    is_internal_only = Column(Boolean, default=False)
    is_confidential = Column(Boolean, default=False)
    requires_referral = Column(Boolean, default=False)
    auto_reject_unqualified = Column(Boolean, default=False)
    
    # External Posting
    external_job_boards = Column(JSON)  # List of external job boards
    external_urls = Column(JSON)  # List of external posting URLs
    
    # Analytics
    view_count = Column(Integer, default=0)
    application_count = Column(Integer, default=0)
    qualified_application_count = Column(Integer, default=0)
    
    # Status
    status = Column(String(20), default="draft", index=True)  # JobPostingStatus enum
    
    # Relationships
    department = relationship("Department")
    hiring_manager = relationship("Employee", foreign_keys=[hiring_manager_id])
    recruiter = relationship("Employee", foreign_keys=[recruiter_id])
    created_by = relationship("Employee", foreign_keys=[created_by_id])
    applications = relationship("JobApplication", back_populates="job_posting")
    
    def __repr__(self):
        return f"<JobPosting(title='{self.title}', status='{self.status}')>"

class JobApplication(BaseModel):
    """
    Job applications from legendary candidates!
    More comprehensive than a Swiss candidate profile! 📄🏆
    """
    __tablename__ = "job_applications"
    
    # References
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False, index=True)
    
    # Application Details
    cover_letter = Column(Text)
    resume_url = Column(String(500))
    portfolio_url = Column(String(500))
    additional_documents = Column(JSON)  # List of additional document URLs
    
    # Application Responses
    application_responses = Column(JSON)  # Responses to application questions
    custom_questions_responses = Column(JSON)  # Custom question responses
    
    # Referral Information
    referred_by_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    referral_bonus_eligible = Column(Boolean, default=False)
    
    # Source Tracking
    application_source = Column(String(100))  # website, linkedin, referral, etc.
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    
    # Status and Timeline
    status = Column(String(30), default="submitted", index=True)  # ApplicationStatus enum
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated_at = Column(DateTime(timezone=True))
    
    # Screening and Qualification
    passes_initial_screening = Column(Boolean)
    qualification_score = Column(Float)  # 0-100 score
    screening_notes = Column(Text)
    disqualification_reason = Column(Text)
    
    # Communication
    last_contact_date = Column(DateTime(timezone=True))
    next_followup_date = Column(DateTime(timezone=True))
    communication_preferences = Column(JSON)  # Email, phone, etc.
    
    # Diversity and Inclusion
    diversity_data = Column(JSON)  # Optional diversity information
    accommodation_requests = Column(Text)
    
    # Relationships
    job_posting = relationship("JobPosting", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")
    referred_by = relationship("Employee", foreign_keys=[referred_by_id])
    interviews = relationship("Interview", back_populates="application")
    
    def __repr__(self):
        return f"<JobApplication(candidate_id={self.candidate_id}, job_id={self.job_posting_id}, status='{self.status}')>"

class Candidate(BaseModel):
    """
    Candidate profiles with legendary potential!
    More detailed than a Swiss candidate dossier! 👤🌟
    """
    __tablename__ = "candidates"
    
    # Personal Information
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    email = Column(String(200), nullable=False, unique=True, index=True)
    phone = Column(String(20))
    
    # Location
    current_location = Column(String(200))
    willing_to_relocate = Column(Boolean, default=False)
    preferred_locations = Column(JSON)  # List of preferred work locations
    
    # Professional Information
    current_title = Column(String(200))
    current_company = Column(String(200))
    years_of_experience = Column(Integer)
    industry_experience = Column(JSON)  # List of industries
    
    # Skills and Qualifications
    skills = Column(JSON)  # List of skills with proficiency levels
    certifications = Column(JSON)  # List of certifications
    education = Column(JSON)  # List of education records
    languages = Column(JSON)  # List of languages with proficiency
    
    # Professional Links
    linkedin_url = Column(String(500))
    github_url = Column(String(500))
    portfolio_url = Column(String(500))
    personal_website = Column(String(500))
    
    # Preferences
    desired_salary_min = Column(Float)
    desired_salary_max = Column(Float)
    preferred_work_arrangement = Column(String(30))  # remote, hybrid, on_site
    availability_date = Column(DateTime(timezone=True))
    notice_period_weeks = Column(Integer)
    
    # Source and Tracking
    source = Column(String(100))  # How they were sourced
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    first_contact_date = Column(DateTime(timezone=True))
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_blacklisted = Column(Boolean, default=False)
    blacklist_reason = Column(Text)
    
    # Privacy and Consent
    gdpr_consent = Column(Boolean, default=False)
    marketing_consent = Column(Boolean, default=False)
    data_retention_date = Column(DateTime(timezone=True))
    
    # Relationships
    applications = relationship("JobApplication", back_populates="candidate")
    
    def __repr__(self):
        return f"<Candidate(name='{self.first_name} {self.last_name}', email='{self.email}')>"

class Interview(BaseModel):
    """
    Interview sessions for legendary talent evaluation!
    More comprehensive than Swiss interview processes! 🎯📋
    """
    __tablename__ = "interviews"
    
    # References
    application_id = Column(Integer, ForeignKey("job_applications.id"), nullable=False, index=True)
    
    # Interview Details
    interview_type = Column(String(30), nullable=False)  # InterviewType enum
    title = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Scheduling
    scheduled_date = Column(DateTime(timezone=True), nullable=False, index=True)
    duration_minutes = Column(Integer, default=60)
    timezone = Column(String(50), default="UTC")
    
    # Location/Method
    interview_method = Column(String(30))  # in_person, video_call, phone
    location = Column(String(500))  # Physical address or video link
    meeting_details = Column(JSON)  # Additional meeting information
    
    # Participants
    interviewer_ids = Column(JSON, nullable=False)  # List of interviewer employee IDs
    panel_lead_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    
    # Interview Structure
    interview_questions = Column(JSON)  # List of interview questions
    evaluation_criteria = Column(JSON)  # List of evaluation criteria
    required_materials = Column(JSON)  # Materials candidate should bring
    
    # Feedback and Evaluation
    interviewer_feedback = Column(JSON)  # Feedback from each interviewer
    overall_rating = Column(Float)  # 1-10 overall rating
    technical_rating = Column(Float)  # 1-10 technical rating
    cultural_fit_rating = Column(Float)  # 1-10 cultural fit rating
    communication_rating = Column(Float)  # 1-10 communication rating
    
    # Recommendations
    recommendation = Column(String(30))  # hire, no_hire, maybe, strong_hire
    recommendation_notes = Column(Text)
    next_steps = Column(Text)
    
    # Status and Timeline
    status = Column(String(30), default="scheduled")  # scheduled, completed, cancelled, no_show
    completed_at = Column(DateTime(timezone=True))
    cancelled_reason = Column(Text)
    
    # Recording and Notes
    recording_url = Column(String(500))
    interview_notes = Column(Text)
    candidate_questions = Column(Text)
    
    # Relationships
    application = relationship("JobApplication", back_populates="interviews")
    panel_lead = relationship("Employee", foreign_keys=[panel_lead_id])
    
    def __repr__(self):
        return f"<Interview(application_id={self.application_id}, type='{self.interview_type}', date='{self.scheduled_date}')>"

class JobOffer(BaseModel):
    """
    Job offers for legendary candidates!
    More attractive than Swiss employment packages! 💼💎
    """
    __tablename__ = "job_offers"
    
    # References
    application_id = Column(Integer, ForeignKey("job_applications.id"), nullable=False, index=True)
    approved_by_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Offer Details
    job_title = Column(String(200), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    
    # Compensation
    base_salary = Column(Float, nullable=False)
    signing_bonus = Column(Float, default=0)
    annual_bonus_target = Column(Float, default=0)
    equity_shares = Column(Integer, default=0)
    equity_value = Column(Float, default=0)
    
    # Benefits
    vacation_days = Column(Integer)
    sick_days = Column(Integer)
    health_insurance = Column(Boolean, default=True)
    retirement_contribution = Column(Float)  # 401k match percentage
    additional_benefits = Column(JSON)  # List of additional benefits
    
    # Work Arrangement
    work_location = Column(String(200))
    remote_work_allowed = Column(Boolean, default=False)
    flexible_hours = Column(Boolean, default=False)
    
    # Terms and Conditions
    employment_type = Column(String(30), nullable=False)  # full_time, part_time, contract
    probation_period_months = Column(Integer, default=3)
    notice_period_weeks = Column(Integer, default=2)
    non_compete_months = Column(Integer, default=0)
    
    # Offer Timeline
    offer_valid_until = Column(DateTime(timezone=True), nullable=False)
    extended_at = Column(DateTime(timezone=True), server_default=func.now())
    response_deadline = Column(DateTime(timezone=True))
    
    # Status and Response
    status = Column(String(30), default="pending")  # pending, accepted, declined, expired, withdrawn
    responded_at = Column(DateTime(timezone=True))
    acceptance_conditions = Column(Text)  # Any conditions from candidate
    decline_reason = Column(Text)
    
    # Negotiation
    is_negotiable = Column(Boolean, default=True)
    negotiation_notes = Column(Text)
    final_terms = Column(JSON)  # Final negotiated terms
    
    # Documentation
    offer_letter_url = Column(String(500))
    contract_url = Column(String(500))
    signed_contract_url = Column(String(500))
    
    # Relationships
    application = relationship("JobApplication")
    approved_by = relationship("Employee", foreign_keys=[approved_by_id])
    department = relationship("Department")
    
    def __repr__(self):
        return f"<JobOffer(application_id={self.application_id}, salary={self.base_salary}, status='{self.status}')>"

class OnboardingPlan(BaseModel):
    """
    Onboarding plans for legendary new hires!
    More comprehensive than Swiss integration programs! 🎯📚
    """
    __tablename__ = "onboarding_plans"
    
    # References
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, unique=True, index=True)
    job_offer_id = Column(Integer, ForeignKey("job_offers.id"), nullable=True)
    buddy_id = Column(Integer, ForeignKey("employees.id"), nullable=True, index=True)
    hr_contact_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    
    # Plan Details
    onboarding_template_id = Column(Integer, nullable=True)  # Reference to template
    start_date = Column(DateTime(timezone=True), nullable=False)
    planned_end_date = Column(DateTime(timezone=True), nullable=False)
    actual_end_date = Column(DateTime(timezone=True))
    
    # Pre-boarding
    pre_boarding_tasks = Column(JSON)  # Tasks before start date
    equipment_needed = Column(JSON)  # List of equipment to prepare
    access_requirements = Column(JSON)  # System access needed
    
    # Week-by-Week Plan
    week_1_objectives = Column(JSON)  # First week learning objectives
    week_2_objectives = Column(JSON)  # Second week objectives
    week_3_objectives = Column(JSON)  # Third week objectives
    week_4_objectives = Column(JSON)  # Fourth week objectives
    extended_objectives = Column(JSON)  # Objectives beyond first month
    
    # Training and Development
    required_training_courses = Column(JSON)  # List of required courses
    recommended_training = Column(JSON)  # List of recommended courses
    mentorship_program = Column(Boolean, default=False)
    skills_assessment_schedule = Column(JSON)  # Schedule for skill assessments
    
    # Social Integration
    team_introduction_plan = Column(JSON)  # Plan for meeting team members
    company_culture_activities = Column(JSON)  # Cultural integration activities
    networking_opportunities = Column(JSON)  # Internal networking events
    
    # Performance and Feedback
    check_in_schedule = Column(JSON)  # Schedule for check-ins
    feedback_collection_points = Column(JSON)  # When to collect feedback
    performance_milestones = Column(JSON)  # Key performance milestones
    
    # Progress Tracking
    completion_percentage = Column(Float, default=0.0)
    current_week = Column(Integer, default=1)
    tasks_completed = Column(JSON)  # List of completed tasks
    tasks_pending = Column(JSON)  # List of pending tasks
    
    # Status and Timeline
    status = Column(String(30), default="not_started")  # OnboardingStatus enum
    last_updated_at = Column(DateTime(timezone=True))
    
    # Feedback and Notes
    new_hire_feedback = Column(Text)
    manager_notes = Column(Text)
    hr_notes = Column(Text)
    improvement_suggestions = Column(Text)
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    buddy = relationship("Employee", foreign_keys=[buddy_id])
    hr_contact = relationship("Employee", foreign_keys=[hr_contact_id])
    job_offer = relationship("JobOffer")
    
    def __repr__(self):
        return f"<OnboardingPlan(employee_id={self.employee_id}, status='{self.status}')>"

# Add relationships to Employee model (if not already added)
# Employee.job_postings_created = relationship("JobPosting", foreign_keys="JobPosting.created_by_id")
# Employee.job_postings_managed = relationship("JobPosting", foreign_keys="JobPosting.hiring_manager_id")
# Employee.job_postings_recruited = relationship("JobPosting", foreign_keys="JobPosting.recruiter_id")
# Employee.referrals_made = relationship("JobApplication", foreign_keys="JobApplication.referred_by_id")
# Employee.onboarding_plan = relationship("OnboardingPlan", foreign_keys="OnboardingPlan.employee_id", uselist=False)
# Employee.onboarding_buddy_assignments = relationship("OnboardingPlan", foreign_keys="OnboardingPlan.buddy_id")
# Employee.hr_onboarding_contacts = relationship("OnboardingPlan", foreign_keys="OnboardingPlan.hr_contact_id")