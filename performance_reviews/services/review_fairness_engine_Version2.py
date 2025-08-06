"""
LEGENDARY REVIEW FAIRNESS ENGINE ⚖️🤖
More balanced than a Supreme Court with a computer science degree!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
import statistics
from collections import defaultdict, Counter
import re
from dataclasses import dataclass

from ..models.review_models import (
    PerformanceReview, ReviewGoal, PeerReview, PerformanceReviewCycle,
    RatingScale, ReviewStatus
)
from ...core.auth.authorization import AuthContext
from ...core.database.base_models import Employee, User, Department

logger = logging.getLogger(__name__)

@dataclass
class BiasDetectionResult:
    """
    Bias detection results that are more detailed than a forensic report!
    More comprehensive than a PhD thesis on fairness! 📊🔍
    """
    has_bias: bool
    bias_type: str
    confidence_score: float
    affected_groups: List[str]
    evidence: List[str]
    recommendations: List[str]
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL

@dataclass
class FairnessMetrics:
    """
    Fairness metrics that are more precise than a Swiss timepiece!
    More accurate than a mathematician with OCD! 📐🎯
    """
    overall_fairness_score: float
    rating_distribution_balance: float
    demographic_parity: float
    calibration_quality: float
    bias_indicators: List[BiasDetectionResult]
    recommendations: List[str]

class LegendaryFairnessEngine:
    """
    The most advanced fairness engine in the galaxy!
    More ethical than a philosophy professor with a justice complex! ⚖️🤖
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # FAIRNESS ENGINE JOKES FOR SUNDAY MORNING MOTIVATION
        self.fairness_jokes = [
            "Why did the bias detector go to therapy? It had discrimination issues! 🤖😄",
            "What's the difference between our fairness engine and a fair judge? Nothing - both are impartial! ⚖️",
            "Why don't biased reviews survive our system? Because fairness always wins! 🏆",
            "What do you call fairness at 3 AM? Night shift justice with style! 🌙",
            "Why did the algorithm become a comedian? It had perfect timing for fairness! ⏰"
        ]
        
        # Bias detection patterns
        self.bias_patterns = {
            "gender_bias": [
                r"\b(emotional|moody|difficult|aggressive|bossy|shrill)\b",
                r"\b(nurturing|caring|supportive)\s+(?:but|however)",
                r"\bfor\s+a\s+(woman|girl|female|lady)\b"
            ],
            "age_bias": [
                r"\b(young|old|seasoned|experienced|senior|junior)\s+(?:for|considering)",
                r"\b(digital\s+native|old\s+school|new\s+generation)\b",
                r"\b(energy\s+of\s+youth|wisdom\s+of\s+age)\b"
            ],
            "racial_bias": [
                r"\b(articulate|well-spoken)\s+(?:for|considering)",
                r"\b(cultural\s+fit|team\s+fit)\b",
                r"\b(natural\s+athlete|good\s+with\s+numbers)\b"
            ],
            "appearance_bias": [
                r"\b(professional\s+appearance|dress|grooming)\b",
                r"\b(polished|presentable|sharp)\b",
                r"\b(image|presence|charisma)\b"
            ],
            "halo_effect": [
                r"\b(excellent\s+in\s+everything|perfect|flawless)\b",
                r"\b(star\s+performer)\s+(?:in|at)\s+everything\b",
                r"\b(can\s+do\s+no\s+wrong)\b"
            ],
            "recency_bias": [
                r"\b(recently|lately|last\s+week|last\s+month)\b.*\b(always|never|consistently)\b",
                r"\b(most\s+recent|latest)\s+(?:project|achievement|mistake)\b"
            ]
        }
        
        # Statistical thresholds for fairness
        self.fairness_thresholds = {
            "rating_variance_max": 0.3,  # Maximum acceptable variance in ratings
            "demographic_parity_min": 0.8,  # Minimum demographic parity score
            "calibration_quality_min": 0.7,  # Minimum calibration quality
            "bias_confidence_threshold": 0.6  # Bias detection confidence threshold
        }
        
        logger.info("⚖️ Legendary Fairness Engine initialized - Justice mode activated!")
    
    def analyze_review_fairness(self, review_id: int, 
                               auth_context: AuthContext) -> Dict[str, Any]:
        """
        Analyze individual review for fairness issues!
        More thorough than a Supreme Court investigation! 🔍⚖️
        """
        try:
            logger.info(f"⚖️ Analyzing review fairness: {review_id}")
            
            # Get review with related data
            review = self.db.query(PerformanceReview).filter(
                PerformanceReview.id == review_id
            ).first()
            
            if not review:
                return {
                    "success": False,
                    "error": "Review not found"
                }
            
            # Perform bias detection
            bias_results = self._detect_bias_in_review(review)
            
            # Analyze rating consistency
            rating_analysis = self._analyze_rating_consistency(review)
            
            # Check for fairness red flags
            red_flags = self._check_fairness_red_flags(review)
            
            # Calculate overall fairness score
            fairness_score = self._calculate_review_fairness_score(
                bias_results, rating_analysis, red_flags
            )
            
            # Generate recommendations
            recommendations = self._generate_fairness_recommendations(
                bias_results, rating_analysis, red_flags
            )
            
            # Compile results
            fairness_analysis = {
                "review_id": review_id,
                "overall_fairness_score": fairness_score,
                "bias_detection": {
                    "has_bias_indicators": len(bias_results) > 0,
                    "bias_count": len(bias_results),
                    "bias_details": [
                        {
                            "type": result.bias_type,
                            "confidence": result.confidence_score,
                            "severity": result.severity,
                            "evidence": result.evidence,
                            "affected_groups": result.affected_groups
                        }
                        for result in bias_results
                    ]
                },
                "rating_analysis": rating_analysis,
                "red_flags": red_flags,
                "recommendations": recommendations,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "requires_attention": fairness_score < 0.7 or len(bias_results) > 0,
                "legendary_joke": "Why did the fairness analysis become legendary? Because it was perfectly balanced! ⚖️🏆"
            }
            
            # Log significant fairness issues
            if fairness_score < 0.6:
                logger.warning(f"🚨 Significant fairness issues detected in review {review_id}")
            elif fairness_score < 0.8:
                logger.info(f"⚠️ Minor fairness concerns in review {review_id}")
            
            return {
                "success": True,
                "fairness_analysis": fairness_analysis
            }
            
        except Exception as e:
            logger.error(f"💥 Review fairness analysis error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def analyze_cycle_fairness(self, cycle_id: int,
                             auth_context: AuthContext) -> Dict[str, Any]:
        """
        Analyze entire review cycle for fairness patterns!
        More comprehensive than a census with attitude! 📊⚖️
        """
        try:
            logger.info(f"📊 Analyzing cycle fairness: {cycle_id}")
            
            # Get all reviews in cycle
            reviews = self.db.query(PerformanceReview).filter(
                PerformanceReview.review_cycle_id == cycle_id
            ).all()
            
            if not reviews:
                return {
                    "success": False,
                    "error": "No reviews found in cycle"
                }
            
            # Analyze rating distributions
            rating_distribution = self._analyze_rating_distribution(reviews)
            
            # Check demographic parity
            demographic_analysis = self._analyze_demographic_parity(reviews)
            
            # Detect systemic bias patterns
            systemic_bias = self._detect_systemic_bias(reviews)
            
            # Analyze calibration quality
            calibration_analysis = self._analyze_calibration_quality(reviews)
            
            # Calculate overall cycle fairness metrics
            cycle_fairness = FairnessMetrics(
                overall_fairness_score=self._calculate_cycle_fairness_score(
                    rating_distribution, demographic_analysis, systemic_bias, calibration_analysis
                ),
                rating_distribution_balance=rating_distribution["balance_score"],
                demographic_parity=demographic_analysis["parity_score"],
                calibration_quality=calibration_analysis["quality_score"],
                bias_indicators=systemic_bias,
                recommendations=self._generate_cycle_recommendations(
                    rating_distribution, demographic_analysis, systemic_bias
                )
            )
            
            # Generate detailed report
            fairness_report = {
                "cycle_id": cycle_id,
                "reviews_analyzed": len(reviews),
                "overall_metrics": {
                    "fairness_score": cycle_fairness.overall_fairness_score,
                    "rating_balance": cycle_fairness.rating_distribution_balance,
                    "demographic_parity": cycle_fairness.demographic_parity,
                    "calibration_quality": cycle_fairness.calibration_quality
                },
                "rating_distribution": rating_distribution,
                "demographic_analysis": demographic_analysis,
                "bias_indicators": [
                    {
                        "type": bias.bias_type,
                        "confidence": bias.confidence_score,
                        "severity": bias.severity,
                        "affected_groups": bias.affected_groups,
                        "evidence_count": len(bias.evidence)
                    }
                    for bias in cycle_fairness.bias_indicators
                ],
                "calibration_analysis": calibration_analysis,
                "recommendations": cycle_fairness.recommendations,
                "requires_intervention": cycle_fairness.overall_fairness_score < 0.7,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "legendary_joke": "Why did the cycle analysis become legendary? Because it brought perfect balance to the force! ⚖️🌟"
            }
            
            logger.info(f"📈 Cycle fairness analysis complete - Score: {cycle_fairness.overall_fairness_score:.2f}")
            
            return {
                "success": True,
                "fairness_report": fairness_report
            }
            
        except Exception as e:
            logger.error(f"💥 Cycle fairness analysis error: {e}")
            return {
                "success": False,
                "error": f"System error: {str(e)}"
            }
    
    def _detect_bias_in_review(self, review: PerformanceReview) -> List[BiasDetectionResult]:
        """Detect bias patterns in review text"""
        bias_results = []
        
        try:
            # Combine all text fields for analysis
            text_fields = [
                review.manager_comments or "",
                review.strengths or "",
                review.areas_for_improvement or "",
                review.self_assessment_comments or ""
            ]
            
            full_text = " ".join(text_fields).lower()
            
            if not full_text.strip():
                return bias_results
            
            # Check each bias pattern
            for bias_type, patterns in self.bias_patterns.items():
                matches = []
                confidence = 0.0
                
                for pattern in patterns:
                    pattern_matches = re.findall(pattern, full_text, re.IGNORECASE)
                    if pattern_matches:
                        matches.extend(pattern_matches)
                        confidence += 0.2  # Each pattern match increases confidence
                
                if matches and confidence >= self.fairness_thresholds["bias_confidence_threshold"]:
                    # Determine severity based on confidence and match count
                    if confidence >= 0.9 or len(matches) >= 3:
                        severity = "HIGH"
                    elif confidence >= 0.7 or len(matches) >= 2:
                        severity = "MEDIUM"
                    else:
                        severity = "LOW"
                    
                    bias_result = BiasDetectionResult(
                        has_bias=True,
                        bias_type=bias_type,
                        confidence_score=min(confidence, 1.0),
                        affected_groups=self._identify_affected_groups(bias_type),
                        evidence=[f"Pattern match: {match}" for match in matches[:3]],  # Limit evidence
                        recommendations=self._get_bias_recommendations(bias_type),
                        severity=severity
                    )
                    
                    bias_results.append(bias_result)
            
            return bias_results
            
        except Exception as e:
            logger.error(f"💥 Bias detection error: {e}")
            return []
    
    def _analyze_rating_consistency(self, review: PerformanceReview) -> Dict[str, Any]:
        """Analyze rating consistency within a review"""
        try:
            # Get all ratings from goals and peer reviews
            goal_ratings = []
            if review.goals:
                for goal in review.goals:
                    if goal.manager_rating:
                        goal_ratings.append(self._rating_to_numeric(goal.manager_rating))
            
            peer_ratings = []
            if review.peer_reviews:
                for peer_review in review.peer_reviews:
                    ratings = [
                        peer_review.collaboration_rating,
                        peer_review.communication_rating,
                        peer_review.leadership_rating,
                        peer_review.technical_skills_rating,
                        peer_review.reliability_rating
                    ]
                    peer_ratings.extend([
                        self._rating_to_numeric(rating) for rating in ratings if rating
                    ])
            
            # Calculate consistency metrics
            all_ratings = goal_ratings + peer_ratings
            
            if len(all_ratings) < 2:
                return {
                    "consistency_score": 1.0,
                    "variance": 0.0,
                    "rating_count": len(all_ratings),
                    "has_inconsistencies": False
                }
            
            variance = statistics.variance(all_ratings)
            consistency_score = max(0.0, 1.0 - (variance / 2.0))  # Normalize variance to 0-1 scale
            
            return {
                "consistency_score": consistency_score,
                "variance": variance,
                "rating_count": len(all_ratings),
                "mean_rating": statistics.mean(all_ratings),
                "has_inconsistencies": variance > self.fairness_thresholds["rating_variance_max"]
            }
            
        except Exception as e:
            logger.error(f"💥 Rating consistency analysis error: {e}")
            return {"consistency_score": 0.5, "variance": 0.0, "rating_count": 0, "has_inconsistencies": False}
    
    def _check_fairness_red_flags(self, review: PerformanceReview) -> List[Dict[str, Any]]:
        """Check for common fairness red flags"""
        red_flags = []
        
        try:
            # Red flag: Extremely short or long feedback
            text_fields = [
                review.manager_comments or "",
                review.strengths or "",
                review.areas_for_improvement or ""
            ]
            
            for field_name, text in zip(["manager_comments", "strengths", "areas_for_improvement"], text_fields):
                word_count = len(text.split()) if text else 0
                
                if word_count < 10 and text:
                    red_flags.append({
                        "type": "insufficient_feedback",
                        "field": field_name,
                        "description": f"Very brief feedback ({word_count} words)",
                        "severity": "MEDIUM"
                    })
                elif word_count > 500:
                    red_flags.append({
                        "type": "excessive_feedback",
                        "field": field_name,
                        "description": f"Unusually long feedback ({word_count} words)",
                        "severity": "LOW"
                    })
            
            # Red flag: Missing key components
            if not review.strengths:
                red_flags.append({
                    "type": "missing_strengths",
                    "description": "No strengths identified",
                    "severity": "MEDIUM"
                })
            
            if not review.areas_for_improvement:
                red_flags.append({
                    "type": "missing_development_areas",
                    "description": "No areas for improvement identified",
                    "severity": "MEDIUM"
                })
            
            # Red flag: Extreme ratings without justification
            if review.overall_rating in [RatingScale.EXCEEDS_EXPECTATIONS, RatingScale.BELOW_EXPECTATIONS]:
                combined_text = " ".join(text_fields)
                if len(combined_text.split()) < 50:
                    red_flags.append({
                        "type": "extreme_rating_insufficient_justification",
                        "description": f"Extreme rating ({review.overall_rating.value}) with minimal justification",
                        "severity": "HIGH"
                    })
            
            return red_flags
            
        except Exception as e:
            logger.error(f"💥 Red flag check error: {e}")
            return []
    
    def _calculate_review_fairness_score(self, bias_results: List[BiasDetectionResult],
                                       rating_analysis: Dict[str, Any],
                                       red_flags: List[Dict[str, Any]]) -> float:
        """Calculate overall fairness score for a review"""
        try:
            base_score = 1.0
            
            # Deduct for bias indicators
            for bias in bias_results:
                if bias.severity == "CRITICAL":
                    base_score -= 0.3
                elif bias.severity == "HIGH":
                    base_score -= 0.2
                elif bias.severity == "MEDIUM":
                    base_score -= 0.1
                else:  # LOW
                    base_score -= 0.05
            
            # Deduct for rating inconsistencies
            if rating_analysis.get("has_inconsistencies"):
                base_score -= 0.15
            
            # Deduct for red flags
            for flag in red_flags:
                if flag["severity"] == "HIGH":
                    base_score -= 0.1
                elif flag["severity"] == "MEDIUM":
                    base_score -= 0.05
                else:  # LOW
                    base_score -= 0.02
            
            # Add bonus for consistency
            base_score += rating_analysis.get("consistency_score", 0.5) * 0.2
            
            return max(0.0, min(1.0, base_score))
            
        except Exception as e:
            logger.error(f"💥 Fairness score calculation error: {e}")
            return 0.5
    
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
    
    def _identify_affected_groups(self, bias_type: str) -> List[str]:
        """Identify groups potentially affected by bias type"""
        affected_groups_map = {
            "gender_bias": ["women", "non-binary individuals"],
            "age_bias": ["younger employees", "older employees"],
            "racial_bias": ["racial minorities", "ethnic minorities"],
            "appearance_bias": ["individuals with non-traditional appearance"],
            "halo_effect": ["all employees"],
            "recency_bias": ["all employees"]
        }
        return affected_groups_map.get(bias_type, ["all employees"])
    
    def _get_bias_recommendations(self, bias_type: str) -> List[str]:
        """Get recommendations for addressing specific bias types"""
        recommendations_map = {
            "gender_bias": [
                "Review language for gender-neutral alternatives",
                "Focus on specific behaviors and outcomes",
                "Avoid appearance or personality-based comments"
            ],
            "age_bias": [
                "Focus on skills and performance, not age-related assumptions",
                "Avoid references to generational characteristics",
                "Evaluate based on actual capabilities demonstrated"
            ],
            "racial_bias": [
                "Remove cultural fit references",
                "Focus on job-relevant skills and performance",
                "Avoid stereotypical assumptions"
            ],
            "appearance_bias": [
                "Focus on work quality and professional competencies",
                "Avoid comments on physical appearance",
                "Evaluate based on job performance metrics"
            ],
            "halo_effect": [
                "Evaluate each competency independently",
                "Provide specific examples for each rating",
                "Consider both strengths and areas for improvement"
            ],
            "recency_bias": [
                "Review performance across the entire evaluation period",
                "Document examples from throughout the review period",
                "Weight recent events appropriately, not exclusively"
            ]
        }
        return recommendations_map.get(bias_type, ["Review feedback for potential bias"])
    """
LEGENDARY REVIEW FAIRNESS ENGINE - CONTINUATION ⚖️🤖
More balanced than a Supreme Court with a computer science degree!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

    def _analyze_rating_distribution(self, reviews: List[PerformanceReview]) -> Dict[str, Any]:
        """
        Analyze rating distribution across all reviews!
        More precise than a statistician with OCD! 📊🎯
        """
        try:
            # Collect all overall ratings
            ratings = []
            for review in reviews:
                if review.overall_rating:
                    ratings.append(self._rating_to_numeric(review.overall_rating))
            
            if not ratings:
                return {
                    "balance_score": 1.0,
                    "distribution": {},
                    "statistical_metrics": {},
                    "anomalies": []
                }
            
            # Calculate distribution
            rating_counts = Counter(ratings)
            total_reviews = len(ratings)
            
            distribution = {
                "exceeds_expectations": rating_counts.get(5.0, 0) / total_reviews,
                "meets_expectations": rating_counts.get(4.0, 0) / total_reviews,
                "partially_meets": rating_counts.get(3.0, 0) / total_reviews,
                "below_expectations": rating_counts.get(2.0, 0) / total_reviews,
                "needs_improvement": rating_counts.get(1.0, 0) / total_reviews
            }
            
            # Calculate statistical metrics
            mean_rating = statistics.mean(ratings)
            median_rating = statistics.median(ratings)
            std_dev = statistics.stdev(ratings) if len(ratings) > 1 else 0
            
            # Expected distribution (benchmark)
            expected_distribution = {
                "exceeds_expectations": 0.10,  # 10% top performers
                "meets_expectations": 0.70,   # 70% solid performers
                "partially_meets": 0.15,      # 15% developing
                "below_expectations": 0.04,   # 4% underperforming
                "needs_improvement": 0.01     # 1% serious issues
            }
            
            # Calculate balance score (how close to expected distribution)
            balance_score = 1.0
            for category, expected in expected_distribution.items():
                actual = distribution[category]
                deviation = abs(actual - expected)
                balance_score -= deviation * 0.5  # Penalize large deviations
            
            balance_score = max(0.0, balance_score)
            
            # Detect anomalies
            anomalies = []
            if distribution["exceeds_expectations"] > 0.25:
                anomalies.append({
                    "type": "grade_inflation",
                    "description": f"Unusually high percentage of top ratings ({distribution['exceeds_expectations']:.1%})",
                    "severity": "MEDIUM"
                })
            
            if distribution["needs_improvement"] + distribution["below_expectations"] > 0.15:
                anomalies.append({
                    "type": "harsh_grading",
                    "description": f"Unusually high percentage of low ratings ({(distribution['needs_improvement'] + distribution['below_expectations']):.1%})",
                    "severity": "MEDIUM"
                })
            
            if std_dev < 0.3:
                anomalies.append({
                    "type": "insufficient_differentiation",
                    "description": f"Very low rating variance (σ={std_dev:.2f})",
                    "severity": "LOW"
                })
            
            return {
                "balance_score": balance_score,
                "distribution": distribution,
                "statistical_metrics": {
                    "mean": mean_rating,
                    "median": median_rating,
                    "std_dev": std_dev,
                    "total_reviews": total_reviews
                },
                "expected_vs_actual": {
                    category: {
                        "expected": expected,
                        "actual": distribution[category],
                        "deviation": abs(distribution[category] - expected)
                    }
                    for category, expected in expected_distribution.items()
                },
                "anomalies": anomalies
            }
            
        except Exception as e:
            logger.error(f"💥 Rating distribution analysis error: {e}")
            return {"balance_score": 0.5, "distribution": {}, "anomalies": []}
    
    def _analyze_demographic_parity(self, reviews: List[PerformanceReview]) -> Dict[str, Any]:
        """
        Analyze demographic parity across different groups!
        More thorough than a civil rights investigation! 👥⚖️
        """
        try:
            # Group reviews by demographic characteristics
            demographic_groups = defaultdict(list)
            
            for review in reviews:
                if review.employee and review.employee.user:
                    user = review.employee.user
                    
                    # Group by department
                    dept_name = review.employee.department.name if review.employee.department else "Unknown"
                    demographic_groups[f"dept_{dept_name}"].append(review)
                    
                    # Group by manager (to detect manager bias)
                    manager_id = review.reviewer_id
                    demographic_groups[f"manager_{manager_id}"].append(review)
                    
                    # Group by employment type
                    emp_type = review.employee.employment_type or "Unknown"
                    demographic_groups[f"emp_type_{emp_type}"].append(review)
            
            # Calculate rating statistics for each group
            group_statistics = {}
            overall_ratings = []
            
            for group_name, group_reviews in demographic_groups.items():
                if len(group_reviews) >= 3:  # Only analyze groups with sufficient data
                    group_ratings = [
                        self._rating_to_numeric(review.overall_rating)
                        for review in group_reviews
                        if review.overall_rating
                    ]
                    
                    if group_ratings:
                        group_statistics[group_name] = {
                            "count": len(group_ratings),
                            "mean_rating": statistics.mean(group_ratings),
                            "std_dev": statistics.stdev(group_ratings) if len(group_ratings) > 1 else 0,
                            "top_rating_percentage": sum(1 for r in group_ratings if r >= 4.5) / len(group_ratings)
                        }
                        overall_ratings.extend(group_ratings)
            
            if not overall_ratings:
                return {"parity_score": 1.0, "group_analysis": {}, "disparities": []}
            
            overall_mean = statistics.mean(overall_ratings)
            
            # Detect disparities
            disparities = []
            parity_scores = []
            
            for group_name, stats in group_statistics.items():
                # Check for significant deviation from overall mean
                deviation = abs(stats["mean_rating"] - overall_mean)
                
                if deviation > 0.5:  # Significant deviation threshold
                    disparities.append({
                        "group": group_name,
                        "type": "rating_disparity",
                        "group_mean": stats["mean_rating"],
                        "overall_mean": overall_mean,
                        "deviation": deviation,
                        "severity": "HIGH" if deviation > 1.0 else "MEDIUM"
                    })
                    parity_scores.append(max(0.0, 1.0 - deviation))
                else:
                    parity_scores.append(1.0)
            
            # Calculate overall parity score
            parity_score = statistics.mean(parity_scores) if parity_scores else 1.0
            
            return {
                "parity_score": parity_score,
                "group_analysis": group_statistics,
                "overall_statistics": {
                    "mean_rating": overall_mean,
                    "total_reviews": len(overall_ratings)
                },
                "disparities": disparities,
                "groups_analyzed": len(group_statistics)
            }
            
        except Exception as e:
            logger.error(f"💥 Demographic parity analysis error: {e}")
            return {"parity_score": 1.0, "group_analysis": {}, "disparities": []}
    
    def _detect_systemic_bias(self, reviews: List[PerformanceReview]) -> List[BiasDetectionResult]:
        """
        Detect systemic bias patterns across multiple reviews!
        More comprehensive than a federal investigation! 🔍🏛️
        """
        try:
            systemic_bias = []
            
            # Analyze all review text for bias patterns
            all_bias_results = []
            for review in reviews:
                review_bias = self._detect_bias_in_review(review)
                all_bias_results.extend(review_bias)
            
            # Group bias by type
            bias_by_type = defaultdict(list)
            for bias in all_bias_results:
                bias_by_type[bias.bias_type].append(bias)
            
            # Detect systemic patterns
            for bias_type, bias_instances in bias_by_type.items():
                if len(bias_instances) >= 3:  # Systemic threshold
                    total_confidence = sum(bias.confidence_score for bias in bias_instances)
                    avg_confidence = total_confidence / len(bias_instances)
                    
                    # Determine if this represents systemic bias
                    prevalence = len(bias_instances) / len(reviews)
                    
                    if prevalence > 0.1:  # More than 10% of reviews show this bias
                        severity = "CRITICAL" if prevalence > 0.3 else "HIGH"
                        
                        systemic_bias_result = BiasDetectionResult(
                            has_bias=True,
                            bias_type=f"systemic_{bias_type}",
                            confidence_score=min(avg_confidence + (prevalence * 0.3), 1.0),
                            affected_groups=self._identify_affected_groups(bias_type),
                            evidence=[f"Detected in {len(bias_instances)} out of {len(reviews)} reviews ({prevalence:.1%})"],
                            recommendations=self._get_systemic_bias_recommendations(bias_type),
                            severity=severity
                        )
                        
                        systemic_bias.append(systemic_bias_result)
            
            return systemic_bias
            
        except Exception as e:
            logger.error(f"💥 Systemic bias detection error: {e}")
            return []
    
    def _analyze_calibration_quality(self, reviews: List[PerformanceReview]) -> Dict[str, Any]:
        """
        Analyze calibration quality across reviews!
        More precise than a Swiss timepiece calibration! ⏰🔧
        """
        try:
            # Get reviews that have been through calibration
            calibrated_reviews = [r for r in reviews if r.calibration_notes or r.calibration_adjustments]
            
            if not calibrated_reviews:
                return {
                    "quality_score": 0.5,
                    "calibrated_count": 0,
                    "adjustment_analysis": {},
                    "needs_calibration": len(reviews)
                }
            
            # Analyze calibration adjustments
            total_adjustments = 0
            significant_adjustments = 0
            
            for review in calibrated_reviews:
                if review.calibration_adjustments:
                    adjustments = review.calibration_adjustments.get("rating_changes", {})
                    
                    for original, adjusted in adjustments.items():
                        try:
                            orig_numeric = float(original)
                            adj_numeric = float(adjusted)
                            adjustment_size = abs(orig_numeric - adj_numeric)
                            
                            total_adjustments += 1
                            if adjustment_size >= 1.0:  # Significant adjustment threshold
                                significant_adjustments += 1
                        except (ValueError, TypeError):
                            continue
            
            # Calculate quality metrics
            if total_adjustments > 0:
                significant_adjustment_rate = significant_adjustments / total_adjustments
                
                # Lower significant adjustment rate indicates better initial calibration
                quality_score = max(0.0, 1.0 - (significant_adjustment_rate * 0.8))
            else:
                quality_score = 0.8  # Assume good quality if no adjustments needed
            
            return {
                "quality_score": quality_score,
                "calibrated_count": len(calibrated_reviews),
                "total_count": len(reviews),
                "calibration_coverage": len(calibrated_reviews) / len(reviews),
                "adjustment_analysis": {
                    "total_adjustments": total_adjustments,
                    "significant_adjustments": significant_adjustments,
                    "significant_rate": significant_adjustment_rate if total_adjustments > 0 else 0.0
                },
                "needs_calibration": len(reviews) - len(calibrated_reviews)
            }
            
        except Exception as e:
            logger.error(f"💥 Calibration quality analysis error: {e}")
            return {"quality_score": 0.5, "calibrated_count": 0, "needs_calibration": 0}
    
    def _calculate_cycle_fairness_score(self, rating_dist: Dict[str, Any],
                                      demographic: Dict[str, Any],
                                      systemic_bias: List[BiasDetectionResult],
                                      calibration: Dict[str, Any]) -> float:
        """
        Calculate overall cycle fairness score!
        More balanced than a supreme court decision! ⚖️📊
        """
        try:
            # Base components with weights
            components = {
                "rating_distribution": (rating_dist.get("balance_score", 0.5), 0.25),
                "demographic_parity": (demographic.get("parity_score", 0.5), 0.30),
                "calibration_quality": (calibration.get("quality_score", 0.5), 0.20),
                "bias_absence": (1.0, 0.25)  # Start with perfect score, deduct for bias
            }
            
            # Deduct for systemic bias
            bias_penalty = 0.0
            for bias in systemic_bias:
                if bias.severity == "CRITICAL":
                    bias_penalty += 0.4
                elif bias.severity == "HIGH":
                    bias_penalty += 0.2
                elif bias.severity == "MEDIUM":
                    bias_penalty += 0.1
            
            components["bias_absence"] = (max(0.0, 1.0 - bias_penalty), 0.25)
            
            # Calculate weighted score
            total_score = sum(score * weight for score, weight in components.values())
            
            return max(0.0, min(1.0, total_score))
            
        except Exception as e:
            logger.error(f"💥 Cycle fairness score calculation error: {e}")
            return 0.5
    
    def _generate_cycle_recommendations(self, rating_dist: Dict[str, Any],
                                      demographic: Dict[str, Any],
                                      systemic_bias: List[BiasDetectionResult]) -> List[str]:
        """Generate recommendations for improving cycle fairness"""
        recommendations = []
        
        try:
            # Rating distribution recommendations
            if rating_dist.get("balance_score", 1.0) < 0.7:
                for anomaly in rating_dist.get("anomalies", []):
                    if anomaly["type"] == "grade_inflation":
                        recommendations.append("Consider calibration sessions to address potential grade inflation")
                    elif anomaly["type"] == "harsh_grading":
                        recommendations.append("Review grading standards to ensure fair evaluation criteria")
                    elif anomaly["type"] == "insufficient_differentiation":
                        recommendations.append("Encourage managers to provide more differentiated ratings")
            
            # Demographic parity recommendations
            if demographic.get("parity_score", 1.0) < 0.8:
                recommendations.append("Conduct bias training for managers showing rating disparities")
                recommendations.append("Implement structured interview guides and evaluation criteria")
                
                for disparity in demographic.get("disparities", []):
                    if "manager_" in disparity["group"]:
                        recommendations.append(f"Provide additional calibration support for manager {disparity['group']}")
            
            # Systemic bias recommendations
            if systemic_bias:
                recommendations.append("Implement organization-wide bias awareness training")
                recommendations.append("Consider using structured evaluation templates")
                recommendations.append("Establish bias review committees for performance evaluations")
            
            # General recommendations
            recommendations.extend([
                "Regular calibration sessions across all departments",
                "Anonymous feedback collection on review process fairness",
                "Quarterly fairness metrics review and improvement planning"
            ])
            
            return recommendations
            
        except Exception as e:
            logger.error(f"💥 Recommendation generation error: {e}")
            return ["Review performance evaluation processes for potential improvements"]
    
    def _get_systemic_bias_recommendations(self, bias_type: str) -> List[str]:
        """Get recommendations for addressing systemic bias"""
        systemic_recommendations = {
            "gender_bias": [
                "Implement organization-wide gender bias training",
                "Use structured evaluation forms with specific behavioral anchors",
                "Establish diverse review panels for performance evaluations"
            ],
            "age_bias": [
                "Train managers on age-inclusive performance evaluation",
                "Focus evaluation criteria on job-relevant competencies",
                "Implement reverse mentoring programs"
            ],
            "racial_bias": [
                "Conduct comprehensive diversity and inclusion training",
                "Establish bias review committees with diverse representation",
                "Implement blind review processes where possible"
            ],
            "halo_effect": [
                "Use competency-based evaluation frameworks",
                "Require specific examples for each rating category",
                "Implement multi-rater feedback systems"
            ],
            "recency_bias": [
                "Implement quarterly performance documentation requirements",
                "Use performance tracking tools throughout the review period",
                "Train managers on comprehensive performance evaluation"
            ]
        }
        
        return systemic_recommendations.get(bias_type, ["Address systemic bias through comprehensive training"])
    
    def _generate_fairness_recommendations(self, bias_results: List[BiasDetectionResult],
                                         rating_analysis: Dict[str, Any],
                                         red_flags: List[Dict[str, Any]]) -> List[str]:
        """Generate specific recommendations for individual review fairness"""
        recommendations = []
        
        # Bias-specific recommendations
        for bias in bias_results:
            recommendations.extend(bias.recommendations)
        
        # Rating consistency recommendations
        if rating_analysis.get("has_inconsistencies"):
            recommendations.append("Review rating consistency across different competency areas")
            recommendations.append("Provide specific examples to support each rating")
        
        # Red flag recommendations
        for flag in red_flags:
            if flag["type"] == "insufficient_feedback":
                recommendations.append("Provide more detailed feedback with specific examples")
            elif flag["type"] == "missing_strengths":
                recommendations.append("Identify and document specific employee strengths")
            elif flag["type"] == "missing_development_areas":
                recommendations.append("Provide constructive feedback on development opportunities")
        
        # General fairness recommendations
        if not recommendations:
            recommendations = [
                "Review appears fair and balanced",
                "Continue providing specific, actionable feedback",
                "Maintain focus on job-relevant performance criteria"
            ]
        
        return recommendations

# FAIRNESS ENGINE UTILITIES
class FairnessReportGenerator:
    """
    Generate comprehensive fairness reports!
    More detailed than a federal audit with style! 📊✨
    """
    
    @staticmethod
    def generate_executive_summary(fairness_metrics: FairnessMetrics) -> Dict[str, Any]:
        """Generate executive summary of fairness analysis"""
        
        # Determine overall status
        if fairness_metrics.overall_fairness_score >= 0.9:
            status = "EXCELLENT"
            status_emoji = "🏆"
        elif fairness_metrics.overall_fairness_score >= 0.8:
            status = "GOOD"
            status_emoji = "✅"
        elif fairness_metrics.overall_fairness_score >= 0.7:
            status = "ACCEPTABLE"
            status_emoji = "⚠️"
        else:
            status = "NEEDS_IMPROVEMENT"
            status_emoji = "🚨"
        
        # Count high-severity bias indicators
        critical_issues = sum(1 for bias in fairness_metrics.bias_indicators if bias.severity in ["CRITICAL", "HIGH"])
        
        return {
            "overall_status": status,
            "status_emoji": status_emoji,
            "fairness_score": fairness_metrics.overall_fairness_score,
            "key_metrics": {
                "rating_balance": fairness_metrics.rating_distribution_balance,
                "demographic_parity": fairness_metrics.demographic_parity,
                "calibration_quality": fairness_metrics.calibration_quality
            },
            "critical_issues_count": critical_issues,
            "requires_immediate_attention": fairness_metrics.overall_fairness_score < 0.7 or critical_issues > 0,
            "top_recommendations": fairness_metrics.recommendations[:3],
            "legendary_status": "FAIR AND BALANCED LIKE A LEGENDARY SUPREME COURT! ⚖️🏆"
        }
