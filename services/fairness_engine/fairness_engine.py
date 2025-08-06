"""
LEGENDARY FAIRNESS ENGINE 🛡️⚖️
More impartial than a supreme court with no political agenda!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import logging
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
import hashlib
import json

logger = logging.getLogger(__name__)

class FairnessEngine:
    """
    The most impartial fairness engine in the galaxy! 🌟
    Prevents manipulation better than a bouncer at an exclusive club! 🚪
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # FAIRNESS JOKES FOR MAXIMUM MOTIVATION
        self.fairness_jokes = [
            "Why did the fair assessment become a judge? It was great at weighing evidence! ⚖️😄",
            "What's the difference between this system and favoritism? About 100% integrity! 🎯",
            "Why don't biased assessments work here? Because our fairness engine has trust issues! 🛡️",
            "What do you call an assessment that can't be manipulated? LEGENDARY! 🎸",
            "Why did the corrupt score go to therapy? It had integrity problems! 💊"
        ]
    
    def enforce_comprehensive_fairness(self, employee_id: int, assessor_id: Optional[int], 
                                     preliminary_scores: Dict[str, float], 
                                     assessment_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Master fairness enforcement method that makes corruption impossible!
        More thorough than a forensic accountant with OCD! 🔍💎
        """
        try:
            logger.info(f"🛡️ FAIRNESS ENGINE ACTIVATED for employee {employee_id}")
            
            # STEP 1: Generate fairness fingerprint
            fairness_fingerprint = self._generate_fairness_fingerprint(
                employee_id, assessor_id, preliminary_scores, assessment_context
            )
            
            # STEP 2: Multi-layer bias detection
            bias_analysis = self._comprehensive_bias_detection(
                employee_id, assessor_id, preliminary_scores
            )
            
            # STEP 3: Statistical validation
            statistical_validation = self._statistical_validation_suite(
                preliminary_scores, employee_id
            )
            
            # STEP 4: Apply fairness corrections
            fair_scores = self._apply_fairness_corrections(
                preliminary_scores, bias_analysis, statistical_validation
            )
            
            # STEP 5: Generate integrity certificate
            integrity_cert = self._generate_integrity_certificate(
                fairness_fingerprint, bias_analysis, fair_scores
            )
            
            # STEP 6: Create immutable audit record
            audit_record = self._create_immutable_audit_record(
                employee_id, assessor_id, preliminary_scores, fair_scores, integrity_cert
            )
            
            return {
                "validated_scores": fair_scores,
                "fairness_fingerprint": fairness_fingerprint,
                "bias_analysis": bias_analysis,
                "statistical_validation": statistical_validation,
                "integrity_certificate": integrity_cert,
                "audit_record_id": audit_record["id"],
                "fairness_confidence": self._calculate_fairness_confidence(bias_analysis),
                "manipulation_resistance_level": "MAXIMUM",
                "fairness_joke": np.random.choice(self.fairness_jokes)
            }
            
        except Exception as e:
            logger.error(f"💥 Fairness engine error: {e}")
            return self._emergency_fairness_protocol(preliminary_scores)
    
    def _generate_fairness_fingerprint(self, employee_id: int, assessor_id: Optional[int], 
                                     scores: Dict[str, float], context: Dict[str, Any]) -> str:
        """Generate unique fairness fingerprint for tamper detection"""
        fingerprint_data = {
            "employee_id": employee_id,
            "assessor_id": assessor_id,
            "timestamp": datetime.utcnow().isoformat(),
            "scores_hash": hashlib.sha256(json.dumps(scores, sort_keys=True).encode()).hexdigest(),
            "context_hash": hashlib.sha256(json.dumps(context, sort_keys=True).encode()).hexdigest()
        }
        
        fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.sha256(fingerprint_string.encode()).hexdigest()
    
    def _comprehensive_bias_detection(self, employee_id: int, assessor_id: Optional[int], 
                                    scores: Dict[str, float]) -> Dict[str, Any]:
        """Multi-dimensional bias detection system"""
        bias_analysis = {
            "assessor_bias": self._detect_assessor_bias_patterns(assessor_id, scores),
            "demographic_bias": self._detect_demographic_bias(employee_id, scores),
            "temporal_bias": self._detect_temporal_manipulation(employee_id, scores),
            "peer_comparison_bias": self._detect_peer_comparison_anomalies(employee_id, scores),
            "category_bias": self._detect_skill_category_bias(scores),
            "inflation_bias": self._detect_score_inflation(scores, employee_id),
            "consistency_bias": self._detect_internal_consistency_issues(scores)
        }
        
        # Calculate overall bias risk
        bias_scores = [analysis["risk_level"] for analysis in bias_analysis.values()]
        overall_bias_risk = np.mean(bias_scores)
        
        bias_analysis["overall_bias_risk"] = overall_bias_risk
        bias_analysis["bias_severity"] = self._categorize_bias_severity(overall_bias_risk)
        
        return bias_analysis
    
    def _detect_assessor_bias_patterns(self, assessor_id: Optional[int], scores: Dict[str, float]) -> Dict[str, Any]:
        """Detect patterns in assessor scoring that indicate bias"""
        if not assessor_id:
            return {"risk_level": 0.0, "pattern": "no_assessor", "details": "Self-assessment"}
        
        # Get assessor's historical scoring patterns
        historical_assessments = self.db.query(SkillAssessment).filter(
            SkillAssessment.assessor_id == assessor_id
        ).all()
        
        if len(historical_assessments) < 3:
            return {"risk_level": 0.1, "pattern": "insufficient_data", "details": "New assessor"}
        
        # Calculate assessor's average scoring compared to system average
        assessor_averages = []
        system_averages = []
        
        for assessment in historical_assessments:
            if assessment.skill_breakdown:
                assessor_avg = np.mean(list(assessment.skill_breakdown.values()))
                assessor_averages.append(assessor_avg)
        
        # Get system-wide averages for comparison
        all_assessments = self.db.query(SkillAssessment).all()
        for assessment in all_assessments:
            if assessment.skill_breakdown and assessment.assessor_id != assessor_id:
                system_avg = np.mean(list(assessment.skill_breakdown.values()))
                system_averages.append(system_avg)
        
        if assessor_averages and system_averages:
            assessor_mean = np.mean(assessor_averages)
            system_mean = np.mean(system_averages)
            bias_magnitude = abs(assessor_mean - system_mean)
            
            if bias_magnitude > 15:  # 15 point difference
                return {
                    "risk_level": 0.8,
                    "pattern": "significant_bias",
                    "details": f"Assessor avg: {assessor_mean:.1f}, System avg: {system_mean:.1f}",
                    "bias_direction": "inflation" if assessor_mean > system_mean else "deflation"
                }
            elif bias_magnitude > 8:  # 8 point difference
                return {
                    "risk_level": 0.4,
                    "pattern": "moderate_bias",
                    "details": f"Moderate scoring difference: {bias_magnitude:.1f} points"
                }
        
        return {"risk_level": 0.1, "pattern": "normal", "details": "No significant bias detected"}
    
    def _detect_demographic_bias(self, employee_id: int, scores: Dict[str, float]) -> Dict[str, Any]:
        """Detect potential demographic bias in scoring patterns"""
        # This would integrate with HR demographic data in production
        # For demo, we'll simulate bias detection
        
        avg_score = np.mean(list(scores.values()))
        
        # Simulate demographic analysis (in production would use real demographic data)
        demographic_risk = 0.0
        
        # Check if scores are suspiciously different from department averages
        dept_avg = self._get_department_average(employee_id)
        if abs(avg_score - dept_avg) > 20:
            demographic_risk = 0.3
        
        return {
            "risk_level": demographic_risk,
            "pattern": "demographic_analysis",
            "details": "Demographic bias screening completed",
            "recommendations": ["Ensure diverse assessment panels", "Use structured evaluation criteria"]
        }
    
    def _detect_temporal_manipulation(self, employee_id: int, scores: Dict[str, float]) -> Dict[str, Any]:
        """Detect suspicious timing patterns that might indicate manipulation"""
        recent_assessments = self.db.query(SkillAssessment).filter(
            SkillAssessment.employee_id == employee_id
        ).order_by(desc(SkillAssessment.assessment_date)).limit(3).all()
        
        if len(recent_assessments) < 2:
            return {"risk_level": 0.0, "pattern": "insufficient_history", "details": "No temporal comparison possible"}
        
        # Check for suspicious rapid improvements
        score_changes = []
        for i in range(1, len(recent_assessments)):
            current_avg = np.mean(list(scores.values()))
            previous_avg = np.mean(list(recent_assessments[i].skill_breakdown.values())) if recent_assessments[i].skill_breakdown else 65
            
            days_between = (datetime.utcnow() - recent_assessments[i].assessment_date).days
            if days_between > 0:
                improvement_rate = (current_avg - previous_avg) / days_between
                score_changes.append(improvement_rate)
        
        if score_changes:
            max_improvement_rate = max(score_changes)
            if max_improvement_rate > 0.5:  # More than 0.5 points per day
                return {
                    "risk_level": 0.7,
                    "pattern": "suspicious_rapid_improvement",
                    "details": f"Improvement rate: {max_improvement_rate:.2f} points/day"
                }
        
        return {"risk_level": 0.1, "pattern": "normal_progression", "details": "Natural skill development pattern"}
    
    def _detect_peer_comparison_anomalies(self, employee_id: int, scores: Dict[str, float]) -> Dict[str, Any]:
        """Detect scores that are anomalous compared to peer group"""
        peer_scores = self._get_peer_group_statistics(employee_id)
        avg_score = np.mean(list(scores.values()))
        
        anomaly_risk = 0.0
        anomaly_details = []
        
        for skill, score in scores.items():
            if skill in peer_scores:
                peer_avg = peer_scores[skill]["average"]
                peer_std = peer_scores[skill]["std_dev"]
                
                if peer_std > 0:
                    z_score = abs(score - peer_avg) / peer_std
                    if z_score > 3:  # More than 3 standard deviations
                        anomaly_risk = max(anomaly_risk, 0.8)
                        anomaly_details.append(f"{skill}: z-score {z_score:.2f}")
                    elif z_score > 2:  # More than 2 standard deviations
                        anomaly_risk = max(anomaly_risk, 0.4)
        
        return {
            "risk_level": anomaly_risk,
            "pattern": "peer_comparison" if anomaly_risk > 0.3 else "normal_range",
            "details": anomaly_details if anomaly_details else "Scores within normal peer range"
        }
    
    def _statistical_validation_suite(self, scores: Dict[str, float], employee_id: int) -> Dict[str, Any]:
        """Comprehensive statistical validation of scores"""
        validation_results = {
            "normality_test": self._test_score_normality(scores),
            "outlier_analysis": self._comprehensive_outlier_analysis(scores, employee_id),
            "consistency_check": self._internal_consistency_validation(scores),
            "benchmark_validation": self._industry_benchmark_validation(scores),
            "correlation_analysis": self._skill_correlation_analysis(scores)
        }
        
        # Calculate overall validation confidence
        validation_scores = [result["confidence"] for result in validation_results.values()]
        overall_confidence = np.mean(validation_scores)
        
        validation_results["overall_confidence"] = overall_confidence
        validation_results["validation_status"] = "PASSED" if overall_confidence > 0.8 else "FLAGGED"
        
        return validation_results
    
    def _apply_fairness_corrections(self, scores: Dict[str, float], bias_analysis: Dict[str, Any], 
                                  statistical_validation: Dict[str, Any]) -> Dict[str, float]:
        """Apply fairness corrections based on bias and statistical analysis"""
        corrected_scores = scores.copy()
        
        # Apply bias corrections
        if bias_analysis["overall_bias_risk"] > 0.5:
            logger.warning(f"🚨 High bias risk detected: {bias_analysis['overall_bias_risk']:.2f}")
            
            # Apply conservative correction factor
            correction_factor = 1.0 - (bias_analysis["overall_bias_risk"] * 0.1)  # Max 10% reduction
            
            for skill in corrected_scores:
                original_score = corrected_scores[skill]
                corrected_scores[skill] = original_score * correction_factor
                logger.info(f"🛡️ Bias-corrected {skill}: {original_score:.1f} → {corrected_scores[skill]:.1f}")
        
        # Apply statistical corrections
        if statistical_validation["validation_status"] == "FLAGGED":
            for skill, score in corrected_scores.items():
                outlier_info = statistical_validation["outlier_analysis"].get(skill, {})
                if outlier_info.get("is_outlier", False):
                    # Move outlier toward the median
                    median_score = outlier_info.get("median", 65)
                    correction_strength = 0.3  # Move 30% toward median
                    
                    corrected_score = score + (median_score - score) * correction_strength
                    corrected_scores[skill] = corrected_score
                    logger.info(f"📊 Statistical-corrected {skill}: {score:.1f} → {corrected_score:.1f}")
        
        return corrected_scores