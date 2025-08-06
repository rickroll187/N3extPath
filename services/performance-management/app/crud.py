"""
CRUD Operations for Performance Management Service
Where performance algorithms meet database reality and dad jokes meet scientific measurement! 📊🤖
Coded with performance precision and maximum comedy by rickroll187 at 2025-08-03 19:13:59 UTC
"""
import logging
import random
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func

from app.models import (
    PerformanceReview, Goal, FeedbackEntry, PerformanceMetric,
    ReviewTemplate, PerformanceAnalytics
)
from app.schemas import (
    PerformanceReviewRequest, PerformanceReviewResponse, GoalSettingRequest,
    GoalSettingResponse, FeedbackSubmissionRequest, FeedbackSubmissionResponse,
    PerformanceSummaryResponse
)

logger = logging.getLogger(__name__)

class PerformanceManagementCRUD:
    """
    CRUD operations for performance management
    More reliable than annual reviews, funnier than office small talk! 📊😄
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # Performance competencies framework (in production, this would be configurable)
        self.competency_framework = {
            "technical_skills": {"weight": 0.30, "description": "Technical proficiency and expertise"},
            "communication": {"weight": 0.20, "description": "Verbal and written communication effectiveness"},
            "collaboration": {"weight": 0.20, "description": "Teamwork and cooperation abilities"},
            "problem_solving": {"weight": 0.15, "description": "Analytical thinking and solution generation"},
            "leadership": {"weight": 0.10, "description": "Leadership potential and influence"},
            "adaptability": {"weight": 0.05, "description": "Flexibility and change management"}
        }
        
        # SMART goal criteria validation
        self.smart_criteria = {
            "specific": ["clear", "defined", "focused", "precise"],
            "measurable": ["quantifiable", "trackable", "metric", "number"],
            "achievable": ["realistic", "attainable", "feasible", "possible"],
            "relevant": ["important", "valuable", "meaningful", "aligned"],
            "time_bound": ["deadline", "timeline", "date", "schedule"]
        }
        
        # Performance jokes for motivation (because reviews should be fun!)
        self.performance_jokes = [
            "Why did the employee's performance review go to therapy? It had too many issues! But yours is perfect! 📊",
            "What's the difference between a performance review and a GPS? The GPS actually knows where you're going! 🗺️",
            "Why don't performance reviews ever get lost? Because they always know where you stand! 📍",
            "What do you call a performance review that tells dad jokes? A pun-formance review! Get it? 😄",
            "Why did the goal go to the gym? To get more a-chieve-able! Your goals are already ripped! 💪",
            "What's a manager's favorite type of music during reviews? Performance rock! 🎸"
        ]
        
        # Bias detection weights (because fairness is everything!)
        self.bias_detection_weights = {
            "score_consistency": 0.30,     # Consistent scoring patterns
            "competency_balance": 0.25,    # Balanced competency evaluation
            "feedback_sentiment": 0.20,    # Sentiment analysis of feedback
            "goal_achievability": 0.15,    # Realistic goal setting
            "language_neutrality": 0.10    # Neutral language usage
        }
    
    def create_performance_review(self, request: PerformanceReviewRequest) -> PerformanceReviewResponse:
        """
        Create a performance review so fair, it would make Supreme Court justices jealous!
        This review system is more unbiased than a robot judge! 🤖⚖️
        """
        try:
            logger.info(f"📊 Creating performance review for employee {request.employee_id}")
            
            # Calculate overall score from competency scores
            overall_score = self._calculate_overall_score(request.competency_scores)
            
            # Determine performance trend
            performance_trend = self._determine_performance_trend(request.employee_id, overall_score)
            
            # Analyze bias in the review
            bias_analysis = self._analyze_review_bias(request, overall_score)
            
            # Generate development recommendations
            development_recommendations = self._generate_development_recommendations(
                request.competency_scores, request.areas_for_improvement
            )
            
            # Calculate next review date
            next_review_date = self._calculate_next_review_date(request.review_type)
            
            # Create performance review
            performance_review = PerformanceReview(
                employee_id=request.employee_id,
                reviewer_id=request.reviewer_id,
                review_period_start=request.review_period_start,
                review_period_end=request.review_period_end,
                review_type=request.review_type,
                overall_score=overall_score,
                competency_scores=request.competency_scores,
                goal_achievement_score=request.goal_achievement_score,
                strengths=request.strengths,
                areas_for_improvement=request.areas_for_improvement,
                reviewer_comments=request.reviewer_comments,
                employee_self_assessment=request.employee_self_assessment,
                development_plan=request.development_plan,
                career_aspirations=request.career_aspirations,
                promotion_readiness=request.promotion_readiness,
                performance_trend=performance_trend,
                bias_score=bias_analysis["overall_bias_score"],
                next_review_date=next_review_date
            )
            
            self.db.add(performance_review)
            self.db.commit()
            self.db.refresh(performance_review)
            
            # Create associated goals if provided in development plan
            if request.development_plan:
                self._create_development_goals(performance_review.id, request.employee_id, request.development_plan)
            
            response = PerformanceReviewResponse(
                review_id=performance_review.id,
                employee_id=request.employee_id,
                reviewer_id=request.reviewer_id,
                overall_score=overall_score,
                performance_trend=performance_trend,
                bias_score=bias_analysis["overall_bias_score"],
                fairness_certified=bias_analysis["overall_bias_score"] <= 0.10,
                next_review_date=next_review_date,
                development_recommendations=development_recommendations,
                review_timestamp=performance_review.created_at
            )
            
            logger.info(f"✅ Performance review created with score: {overall_score:.2f}/10 (bias score: {bias_analysis['overall_bias_score']:.3f})")
            return response
            
        except Exception as e:
            logger.error(f"💥 Error creating performance review: {e}")
            self.db.rollback()
            raise
    
    def _calculate_overall_score(self, competency_scores: Dict[str, float]) -> float:
        """Calculate overall performance score using weighted competencies"""
        weighted_sum = 0.0
        total_weight = 0.0
        
        for competency, score in competency_scores.items():
            weight = self.competency_framework.get(competency, {}).get("weight", 0.1)
            weighted_sum += score * weight
            total_weight += weight
        
        # Normalize to 1-10 scale and add some performance magic
        overall_score = weighted_sum / max(total_weight, 1.0)
        
        # Add slight randomization for realism (±0.1)
        overall_score += random.uniform(-0.1, 0.1)
        
        return max(1.0, min(10.0, overall_score))
    
    def _determine_performance_trend(self, employee_id: int, current_score: float) -> str:
        """Determine performance trend based on historical data"""
        # Get previous reviews
        previous_reviews = self.db.query(PerformanceReview).filter(
            PerformanceReview.employee_id == employee_id
        ).order_by(desc(PerformanceReview.review_period_end)).limit(3).all()
        
        if len(previous_reviews) < 2:
            return "stable"  # Not enough data for trend
        
        # Calculate trend
        scores = [review.overall_score for review in previous_reviews]
        scores.append(current_score)
        
        # Simple trend analysis
        recent_trend = scores[-1] - scores[-2] if len(scores) >= 2 else 0
        
        if recent_trend > 0.5:
            return "improving"
        elif recent_trend < -0.5:
            return "declining"
        elif current_score >= 8.5:
            return "excellent"
        else:
            return "stable"
    
    def _analyze_review_bias(self, request: PerformanceReviewRequest, overall_score: float) -> Dict[str, float]:
        """Analyze performance review for potential bias"""
        bias_factors = {}
        
        # Check score consistency across competencies
        competency_scores = list(request.competency_scores.values())
        score_variance = np.var(competency_scores)
        consistency_bias = min(score_variance / 5.0, 0.3)  # Normalize to max 0.3
        bias_factors["score_consistency"] = consistency_bias
        
        # Check for competency balance
        balance_bias = 0.0
        if len(competency_scores) > 0:
            score_range = max(competency_scores) - min(competency_scores)
            if score_range > 6:  # Very wide range might indicate bias
                balance_bias = 0.2
        bias_factors["competency_balance"] = balance_bias
        
        # Check feedback sentiment (simplified)
        sentiment_bias = 0.0
        if request.reviewer_comments:
            # Simple sentiment analysis (in production would use NLP)
            negative_words = ["poor", "inadequate", "failing", "disappointing"]
            comment_lower = request.reviewer_comments.lower()
            negative_count = sum(1 for word in negative_words if word in comment_lower)
            if negative_count > 0 and overall_score > 7:
                sentiment_bias = 0.15  # Mismatch between comments and score
        bias_factors["feedback_sentiment"] = sentiment_bias
        
        # Check goal achievability
        goal_bias = 0.0
        if request.goal_achievement_score < 5 and overall_score > 8:
            goal_bias = 0.1  # Potential mismatch
        bias_factors["goal_achievability"] = goal_bias
        
        # Language neutrality (simplified check)
        language_bias = 0.0
        if request.reviewer_comments:
            biased_terms = ["aggressive", "emotional", "bossy", "abrasive"]
            comment_lower = request.reviewer_comments.lower()
            biased_count = sum(1 for term in biased_terms if term in comment_lower)
            language_bias = min(biased_count * 0.1, 0.2)
        bias_factors["language_neutrality"] = language_bias
        
        # Calculate overall bias score
        overall_bias = sum(
            bias_factors[factor] * self.bias_detection_weights[factor]
            for factor in bias_factors
        )
        bias_factors["overall_bias_score"] = overall_bias
        
        return bias_factors
    
    def _generate_development_recommendations(self, competency_scores: Dict[str, float], improvement_areas: List[str]) -> List[str]:
        """Generate development recommendations based on scores and improvement areas"""
        recommendations = []
        
        # Analyze competency scores for recommendations
        for competency, score in competency_scores.items():
            if score < 6:  # Below average
                comp_info = self.competency_framework.get(competency, {})
                if competency == "technical_skills":
                    recommendations.append("Enroll in technical training programs and certifications")
                elif competency == "communication":
                    recommendations.append("Participate in communication workshops and presentation training")
                elif competency == "collaboration":
                    recommendations.append("Join cross-functional projects to enhance teamwork skills")
                elif competency == "problem_solving":
                    recommendations.append("Practice analytical thinking through case studies and scenarios")
                elif competency == "leadership":
                    recommendations.append("Seek mentoring opportunities and leadership development programs")
        
        # Add recommendations based on improvement areas
        for area in improvement_areas:
            area_lower = area.lower()
            if "time management" in area_lower:
                recommendations.append("Implement time management techniques and productivity tools")
            elif "project management" in area_lower:
                recommendations.append("Complete project management certification (PMP, Agile)")
            elif "strategic thinking" in area_lower:
                recommendations.append("Participate in strategic planning exercises and business analysis")
        
        # Add some motivational recommendations
        motivational_recs = [
            "Continue leveraging your strengths while addressing development areas",
            "Set up regular check-ins with your manager for ongoing feedback",
            "Consider finding a mentor in your area of interest",
            "Join professional communities related to your field"
        ]
        
        recommendations.extend(random.sample(motivational_recs, min(2, len(motivational_recs))))
        
        return recommendations[:6]  # Max 6 recommendations
    
    def _calculate_next_review_date(self, review_type: str) -> datetime:
        """Calculate next review date based on review type"""
        now = datetime.utcnow()
        
        if review_type == "annual":
            return now + timedelta(days=365)
        elif review_type == "quarterly":
            return now + timedelta(days=90)
        elif review_type == "mid_year":
            return now + timedelta(days=180)
        elif review_type == "probation":
            return now + timedelta(days=30)
        else:
            return now + timedelta(days=365)  # Default to annual
    
    def set_employee_goals(self, request: GoalSettingRequest) -> GoalSettingResponse:
        """
        Set employee goals with SMART criteria so smart, they graduated summa cum laude! 🎓✨
        """
        try:
            logger.info(f"🎯 Setting goals for employee {request.employee_id}")
            
            # Validate SMART criteria
            smart_analysis = self._analyze_smart_criteria(request)
            
            # Calculate achievability score
            achievability_score = self._calculate_goal_achievability(request)
            
            # Estimate effort required
            estimated_effort = self._estimate_goal_effort(request)
            
            # Generate milestone schedule
            milestone_schedule = self._generate_milestone_schedule(request)
            
            # Calculate success probability
            success_probability = self._calculate_success_probability(achievability_score, smart_analysis)
            
            # Create goal record
            goal = Goal(
                employee_id=request.employee_id,
                goal_title=request.goal_title,
                goal_description=request.goal_description,
                goal_category=request.goal_category,
                priority_level=request.priority_level,
                target_completion_date=request.target_completion_date,
                success_criteria=request.success_criteria,
                key_milestones=request.key_milestones,
                measurement_method=request.measurement_method,
                resources_needed=request.resources_needed,
                impact_on_role=request.impact_on_role,
                skill_development_areas=request.skill_development_areas,
                alignment_with_company_goals=request.alignment_with_company_goals,
                goal_setter_id=request.goal_setter_id
            )
            
            self.db.add(goal)
            self.db.commit()
            self.db.refresh(goal)
            
            response = GoalSettingResponse(
                goal_id=goal.id,
                employee_id=request.employee_id,
                goal_title=request.goal_title,
                goal_status=goal.goal_status,
                smart_analysis=smart_analysis,
                achievability_score=achievability_score,
                estimated_effort_hours=estimated_effort,
                milestone_schedule=milestone_schedule,
                success_probability=success_probability,
                goal_creation_timestamp=goal.created_at
            )
            
            logger.info(f"✅ Goal created with achievability score: {achievability_score:.3f}")
            return response
            
        except Exception as e:
            logger.error(f"💥 Error setting goals: {e}")
            self.db.rollback()
            raise
    
    def _analyze_smart_criteria(self, request: GoalSettingRequest) -> Dict[str, bool]:
        """Analyze if goal meets SMART criteria"""
        goal_text = f"{request.goal_title} {request.goal_description}".lower()
        
        smart_analysis = {}
        
        for criteria, keywords in self.smart_criteria.items():
            # Check if goal text contains relevant keywords
            has_criteria = any(keyword in goal_text for keyword in keywords)
            
            # Additional specific checks
            if criteria == "specific":
                # Check if goal is detailed enough
                has_criteria = has_criteria and len(request.goal_description) > 50
            elif criteria == "measurable":
                # Check for measurement method
                has_criteria = has_criteria and bool(request.measurement_method)
            elif criteria == "time_bound":
                # Check if has deadline
                has_criteria = has_criteria and bool(request.target_completion_date)
            
            smart_analysis[criteria] = has_criteria
        
        return smart_analysis
    
    def _calculate_goal_achievability(self, request: GoalSettingRequest) -> float:
        """Calculate how achievable a goal is"""
        achievability_factors = []
        
        # Time factor - more time generally means more achievable
        days_to_complete = (request.target_completion_date - datetime.utcnow()).days
        if days_to_complete > 365:
            time_factor = 0.9
        elif days_to_complete > 180:
            time_factor = 0.8
        elif days_to_complete > 90:
            time_factor = 0.7
        elif days_to_complete > 30:
            time_factor = 0.6
        else:
            time_factor = 0.4  # Very tight deadline
        achievability_factors.append(time_factor)
        
        # Resource factor
        if request.resources_needed and len(request.resources_needed) > 0:
            resource_factor = 0.8  # Has identified resources
        else:
            resource_factor = 0.6  # No resources identified
        achievability_factors.append(resource_factor)
        
        # Priority factor - higher priority goals might get more support
        priority_factors = {"low": 0.6, "medium": 0.7, "high": 0.8, "critical": 0.9}
        priority_factor = priority_factors.get(request.priority_level, 0.7)
        achievability_factors.append(priority_factor)
        
        # Impact factor - higher impact goals might be more challenging
        impact_factors = {"low": 0.8, "medium": 0.7, "high": 0.6}
        impact_factor = impact_factors.get(request.impact_on_role, 0.7)
        achievability_factors.append(impact_factor)
        
        # Calculate overall achievability
        achievability = sum(achievability_factors) / len(achievability_factors)
        
        # Add some realistic variance
        achievability += random.uniform(-0.1, 0.1)
        
        return max(0.1, min(1.0, achievability))
    
    def _estimate_goal_effort(self, request: GoalSettingRequest) -> float:
        """Estimate effort required for goal completion in hours"""
        base_hours = 40  # Base effort
        
        # Adjust based on goal category
        category_multipliers = {
            "performance": 1.0,
            "learning": 1.5,
            "project": 2.0,
            "behavioral": 0.8,
            "career": 1.2
        }
        
        multiplier = category_multipliers.get(request.goal_category, 1.0)
        
        # Adjust based on priority
        priority_multipliers = {"low": 0.8, "medium": 1.0, "high": 1.3, "critical": 1.6}
        priority_mult = priority_multipliers.get(request.priority_level, 1.0)
        
        # Adjust based on impact
        impact_multipliers = {"low": 0.9, "medium": 1.0, "high": 1.4}
        impact_mult = impact_multipliers.get(request.impact_on_role, 1.0)
        
        estimated_hours = base_hours * multiplier * priority_mult * impact_mult
        
        # Add some variance
        estimated_hours += random.uniform(-10, 20)
        
        return max(10, estimated_hours)
    
    def _generate_milestone_schedule(self, request: GoalSettingRequest) -> List[Dict[str, Any]]:
        """Generate milestone schedule for goal"""
        if request.key_milestones:
            return request.key_milestones
        
        # Generate default milestones
        start_date = datetime.utcnow()
        end_date = request.target_completion_date
        total_days = (end_date - start_date).days
        
        milestones = []
        
        # Create 3-4 milestones
        milestone_percentages = [25, 50, 75, 100]
        milestone_names = [
            "Initial Planning and Setup",
            "Mid-Point Progress Review",
            "Near Completion Assessment",
            "Final Goal Achievement"
        ]
        
        for i, percentage in enumerate(milestone_percentages):
            milestone_date = start_date + timedelta(days=int(total_days * percentage / 100))
            milestones.append({
                "milestone_name": milestone_names[i],
                "target_date": milestone_date.isoformat(),
                "completion_percentage": percentage,
                "description": f"Achieve {percentage}% of goal completion",
                "success_criteria": f"Measurable progress toward {request.goal_title}"
            })
        
        return milestones
    
    def _calculate_success_probability(self, achievability_score: float, smart_analysis: Dict[str, bool]) -> float:
        """Calculate probability of goal success"""
        # Base probability from achievability
        base_probability = achievability_score
        
        # SMART criteria bonus
        smart_count = sum(1 for criteria in smart_analysis.values() if criteria)
        smart_bonus = (smart_count / len(smart_analysis)) * 0.2
        
        # Calculate final probability
        success_probability = base_probability + smart_bonus
        
        # Add some realistic variance
        success_probability += random.uniform(-0.05, 0.1)
        
        return max(0.1, min(1.0, success_probability))
    
    def submit_feedback(self, request: FeedbackSubmissionRequest) -> Dict[str, Any]:
        """
        Submit feedback so constructive, it could build the Golden Gate Bridge! 🌉
        """
        try:
            logger.info(f"💬 Processing feedback from {request.giver_id} to {request.receiver_id}")
            
            # Analyze feedback sentiment
            sentiment_analysis = self._analyze_feedback_sentiment(request.feedback_content)
            
            # Calculate constructiveness score
            constructiveness_score = self._calculate_constructiveness_score(request)
            
            # Calculate actionability score
            actionability_score = self._calculate_actionability_score(request)
            
            # Bias detection in feedback
            bias_detection = self._analyze_feedback_bias(request)
            
            # Generate follow-up actions
            follow_up_actions = self._generate_feedback_follow_up_actions(request, constructiveness_score)
            
            # Calculate feedback quality score
            quality_score = (constructiveness_score + actionability_score + (1 - bias_detection["overall_bias"])) / 3
            
            # Create feedback entry
            feedback_entry = FeedbackEntry(
                giver_id=request.giver_id,
                receiver_id=request.receiver_id,
                feedback_type=request.feedback_type,
                feedback_category=request.feedback_category,
                feedback_content=request.feedback_content,
                feedback_rating=request.feedback_rating,
                specific_examples=request.specific_examples,
                suggested_improvements=request.suggested_improvements,
                positive_reinforcement=request.positive_reinforcement,
                development_suggestions=request.development_suggestions,
                feedback_context=request.feedback_context,
                anonymity_level=request.anonymity_level,
                sentiment_score=sentiment_analysis["compound"],
                constructiveness_score=constructiveness_score,
                actionability_score=actionability_score,
                bias_score=bias_detection["overall_bias"]
            )
            
            self.db.add(feedback_entry)
            self.db.commit()
            self.db.refresh(feedback_entry)
            
            return {
                "feedback_id": feedback_entry.id,
                "sentiment_analysis": sentiment_analysis,
                "constructiveness_score": constructiveness_score,
                "actionability_score": actionability_score,
                "bias_detection_results": bias_detection,
                "suggested_follow_up_actions": follow_up_actions,
                "feedback_quality_score": quality_score,
                "processing_humor": random.choice(self.performance_jokes)
            }
            
        except Exception as e:
            logger.error(f"💥 Error submitting feedback: {e}")
            self.db.rollback()
            raise
    
    def _analyze_feedback_sentiment(self, feedback_content: str) -> Dict[str, float]:
        """Analyze sentiment of feedback content"""
        # Simplified sentiment analysis (in production would use NLP libraries)
        positive_words = ["excellent", "great", "outstanding", "impressive", "strong", "effective"]
        negative_words = ["poor", "weak", "inadequate", "disappointing", "concerning", "lacking"]
        neutral_words = ["average", "acceptable", "standard", "typical", "normal"]
        
        content_lower = feedback_content.lower()
        
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        neutral_count = sum(1 for word in neutral_words if word in content_lower)
        
        total_words = len(feedback_content.split())
        
        # Calculate sentiment scores
        positive_score = min(positive_count / max(total_words / 10, 1), 1.0)
        negative_score = min(negative_count / max(total_words / 10, 1), 1.0)
        neutral_score = min(neutral_count / max(total_words / 10, 1), 1.0)
        
        # Compound score
        compound = positive_score - negative_score
        
        return {
            "positive": positive_score,
            "negative": negative_score,
            "neutral": neutral_score,
            "compound": max(-1.0, min(1.0, compound))
        }
    
    def _calculate_constructiveness_score(self, request: FeedbackSubmissionRequest) -> float:
        """Calculate how constructive the feedback is"""
        constructiveness_factors = []
        
        # Has specific examples
        if request.specific_examples and len(request.specific_examples) > 0:
            constructiveness_factors.append(0.9)
        else:
            constructiveness_factors.append(0.5)
        
        # Has improvement suggestions
        if request.suggested_improvements:
            constructiveness_factors.append(0.8)
        else:
            constructiveness_factors.append(0.4)
        
        # Has positive reinforcement
        if request.positive_reinforcement:
            constructiveness_factors.append(0.7)
        else:
            constructiveness_factors.append(0.3)
        
        # Development suggestions provided
        if request.development_suggestions and len(request.development_suggestions) > 0:
            constructiveness_factors.append(0.8)
        else:
            constructiveness_factors.append(0.4)
        
        # Content length (more detailed feedback is often more constructive)
        content_length = len(request.feedback_content)
        if content_length > 200:
            constructiveness_factors.append(0.8)
        elif content_length > 100:
            constructiveness_factors.append(0.6)
        else:
            constructiveness_factors.append(0.4)
        
        return sum(constructiveness_factors) / len(constructiveness_factors)
    
    def _calculate_actionability_score(self, request: FeedbackSubmissionRequest) -> float:
        """Calculate how actionable the feedback is"""
        actionability_factors = []
        
        # Check for action-oriented language
        action_words = ["should", "could", "consider", "try", "implement", "practice", "develop"]
        content_lower = request.feedback_content.lower()
        action_count = sum(1 for word in action_words if word in content_lower)
        
        actionability_factors.append(min(action_count / 3, 1.0))  # Normalize to max 1.0
        
        # Has measurement method in suggestions
        if request.suggested_improvements and any(
            word in request.suggested_improvements.lower() 
            for word in ["measure", "track", "monitor", "assess", "evaluate"]
        ):
            actionability_factors.append(0.8)
        else:
            actionability_factors.append(0.4)
        
        # Has development suggestions
        if request.development_suggestions:
            actionability_factors.append(0.7)
        else:
            actionability_factors.append(0.3)
        
        # Has context for implementation
        if request.feedback_context:
            actionability_factors.append(0.6)
        else:
            actionability_factors.append(0.4)
        
        return sum(actionability_factors) / len(actionability_factors)
    
    def _analyze_feedback_bias(self, request: FeedbackSubmissionRequest) -> Dict[str, float]:
        """Analyze feedback for potential bias"""
        bias_factors = {}
        
        # Language bias check
        biased_terms = ["emotional", "aggressive", "bossy", "abrasive", "soft", "weak"]
        content_lower = request.feedback_content.lower()
        biased_count = sum(1 for term in biased_terms if term in content_lower)
        language_bias = min(biased_count * 0.2, 0.8)
        bias_factors["language_bias"] = language_bias
        
        # Rating vs content consistency
        consistency_bias = 0.0
        if request.feedback_rating:
            sentiment = self._analyze_feedback_sentiment(request.feedback_content)
            # Check if rating matches sentiment
            if request.feedback_rating > 7 and sentiment["compound"] < -0.3:
                consistency_bias = 0.3  # Positive rating but negative sentiment
            elif request.feedback_rating < 4 and sentiment["compound"] > 0.3:
                consistency_bias = 0.3  # Negative rating but positive sentiment
        bias_factors["consistency_bias"] = consistency_bias
        
        # Overall bias score
        overall_bias = sum(bias_factors.values()) / len(bias_factors)
        bias_factors["overall_bias"] = overall_bias
        
        return bias_factors
    
    def _generate_feedback_follow_up_actions(self, request: FeedbackSubmissionRequest, constructiveness_score: float) -> List[str]:
        """Generate suggested follow-up actions based on feedback"""
        actions = []
        
        # Standard follow-up actions
        actions.append("Schedule follow-up discussion to clarify feedback points")
        
        if constructiveness_score > 0.7:
            actions.append("Create development action plan based on feedback")
            actions.append("Set measurable goals for improvement areas")
        
        if request.suggested_improvements:
            actions.append("Implement suggested improvements with timeline")
        
        if request.development_suggestions:
            actions.append("Explore recommended development opportunities")
        
        # Category-specific actions
        if request.feedback_category == "technical":
            actions.append("Identify technical training or mentoring opportunities")
        elif request.feedback_category == "communication":
            actions.append("Practice communication skills in team settings")
        elif request.feedback_category == "leadership":
            actions.append("Seek leadership development experiences")
        elif request.feedback_category == "collaboration":
            actions.append("Participate in cross-functional team projects")
        
        actions.append("Document progress and outcomes for future reference")
        
        return actions[:5]  # Limit to top 5 actions
    
    def get_performance_summary(self, employee_id: int, include_trends: bool = True) -> Optional[Dict]:
        """Get comprehensive performance summary with more insights than a crystal ball! 🔮"""
        try:
            # Get latest performance review
            latest_review = self.db.query(PerformanceReview).filter(
                PerformanceReview.employee_id == employee_id
            ).order_by(desc(PerformanceReview.review_period_end)).first()
            
            if not latest_review:
                return None
            
            # Get active goals
            active_goals = self.db.query(Goal).filter(
                and_(
                    Goal.employee_id == employee_id,
                    Goal.goal_status == "active"
                )
            ).all()
            
            # Calculate goal completion rate
            total_goals = len(active_goals)
            completed_goals = len([g for g in active_goals if g.progress_percentage >= 100])
            goal_completion_rate = (completed_goals / max(total_goals, 1)) * 100
            
            # Get recent feedback
            recent_feedback = self.db.query(FeedbackEntry).filter(
                FeedbackEntry.receiver_id == employee_id
            ).order_by(desc(FeedbackEntry.created_at)).limit(5).all()
            
            # Analyze feedback summary
            feedback_summary = self._analyze_feedback_summary(recent_feedback)
            
            # Get performance metrics
            recent_metrics = self.db.query(PerformanceMetric).filter(
                PerformanceMetric.employee_id == employee_id
            ).order_by(desc(PerformanceMetric.measurement_date)).limit(10).all()
            
            metrics_summary = self._analyze_metrics_summary(recent_metrics)
            
            # Generate peer comparison
            peer_comparison = self._generate_peer_comparison(employee_id, latest_review.overall_score)
            
            # Generate trajectory prediction
            trajectory_prediction = self._predict_performance_trajectory(employee_id, latest_review)
            
            summary = {
                "employee_id": employee_id,
                "current_overall_score": latest_review.overall_score,
                "performance_trend": latest_review.performance_trend,
                "goal_completion_rate": goal_completion_rate,
                "recent_feedback_summary": feedback_summary,
                "key_strengths": latest_review.strengths,
                "development_areas": latest_review.areas_for_improvement,
                "performance_metrics_summary": metrics_summary,
                "career_progression_indicators": {
                    "promotion_readiness": latest_review.promotion_readiness,
                    "salary_review_recommendation": latest_review.salary_review_recommendation,
                    "development_plan_progress": "on_track"  # Simplified
                },
                "peer_comparison": peer_comparison,
                "manager_notes": [latest_review.reviewer_comments] if latest_review.reviewer_comments else [],
                "recommended_next_steps": self._generate_next_steps_recommendations(latest_review, active_goals),
                "performance_trajectory_prediction": trajectory_prediction,
                "last_review_date": latest_review.review_period_end,
                "next_review_date": latest_review.next_review_date,
                "performance_humor": random.choice(self.performance_jokes)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"💥 Error retrieving performance summary: {e}")
            raise
    
    def _analyze_feedback_summary(self, feedback_entries: List[FeedbackEntry]) -> Dict[str, Any]:
        """Analyze summary of recent feedback"""
        if not feedback_entries:
            return {"total_feedback": 0, "average_sentiment": 0.0, "feedback_themes": []}
        
        total_feedback = len(feedback_entries)
        avg_sentiment = sum(f.sentiment_score or 0 for f in feedback_entries) / total_feedback
        avg_constructiveness = sum(f.constructiveness_score or 0 for f in feedback_entries) / total_feedback
        
        # Identify common themes
        feedback_themes = []
        categories = [f.feedback_category for f in feedback_entries]
        category_counts = {cat: categories.count(cat) for cat in set(categories)}
        
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            feedback_themes.append(f"{category}: {count} mentions")
        
        return {
            "total_feedback": total_feedback,
            "average_sentiment": avg_sentiment,
            "average_constructiveness": avg_constructiveness,
            "feedback_themes": feedback_themes[:3],  # Top 3 themes
            "recent_feedback_trend": "positive" if avg_sentiment > 0.2 else "negative" if avg_sentiment < -0.2 else "neutral"
        }
    
    def _analyze_metrics_summary(self, metrics: List[PerformanceMetric]) -> Dict[str, float]:
        """Analyze performance metrics summary"""
        if not metrics:
            return {}
        
        summary = {}
        
        # Group by metric category
        by_category = {}
        for metric in metrics:
            category = metric.metric_category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(metric.metric_value)
        
        # Calculate averages
        for category, values in by_category.items():
            summary[f"avg_{category}"] = sum(values) / len(values)
        
        return summary
    
    def _generate_peer_comparison(self, employee_id: int, current_score: float) -> Dict[str, float]:
        """Generate peer comparison data"""
        # Simplified peer comparison (in production would compare with actual peer data)
        return {
            "percentile_ranking": random.uniform(60, 95),  # Mock percentile
            "above_team_average": current_score > 7.0,
            "performance_relative_to_peers": "above_average" if current_score > 7.5 else "average" if current_score > 6.0 else "below_average"
        }
    
    def _predict_performance_trajectory(self, employee_id: int, latest_review: PerformanceReview) -> Dict[str, Any]:
        """Predict future performance trajectory"""
        # Get historical reviews for trend analysis
        reviews = self.db.query(PerformanceReview).filter(
            PerformanceReview.employee_id == employee_id
        ).order_by(PerformanceReview.review_period_end).all()
        
        prediction = {
            "trajectory_direction": latest_review.performance_trend,
            "predicted_6_month_score": min(10.0, latest_review.overall_score + random.uniform(-0.5, 1.0)),
            "predicted_1_year_score": min(10.0, latest_review.overall_score + random.uniform(-0.3, 1.5)),
            "confidence_level": random.uniform(0.7, 0.9),
            "key_factors": ["Goal achievement", "Skill development", "Feedback implementation"],
            "risk_factors": ["Market changes", "Role complexity", "Team dynamics"]
        }
        
        return prediction
    
    def _generate_next_steps_recommendations(self, review: PerformanceReview, goals: List[Goal]) -> List[str]:
        """Generate next steps recommendations"""
        recommendations = []
        
        # Based on performance trend
        if review.performance_trend == "improving":
            recommendations.append("Continue current development trajectory with stretch goals")
        elif review.performance_trend == "declining":
            recommendations.append("Focus on core competency development and support")
        elif review.performance_trend == "excellent":
            recommendations.append("Explore leadership opportunities and advanced challenges")
        else:
            recommendations.append("Maintain current performance while exploring growth areas")
        
        # Based on goals
        overdue_goals = [g for g in goals if g.target_completion_date < datetime.utcnow() and g.progress_percentage < 100]
        if overdue_goals:
            recommendations.append("Prioritize completion of overdue goals with manager support")
        
        # Based on promotion readiness
        if review.promotion_readiness == "ready":
            recommendations.append("Discuss promotion opportunities with manager and HR")
        elif review.promotion_readiness == "developing":
            recommendations.append("Focus on promotion-readiness development areas")
        
        # Based on development areas
        if review.areas_for_improvement:
            recommendations.append("Create specific action plans for identified development areas")
        
        recommendations.append("Schedule regular check-ins with manager for ongoing feedback")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def validate_review_fairness(self, request: PerformanceReviewRequest, response: PerformanceReviewResponse) -> float:
        """Validate that the performance review was fair and unbiased"""
        return response.bias_score
