"""
Database Models for Performance Management Service
Where performance data structures meet measurement excellence! 📊🏆
Built at 2025-08-03 19:10:09 UTC by the legendary performance master rickroll187
"""
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class PerformanceReview(Base):
    """Model for performance reviews - the report card for grown-ups! 📊"""
    __tablename__ = "performance_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, index=True)
    reviewer_id = Column(Integer, nullable=False, index=True)
    review_period_start = Column(DateTime, nullable=False)
    review_period_end = Column(DateTime, nullable=False)
    review_type = Column(String(20), default="annual")  # annual, quarterly, mid_year, probation
    overall_score = Column(Float, nullable=False)  # 1-10 scale
    competency_scores = Column(JSON, nullable=False)  # Individual competency ratings
    goal_achievement_score = Column(Float, nullable=False)  # How well goals were met
    strengths = Column(JSON, nullable=False)  # List of identified strengths
    areas_for_improvement = Column(JSON, nullable=False)  # Growth opportunities
    reviewer_comments = Column(Text, nullable=True)
    employee_self_assessment = Column(JSON, nullable=True)  # Employee's self-evaluation
    development_plan = Column(JSON, nullable=True)  # Future development goals
    career_aspirations = Column(Text, nullable=True)  # Employee's career goals
    promotion_readiness = Column(String(20), nullable=True)  # ready, developing, not_ready
    salary_review_recommendation = Column(String(20), nullable=True)  # increase, maintain, review
    performance_trend = Column(String(20), nullable=False)  # improving, stable, declining, excellent
    bias_score = Column(Float, default=0.0)  # Bias detection in review
    review_status = Column(String(20), default="draft")  # draft, submitted, approved, archived
    manager_approval = Column(Boolean, default=False)
    hr_approval = Column(Boolean, default=False)
    employee_acknowledgment = Column(Boolean, default=False)
    next_review_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    
    # Relationships
    goals = relationship("Goal", back_populates="performance_review", cascade="all, delete-orphan")
    feedback_entries = relationship("FeedbackEntry", back_populates="performance_review")
    
    def __repr__(self):
        return f"<PerformanceReview(employee_id={self.employee_id}, score={self.overall_score}, period='{self.review_type}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "reviewer_id": self.reviewer_id,
            "review_period_start": self.review_period_start.isoformat(),
            "review_period_end": self.review_period_end.isoformat(),
            "review_type": self.review_type,
            "overall_score": self.overall_score,
            "competency_scores": self.competency_scores,
            "goal_achievement_score": self.goal_achievement_score,
            "strengths": self.strengths,
            "areas_for_improvement": self.areas_for_improvement,
            "reviewer_comments": self.reviewer_comments,
            "employee_self_assessment": self.employee_self_assessment,
            "development_plan": self.development_plan,
            "career_aspirations": self.career_aspirations,
            "promotion_readiness": self.promotion_readiness,
            "salary_review_recommendation": self.salary_review_recommendation,
            "performance_trend": self.performance_trend,
            "bias_score": self.bias_score,
            "review_status": self.review_status,
            "manager_approval": self.manager_approval,
            "hr_approval": self.hr_approval,
            "employee_acknowledgment": self.employee_acknowledgment,
            "next_review_date": self.next_review_date.isoformat() if self.next_review_date else None,
            "created_at": self.created_at.isoformat(),
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None
        }

