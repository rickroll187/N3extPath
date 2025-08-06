"""
LEGENDARY 360 FEEDBACK SERVICE 🔄🎯
More comprehensive than a 720-degree view with X-ray vision!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc
from dataclasses import dataclass
import statistics
from enum import Enum
import numpy as np
from collections import defaultdict, Counter

from ..models.review_models import (
    PeerReview, PerformanceReview, PerformanceReviewCycle,
    RatingScale
)
from ...core.auth.authorization import AuthContext, Permission
from ...core.database.base_models import Employee, User, Department, AuditLog

logger = logging.getLogger(__name__)

class FeedbackType(Enum):
    """360 feedback types - more comprehensive than a Swiss survey!"""
    PEER = "peer"
    DIRECT_REPORT = "direct_report"
    MANAGER = "manager"
    CROSS_FUNCTIONAL = "cross_functional"
    CUSTOMER = "customer"
    VENDOR = "vendor"
    SELF = "self"

class FeedbackCategory(Enum):
    """Feedback categories for structured assessment"""
    COLLABORATION = "collaboration"
    COMMUNICATION = "communication"
    LEADERSHIP = "leadership"
    TECHNICAL_SKILLS = "technical_skills"
    RELIABILITY = "reliability"
    INNOVATION = "innovation"
    PROBLEM_SOLVING = "problem_solving"
    ADAPTABILITY = "adaptability"

@dataclass
class FeedbackAnalytics:
    """
    360 feedback analytics that are more insightful than a psychologist!
    More comprehensive than a doctoral thesis on human behavior! 🧠📊
    """
    total_feedback_count: int
    feedback_by_type: Dict[str, int]
    average_ratings: Dict[str, float]
    rating_consistency: float
    response_rate: float
    feedback_themes: List[str]
    strengths_consensus: List[str]
    development_areas_consensus: List[str]
    outlier_feedback: List[Dict[str, Any]]

class Legendary360FeedbackService:
    """
    The most comprehensive 360 feedback system in the galaxy!
    More thorough than a Swiss investigation with attitude! 🔄🕵️
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # 360 FEEDBACK JOKES FOR SUNDAY MORNING MOTIVATION
        self.feedback_jokes = [
            "Why did the 360 feedback go to therapy? It had too many perspectives! 🔄😄",
            "What's the difference between our 360 feedback and a mirror? Both show the truth! 🪞",
            "Why don't our feedback systems ever lie? Because honesty is legendary! 💎",
            "What do you call 360 feedback at 3 AM? All-around night shift wisdom! 🌙",
            "Why did the feedback become a comedian? It had perfect 360-degree timing! 🎭"
        ]
        
        # Feedback relationship mapping
        self.relationship_weights = {
            FeedbackType.MANAGER: 1.5,           # Manager feedback weighted higher
            FeedbackType.PEER: 1.0,              # Standard peer weight
            FeedbackType.DIRECT_REPORT: 1.2,     # Direct reports valuable perspective
            FeedbackType.CROSS_FUNCTIONAL: 0.9,  # Cross-functional slightly lower
            FeedbackType.CUSTOMER: 1.3,          # Customer feedback highly valuable
            FeedbackType.VENDOR: 0.8,            # Vendor feedback contextual
            FeedbackType.SELF: 0.7               # Self-assessment for comparison
        }
        
        # Minimum feedback thresholds for reliability
        self.feedback_thresholds = {
            "min_peer_feedback": 3,
            "min_total_feedback": 5,
            "response_rate_threshold": 0.6,  # 60% response rate
            "consensus_threshold": 0.7,      # 70% agreement for consensus
            "outlier_threshold": 2.0         # 2 standard deviations for outliers
        }
        
        # Rating consistency calculation parameters
        self.consistency_params = {
            "max_variance_threshold": 1.0,   # Maximum acceptable variance
            "consensus_range": 0.5,          # Range for rating consensus
            "reliability_threshold": 0.8     # Minimum reliability score
        }
        
        logger.info("🔄 Legendary 360 Feedback Service initialized - Ready for all-around excellence!")
    
    def initiate_360_feedback(self, review_id: int, feedback_config: Dict[str, Any],
                             auth_context: AuthContext) -> Dict[str, Any]:
        """
        Initiate 360 feedback collection process!
        More organized than a Swiss orchestra with perfect harmony! 🎼🔄
        """
        try:
            logger.info(f"🔄 Initiating 360 feedback for review: {review_id}")
            
            # Validate permissions
            if not auth_context.has_permission(Permission.PERFORMANCE_ADMIN):
                return {
                    "success": False,
                    "error": "Insufficient permissions to initiate 360 feedback"
                }
            
            # Get performance review
            review = self.db.query(PerformanceReview).filter(
                PerformanceReview.id == review_id
            ).first()
            
            if not review:
                return {
                    "success": False,
                    "error": "Performance review not found"
                }
            
            # Validate review cycle allows 360 feedback
            if not review.review_cycle.enable_360_feedback:
                return {
                    "success": False,
                    "error": "360 feedback not enabled for this review cycle"
                }
            
            # Generate feedback participant list
            participants_result = self._generate_feedback_participants(
                review, feedback_config
            )
            
            if not participants_result["success"]:
                return participants_result
            
            participants = participants_result["participants"]
            
            # Create feedback requests
            feedback_requests = []
            for participant in participants:
                # Check if feedback already exists
                existing_feedback = self.db.query(PeerReview).filter(
                    and_(
                        PeerReview.review_id == review_id,
                        PeerReview.reviewer_id == participant["reviewer_id"]
                    )
                ).first()
                
                if not existing_feedback:
                    # Create new peer review entry
                    peer_review = PeerReview(
                        review_id=review_id,
                        reviewer_id=participant["reviewer_id"],
                        relationship_type=participant["relationship_type"],
                        feedback_requested_at=datetime.utcnow(),
                        feedback_deadline=feedback_config.get(
                            "deadline", 
                            datetime.utcnow() + timedelta(days=14)
                        ),
                        created_by=auth_context.user_id,
                        updated_by=auth_context.user_id
                    )
                    
                    self.db.add(peer_review)
                    feedback_requests.append({
                        "reviewer_id": participant["reviewer_id"],
                        "reviewer_name": participant["reviewer_name"],
                        "relationship_type": participant["relationship_type"]
                    })
            
            self.db.flush()
            
            # Log 360 feedback initiation
            self._log_360_action("FEEDBACK_360_INITIATED", review_id, auth_context, {
                "participants_count": len(participants),
                "feedback_requests_created": len(feedback_requests),
                "deadline": feedback_config.get("deadline", "14 days").isoformat() if isinstance(feedback_config.get("deadline"), datetime) else str(feedback_config.get("deadline", "14 days")),
                "config": feedback_config
            })
            
            self.db.commit()
            
            logger.info(f"✅ 360 feedback initiated: {len(feedback_requests)} requests created")
            
            return {
                "success": True,
                "review_id": review_id,
                "participants_invited": len(participants),
                "feedback_requests_created": len(feedback_requests),
                "feedback_deadline": feedback_config.get("deadline", datetime.utcnow() + timedelta(days=14)).isoformat() if isinstance(feedback_config.get("deadline"), datetime) else str(feedback_config.get("deadline")),
                "participants": feedback_requests,
                "legendary_joke": "Why did the 360 feedback become legendary? Because it covered all the angles! 🔄🏆"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 360 feedback initiation error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def submit_360_feedback(self, feedback_id: int, feedback_data: Dict[str, Any],
                          auth_context: AuthContext) -> Dict[str, Any]:
        """
        Submit 360 feedback with more precision than a Swiss watch!
        More thorough than a comprehensive performance analysis! 📝🎯
        """
        try:
            logger.info(f"📝 Submitting 360 feedback: {feedback_id}")
            
            # Get peer review entry
            peer_review = self.db.query(PeerReview).filter(
                PeerReview.id == feedback_id
            ).first()
            
            if not peer_review:
                return {
                    "success": False,
                    "error": "Feedback request not found"
                }
            
            # Check permissions
            if peer_review.reviewer_id != auth_context.user_id:
                return {
                    "success": False,
                    "error": "You can only submit your own feedback"
                }
            
            # Check if already submitted
            if peer_review.feedback_submitted_at:
                return {
                    "success": False,
                    "error": "Feedback already submitted"
                }
            
            # Check deadline
            if peer_review.feedback_deadline and datetime.utcnow() > peer_review.feedback_deadline:
                # Allow submission but log as late
                logger.warning(f"⚠️ Late feedback submission for feedback {feedback_id}")
            
            # Validate feedback data
            validation_result = self._validate_feedback_data(feedback_data)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "errors": validation_result["errors"]
                }
            
            # Update peer review with feedback
            peer_review.collaboration_rating = RatingScale(feedback_data.get("collaboration_rating")) if feedback_data.get("collaboration_rating") else None
            peer_review.communication_rating = RatingScale(feedback_data.get("communication_rating")) if feedback_data.get("communication_rating") else None
            peer_review.leadership_rating = RatingScale(feedback_data.get("leadership_rating")) if feedback_data.get("leadership_rating") else None
            peer_review.technical_skills_rating = RatingScale(feedback_data.get("technical_skills_rating")) if feedback_data.get("technical_skills_rating") else None
            peer_review.reliability_rating = RatingScale(feedback_data.get("reliability_rating")) if feedback_data.get("reliability_rating") else None
            
            peer_review.strengths = feedback_data.get("strengths")
            peer_review.areas_for_improvement = feedback_data.get("areas_for_improvement")
            peer_review.specific_examples = feedback_data.get("specific_examples")
            peer_review.additional_comments = feedback_data.get("additional_comments")
            
            peer_review.feedback_submitted_at = datetime.utcnow()
            peer_review.updated_by = auth_context.user_id
            
            # Calculate overall rating if individual ratings provided
            ratings = [
                peer_review.collaboration_rating,
                peer_review.communication_rating,
                peer_review.leadership_rating,
                peer_review.technical_skills_rating,
                peer_review.reliability_rating
            ]
            
            numeric_ratings = [self._rating_to_numeric(r) for r in ratings if r]
            if numeric_ratings:
                avg_rating = statistics.mean(numeric_ratings)
                peer_review.overall_rating = self._numeric_to_rating(avg_rating)
            
            # Log feedback submission
            self._log_360_action("FEEDBACK_360_SUBMITTED", peer_review.review_id, auth_context, {
                "feedback_id": feedback_id,
                "reviewer_id": peer_review.reviewer_id,
                "relationship_type": peer_review.relationship_type,
                "ratings_provided": len(numeric_ratings),
                "is_late_submission": peer_review.feedback_deadline and datetime.utcnow() > peer_review.feedback_deadline
            })
            
            self.db.commit()
            
            logger.info(f"✅ 360 feedback submitted successfully: {feedback_id}")
            
            return {
                "success": True,
                "feedback_id": feedback_id,
                "review_id": peer_review.review_id,
                "overall_rating": peer_review.overall_rating.value if peer_review.overall_rating else None,
                "submission_timestamp": peer_review.feedback_submitted_at.isoformat(),
                "is_late_submission": peer_review.feedback_deadline and datetime.utcnow() > peer_review.feedback_deadline,
                "legendary_joke": "Why did the feedback submission become legendary? Because it was perfectly honest! 💎📝"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 360 feedback submission error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def analyze_360_feedback(self, review_id: int, 
                           auth_context: AuthContext) -> Dict[str, Any]:
        """
        Analyze 360 feedback with more insight than a Swiss psychologist!
        More comprehensive than a PhD thesis on human behavior! 🧠📊
        """
        try:
            logger.info(f"📊 Analyzing 360 feedback for review: {review_id}")
            
            # Get all feedback for the review
            feedback_entries = self.db.query(PeerReview).filter(
                and_(
                    PeerReview.review_id == review_id,
                    PeerReview.feedback_submitted_at.isnot(None)
                )
            ).all()
            
            if not feedback_entries:
                return {
                    "success": False,
                    "error": "No feedback submissions found for analysis"
                }
            
            # Calculate response rate
            total_requests = self.db.query(PeerReview).filter(
                PeerReview.review_id == review_id
            ).count()
            
            response_rate = len(feedback_entries) / total_requests if total_requests > 0 else 0.0
            
            # Group feedback by relationship type
            feedback_by_type = defaultdict(list)
            for feedback in feedback_entries:
                feedback_by_type[feedback.relationship_type].append(feedback)
            
            # Calculate rating analytics
            rating_analytics = self._calculate_rating_analytics(feedback_entries)
            
            # Analyze qualitative feedback
            qualitative_analysis = self._analyze_qualitative_feedback(feedback_entries)
            
            # Identify consensus themes
            consensus_analysis = self._identify_consensus_themes(feedback_entries)
            
            # Detect outlier feedback
            outlier_analysis = self._detect_outlier_feedback(feedback_entries, rating_analytics)
            
            # Calculate overall 360 score
            overall_360_score = self._calculate_360_score(
                rating_analytics, response_rate, len(feedback_entries)
            )
            
            # Generate insights and recommendations
            insights = self._generate_360_insights(
                rating_analytics, consensus_analysis, outlier_analysis, response_rate
            )
            
            # Compile comprehensive analysis
            analysis_result = {
                "review_id": review_id,
                "response_statistics": {
                    "total_requests_sent": total_requests,
                    "responses_received": len(feedback_entries),
                    "response_rate": response_rate,
                    "feedback_by_type": {
                        ftype: len(feedbacks) for ftype, feedbacks in feedback_by_type.items()
                    }
                },
                "rating_analytics": rating_analytics,
                "qualitative_analysis": qualitative_analysis,
                "consensus_analysis": consensus_analysis,
                "outlier_analysis": outlier_analysis,
                "overall_360_score": overall_360_score,
                "insights_and_recommendations": insights,
                "reliability_assessment": {
                    "sufficient_responses": len(feedback_entries) >= self.feedback_thresholds["min_total_feedback"],
                    "good_response_rate": response_rate >= self.feedback_thresholds["response_rate_threshold"],
                    "rating_consistency": rating_analytics.get("overall_consistency", 0.0),
                    "analysis_reliability": "HIGH" if (
                        len(feedback_entries) >= self.feedback_thresholds["min_total_feedback"] and 
                        response_rate >= self.feedback_thresholds["response_rate_threshold"]
                    ) else "MEDIUM" if len(feedback_entries) >= 3 else "LOW"
                },
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "legendary_status": "360 FEEDBACK ANALYZED WITH LEGENDARY PRECISION! 🔄🏆"
            }
            
            logger.info(f"📈 360 feedback analysis complete: {len(feedback_entries)} responses analyzed")
            
            return {
                "success": True,
                "feedback_analysis": analysis_result
            }
            
        except Exception as e:
            logger.error(f"💥 360 feedback analysis error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def _generate_feedback_participants(self, review: PerformanceReview, 
                                      config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate list of 360 feedback participants"""
        try:
            participants = []
            employee = review.employee
            
            # Include manager (if different from reviewer)
            if employee.manager_id and employee.manager_id != review.reviewer_id:
                manager = self.db.query(Employee).filter(Employee.id == employee.manager_id).first()
                if manager:
                    participants.append({
                        "reviewer_id": manager.id,
                        "reviewer_name": f"{manager.user.first_name} {manager.user.last_name}",
                        "relationship_type": FeedbackType.MANAGER.value
                    })
            
            # Include peers from same department
            if config.get("include_peers", True):
                peers = self.db.query(Employee).filter(
                    and_(
                        Employee.department_id == employee.department_id,
                        Employee.id != employee.id,
                        Employee.id != employee.manager_id,
                        Employee.employment_status == "ACTIVE"
                    )
                ).limit(config.get("max_peers", 5)).all()
                
                for peer in peers:
                    participants.append({
                        "reviewer_id": peer.id,
                        "reviewer_name": f"{peer.user.first_name} {peer.user.last_name}",
                        "relationship_type": FeedbackType.PEER.value
                    })
            
            # Include direct reports (if manager)
            if config.get("include_direct_reports", True):
                direct_reports = self.db.query(Employee).filter(
                    and_(
                        Employee.manager_id == employee.id,
                        Employee.employment_status == "ACTIVE"
                    )
                ).limit(config.get("max_direct_reports", 8)).all()
                
                for report in direct_reports:
                    participants.append({
                        "reviewer_id": report.id,
                        "reviewer_name": f"{report.user.first_name} {report.user.last_name}",
                        "relationship_type": FeedbackType.DIRECT_REPORT.value
                    })
            
            # Include cross-functional colleagues
            if config.get("include_cross_functional", False):
                # This would require additional relationship mapping
                # For now, we'll skip cross-functional unless specifically configured
                pass
            
            # Add self-assessment if enabled
            if config.get("include_self_assessment", True):
                participants.append({
                    "reviewer_id": employee.id,
                    "reviewer_name": f"{employee.user.first_name} {employee.user.last_name}",
                    "relationship_type": FeedbackType.SELF.value
                })
            
            return {
                "success": True,
                "participants": participants
            }
            
        except Exception as e:
            logger.error(f"💥 Participant generation error: {e}")
            return {
                "success": False,
                "error": f"Failed to generate participants: {str(e)}"
            }
        """
LEGENDARY 360 FEEDBACK SERVICE - CONTINUATION 🔄🎯
More comprehensive than a 720-degree view with X-ray vision!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

    def _validate_feedback_data(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate 360 feedback data with Swiss precision!
        More thorough than a customs inspection with OCD! 🛂📋
        """
        errors = []
        warnings = []
        
        try:
            # Rating validations
            rating_fields = [
                "collaboration_rating", "communication_rating", "leadership_rating",
                "technical_skills_rating", "reliability_rating"
            ]
            
            ratings_provided = 0
            for field in rating_fields:
                if feedback_data.get(field):
                    try:
                        RatingScale(feedback_data[field])
                        ratings_provided += 1
                    except ValueError:
                        errors.append(f"Invalid rating value for {field}")
            
            # Require at least 3 ratings
            if ratings_provided < 3:
                errors.append("At least 3 rating categories must be provided")
            
            # Text field validations
            if feedback_data.get("strengths"):
                strengths = feedback_data["strengths"]
                if len(strengths) < 10:
                    warnings.append("Strengths feedback is quite brief - consider adding more detail")
                elif len(strengths) > 1000:
                    errors.append("Strengths feedback must be no more than 1000 characters")
            
            if feedback_data.get("areas_for_improvement"):
                areas = feedback_data["areas_for_improvement"]
                if len(areas) < 10:
                    warnings.append("Areas for improvement feedback is quite brief")
                elif len(areas) > 1000:
                    errors.append("Areas for improvement must be no more than 1000 characters")
            
            # Require either strengths or areas for improvement
            if not feedback_data.get("strengths") and not feedback_data.get("areas_for_improvement"):
                errors.append("Either strengths or areas for improvement must be provided")
            
            # Specific examples validation
            if feedback_data.get("specific_examples"):
                examples = feedback_data["specific_examples"]
                if len(examples) > 2000:
                    errors.append("Specific examples must be no more than 2000 characters")
            
            return {
                "is_valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings
            }
            
        except Exception as e:
            logger.error(f"💥 Feedback validation error: {e}")
            return {
                "is_valid": False,
                "errors": ["Validation system error"],
                "warnings": []
            }
    
    def _calculate_rating_analytics(self, feedback_entries: List[PeerReview]) -> Dict[str, Any]:
        """
        Calculate comprehensive rating analytics!
        More analytical than a Swiss mathematician with a PhD in statistics! 📊🔢
        """
        try:
            analytics = {}
            
            # Collect all ratings by category
            rating_categories = [
                "collaboration_rating", "communication_rating", "leadership_rating",
                "technical_skills_rating", "reliability_rating", "overall_rating"
            ]
            
            category_analytics = {}
            
            for category in rating_categories:
                ratings = []
                for feedback in feedback_entries:
                    rating = getattr(feedback, category, None)
                    if rating:
                        ratings.append(self._rating_to_numeric(rating))
                
                if ratings:
                    category_analytics[category] = {
                        "count": len(ratings),
                        "mean": statistics.mean(ratings),
                        "median": statistics.median(ratings),
                        "std_dev": statistics.stdev(ratings) if len(ratings) > 1 else 0.0,
                        "min": min(ratings),
                        "max": max(ratings),
                        "distribution": dict(Counter(ratings))
                    }
                else:
                    category_analytics[category] = {
                        "count": 0,
                        "mean": 0.0,
                        "median": 0.0,
                        "std_dev": 0.0,
                        "min": 0.0,
                        "max": 0.0,
                        "distribution": {}
                    }
            
            # Calculate overall consistency
            all_ratings = []
            for category in rating_categories:
                if category_analytics[category]["count"] > 0:
                    all_ratings.extend([
                        self._rating_to_numeric(getattr(feedback, category))
                        for feedback in feedback_entries
                        if getattr(feedback, category, None)
                    ])
            
            overall_consistency = 1.0
            if len(all_ratings) > 1:
                overall_variance = statistics.variance(all_ratings)
                # Normalize variance to 0-1 scale (lower variance = higher consistency)
                overall_consistency = max(0.0, 1.0 - (overall_variance / 4.0))
            
            # Calculate rating agreement by relationship type
            relationship_analytics = {}
            relationship_types = set(feedback.relationship_type for feedback in feedback_entries)
            
            for rel_type in relationship_types:
                rel_feedback = [f for f in feedback_entries if f.relationship_type == rel_type]
                rel_ratings = []
                
                for feedback in rel_feedback:
                    if feedback.overall_rating:
                        rel_ratings.append(self._rating_to_numeric(feedback.overall_rating))
                
                if rel_ratings:
                    relationship_analytics[rel_type] = {
                        "count": len(rel_ratings),
                        "mean": statistics.mean(rel_ratings),
                        "std_dev": statistics.stdev(rel_ratings) if len(rel_ratings) > 1 else 0.0
                    }
            
            analytics = {
                "category_analytics": category_analytics,
                "overall_consistency": overall_consistency,
                "relationship_analytics": relationship_analytics,
                "total_feedback_count": len(feedback_entries),
                "categories_with_data": sum(1 for cat in category_analytics.values() if cat["count"] > 0)
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"💥 Rating analytics calculation error: {e}")
            return {"error": "Failed to calculate rating analytics"}
    
    def _analyze_qualitative_feedback(self, feedback_entries: List[PeerReview]) -> Dict[str, Any]:
        """
        Analyze qualitative feedback with more insight than a Swiss psychologist!
        More comprehensive than a behavioral analysis with attitude! 🧠💭
        """
        try:
            # Collect all text feedback
            strengths_feedback = []
            improvement_feedback = []
            examples_feedback = []
            additional_comments = []
            
            for feedback in feedback_entries:
                if feedback.strengths:
                    strengths_feedback.append({
                        "text": feedback.strengths,
                        "relationship_type": feedback.relationship_type,
                        "reviewer_id": feedback.reviewer_id
                    })
                
                if feedback.areas_for_improvement:
                    improvement_feedback.append({
                        "text": feedback.areas_for_improvement,
                        "relationship_type": feedback.relationship_type,
                        "reviewer_id": feedback.reviewer_id
                    })
                
                if feedback.specific_examples:
                    examples_feedback.append({
                        "text": feedback.specific_examples,
                        "relationship_type": feedback.relationship_type,
                        "reviewer_id": feedback.reviewer_id
                    })
                
                if feedback.additional_comments:
                    additional_comments.append({
                        "text": feedback.additional_comments,
                        "relationship_type": feedback.relationship_type,
                        "reviewer_id": feedback.reviewer_id
                    })
            
            # Extract common themes (simplified keyword analysis)
            strengths_themes = self._extract_themes(strengths_feedback)
            improvement_themes = self._extract_themes(improvement_feedback)
            
            # Calculate feedback richness
            total_text_length = sum(
                len(item["text"]) for item in 
                strengths_feedback + improvement_feedback + examples_feedback + additional_comments
            )
            
            avg_feedback_length = total_text_length / len(feedback_entries) if feedback_entries else 0
            
            qualitative_analysis = {
                "strengths_themes": strengths_themes,
                "improvement_themes": improvement_themes,
                "feedback_richness": {
                    "total_text_length": total_text_length,
                    "average_feedback_length": avg_feedback_length,
                    "detailed_feedback_count": sum(1 for item in strengths_feedback + improvement_feedback if len(item["text"]) > 100),
                    "has_specific_examples": len(examples_feedback) > 0
                },
                "feedback_distribution": {
                    "strengths_provided": len(strengths_feedback),
                    "improvements_provided": len(improvement_feedback),
                    "examples_provided": len(examples_feedback),
                    "additional_comments": len(additional_comments)
                }
            }
            
            return qualitative_analysis
            
        except Exception as e:
            logger.error(f"💥 Qualitative analysis error: {e}")
            return {"error": "Failed to analyze qualitative feedback"}
    
    def _extract_themes(self, feedback_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract common themes from feedback text"""
        try:
            # Simplified theme extraction using keyword frequency
            # In a production system, you'd use NLP libraries for better analysis
            
            common_keywords = {
                "communication": ["communication", "communicates", "articulate", "clear", "explains"],
                "collaboration": ["teamwork", "collaborative", "works well", "team player", "cooperation"],
                "leadership": ["leadership", "leads", "guides", "mentors", "inspires", "motivates"],
                "technical": ["technical", "skilled", "expertise", "knowledge", "proficient"],
                "reliability": ["reliable", "dependable", "consistent", "punctual", "delivers"],
                "problem_solving": ["problem solving", "analytical", "solutions", "creative", "innovative"],
                "adaptability": ["flexible", "adaptable", "change", "learns", "adjusts"]
            }
            
            theme_counts = defaultdict(int)
            theme_examples = defaultdict(list)
            
            for feedback_item in feedback_list:
                text = feedback_item["text"].lower()
                
                for theme, keywords in common_keywords.items():
                    for keyword in keywords:
                        if keyword in text:
                            theme_counts[theme] += 1
                            if len(theme_examples[theme]) < 3:  # Limit examples
                                # Extract sentence containing the keyword
                                sentences = text.split('.')
                                for sentence in sentences:
                                    if keyword in sentence:
                                        theme_examples[theme].append(sentence.strip())
                                        break
                            break
            
            # Format themes with counts and examples
            themes = []
            for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
                if count > 0:
                    themes.append({
                        "theme": theme,
                        "frequency": count,
                        "examples": theme_examples[theme][:2]  # Top 2 examples
                    })
            
            return themes[:5]  # Top 5 themes
            
        except Exception as e:
            logger.error(f"💥 Theme extraction error: {e}")
            return []
    
    def _identify_consensus_themes(self, feedback_entries: List[PeerReview]) -> Dict[str, Any]:
        """
        Identify consensus themes across feedback!
        More accurate than a Swiss referendum with perfect agreement! 🗳️✅
        """
        try:
            # Group feedback by relationship type for consensus analysis
            relationship_groups = defaultdict(list)
            for feedback in feedback_entries:
                relationship_groups[feedback.relationship_type].append(feedback)
            
            # Analyze rating consensus
            rating_consensus = {}
            rating_categories = ["collaboration_rating", "communication_rating", "leadership_rating", 
                               "technical_skills_rating", "reliability_rating"]
            
            for category in rating_categories:
                all_ratings = [
                    self._rating_to_numeric(getattr(feedback, category))
                    for feedback in feedback_entries
                    if getattr(feedback, category, None)
                ]
                
                if len(all_ratings) >= 3:
                    variance = statistics.variance(all_ratings) if len(all_ratings) > 1 else 0
                    consensus_strength = max(0.0, 1.0 - (variance / 2.0))
                    
                    rating_consensus[category] = {
                        "mean_rating": statistics.mean(all_ratings),
                        "consensus_strength": consensus_strength,
                        "has_consensus": consensus_strength >= self.feedback_thresholds["consensus_threshold"]
                    }
            
            # Identify unanimous strengths and improvement areas
            unanimous_strengths = []
            unanimous_improvements = []
            
            # Simple consensus detection (would be more sophisticated in production)
            all_strengths_text = " ".join([
                feedback.strengths.lower() for feedback in feedback_entries 
                if feedback.strengths
            ])
            
            all_improvements_text = " ".join([
                feedback.areas_for_improvement.lower() for feedback in feedback_entries 
                if feedback.areas_for_improvement
            ])
            
            # Check for repeated themes across multiple feedback entries
            strength_themes = self._extract_themes([{"text": all_strengths_text, "relationship_type": "combined", "reviewer_id": 0}])
            improvement_themes = self._extract_themes([{"text": all_improvements_text, "relationship_type": "combined", "reviewer_id": 0}])
            
            # Filter themes that appear in multiple feedback entries
            for theme in strength_themes:
                if theme["frequency"] >= len(feedback_entries) * 0.5:  # 50% consensus
                    unanimous_strengths.append(theme["theme"])
            
            for theme in improvement_themes:
                if theme["frequency"] >= len(feedback_entries) * 0.5:  # 50% consensus
                    unanimous_improvements.append(theme["theme"])
            
            consensus_analysis = {
                "rating_consensus": rating_consensus,
                "unanimous_strengths": unanimous_strengths,
                "unanimous_improvements": unanimous_improvements,
                "consensus_quality": "HIGH" if len(unanimous_strengths) + len(unanimous_improvements) >= 3 else "MEDIUM" if len(unanimous_strengths) + len(unanimous_improvements) >= 1 else "LOW",
                "feedback_alignment": len(unanimous_strengths) + len(unanimous_improvements)
            }
            
            return consensus_analysis
            
        except Exception as e:
            logger.error(f"💥 Consensus analysis error: {e}")
            return {"error": "Failed to analyze consensus"}
    
    def _detect_outlier_feedback(self, feedback_entries: List[PeerReview], 
                                rating_analytics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect outlier feedback that deviates significantly!
        More precise than a Swiss quality control system! 🎯🔍
        """
        try:
            outliers = []
            
            # Get overall rating statistics
            overall_ratings = [
                self._rating_to_numeric(feedback.overall_rating)
                for feedback in feedback_entries
                if feedback.overall_rating
            ]
            
            if len(overall_ratings) < 3:
                return outliers  # Need at least 3 ratings to detect outliers
            
            mean_rating = statistics.mean(overall_ratings)
            std_dev = statistics.stdev(overall_ratings) if len(overall_ratings) > 1 else 0
            
            # Detect statistical outliers
            for feedback in feedback_entries:
                if feedback.overall_rating:
                    rating_value = self._rating_to_numeric(feedback.overall_rating)
                    z_score = abs(rating_value - mean_rating) / std_dev if std_dev > 0 else 0
                    
                    if z_score > self.feedback_thresholds["outlier_threshold"]:
                        outlier_info = {
                            "reviewer_id": feedback.reviewer_id,
                            "relationship_type": feedback.relationship_type,
                            "overall_rating": feedback.overall_rating.value,
                            "rating_value": rating_value,
                            "z_score": z_score,
                            "deviation_type": "HIGH" if rating_value > mean_rating else "LOW",
                            "outlier_strength": "STRONG" if z_score > 2.5 else "MODERATE"
                        }
                        outliers.append(outlier_info)
            
            return outliers
            
        except Exception as e:
            logger.error(f"💥 Outlier detection error: {e}")
            return []
    
    def _calculate_360_score(self, rating_analytics: Dict[str, Any], 
                           response_rate: float, feedback_count: int) -> Dict[str, Any]:
        """
        Calculate comprehensive 360 feedback score!
        More balanced than a Swiss accounting system! ⚖️💯
        """
        try:
            # Base score from average ratings
            category_analytics = rating_analytics.get("category_analytics", {})
            
            # Calculate weighted average of all ratings
            total_weighted_score = 0.0
            total_weight = 0.0
            
            for category, analytics in category_analytics.items():
                if analytics["count"] > 0 and category != "overall_rating":
                    # Use category-specific weights if available
                    weight = self.relationship_weights.get(category, 1.0)
                    total_weighted_score += analytics["mean"] * weight
                    total_weight += weight
            
            base_score = (total_weighted_score / total_weight) * 20 if total_weight > 0 else 0  # Convert to 0-100 scale
            
            # Adjust for response rate
            response_rate_factor = min(1.0, response_rate / self.feedback_thresholds["response_rate_threshold"])
            
            # Adjust for feedback count reliability
            count_factor = min(1.0, feedback_count / self.feedback_thresholds["min_total_feedback"])
            
            # Adjust for consistency
            consistency_score = rating_analytics.get("overall_consistency", 0.5)
            consistency_factor = consistency_score
            
            # Calculate final 360 score
            final_score = base_score * response_rate_factor * count_factor * consistency_factor
            
            # Determine score grade
            if final_score >= 85:
                grade = "EXCELLENT"
            elif final_score >= 75:
                grade = "GOOD"
            elif final_score >= 65:
                grade = "SATISFACTORY"
            elif final_score >= 50:
                grade = "NEEDS_IMPROVEMENT"
            else:
                grade = "POOR"
            
            return {
                "final_score": final_score,
                "base_score": base_score,
                "response_rate_factor": response_rate_factor,
                "count_factor": count_factor,
                "consistency_factor": consistency_factor,
                "grade": grade,
                "score_breakdown": {
                    "rating_quality": base_score,
                    "response_reliability": response_rate_factor * 100,
                    "sample_adequacy": count_factor * 100,
                    "rating_consistency": consistency_factor * 100
                }
            }
            
        except Exception as e:
            logger.error(f"💥 360 score calculation error: {e}")
            return {"final_score": 0, "grade": "ERROR", "error": str(e)}
    
    def _generate_360_insights(self, rating_analytics: Dict[str, Any],
                             consensus_analysis: Dict[str, Any],
                             outlier_analysis: List[Dict[str, Any]],
                             response_rate: float) -> List[str]:
        """Generate actionable insights from 360 feedback analysis"""
        insights = []
        
        try:
            # Response rate insights
            if response_rate >= 0.8:
                insights.append("Excellent response rate indicates strong engagement from colleagues")
            elif response_rate < 0.5:
                insights.append("Low response rate may impact feedback reliability - consider follow-up")
            
            # Rating consistency insights
            consistency = rating_analytics.get("overall_consistency", 0.5)
            if consistency >= 0.8:
                insights.append("High rating consistency across reviewers indicates reliable feedback")
            elif consistency < 0.5:
                insights.append("Low rating consistency suggests varied perspectives - explore differences")
            
            # Consensus insights
            unanimous_strengths = consensus_analysis.get("unanimous_strengths", [])
            unanimous_improvements = consensus_analysis.get("unanimous_improvements", [])
            
            if unanimous_strengths:
                insights.append(f"Strong consensus on strengths: {', '.join(unanimous_strengths[:3])}")
            
            if unanimous_improvements:
                insights.append(f"Clear development opportunities identified: {', '.join(unanimous_improvements[:3])}")
            
            # Outlier insights
            if outlier_analysis:
                high_outliers = [o for o in outlier_analysis if o["deviation_type"] == "HIGH"]
                low_outliers = [o for o in outlier_analysis if o["deviation_type"] == "LOW"]
                
                if high_outliers:
                    insights.append(f"Some reviewers provided notably higher ratings - investigate exceptional performance areas")
                
                if low_outliers:
                    insights.append(f"Some reviewers provided notably lower ratings - may indicate specific areas needing attention")
            
            # Relationship-specific insights
            relationship_analytics = rating_analytics.get("relationship_analytics", {})
            
            if "peer" in relationship_analytics and "manager" in relationship_analytics:
                peer_avg = relationship_analytics["peer"]["mean"]
                manager_avg = relationship_analytics["manager"]["mean"]
                
                if abs(peer_avg - manager_avg) > 0.5:
                    if peer_avg > manager_avg:
                        insights.append("Peers rate performance higher than manager - discuss expectations alignment")
                    else:
                        insights.append("Manager rates performance higher than peers - explore peer collaboration")
            
            # General recommendations
            if not insights:
                insights = [
                    "360 feedback analysis complete - review detailed results for specific insights",
                    "Consider discussing feedback results in upcoming 1:1 meetings",
                    "Use feedback themes to develop targeted improvement plans"
                ]
            
            return insights
            
        except Exception as e:
            logger.error(f"💥 Insights generation error: {e}")
            return ["Error generating insights - review raw feedback data"]
    
    def _rating_to_numeric(self, rating: RatingScale) -> float:
        """Convert rating scale to numeric value"""
        rating_map = {
            RatingScale.EXCEEDS_EXPECTATIONS: 5.0,
            RatingScale.MEETS_EXPECTATIONS: 4.0,
            RatingScale.PARTIALLY_MEETS: 3.0,
            RatingScale.BELOW_EXPECTATIONS: 2.0,
            RatingScale.NEEDS_IMPROVEMENT: 1.0
        }
        return rating_map.get(rating, 3.0)
    
    def _numeric_to_rating(self, numeric_value: float) -> RatingScale:
        """Convert numeric value to rating scale"""
        if numeric_value >= 4.5:
            return RatingScale.EXCEEDS_EXPECTATIONS
        elif numeric_value >= 3.5:
            return RatingScale.MEETS_EXPECTATIONS
        elif numeric_value >= 2.5:
            return RatingScale.PARTIALLY_MEETS
        elif numeric_value >= 1.5:
            return RatingScale.BELOW_EXPECTATIONS
        else:
            return RatingScale.NEEDS_IMPROVEMENT
    
    def _log_360_action(self, action: str, review_id: int, auth_context: AuthContext, 
                       details: Dict[str, Any]):
        """Log 360 feedback actions for audit trail"""
        try:
            audit_log = AuditLog(
                user_id=auth_context.user_id,
                action=action,
                resource_type="360_FEEDBACK",
                resource_id=review_id,
                details=details,
                ip_address=getattr(auth_context, 'ip_address', None),
                user_agent=getattr(auth_context, 'user_agent', None)
            )
            self.db.add(audit_log)
            
        except Exception as e:
            logger.error(f"💥 360 feedback action logging error: {e}")

# 360 FEEDBACK UTILITIES
class FeedbackReportGenerator:
    """
    Generate comprehensive 360 feedback reports!
    More detailed than a Swiss behavioral analysis! 📊🎭
    """
    
    @staticmethod
    def generate_executive_summary(feedback_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of 360 feedback"""
        
        response_stats = feedback_analysis.get("response_statistics", {})
        overall_score = feedback_analysis.get("overall_360_score", {})
        consensus = feedback_analysis.get("consensus_analysis", {})
        
        # Determine overall feedback quality
        score = overall_score.get("final_score", 0)
        response_rate = response_stats.get("response_rate", 0)
        
        if score >= 80 and response_rate >= 0.7:
            quality_status = "EXCELLENT"
            quality_emoji = "🏆"
        elif score >= 65 and response_rate >= 0.5:
            quality_status = "GOOD"
            quality_emoji = "✅"
        elif score >= 50:
            quality_status = "ACCEPTABLE"
            quality_emoji = "⚠️"
        else:
            quality_status = "NEEDS_ATTENTION"
            quality_emoji = "🚨"
        
        return {
            "overall_quality": quality_status,
            "quality_emoji": quality_emoji,
            "360_score": score,
            "response_rate": response_rate,
            "total_responses": response_stats.get("responses_received", 0),
            "key_strengths": consensus.get("unanimous_strengths", [])[:3],
            "key_development_areas": consensus.get("unanimous_improvements", [])[:3],
            "feedback_reliability": overall_score.get("score_breakdown", {}),
            "requires_follow_up": score < 65 or response_rate < 0.5,
            "legendary_status": "360 FEEDBACK ANALYZED WITH LEGENDARY PRECISION! 🔄🏆"
        }
