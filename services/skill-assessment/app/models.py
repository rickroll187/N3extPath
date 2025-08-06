"""
Database Models for Skill Assessment Service
Where skill data structures meet educational excellence! 🎓📊
Built at 2025-08-03 19:22:38 UTC by the legendary skill assessment master rickroll187
"""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SkillAssessment(Base):
    """Model for skill assessments - the report card for professional competence! 🎓"""
    __tablename__ = "skill_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, index=True)
    assessor_id = Column(Integer, nullable=True, index=True)  # Who conducted assessment
    assessment_type = Column(String(20), nullable=False)  # self, peer, manager, technical, comprehensive
    assessment_date = Column(DateTime, default=datetime.utcnow)
    overall_proficiency_score = Column(Float, nullable=False)  # 0-100 scale
    skill_breakdown = Column(JSON, nullable=False)  # Individual skill scores
    assessment_method = Column(String(50), nullable=False)  # practical, theoretical, portfolio, interview
    assessment_duration_minutes = Column(Integer, nullable=True)
    confidence_interval = Column(Float, default=0.85)  # Statistical confidence
    bias_score = Column(Float, default=0.0)  # Bias detection in assessment
    assessment_status = Column(String(20), default="completed")  # draft, in_progress, completed, verified
    verification_status = Column(String(20), nullable=True)  # unverified, verified, disputed
    market_relevance_score = Column(Float, nullable=True)  # How relevant skills are to market
    future_skill_potential = Column(Float, nullable=True)  # Growth potential assessment
    assessment_notes = Column(Text, nullable=True)
    strengths_identified = Column(JSON, nullable=False)  # Key strengths found
    improvement_areas = Column(JSON, nullable=False)  # Areas needing development
    recommended_learning_paths = Column(JSON, nullable=True)  # Suggested learning
    next_assessment_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    skill_results = relationship("AssessmentResult", back_populates="skill_assessment", cascade="all, delete-orphan")
    certifications = relationship("CertificationTracking", back_populates="related_assessment")
    
    def __repr__(self):
        return f"<SkillAssessment(employee_id={self.employee_id}, score={self.overall_proficiency_score}, type='{self.assessment_type}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "assessor_id": self.assessor_id,
            "assessment_type": self.assessment_type,
            "assessment_date": self.assessment_date.isoformat(),
            "overall_proficiency_score": self.overall_proficiency_score,
            "skill_breakdown": self.skill_breakdown,
            "assessment_method": self.assessment_method,
            "assessment_duration_minutes": self.assessment_duration_minutes,
            "confidence_interval": self.confidence_interval,
            "bias_score": self.bias_score,
            "assessment_status": self.assessment_status,
            "verification_status": self.verification_status,
            "market_relevance_score": self.market_relevance_score,
            "future_skill_potential": self.future_skill_potential,
            "assessment_notes": self.assessment_notes,
            "strengths_identified": self.strengths_identified,
            "improvement_areas": self.improvement_areas,
            "recommended_learning_paths": self.recommended_learning_paths,
            "next_assessment_date": self.next_assessment_date.isoformat() if self.next_assessment_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class AssessmentResult(Base):
    """Model for individual skill assessment results - the grade breakdown! 📊"""
    __tablename__ = "assessment_results"
    
    id = Column(Integer, primary_key=True, index=True)
    skill_assessment_id = Column(Integer, ForeignKey('skill_assessments.id'), nullable=False)
    employee_id = Column(Integer, nullable=False, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    skill_category = Column(String(50), nullable=False)  # technical, soft, domain, language
    proficiency_level = Column(Float, nullable=False)  # 0-100 proficiency score
    competency_level = Column(String(20), nullable=False)  # beginner, intermediate, advanced, expert
    assessment_criteria = Column(JSON, nullable=False)  # What was assessed
    evidence_provided = Column(JSON, nullable=True)  # Evidence of skill
    practical_score = Column(Float, nullable=True)  # Hands-on assessment score
    theoretical_score = Column(Float, nullable=True)  # Knowledge assessment score
    peer_validation_score = Column(Float, nullable=True)  # Peer assessment
    self_assessment_score = Column(Float, nullable=True)  # Self-evaluation
    market_demand_level = Column(String(20), nullable=True)  # low, medium, high, critical
    skill_currency = Column(String(20), nullable=True)  # current, emerging, declining, obsolete
    years_of_experience = Column(Float, nullable=True)  # Years working with this skill
    last_used_date = Column(DateTime, nullable=True)  # When skill was last applied
    certification_level = Column(String(50), nullable=True)  # Related certifications
    improvement_trajectory = Column(String(20), nullable=True)  # improving, stable, declining
    recommended_actions = Column(JSON, nullable=True)  # Suggested improvements
    skill_dependencies = Column(JSON, nullable=True)  # Related/prerequisite skills
    industry_relevance = Column(Float, nullable=True)  # 0-1 relevance to industry
    assessment_confidence = Column(Float, default=0.85)  # Confidence in this score
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    skill_assessment = relationship("SkillAssessment", back_populates="skill_results")
    
    def to_dict(self):
        return {
            "id": self.id,
            "skill_assessment_id": self.skill_assessment_id,
            "employee_id": self.employee_id,
            "skill_name": self.skill_name,
            "skill_category": self.skill_category,
            "proficiency_level": self.proficiency_level,
            "competency_level": self.competency_level,
            "assessment_criteria": self.assessment_criteria,
            "evidence_provided": self.evidence_provided,
            "practical_score": self.practical_score,
            "theoretical_score": self.theoretical_score,
            "peer_validation_score": self.peer_validation_score,
            "self_assessment_score": self.self_assessment_score,
            "market_demand_level": self.market_demand_level,
            "skill_currency": self.skill_currency,
            "years_of_experience": self.years_of_experience,
            "last_used_date": self.last_used_date.isoformat() if self.last_used_date else None,
            "certification_level": self.certification_level,
            "improvement_trajectory": self.improvement_trajectory,
            "recommended_actions": self.recommended_actions,
            "skill_dependencies": self.skill_dependencies,
            "industry_relevance": self.industry_relevance,
            "assessment_confidence": self.assessment_confidence,
            "created_at": self.created_at.isoformat()
        }

class CertificationTracking(Base):
    """Model for certification tracking - the trophy case of professional development! 🏆"""
    __tablename__ = "certification_tracking"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, index=True)
    related_assessment_id = Column(Integer, ForeignKey('skill_assessments.id'), nullable=True)
    certification_name = Column(String(200), nullable=False)
    certification_provider = Column(String(100), nullable=False)
    certification_type = Column(String(50), nullable=False)  # technical, professional, academic, vendor
    certification_level = Column(String(20), nullable=True)  # foundation, associate, professional, expert
    certification_id = Column(String(100), nullable=True)  # Certificate ID/number
    issue_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=True)
    renewal_required = Column(Boolean, default=False)
    renewal_period_months = Column(Integer, nullable=True)
    next_renewal_date = Column(DateTime, nullable=True)
    certification_status = Column(String(20), default="active")  # active, expired, suspended, renewed
    verification_url = Column(String(500), nullable=True)  # Digital badge/verification link
    skills_covered = Column(JSON, nullable=False)  # Skills this certification covers
    prerequisite_certifications = Column(JSON, nullable=True)  # Required prior certs
    continuing_education_hours = Column(Float, nullable=True)  # CE hours required
    market_value_score = Column(Float, nullable=True)  # Market value of certification
    industry_recognition = Column(String(20), nullable=True)  # high, medium, low
    difficulty_level = Column(String(20), nullable=True)  # easy, moderate, difficult, expert
    study_hours_required = Column(Float, nullable=True)  # Estimated study time
    pass_rate_percentage = Column(Float, nullable=True)  # Industry pass rate
    salary_impact_percentage = Column(Float, nullable=True)  # Impact on salary
    career_advancement_value = Column(Float, nullable=True)  # Career progression value
    digital_badge_url = Column(String(500), nullable=True)  # Digital badge image
    verification_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    related_assessment = relationship("SkillAssessment", back_populates="certifications")
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "related_assessment_id": self.related_assessment_id,
            "certification_name": self.certification_name,
            "certification_provider": self.certification_provider,
            "certification_type": self.certification_type,
            "certification_level": self.certification_level,
            "certification_id": self.certification_id,
            "issue_date": self.issue_date.isoformat(),
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            "renewal_required": self.renewal_required,
            "renewal_period_months": self.renewal_period_months,
            "next_renewal_date": self.next_renewal_date.isoformat() if self.next_renewal_date else None,
            "certification_status": self.certification_status,
            "verification_url": self.verification_url,
            "skills_covered": self.skills_covered,
            "prerequisite_certifications": self.prerequisite_certifications,
            "continuing_education_hours": self.continuing_education_hours,
            "market_value_score": self.market_value_score,
            "industry_recognition": self.industry_recognition,
            "difficulty_level": self.difficulty_level,
            "study_hours_required": self.study_hours_required,
            "pass_rate_percentage": self.pass_rate_percentage,
            "salary_impact_percentage": self.salary_impact_percentage,
            "career_advancement_value": self.career_advancement_value,
            "digital_badge_url": self.digital_badge_url,
            "verification_notes": self.verification_notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class SkillCategory(Base):
    """Model for skill categories - the taxonomy of talent! 📚"""
    __tablename__ = "skill_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False, unique=True)
    category_description = Column(Text, nullable=True)
    parent_category_id = Column(Integer, ForeignKey('skill_categories.id'), nullable=True)
    category_level = Column(Integer, default=1)  # Hierarchy level
    market_demand_trend = Column(String(20), nullable=True)  # increasing, stable, declining
    average_salary_impact = Column(Float, nullable=True)  # Average salary impact
    skills_in_category = Column(JSON, nullable=False)  # List of skills in this category
    assessment_framework = Column(JSON, nullable=True)  # How to assess skills in this category
    learning_resources = Column(JSON, nullable=True)  # Recommended learning resources
    industry_relevance = Column(JSON, nullable=True)  # Which industries value this category
    skill_progression_path = Column(JSON, nullable=True)  # Typical skill development path
    certification_providers = Column(JSON, nullable=True)  # Who provides certs for this category
    market_saturation_level = Column(String(20), nullable=True)  # low, medium, high, oversaturated
    emerging_skills = Column(JSON, nullable=True)  # New skills appearing in this category
    obsolete_skills = Column(JSON, nullable=True)  # Skills becoming less relevant
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Self-referential relationship for hierarchy
    subcategories = relationship("SkillCategory", back_populates="parent_category", remote_side=[id])
    parent_category = relationship("SkillCategory", back_populates="subcategories", remote_side=[parent_category_id])
    
    def to_dict(self):
        return {
            "id": self.id,
            "category_name": self.category_name,
            "category_description": self.category_description,
            "parent_category_id": self.parent_category_id,
            "category_level": self.category_level,
            "market_demand_trend": self.market_demand_trend,
            "average_salary_impact": self.average_salary_impact,
            "skills_in_category": self.skills_in_category,
            "assessment_framework": self.assessment_framework,
            "learning_resources": self.learning_resources,
            "industry_relevance": self.industry_relevance,
            "skill_progression_path": self.skill_progression_path,
            "certification_providers": self.certification_providers,
            "market_saturation_level": self.market_saturation_level,
            "emerging_skills": self.emerging_skills,
            "obsolete_skills": self.obsolete_skills,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class SkillGapAnalysis(Base):
    """Model for skill gap analysis - the roadmap to excellence! 🗺️"""
    __tablename__ = "skill_gap_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, index=True)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    target_role = Column(String(100), nullable=True)  # Role being analyzed for
    target_department = Column(String(50), nullable=True)
    analysis_scope = Column(String(20), nullable=False)  # individual, team, department, organization
    current_skill_profile = Column(JSON, nullable=False)  # Current skills and levels
    target_skill_profile = Column(JSON, nullable=False)  # Required skills and levels
    identified_gaps = Column(JSON, nullable=False)  # Skills that need development
    proficiency_gaps = Column(JSON, nullable=False)  # Level improvements needed
    critical_gaps = Column(JSON, nullable=False)  # Most important gaps to address
    quick_wins = Column(JSON, nullable=True)  # Easy skills to develop quickly
    long_term_development = Column(JSON, nullable=True)  # Skills requiring significant time
    recommended_learning_path = Column(JSON, nullable=False)  # Suggested development plan
    estimated_closure_timeline = Column(JSON, nullable=True)  # Timeline to close gaps
    resource_requirements = Column(JSON, nullable=True)  # Resources needed for development
    mentorship_recommendations = Column(JSON, nullable=True)  # Suggested mentors/coaches
    certification_recommendations = Column(JSON, nullable=True)  # Suggested certifications
    priority_ranking = Column(JSON, nullable=False)  # Priority order for gap closure
    roi_analysis = Column(JSON, nullable=True)  # Return on investment for development
    market_urgency = Column(JSON, nullable=True)  # Market demand urgency for skills
    competitor_analysis = Column(JSON, nullable=True)  # How employee compares to market
    success_metrics = Column(JSON, nullable=False)  # How to measure gap closure success
    progress_tracking_plan = Column(JSON, nullable=True)  # How to track development
    budget_estimate = Column(Float, nullable=True)  # Estimated cost for development
    analysis_confidence = Column(Float, default=0.85)  # Confidence in analysis
    next_review_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "analysis_date": self.analysis_date.isoformat(),
            "target_role": self.target_role,
            "target_department": self.target_department,
            "analysis_scope": self.analysis_scope,
            "current_skill_profile": self.current_skill_profile,
            "target_skill_profile": self.target_skill_profile,
            "identified_gaps": self.identified_gaps,
            "proficiency_gaps": self.proficiency_gaps,
            "critical_gaps": self.critical_gaps,
            "quick_wins": self.quick_wins,
            "long_term_development": self.long_term_development,
            "recommended_learning_path": self.recommended_learning_path,
            "estimated_closure_timeline": self.estimated_closure_timeline,
            "resource_requirements": self.resource_requirements,
            "mentorship_recommendations": self.mentorship_recommendations,
            "certification_recommendations": self.certification_recommendations,
            "priority_ranking": self.priority_ranking,
            "roi_analysis": self.roi_analysis,
            "market_urgency": self.market_urgency,
            "competitor_analysis": self.competitor_analysis,
            "success_metrics": self.success_metrics,
            "progress_tracking_plan": self.progress_tracking_plan,
            "budget_estimate": self.budget_estimate,
            "analysis_confidence": self.analysis_confidence,
            "next_review_date": self.next_review_date.isoformat() if self.next_review_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class SkillEvidence(Base):
    """Model for skill evidence - the proof of competence! 📁"""
    __tablename__ = "skill_evidence"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    evidence_type = Column(String(50), nullable=False)  # portfolio, project, certification, endorsement
    evidence_title = Column(String(200), nullable=False)
    evidence_description = Column(Text, nullable=False)
    evidence_url = Column(String(500), nullable=True)  # Link to evidence
    file_path = Column(String(500), nullable=True)  # Stored file path
    submission_date = Column(DateTime, default=datetime.utcnow)
    verification_status = Column(String(20), default="pending")  # pending, verified, rejected
    verified_by = Column(Integer, nullable=True)  # Who verified
    verification_date = Column(DateTime, nullable=True)
    verification_notes = Column(Text, nullable=True)
    evidence_weight = Column(Float, default=1.0)  # How much this evidence counts
    skill_level_demonstrated = Column(String(20), nullable=True)  # beginner, intermediate, advanced, expert
    proficiency_contribution = Column(Float, nullable=True)  # How much this adds to proficiency
    peer_endorsements = Column(JSON, nullable=True)  # Peer validations
    manager_endorsement = Column(Boolean, default=False)
    client_feedback = Column(JSON, nullable=True)  # Client testimonials
    impact_metrics = Column(JSON, nullable=True)  # Measurable impact
    technology_stack = Column(JSON, nullable=True)  # Technologies used
    project_duration = Column(String(50), nullable=True)  # How long project took
    team_size = Column(Integer, nullable=True)  # Size of team involved
    role_in_project = Column(String(100), nullable=True)  # Person's role
    challenges_overcome = Column(JSON, nullable=True)  # Challenges faced and solved
    learning_outcomes = Column(JSON, nullable=True)  # What was learned
    visibility_level = Column(String(20), default="team")  # team, department, organization, public
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "skill_name": self.skill_name,
            "evidence_type": self.evidence_type,
            "evidence_title": self.evidence_title,
            "evidence_description": self.evidence_description,
            "evidence_url": self.evidence_url,
            "file_path": self.file_path,
            "submission_date": self.submission_date.isoformat(),
            "verification_status": self.verification_status,
            "verified_by": self.verified_by,
            "verification_date": self.verification_date.isoformat() if self.verification_date else None,
            "verification_notes": self.verification_notes,
            "evidence_weight": self.evidence_weight,
            "skill_level_demonstrated": self.skill_level_demonstrated,
            "proficiency_contribution": self.proficiency_contribution,
            "peer_endorsements": self.peer_endorsements,
            "manager_endorsement": self.manager_endorsement,
            "client_feedback": self.client_feedback,
            "impact_metrics": self.impact_metrics,
            "technology_stack": self.technology_stack,
            "project_duration": self.project_duration,
            "team_size": self.team_size,
            "role_in_project": self.role_in_project,
            "challenges_overcome": self.challenges_overcome,
            "learning_outcomes": self.learning_outcomes,
            "visibility_level": self.visibility_level,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class SkillAssessmentAnalytics(Base):
    """Model for skill assessment analytics - the crystal ball of competency! 🔮📊"""
    __tablename__ = "skill_assessment_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    analytics_date = Column(DateTime, default=datetime.utcnow)
    period_type = Column(String(20), nullable=False)  # daily, weekly, monthly, quarterly
    department = Column(String(50), nullable=True)
    team_id = Column(Integer, nullable=True)
    total_assessments_completed = Column(Integer, default=0)
    average_proficiency_score = Column(Float, nullable=True)
    skill_distribution = Column(JSON, nullable=True)  # Distribution of skill levels
    top_performing_skills = Column(JSON, nullable=True)  # Highest scoring skills
    skill_gaps_identified = Column(JSON, nullable=True)  # Common skill gaps
    certification_completion_rate = Column(Float, nullable=True)  # Cert completion %
    learning_engagement_metrics = Column(JSON, nullable=True)  # Learning activity
    bias_detection_summary = Column(JSON, nullable=True)  # Bias metrics summary
    assessment_quality_metrics = Column(JSON, nullable=True)  # Quality of assessments
    market_alignment_score = Column(Float, nullable=True)  # How skills align with market
    future_skills_readiness = Column(Float, nullable=True)  # Readiness for emerging skills
    skill_decay_analysis = Column(JSON, nullable=True)  # Skills becoming obsolete
    competitive_positioning = Column(JSON, nullable=True)  # How org compares to market
    roi_metrics = Column(JSON, nullable=True)  # Return on skill development investment
    predictive_insights = Column(JSON, nullable=True)  # AI predictions
    recommended_interventions = Column(JSON, nullable=True)  # Suggested actions
    
    def to_dict(self):
        return {
            "id": self.id,
            "analytics_date": self.analytics_date.isoformat(),
            "period_type": self.period_type,
            "department": self.department,
            "team_id": self.team_id,
            "total_assessments_completed": self.total_assessments_completed,
            "average_proficiency_score": self.average_proficiency_score,
            "skill_distribution": self.skill_distribution,
            "top_performing_skills": self.top_performing_skills,
            "skill_gaps_identified": self.skill_gaps_identified,
            "certification_completion_rate": self.certification_completion_rate,
            "learning_engagement_metrics": self.learning_engagement_metrics,
            "bias_detection_summary": self.bias_detection_summary,
            "assessment_quality_metrics": self.assessment_quality_metrics,
            "market_alignment_score": self.market_alignment_score,
            "future_skills_readiness": self.future_skills_readiness,
            "skill_decay_analysis": self.skill_decay_analysis,
            "competitive_positioning": self.competitive_positioning,
            "roi_metrics": self.roi_metrics,
            "predictive_insights": self.predictive_insights,
            "recommended_interventions": self.recommended_interventions
        }