class Goal(Base):
    """Model for employee goals - the roadmap to greatness! 🎯"""
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, index=True)
    performance_review_id = Column(Integer, ForeignKey('performance_reviews.id'), nullable=True)
    goal_title = Column(String(200), nullable=False)
    goal_description = Column(Text, nullable=False)
    goal_category = Column(String(50), nullable=False)  # performance, learning, project, behavioral
    priority_level = Column(String(20), default="medium")  # low, medium, high, critical
    target_completion_date = Column(DateTime, nullable=False)
    actual_completion_date = Column(DateTime, nullable=True)
    goal_status = Column(String(20), default="active")  # active, completed, paused, cancelled, overdue
    progress_percentage = Column(Float, default=0.0)  # 0-100
    success_criteria = Column(JSON, nullable=False)  # SMART criteria
    key_milestones = Column(JSON, nullable=True)  # Intermediate checkpoints
    milestone_progress = Column(JSON, nullable=True)  # Progress on each milestone
    measurement_method = Column(String(100), nullable=False)  # How success is measured
    resources_needed = Column(JSON, nullable=True)  # Required resources/support
    obstacles_encountered = Column(JSON, nullable=True)  # Challenges faced
    manager_support_level = Column(String(20), nullable=True)  # high, medium, low
    impact_on_role = Column(String(20), nullable=False)  # high, medium, low
    skill_development_areas = Column(JSON, nullable=True)  # Skills this goal develops
    alignment_with_company_goals = Column(String(20), default="medium")  # high, medium, low
    quarterly_review_notes = Column(JSON, nullable=True)  # Progress notes by quarter
    final_outcome = Column(Text, nullable=True)  # Final results/learnings
    goal_setter_id = Column(Integer, nullable=False)  # Who set this goal
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    performance_review = relationship("PerformanceReview", back_populates="goals")
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "performance_review_id": self.performance_review_id,
            "goal_title": self.goal_title,
            "goal_description": self.goal_description,
            "goal_category": self.goal_category,
            "priority_level": self.priority_level,
            "target_completion_date": self.target_completion_date.isoformat(),
            "actual_completion_date": self.actual_completion_date.isoformat() if self.actual_completion_date else None,
            "goal_status": self.goal_status,
            "progress_percentage": self.progress_percentage,
            "success_criteria": self.success_criteria,
            "key_milestones": self.key_milestones,
            "milestone_progress": self.milestone_progress,
            "measurement_method": self.measurement_method,
            "resources_needed": self.resources_needed,
            "obstacles_encountered": self.obstacles_encountered,
            "manager_support_level": self.manager_support_level,
            "impact_on_role": self.impact_on_role,
            "skill_development_areas": self.skill_development_areas,
            "alignment_with_company_goals": self.alignment_with_company_goals,
            "quarterly_review_notes": self.quarterly_review_notes,
            "final_outcome": self.final_outcome,
            "goal_setter_id": self.goal_setter_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class FeedbackEntry(Base):
    """Model for feedback entries - where constructive criticism meets constructive comedy! 💬"""
    __tablename__ = "feedback_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    giver_id = Column(Integer, nullable=False, index=True)
    receiver_id = Column(Integer, nullable=False, index=True)
    performance_review_id = Column(Integer, ForeignKey('performance_reviews.id'), nullable=True)
    feedback_type = Column(String(20), nullable=False)  # peer, upward, downward, self, 360
    feedback_category = Column(String(50), nullable=False)  # technical, communication, leadership, collaboration
    feedback_content = Column(Text, nullable=False)
    feedback_rating = Column(Float, nullable=True)  # 1-10 scale (optional)
    specific_examples = Column(JSON, nullable=True)  # Concrete examples
    suggested_improvements = Column(Text, nullable=True)
    positive_reinforcement = Column(Text, nullable=True)  # What to keep doing
    development_suggestions = Column(JSON, nullable=True)  # Specific development ideas
    feedback_context = Column(String(100), nullable=True)  # Project, situation context
    feedback_frequency = Column(String(20), default="one_time")  # one_time, recurring, follow_up
    sentiment_score = Column(Float, nullable=True)  # AI-analyzed sentiment (-1 to 1)
    constructiveness_score = Column(Float, nullable=True)  # How constructive (0-1)
    actionability_score = Column(Float, nullable=True)  # How actionable (0-1)
    bias_score = Column(Float, default=0.0)  # Bias detection in feedback
    anonymity_level = Column(String(20), default="identified")  # anonymous, semi_anonymous, identified
    feedback_status = Column(String(20), default="submitted")  # submitted, reviewed, acknowledged, acted_upon
    receiver_response = Column(Text, nullable=True)  # Receiver's response to feedback
    action_plan = Column(JSON, nullable=True)  # Plan to address feedback
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime, nullable=True)
    impact_assessment = Column(Text, nullable=True)  # How feedback was implemented
    created_at = Column(DateTime, default=datetime.utcnow)
    acknowledged_at = Column(DateTime, nullable=True)
    
    # Relationships
    performance_review = relationship("PerformanceReview", back_populates="feedback_entries")
    
    def to_dict(self):
        return {
            "id": self.id,
            "giver_id": self.giver_id,
            "receiver_id": self.receiver_id,
            "performance_review_id": self.performance_review_id,
            "feedback_type": self.feedback_type,
            "feedback_category": self.feedback_category,
            "feedback_content": self.feedback_content,
            "feedback_rating": self.feedback_rating,
            "specific_examples": self.specific_examples,
            "suggested_improvements": self.suggested_improvements,
            "positive_reinforcement": self.positive_reinforcement,
            "development_suggestions": self.development_suggestions,
            "feedback_context": self.feedback_context,
            "feedback_frequency": self.feedback_frequency,
            "sentiment_score": self.sentiment_score,
            "constructiveness_score": self.constructiveness_score,
            "actionability_score": self.actionability_score,
            "bias_score": self.bias_score,
            "anonymity_level": self.anonymity_level,
            "feedback_status": self.feedback_status,
            "receiver_response": self.receiver_response,
            "action_plan": self.action_plan,
            "follow_up_required": self.follow_up_required,
            "follow_up_date": self.follow_up_date.isoformat() if self.follow_up_date else None,
            "impact_assessment": self.impact_assessment,
            "created_at": self.created_at.isoformat(),
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None
        }

