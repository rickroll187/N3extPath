"""
Database Models for Hiring Process Service
Where recruitment data structures meet hiring excellence! 🎯📊
Built at 2025-08-03 18:38:13 UTC by the legendary recruitment master rickroll187
"""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class JobPosting(Base):
    """Model for job postings - the beacon that attracts perfect candidates! 🎯"""
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(200), nullable=False, index=True)
    department = Column(String(100), nullable=False)
    job_description = Column(Text, nullable=False)
    required_skills = Column(JSON, nullable=False)  # List of required skills
    preferred_skills = Column(JSON, nullable=True)  # Nice-to-have skills
    experience_level = Column(String(20), nullable=False)  # junior, mid, senior, expert
    education_requirements = Column(JSON, nullable=True)  # Education criteria
    salary_range = Column(JSON, nullable=True)  # Min/max salary
    location = Column(String(100), nullable=True)
    remote_options = Column(String(20), default="hybrid")  # remote, onsite, hybrid
    employment_type = Column(String(20), default="full_time")  # full_time, part_time, contract
    posting_status = Column(String(20), default="active")  # active, paused, closed, filled
    urgency_level = Column(String(20), default="normal")  # low, normal, high, urgent
    team_size = Column(Integer, nullable=True)
    reporting_structure = Column(String(100), nullable=True)
    growth_opportunities = Column(JSON, nullable=True)
    company_culture_fit = Column(JSON, nullable=True)  # Cultural requirements
    bias_score = Column(Float, default=0.0)  # Bias detection in job posting
    applications_received = Column(Integer, default=0)
    positions_available = Column(Integer, default=1)
    positions_filled = Column(Integer, default=0)
    posted_by = Column(String(100), nullable=False)
    posted_date = Column(DateTime, default=datetime.utcnow)
    closing_date = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = relationship("JobApplication", back_populates="job_posting", cascade="all, delete-orphan")
    evaluations = relationship("CandidateEvaluation", back_populates="job_posting", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<JobPosting(title='{self.job_title}', department='{self.department}', status='{self.posting_status}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "job_title": self.job_title,
            "department": self.department,
            "job_description": self.job_description,
            "required_skills": self.required_skills,
            "preferred_skills": self.preferred_skills,
            "experience_level": self.experience_level,
            "education_requirements": self.education_requirements,
            "salary_range": self.salary_range,
            "location": self.location,
            "remote_options": self.remote_options,
            "employment_type": self.employment_type,
            "posting_status": self.posting_status,
            "urgency_level": self.urgency_level,
            "team_size": self.team_size,
            "reporting_structure": self.reporting_structure,
            "growth_opportunities": self.growth_opportunities,
            "company_culture_fit": self.company_culture_fit,
            "bias_score": self.bias_score,
            "applications_received": self.applications_received,
            "positions_available": self.positions_available,
            "positions_filled": self.positions_filled,
            "posted_by": self.posted_by,
            "posted_date": self.posted_date.isoformat(),
            "closing_date": self.closing_date.isoformat() if self.closing_date else None,
            "last_updated": self.last_updated.isoformat()
        }

class Candidate(Base):
    """Model for candidates - the heroes we're looking for! 🦸‍♂️🦸‍♀️"""
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String(200), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=True)
    location = Column(String(100), nullable=True)
    current_role = Column(String(100), nullable=True)
    current_company = Column(String(100), nullable=True)
    years_experience = Column(Float, nullable=True)
    education_background = Column(JSON, nullable=True)  # Education history
    skills_profile = Column(JSON, nullable=False)  # Self-reported skills
    verified_skills = Column(JSON, nullable=True)  # Verified through assessments
    career_objectives = Column(Text, nullable=True)
    salary_expectations = Column(JSON, nullable=True)  # Min/max expectations
    availability = Column(String(50), nullable=True)  # immediate, 2_weeks, 1_month, etc.
    work_preferences = Column(JSON, nullable=True)  # Remote, team size, etc.
    portfolio_links = Column(JSON, nullable=True)  # GitHub, LinkedIn, etc.
    resume_text = Column(Text, nullable=True)  # Extracted resume text
    resume_analysis = Column(JSON, nullable=True)  # AI analysis of resume
    candidate_status = Column(String(20), default="active")  # active, hired, withdrawn, blacklisted
    source = Column(String(50), nullable=True)  # website, referral, recruiter, etc.
    referrer_info = Column(JSON, nullable=True)  # Referral details
    privacy_consent = Column(Boolean, default=True)
    data_retention_consent = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = relationship("JobApplication", back_populates="candidate", cascade="all, delete-orphan")
    evaluations = relationship("CandidateEvaluation", back_populates="candidate", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "candidate_name": self.candidate_name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "current_role": self.current_role,
            "current_company": self.current_company,
            "years_experience": self.years_experience,
            "education_background": self.education_background,
            "skills_profile": self.skills_profile,
            "verified_skills": self.verified_skills,
            "career_objectives": self.career_objectives,
            "salary_expectations": self.salary_expectations,
            "availability": self.availability,
            "work_preferences": self.work_preferences,
            "portfolio_links": self.portfolio_links,
            "resume_analysis": self.resume_analysis,
            "candidate_status": self.candidate_status,
            "source": self.source,
            "referrer_info": self.referrer_info,
            "privacy_consent": self.privacy_consent,
            "data_retention_consent": self.data_retention_consent,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class JobApplication(Base):
    """Model for job applications - where candidates meet opportunities! 💼"""
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey('job_postings.id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    application_date = Column(DateTime, default=datetime.utcnow)
    application_status = Column(String(20), default="submitted")  # submitted, screening, interview, offer, hired, rejected
    cover_letter = Column(Text, nullable=True)
    custom_responses = Column(JSON, nullable=True)  # Responses to custom questions
    resume_filename = Column(String(255), nullable=True)
    resume_content = Column(Text, nullable=True)  # Extracted text
    application_source = Column(String(50), nullable=True)  # website, referral, etc.
    initial_screening_score = Column(Float, nullable=True)  # 0-100 automated score
    recruiter_notes = Column(Text, nullable=True)
    interview_scheduled = Column(DateTime, nullable=True)
    interview_feedback = Column(JSON, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    offer_details = Column(JSON, nullable=True)  # Salary, benefits, etc.
    candidate_response = Column(String(20), nullable=True)  # accepted, declined, negotiating
    hire_date = Column(DateTime, nullable=True)
    withdrawal_reason = Column(Text, nullable=True)
    last_contact_date = Column(DateTime, nullable=True)
    
    # Relationships
    job_posting = relationship("JobPosting", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")
    
    def to_dict(self):
        return {
            "id": self.id,
            "job_posting_id": self.job_posting_id,
            "candidate_id": self.candidate_id,
            "application_date": self.application_date.isoformat(),
            "application_status": self.application_status,
            "cover_letter": self.cover_letter,
            "custom_responses": self.custom_responses,
            "resume_filename": self.resume_filename,
            "application_source": self.application_source,
            "initial_screening_score": self.initial_screening_score,
            "recruiter_notes": self.recruiter_notes,
            "interview_scheduled": self.interview_scheduled.isoformat() if self.interview_scheduled else None,
            "interview_feedback": self.interview_feedback,
            "rejection_reason": self.rejection_reason,
            "offer_details": self.offer_details,
            "candidate_response": self.candidate_response,
            "hire_date": self.hire_date.isoformat() if self.hire_date else None,
            "withdrawal_reason": self.withdrawal_reason,
            "last_contact_date": self.last_contact_date.isoformat() if self.last_contact_date else None
        }

class CandidateEvaluation(Base):
    """Model for candidate evaluations - where science meets hiring! 🔬🎯"""
    __tablename__ = "candidate_evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey('job_postings.id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    evaluation_date = Column(DateTime, default=datetime.utcnow)
    evaluator = Column(String(100), nullable=False)
    evaluation_type = Column(String(20), nullable=False)  # automated, manual, interview, assessment
    overall_fit_score = Column(Float, nullable=False)  # 0-100 overall match
    skills_match_score = Column(Float, nullable=False)  # How well skills match
    experience_match_score = Column(Float, nullable=False)  # Experience level fit
    cultural_fit_score = Column(Float, nullable=True)  # Cultural alignment
    potential_score = Column(Float, nullable=True)  # Growth potential
    communication_score = Column(Float, nullable=True)  # Communication skills
    technical_assessment_score = Column(Float, nullable=True)  # Technical evaluation
    detailed_scores = Column(JSON, nullable=True)  # Breakdown by criteria
    strengths = Column(JSON, nullable=False)  # Identified strengths
    concerns = Column(JSON, nullable=True)  # Areas of concern
    interview_notes = Column(Text, nullable=True)
    recommendation = Column(String(20), nullable=False)  # hire, reject, interview, hold
    recommendation_confidence = Column(Float, nullable=False)  # 0-1 confidence
    bias_score = Column(Float, default=0.0)  # Bias detection in evaluation
    evaluation_algorithm = Column(String(50), default="bias_free_v5.0")
    comparative_ranking = Column(Integer, nullable=True)  # Rank among candidates
    next_steps = Column(JSON, nullable=True)  # Recommended actions
    
    # Relationships
    job_posting = relationship("JobPosting", back_populates="evaluations")
    candidate = relationship("Candidate", back_populates="evaluations")
    
    def to_dict(self):
        return {
            "id": self.id,
            "job_posting_id": self.job_posting_id,
            "candidate_id": self.candidate_id,
            "evaluation_date": self.evaluation_date.isoformat(),
            "evaluator": self.evaluator,
            "evaluation_type": self.evaluation_type,
            "overall_fit_score": self.overall_fit_score,
            "skills_match_score": self.skills_match_score,
            "experience_match_score": self.experience_match_score,
            "cultural_fit_score": self.cultural_fit_score,
            "potential_score": self.potential_score,
            "communication_score": self.communication_score,
            "technical_assessment_score": self.technical_assessment_score,
            "detailed_scores": self.detailed_scores,
            "strengths": self.strengths,
            "concerns": self.concerns,
            "interview_notes": self.interview_notes,
            "recommendation": self.recommendation,
            "recommendation_confidence": self.recommendation_confidence,
            "bias_score": self.bias_score,
            "evaluation_algorithm": self.evaluation_algorithm,
            "comparative_ranking": self.comparative_ranking,
            "next_steps": self.next_steps
        }

class HiringDecision(Base):
    """Model for hiring decisions - where dreams come true (or don't)! 🎉💔"""
    __tablename__ = "hiring_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey('job_postings.id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    decision = Column(String(20), nullable=False)  # hire, reject, hold, interview
    decision_maker = Column(String(100), nullable=False)
    decision_date = Column(DateTime, default=datetime.utcnow)
    decision_rationale = Column(Text, nullable=False)
    contributing_factors = Column(JSON, nullable=True)  # Factors that influenced decision
    evaluation_scores_summary = Column(JSON, nullable=True)  # Summary of all evaluations
    approval_chain = Column(JSON, nullable=True)  # Who approved this decision
    legal_review_status = Column(String(20), nullable=True)  # approved, pending, flagged
    bias_audit_score = Column(Float, default=0.0)  # Bias audit of decision
    transparency_score = Column(Float, default=1.0)  # How transparent the decision is
    appeal_status = Column(String(20), nullable=True)  # none, filed, resolved
    decision_reversibility = Column(Boolean, default=True)  # Can this be changed
    notification_sent = Column(Boolean, default=False)
    candidate_feedback_provided = Column(Boolean, default=False)
    internal_notes = Column(Text, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "job_posting_id": self.job_posting_id,
            "candidate_id": self.candidate_id,
            "decision": self.decision,
            "decision_maker": self.decision_maker,
            "decision_date": self.decision_date.isoformat(),
            "decision_rationale": self.decision_rationale,
            "contributing_factors": self.contributing_factors,
            "evaluation_scores_summary": self.evaluation_scores_summary,
            "approval_chain": self.approval_chain,
            "legal_review_status": self.legal_review_status,
            "bias_audit_score": self.bias_audit_score,
            "transparency_score": self.transparency_score,
            "appeal_status": self.appeal_status,
            "decision_reversibility": self.decision_reversibility,
            "notification_sent": self.notification_sent,
            "candidate_feedback_provided": self.candidate_feedback_provided,
            "internal_notes": self.internal_notes
        }

class RecruitmentAnalytics(Base):
    """Model for recruitment analytics - the crystal ball of hiring! 🔮📊"""
    __tablename__ = "recruitment_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    analytics_date = Column(DateTime, default=datetime.utcnow)
    period_type = Column(String(20), nullable=False)  # daily, weekly, monthly, quarterly
    job_postings_created = Column(Integer, default=0)
    applications_received = Column(Integer, default=0)
    candidates_screened = Column(Integer, default=0)
    interviews_conducted = Column(Integer, default=0)
    offers_made = Column(Integer, default=0)
    hires_completed = Column(Integer, default=0)
    rejections_made = Column(Integer, default=0)
    average_time_to_hire = Column(Float, nullable=True)  # Days
    average_time_to_screen = Column(Float, nullable=True)  # Days
    cost_per_hire = Column(Float, nullable=True)
    candidate_satisfaction_score = Column(Float, nullable=True)  # 1-10 scale
    hiring_manager_satisfaction = Column(Float, nullable=True)  # 1-10 scale
    diversity_metrics = Column(JSON, nullable=True)  # Diversity tracking
    source_effectiveness = Column(JSON, nullable=True)  # Which sources work best
    skills_demand_trends = Column(JSON, nullable=True)  # Most requested skills
    salary_trends = Column(JSON, nullable=True)  # Salary expectations vs offers
    bias_audit_summary = Column(JSON, nullable=True)  # Bias metrics summary
    algorithm_performance = Column(JSON, nullable=True)  # How well our algorithms work
    
    def to_dict(self):
        return {
            "id": self.id,
            "analytics_date": self.analytics_date.isoformat(),
            "period_type": self.period_type,
            "job_postings_created": self.job_postings_created,
            "applications_received": self.applications_received,
            "candidates_screened": self.candidates_screened,
            "interviews_conducted": self.interviews_conducted,
            "offers_made": self.offers_made,
            "hires_completed": self.hires_completed,
            "rejections_made": self.rejections_made,
            "average_time_to_hire": self.average_time_to_hire,
            "average_time_to_screen": self.average_time_to_screen,
            "cost_per_hire": self.cost_per_hire,
            "candidate_satisfaction_score": self.candidate_satisfaction_score,
            "hiring_manager_satisfaction": self.hiring_manager_satisfaction,
            "diversity_metrics": self.diversity_metrics,
            "source_effectiveness": self.source_effectiveness,
            "skills_demand_trends": self.skills_demand_trends,
            "salary_trends": self.salary_trends,
            "bias_audit_summary": self.bias_audit_summary,
            "algorithm_performance": self.algorithm_performance
        }