class PerformanceMetric(Base):
    """Model for performance metrics - the numbers that never lie! 📈"""
    __tablename__ = "performance_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, index=True)
    metric_name = Column(String(100), nullable=False)
    metric_category = Column(String(50), nullable=False)  # productivity, quality, efficiency, collaboration
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(20), nullable=False)  # percentage, count, hours, rating
    target_value = Column(Float, nullable=True)  # Target/goal for this metric
    benchmark_value = Column(Float, nullable=True)  # Industry/company benchmark
    measurement_period = Column(String(20), nullable=False)  # daily, weekly, monthly, quarterly
    measurement_date = Column(DateTime, nullable=False)
    data_source = Column(String(50), nullable=False)  # system, manual, survey, observation
    collection_method = Column(String(50), nullable=False)  # automated, self_reported, manager_assessed
    metric_trend = Column(String(20), nullable=True)  # improving, stable, declining
    percentile_rank = Column(Float, nullable=True)  # Ranking among peers (0-100)
    variance_from_target = Column(Float, nullable=True)  # How far from target
    improvement_suggestions = Column(JSON, nullable=True)  # AI-generated suggestions
    contextual_factors = Column(JSON, nullable=True)  # Factors affecting performance
    quality_score = Column(Float, default=1.0)  # Data quality score (0-1)
    reliability_score = Column(Float, default=1.0)  # Measurement reliability (0-1)
    aggregation_level = Column(String(20), default="individual")  # individual, team, department
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "metric_name": self.metric_name,
            "metric_category": self.metric_category,
            "metric_value": self.metric_value,
            "metric_unit": self.metric_unit,
            "target_value": self.target_value,
            "benchmark_value": self.benchmark_value,
            "measurement_period": self.measurement_period,
            "measurement_date": self.measurement_date.isoformat(),
            "data_source": self.data_source,
            "collection_method": self.collection_method,
            "metric_trend": self.metric_trend,
            "percentile_rank": self.percentile_rank,
            "variance_from_target": self.variance_from_target,
            "improvement_suggestions": self.improvement_suggestions,
            "contextual_factors": self.contextual_factors,
            "quality_score": self.quality_score,
            "reliability_score": self.reliability_score,
            "aggregation_level": self.aggregation_level,
            "created_at": self.created_at.isoformat()
        }

class ReviewTemplate(Base):
    """Model for review templates - the blueprint for fair evaluations! 📋"""
    __tablename__ = "review_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String(100), nullable=False)
    template_version = Column(String(20), default="1.0")
    applicable_roles = Column(JSON, nullable=False)  # Roles this template applies to
    review_type = Column(String(20), nullable=False)  # annual, quarterly, probation, etc.
    competency_framework = Column(JSON, nullable=False)  # Competencies and weights
    scoring_methodology = Column(JSON, nullable=False)  # How scores are calculated
    evaluation_criteria = Column(JSON, nullable=False)  # Detailed criteria for each score
    required_sections = Column(JSON, nullable=False)  # Sections that must be completed
    optional_sections = Column(JSON, nullable=True)  # Optional sections
    bias_mitigation_guidelines = Column(JSON, nullable=False)  # Anti-bias guidelines
    calibration_instructions = Column(Text, nullable=True)  # Manager calibration guidance
    employee_preparation_guide = Column(Text, nullable=True)  # How employees should prepare
    timeline_recommendations = Column(JSON, nullable=True)  # Recommended review timeline
    approval_workflow = Column(JSON, nullable=False)  # Who needs to approve
    template_status = Column(String(20), default="active")  # active, deprecated, draft
    created_by = Column(String(100), nullable=False)
    approved_by = Column(String(100), nullable=True)
    effective_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0)  # How many times used
    average_completion_time = Column(Float, nullable=True)  # Minutes to complete
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "template_name": self.template_name,
            "template_version": self.template_version,
            "applicable_roles": self.applicable_roles,
            "review_type": self.review_type,
            "competency_framework": self.competency_framework,
            "scoring_methodology": self.scoring_methodology,
            "evaluation_criteria": self.evaluation_criteria,
            "required_sections": self.required_sections,
            "optional_sections": self.optional_sections,
            "bias_mitigation_guidelines": self.bias_mitigation_guidelines,
            "calibration_instructions": self.calibration_instructions,
            "employee_preparation_guide": self.employee_preparation_guide,
            "timeline_recommendations": self.timeline_recommendations,
            "approval_workflow": self.approval_workflow,
            "template_status": self.template_status,
            "created_by": self.created_by,
            "approved_by": self.approved_by,
            "effective_date": self.effective_date.isoformat(),
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            "usage_count": self.usage_count,
            "average_completion_time": self.average_completion_time,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class PerformanceAnalytics(Base):
    """Model for performance analytics - the crystal ball of productivity! 🔮📊"""
    __tablename__ = "performance_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    analytics_date = Column(DateTime, default=datetime.utcnow)
    period_type = Column(String(20), nullable=False)  # daily, weekly, monthly, quarterly, annual
    department = Column(String(50), nullable=True)
    team_id = Column(Integer, nullable=True)
    total_reviews_completed = Column(Integer, default=0)
    average_overall_score = Column(Float, nullable=True)
    performance_distribution = Column(JSON, nullable=True)  # Distribution of scores
    goal_completion_rate = Column(Float, nullable=True)  # Percentage of goals completed
    feedback_volume = Column(Integer, default=0)  # Number of feedback entries
    feedback_sentiment_average = Column(Float, nullable=True)  # Average sentiment
    top_performing_areas = Column(JSON, nullable=True)  # Areas of strength
    improvement_opportunities = Column(JSON, nullable=True)  # Areas needing work
    bias_detection_summary = Column(JSON, nullable=True)  # Bias metrics summary
    calibration_variance = Column(Float, nullable=True)  # Review calibration consistency
    manager_effectiveness_scores = Column(JSON, nullable=True)  # How well managers review
    employee_satisfaction_scores = Column(JSON, nullable=True)  # Employee satisfaction with process
    trend_analysis = Column(JSON, nullable=True)  # Performance trends over time
    predictive_insights = Column(JSON, nullable=True)  # AI predictions
    recommended_actions = Column(JSON, nullable=True)  # Suggested improvements
    
    def to_dict(self):
        return {
            "id": self.id,
            "analytics_date": self.analytics_date.isoformat(),
            "period_type": self.period_type,
            "department": self.department,
            "team_id": self.team_id,
            "total_reviews_completed": self.total_reviews_completed,
            "average_overall_score": self.average_overall_score,
            "performance_distribution": self.performance_distribution,
            "goal_completion_rate": self.goal_completion_rate,
            "feedback_volume": self.feedback_volume,
            "feedback_sentiment_average": self.feedback_sentiment_average,
            "top_performing_areas": self.top_performing_areas,
            "improvement_opportunities": self.improvement_opportunities,
            "bias_detection_summary": self.bias_detection_summary,
            "calibration_variance": self.calibration_variance,
            "manager_effectiveness_scores": self.manager_effectiveness_scores,
            "employee_satisfaction_scores": self.employee_satisfaction_scores,
            "trend_analysis": self.trend_analysis,
            "predictive_insights": self.predictive_insights,
            "recommended_actions": self.recommended_actions
        }
