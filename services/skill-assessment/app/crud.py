"""
CRUD Operations for Skill Assessment Service - PART 1
Where skill algorithms meet database reality! 🎓🤖
Coded by rickroll187 at 2025-08-03 19:45:16 UTC
"""
import logging
import random
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func

from app.models import (
    SkillAssessment, AssessmentResult, CertificationTracking, SkillCategory,
    SkillGapAnalysis, SkillEvidence, SkillAssessmentAnalytics
)
from app.schemas import (
    SkillAssessmentRequest, SkillAssessmentResponse, CertificationTrackingRequest,
    CertificationTrackingResponse, SkillGapAnalysisRequest, SkillGapAnalysisResponse,
    SkillProficiency, SkillProfileSummary, SkillGap
)

logger = logging.getLogger(__name__)

class SkillAssessmentCRUD:
    """
    CRUD operations for skill assessment
    More reliable than standardized tests, funnier than academic conferences! 🎓😄
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # Skill competency framework
        self.skill_framework = {
            "technical": {
                "python": {"weight": 0.95, "market_demand": "critical", "learning_curve": "moderate"},
                "javascript": {"weight": 0.93, "market_demand": "critical", "learning_curve": "moderate"},
                "java": {"weight": 0.88, "market_demand": "high", "learning_curve": "steep"},
                "react": {"weight": 0.90, "market_demand": "high", "learning_curve": "moderate"},
                "node.js": {"weight": 0.85, "market_demand": "high", "learning_curve": "easy"},
                "sql": {"weight": 0.82, "market_demand": "critical", "learning_curve": "easy"},
                "docker": {"weight": 0.80, "market_demand": "high", "learning_curve": "moderate"},
                "kubernetes": {"weight": 0.78, "market_demand": "high", "learning_curve": "steep"},
                "aws": {"weight": 0.85, "market_demand": "critical", "learning_curve": "moderate"},
                "machine_learning": {"weight": 0.87, "market_demand": "high", "learning_curve": "steep"}
            },
            "soft_skills": {
                "communication": {"weight": 0.98, "market_demand": "critical", "learning_curve": "moderate"},
                "leadership": {"weight": 0.90, "market_demand": "high", "learning_curve": "steep"},
                "teamwork": {"weight": 0.95, "market_demand": "critical", "learning_curve": "moderate"},
                "problem_solving": {"weight": 0.97, "market_demand": "critical", "learning_curve": "moderate"},
                "adaptability": {"weight": 0.92, "market_demand": "high", "learning_curve": "moderate"},
                "time_management": {"weight": 0.85, "market_demand": "high", "learning_curve": "easy"},
                "critical_thinking": {"weight": 0.94, "market_demand": "high", "learning_curve": "steep"}
            },
            "domain": {
                "project_management": {"weight": 0.85, "market_demand": "high", "learning_curve": "moderate"},
                "data_analysis": {"weight": 0.88, "market_demand": "high", "learning_curve": "moderate"},
                "cloud_architecture": {"weight": 0.90, "market_demand": "high", "learning_curve": "steep"},
                "devops": {"weight": 0.83, "market_demand": "high", "learning_curve": "moderate"},
                "cybersecurity": {"weight": 0.86, "market_demand": "critical", "learning_curve": "steep"},
                "ui_ux_design": {"weight": 0.78, "market_demand": "medium", "learning_curve": "moderate"}
            }
        }
        
        # Assessment jokes for motivation
        self.assessment_jokes = [
            "Why did the skill assessment go to school? To get more class! 🎓",
            "What's the difference between a skill assessment and a final exam? One measures what you know! 📚",
            "Why don't skill assessments ever get lost? Because they always know where you stand! 📍",
            "What do you call a skill assessment that tells dad jokes? A pun-ficiency test! 😄",
            "Why did the competency go to therapy? It had skill issues! But yours are perfect! 💪",
            "What's a skill's favorite type of music? Competency rock! 🎸"
        ]
        
        # Bias detection weights
        self.bias_detection_weights = {
            "assessment_consistency": 0.30,
            "skill_category_balance": 0.25,
            "evidence_objectivity": 0.20,
            "competency_progression": 0.15,
            "market_alignment": 0.10
        }
        
        # Competency level mappings
        self.competency_levels = {
            (0, 25): "beginner",
            (25, 50): "intermediate", 
            (50, 75): "advanced",
            (75, 100): "expert"
        }    def assess_employee_skills(self, request: SkillAssessmentRequest) -> SkillAssessmentResponse:
        """
        Assess employee skills with more precision than a Swiss chronometer!
        This assessment is so accurate, it makes standardized tests weep! 🎓✨
        """
        try:
            logger.info(f"🎓 Assessing {len(request.skills_to_assess)} skills for employee {request.employee_id}")
            
            # Perform individual skill assessments
            skill_proficiencies = []
            total_proficiency = 0.0
            
            for skill in request.skills_to_assess:
                proficiency = self._assess_individual_skill(request.employee_id, skill, request.assessment_type)
                skill_proficiencies.append(proficiency)
                total_proficiency += proficiency.proficiency_level
            
            # Calculate overall proficiency score
            overall_proficiency = total_proficiency / len(request.skills_to_assess) if skill_proficiencies else 0
            
            # Identify strengths and improvement areas
            strengths = self._identify_skill_strengths(skill_proficiencies)
            improvement_areas = self._identify_improvement_areas(skill_proficiencies)
            
            # Calculate market relevance
            market_relevance_score = self._calculate_market_relevance(skill_proficiencies)
            
            # Assess future skill potential
            future_potential = self._assess_future_skill_potential(request.employee_id, skill_proficiencies)
            
            # Generate learning recommendations
            learning_paths = self._generate_learning_recommendations(skill_proficiencies, improvement_areas)
            
            # Generate certification recommendations
            cert_recommendations = self._generate_certification_recommendations(skill_proficiencies)
            
            # Bias detection analysis
            bias_metrics = self._analyze_assessment_bias(request, skill_proficiencies, overall_proficiency)
            
            # Calculate confidence interval
            confidence_interval = self._calculate_assessment_confidence(request, skill_proficiencies)
            
            # Generate assessment summary
            assessment_summary = self._generate_assessment_summary(overall_proficiency, strengths, improvement_areas)
            
            # Determine next assessment date
            next_assessment_date = self._calculate_next_assessment_date(request.assessment_type, overall_proficiency)
            
            # Create skill assessment record
            skill_assessment = SkillAssessment(
                employee_id=request.employee_id,
                assessor_id=request.assessor_id,
                assessment_type=request.assessment_type,
                overall_proficiency_score=overall_proficiency,
                skill_breakdown={skill.skill_name: skill.proficiency_level for skill in skill_proficiencies},
                assessment_method=request.assessment_method,
                assessment_duration_minutes=self._estimate_assessment_duration(request),
                confidence_interval=confidence_interval,
                bias_score=bias_metrics["overall_bias"],
                market_relevance_score=market_relevance_score,
                future_skill_potential=future_potential,
                strengths_identified=strengths,
                improvement_areas=improvement_areas,
                recommended_learning_paths=learning_paths,
                next_assessment_date=next_assessment_date
            )
            
            self.db.add(skill_assessment)
            self.db.commit()
            self.db.refresh(skill_assessment)
            
            # Create individual assessment results
            for proficiency in skill_proficiencies:
                assessment_result = AssessmentResult(
                    skill_assessment_id=skill_assessment.id,
                    employee_id=request.employee_id,
                    skill_name=proficiency.skill_name,
                    skill_category=proficiency.skill_category,
                    proficiency_level=proficiency.proficiency_level,
                    competency_level=proficiency.competency_level,
                    assessment_criteria=self._get_assessment_criteria(proficiency.skill_name),
                    market_demand_level=proficiency.market_demand_level,
                    skill_currency=proficiency.skill_currency,
                    recommended_actions=proficiency.recommended_actions,
                    industry_relevance=self._calculate_industry_relevance(proficiency.skill_name),
                    assessment_confidence=proficiency.assessment_confidence
                )
                self.db.add(assessment_result)
            
            self.db.commit()
            
            response = SkillAssessmentResponse(
                assessment_id=skill_assessment.id,
                employee_id=request.employee_id,
                assessor_id=request.assessor_id,
                assessment_type=request.assessment_type,
                assessment_date=skill_assessment.assessment_date,
                overall_proficiency_score=overall_proficiency,
                skill_proficiencies=skill_proficiencies,
                strengths_identified=strengths,
                improvement_areas=improvement_areas,
                market_relevance_score=market_relevance_score,
                future_skill_potential=future_potential,
                recommended_learning_paths=learning_paths,
                certification_recommendations=cert_recommendations,
                bias_metrics=bias_metrics,
                confidence_interval=confidence_interval,
                next_assessment_date=next_assessment_date,
                assessment_summary=assessment_summary
            )
            
            logger.info(f"✅ Skill assessment completed with overall score: {overall_proficiency:.2f}/100")
            return response
            
        except Exception as e:
            logger.error(f"💥 Error assessing skills: {e}")
            self.db.rollback()
            raise          def _assess_individual_skill(self, employee_id: int, skill_name: str, assessment_type: str) -> SkillProficiency:
        """Assess individual skill proficiency"""
        # Get skill information from framework
        skill_info = self._get_skill_info(skill_name)
        
        # Base proficiency calculation (in production would use multiple data sources)
        base_proficiency = random.uniform(40, 95)  # Simulated proficiency
        
        # Adjust based on assessment type
        type_modifiers = {
            "self": 0.9,          # Self-assessments tend to be slightly inflated
            "peer": 1.0,          # Peer assessments are generally accurate
            "manager": 1.1,       # Manager assessments might be more critical
            "technical": 1.2,     # Technical assessments are most rigorous
            "comprehensive": 1.0   # Balanced assessment
        }
        
        adjusted_proficiency = base_proficiency * type_modifiers.get(assessment_type, 1.0)
        adjusted_proficiency = min(100, max(0, adjusted_proficiency))
        
        # Determine competency level
        competency_level = self._determine_competency_level(adjusted_proficiency)
        
        # Calculate assessment confidence
        confidence = random.uniform(0.75, 0.95)
        
        # Get market demand and currency info
        market_demand = skill_info.get("market_demand", "medium")
        skill_currency = self._determine_skill_currency(skill_name)
        
        # Calculate evidence strength (simulated)
        evidence_strength = random.uniform(0.6, 0.9)
        
        # Generate recommended actions
        recommended_actions = self._generate_skill_recommendations(skill_name, adjusted_proficiency)
        
        return SkillProficiency(
            skill_name=skill_name,
            skill_category=self._get_skill_category(skill_name),
            proficiency_level=adjusted_proficiency,
            competency_level=competency_level,
            assessment_confidence=confidence,
            market_demand_level=market_demand,
            skill_currency=skill_currency,
            evidence_strength=evidence_strength,
            recommended_actions=recommended_actions
        )
    
    def _get_skill_info(self, skill_name: str) -> Dict[str, Any]:
        """Get skill information from framework"""
        skill_lower = skill_name.lower().replace(" ", "_")
        
        # Search in all categories
        for category, skills in self.skill_framework.items():
            if skill_lower in skills:
                return skills[skill_lower]
        
        # Default if skill not found
        return {"weight": 0.5, "market_demand": "medium", "learning_curve": "moderate"}
    
    def _get_skill_category(self, skill_name: str) -> str:
        """Determine skill category"""
        skill_lower = skill_name.lower().replace(" ", "_")
        
        for category, skills in self.skill_framework.items():
            if skill_lower in skills:
                return category
        
        return "other"  # Default category
    
    def _determine_competency_level(self, proficiency: float) -> str:
        """Determine competency level based on proficiency score"""
        for (min_score, max_score), level in self.competency_levels.items():
            if min_score <= proficiency < max_score:
                return level
        return "expert"  # 100 and above
    
    def _determine_skill_currency(self, skill_name: str) -> str:
        """Determine if skill is current, emerging, declining, or obsolete"""
        skill_lower = skill_name.lower()
        
        # Emerging skills
        emerging_skills = ["machine_learning", "kubernetes", "blockchain", "ai", "cloud", "devops"]
        if any(emerging in skill_lower for emerging in emerging_skills):
            return "emerging"
        
        # Declining skills
        declining_skills = ["flash", "jquery", "perl", "cobol"]
        if any(declining in skill_lower for declining in declining_skills):
            return "declining"
        
        # Current skills (most skills fall here)
        return "current"                   def _generate_skill_recommendations(self, skill_name: str, proficiency: float) -> List[str]:
        """Generate recommendations for skill improvement"""
        recommendations = []
        
        if proficiency < 50:
            recommendations.append("Focus on foundational concepts and basic practice")
            recommendations.append("Complete introductory courses or tutorials")
            recommendations.append("Find a mentor or study partner")
        elif proficiency < 75:
            recommendations.append("Work on intermediate-level projects")
            recommendations.append("Participate in hands-on workshops")
            recommendations.append("Contribute to open-source projects")
        else:
            recommendations.append("Take on advanced challenging projects")
            recommendations.append("Mentor others in this skill")
            recommendations.append("Contribute to community knowledge sharing")
        
        # Skill-specific recommendations
        skill_lower = skill_name.lower()
        if "python" in skill_lower:
            recommendations.append("Explore advanced Python libraries and frameworks")
        elif "leadership" in skill_lower:
            recommendations.append("Lead cross-functional projects and teams")
        elif "communication" in skill_lower:
            recommendations.append("Practice public speaking and presentation skills")
        
        return recommendations[:3]  # Limit to top 3
    
    def _identify_skill_strengths(self, proficiencies: List[SkillProficiency]) -> List[str]:
        """Identify top skill strengths"""
        # Sort by proficiency level
        sorted_skills = sorted(proficiencies, key=lambda x: x.proficiency_level, reverse=True)
        
        strengths = []
        for skill in sorted_skills[:5]:  # Top 5 skills
            if skill.proficiency_level >= 75:
                strengths.append(f"Excellent {skill.skill_name} proficiency ({skill.proficiency_level:.1f}/100)")
            elif skill.proficiency_level >= 60:
                strengths.append(f"Strong {skill.skill_name} competency ({skill.proficiency_level:.1f}/100)")
        
        # Add category-based strengths
        category_averages = {}
        for skill in proficiencies:
            if skill.skill_category not in category_averages:
                category_averages[skill.skill_category] = []
            category_averages[skill.skill_category].append(skill.proficiency_level)
        
        for category, scores in category_averages.items():
            avg_score = sum(scores) / len(scores)
            if avg_score >= 70:
                strengths.append(f"Well-rounded {category} skills (avg: {avg_score:.1f}/100)")
        
        return strengths[:6]  # Limit to 6 strengths
    
    def _identify_improvement_areas(self, proficiencies: List[SkillProficiency]) -> List[str]:
        """Identify areas needing improvement"""
        improvement_areas = []
        
        # Skills with low proficiency
        for skill in proficiencies:
            if skill.proficiency_level < 50:
                improvement_areas.append(f"{skill.skill_name} development needed (current: {skill.proficiency_level:.1f}/100)")
            elif skill.proficiency_level < 70 and skill.market_demand_level in ["high", "critical"]:
                improvement_areas.append(f"Enhance {skill.skill_name} for market demand (current: {skill.proficiency_level:.1f}/100)")
        
        # Category-based improvement areas
        category_averages = {}
        for skill in proficiencies:
            if skill.skill_category not in category_averages:
                category_averages[skill.skill_category] = []
            category_averages[skill.skill_category].append(skill.proficiency_level)
        
        for category, scores in category_averages.items():
            avg_score = sum(scores) / len(scores)
            if avg_score < 60:
                improvement_areas.append(f"Strengthen overall {category} competencies (avg: {avg_score:.1f}/100)")
        
        return improvement_areas[:5]  # Limit to 5 areas
    
    def _calculate_market_relevance(self, proficiencies: List[SkillProficiency]) -> float:
        """Calculate overall market relevance score"""
        if not proficiencies:
            return 0.0
        
        relevance_scores = []
        for skill in proficiencies:
            # Weight by market demand
            demand_weights = {"low": 0.3, "medium": 0.6, "high": 0.8, "critical": 1.0}
            demand_weight = demand_weights.get(skill.market_demand_level, 0.5)
            
            # Weight by skill currency
            currency_weights = {"obsolete": 0.1, "declining": 0.4, "current": 0.8, "emerging": 1.0}
            currency_weight = currency_weights.get(skill.skill_currency, 0.6)
            
            # Calculate weighted relevance
            skill_relevance = (skill.proficiency_level / 100) * demand_weight * currency_weight
            relevance_scores.append(skill_relevance)
        
        return (sum(relevance_scores) / len(relevance_scores)) * 100
    
    def _assess_future_skill_potential(self, employee_id: int, proficiencies: List[SkillProficiency]) -> float:
        """Assess potential for future skill development"""
        # Base potential calculation
        learning_indicators = []
        
        # Skill diversity indicates learning ability
        unique_categories = len(set(skill.skill_category for skill in proficiencies))
        diversity_score = min(unique_categories / 3, 1.0)  # Normalize to max 1.0
        learning_indicators.append(diversity_score)
        
        # High proficiency in emerging skills indicates adaptability
        emerging_skills_count = sum(1 for skill in proficiencies if skill.skill_currency == "emerging")
        adaptability_score = min(emerging_skills_count / 2, 1.0)  # Normalize
        learning_indicators.append(adaptability_score)
        
        # High confidence scores indicate strong learning foundation
        avg_confidence = sum(skill.assessment_confidence for skill in proficiencies) / len(proficiencies)
        learning_indicators.append(avg_confidence)
        
        # Overall proficiency trajectory
        avg_proficiency = sum(skill.proficiency_level for skill in proficiencies) / len(proficiencies)
        proficiency_indicator = min(avg_proficiency / 80, 1.0)  # Normalize to max 1.0
        learning_indicators.append(proficiency_indicator)
        
        # Calculate overall potential
        potential_score = (sum(learning_indicators) / len(learning_indicators)) * 100
        
        # Add some realistic variance
        potential_score += random.uniform(-5, 10)
        
        return max(0, min(100, potential_score))
        def _generate_learning_recommendations(self, proficiencies: List[SkillProficiency], improvement_areas: List[str]) -> List[str]:
        """Generate personalized learning path recommendations"""
        recommendations = []
        
        # Priority skills based on market demand and current proficiency
        priority_skills = []
        for skill in proficiencies:
            if skill.market_demand_level in ["high", "critical"] and skill.proficiency_level < 75:
                priority_skills.append(skill.skill_name)
        
        if priority_skills:
            recommendations.append(f"Focus on high-demand skills: {', '.join(priority_skills[:3])}")
        
        # Learning path based on skill categories
        category_gaps = {}
        for skill in proficiencies:
            if skill.proficiency_level < 70:
                if skill.skill_category not in category_gaps:
                    category_gaps[skill.skill_category] = []
                category_gaps[skill.skill_category].append(skill.skill_name)
        
        for category, skills in category_gaps.items():
            if len(skills) >= 2:
                recommendations.append(f"Comprehensive {category} skill development program")
        
        # Emerging skills opportunities
        emerging_opportunities = [skill.skill_name for skill in proficiencies 
                                if skill.skill_currency == "emerging" and skill.proficiency_level < 60]
        if emerging_opportunities:
            recommendations.append(f"Explore emerging technologies: {', '.join(emerging_opportunities[:2])}")
        
        # Cross-skill development
        if len(set(skill.skill_category for skill in proficiencies)) < 3:
            recommendations.append("Diversify skill portfolio across technical and soft skills")
        
        # Advanced development for strengths
        strengths = [skill.skill_name for skill in proficiencies if skill.proficiency_level >= 80]
        if strengths:
            recommendations.append(f"Advanced specialization in: {', '.join(strengths[:2])}")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _generate_certification_recommendations(self, proficiencies: List[SkillProficiency]) -> List[str]:
        """Generate certification recommendations based on skills"""
        cert_recommendations = []
        
        # Skill-based certification mapping
        cert_mapping = {
            "aws": ["AWS Solutions Architect", "AWS Developer Associate"],
            "python": ["Python Institute PCAP", "Microsoft Python Certification"],
            "project_management": ["PMP", "Scrum Master", "Agile Certification"],
            "cybersecurity": ["CISSP", "CompTIA Security+", "Certified Ethical Hacker"],
            "data_analysis": ["Google Data Analytics", "Microsoft Power BI", "Tableau Specialist"],
            "cloud_architecture": ["Google Cloud Architect", "Azure Solutions Architect"],
            "machine_learning": ["Google ML Engineer", "AWS ML Specialty"]
        }
        
        for skill in proficiencies:
            skill_lower = skill.skill_name.lower().replace(" ", "_")
            if skill_lower in cert_mapping and skill.proficiency_level >= 60:
                cert_recommendations.extend(cert_mapping[skill_lower])
        
        # Remove duplicates and limit
        return list(set(cert_recommendations))[:5]
    
    def _analyze_assessment_bias(self, request: SkillAssessmentRequest, proficiencies: List[SkillProficiency], overall_score: float) -> Dict[str, float]:
        """Analyze potential bias in skill assessment"""
        bias_factors = {}
        
        # Assessment consistency check
        proficiency_scores = [p.proficiency_level for p in proficiencies]
        score_variance = np.var(proficiency_scores) if proficiency_scores else 0
        consistency_bias = min(score_variance / 1000, 0.3)  # Normalize to max 0.3
        bias_factors["assessment_consistency"] = consistency_bias
        
        # Category balance check
        category_scores = {}
        for prof in proficiencies:
            if prof.skill_category not in category_scores:
                category_scores[prof.skill_category] = []
            category_scores[prof.skill_category].append(prof.proficiency_level)
        
        balance_bias = 0.0
        if len(category_scores) > 1:
            category_averages = [sum(scores)/len(scores) for scores in category_scores.values()]
            category_range = max(category_averages) - min(category_averages)
            if category_range > 40:  # Large range might indicate bias
                balance_bias = 0.2
        bias_factors["skill_category_balance"] = balance_bias
        
        # Evidence objectivity (simplified check)
        evidence_bias = 0.0
        high_confidence_count = sum(1 for p in proficiencies if p.assessment_confidence > 0.9)
        if high_confidence_count == len(proficiencies):
            evidence_bias = 0.1  # Overly confident might indicate bias
        bias_factors["evidence_objectivity"] = evidence_bias
        
        # Competency progression check
        progression_bias = 0.0
        expert_count = sum(1 for p in proficiencies if p.competency_level == "expert")
        if expert_count > len(proficiencies) * 0.8:  # Too many experts might be inflated
            progression_bias = 0.15
        bias_factors["competency_progression"] = progression_bias
        
        # Market alignment check
        market_bias = 0.0
        high_demand_skills = [p for p in proficiencies if p.market_demand_level in ["high", "critical"]]
        if high_demand_skills:
            avg_high_demand_score = sum(p.proficiency_level for p in high_demand_skills) / len(high_demand_skills)
            if avg_high_demand_score < overall_score - 20:  # Misalignment with market needs
                market_bias = 0.1
        bias_factors["market_alignment"] = market_bias
        
        # Calculate overall bias score
        overall_bias = sum(
            bias_factors[factor] * self.bias_detection_weights[factor]
            for factor in bias_factors
        )
        bias_factors["overall_bias"] = overall_bias
        
        return bias_factors
    
    def _calculate_assessment_confidence(self, request: SkillAssessmentRequest, proficiencies: List[SkillProficiency]) -> float:
        """Calculate statistical confidence in assessment"""
        confidence_factors = []
        
        # Assessment type confidence
        type_confidence = {
            "self": 0.7,
            "peer": 0.8,
            "manager": 0.85,
            "technical": 0.95,
            "comprehensive": 0.9
        }
        confidence_factors.append(type_confidence.get(request.assessment_type, 0.8))
        
        # Skill count confidence (more skills = better picture)
        skill_count_confidence = min(len(request.skills_to_assess) / 10, 1.0)
        confidence_factors.append(skill_count_confidence)
        
        # Individual skill confidence average
        if proficiencies:
            avg_skill_confidence = sum(p.assessment_confidence for p in proficiencies) / len(proficiencies)
            confidence_factors.append(avg_skill_confidence)
        
        # Assessment depth confidence
        depth_confidence = {
            "quick": 0.7,
            "standard": 0.85,
            "comprehensive": 0.95,
            "deep_dive": 0.98
        }
        confidence_factors.append(depth_confidence.get(request.assessment_depth, 0.85))
        
        return sum(confidence_factors) / len(confidence_factors)
    
    def _generate_assessment_summary(self, overall_proficiency: float, strengths: List[str], improvement_areas: List[str]) -> str:
        """Generate executive summary of assessment"""
        # Determine overall performance level
        if overall_proficiency >= 85:
            performance_level = "exceptional"
        elif overall_proficiency >= 75:
            performance_level = "strong"
        elif overall_proficiency >= 65:
            performance_level = "solid"
        elif overall_proficiency >= 50:
            performance_level = "developing"
        else:
            performance_level = "emerging"
        
        summary = f"Employee demonstrates {performance_level} skill proficiency with an overall score of {overall_proficiency:.1f}/100. "
        
        if strengths:
            summary += f"Key strengths include {len(strengths)} areas of excellence. "
        
        if improvement_areas:
            summary += f"Development opportunities identified in {len(improvement_areas)} skill areas. "
        
        summary += "Detailed recommendations provided for continued professional growth."
        
        return summary
        def _calculate_next_assessment_date(self, assessment_type: str, proficiency_score: float) -> datetime:
        """Calculate when next assessment should occur"""
        base_months = {
            "self": 3,
            "peer": 6,
            "manager": 6,
            "technical": 12,
            "comprehensive": 12
        }
        
        months = base_months.get(assessment_type, 6)
        
        # Adjust based on proficiency (lower scores need more frequent assessment)
        if proficiency_score < 50:
            months = max(months // 2, 3)  # More frequent for development
        elif proficiency_score > 85:
            months = min(months * 2, 18)  # Less frequent for high performers
        
        return datetime.utcnow() + timedelta(days=months * 30)
    
    def _estimate_assessment_duration(self, request: SkillAssessmentRequest) -> int:
        """Estimate assessment duration in minutes"""
        base_minutes_per_skill = {
            "quick": 5,
            "standard": 15,
            "comprehensive": 30,
            "deep_dive": 60
        }
        
        minutes_per_skill = base_minutes_per_skill.get(request.assessment_depth, 15)
        total_minutes = len(request.skills_to_assess) * minutes_per_skill
        
        # Add setup and review time
        total_minutes += 20
        
        return total_minutes
    
    def _get_assessment_criteria(self, skill_name: str) -> Dict[str, Any]:
        """Get assessment criteria for a specific skill"""
        # Simplified criteria (in production would be much more detailed)
        return {
            "theoretical_knowledge": "Understanding of core concepts and principles",
            "practical_application": "Ability to apply skill in real-world scenarios", 
            "problem_solving": "Using skill to solve complex problems",
            "best_practices": "Knowledge of industry standards and best practices",
            "continuous_learning": "Staying updated with skill evolution"
        }
    
    def _calculate_industry_relevance(self, skill_name: str) -> float:
        """Calculate industry relevance score for skill"""
        # Simplified relevance calculation
        skill_info = self._get_skill_info(skill_name)
        
        demand_scores = {"low": 0.3, "medium": 0.6, "high": 0.8, "critical": 1.0}
        demand_score = demand_scores.get(skill_info.get("market_demand", "medium"), 0.6)
        
        # Add some industry-specific variance
        relevance = demand_score + random.uniform(-0.1, 0.1)
        
        return max(0.0, min(1.0, relevance))
    
    def _calculate_profile_completeness(self, assessment: SkillAssessment) -> float:
        """Calculate how complete the skill profile is"""
        base_completeness = min(len(assessment.skill_breakdown) * 10, 80)
        
        if assessment.strengths_identified:
            base_completeness += 10
        if assessment.improvement_areas:
            base_completeness += 10
        
        return min(100, base_completeness)
    
    def _calculate_category_proficiencies(self, assessment: SkillAssessment) -> Dict[str, float]:
        """Calculate average proficiency by skill category"""
        categories = {}
        
        for skill, score in assessment.skill_breakdown.items():
            category = self._get_skill_category(skill)
            if category not in categories:
                categories[category] = []
            categories[category].append(score)
        
        return {category: sum(scores)/len(scores) for category, scores in categories.items()}
    
    def _identify_top_skills(self, assessment: SkillAssessment) -> List[str]:
        """Identify top skills from assessment"""
        sorted_skills = sorted(assessment.skill_breakdown.items(), key=lambda x: x[1], reverse=True)
        return [skill for skill, score in sorted_skills[:5] if score >= 70]
    
    def _determine_career_trajectory(self, assessments: List[SkillAssessment]) -> str:
        """Determine career trajectory based on assessment history"""
        if len(assessments) < 2:
            return "developing"
        
        scores = [a.overall_proficiency_score for a in assessments[-3:]]  # Last 3 assessments
        
        if len(scores) >= 2:
            recent_trend = scores[-1] - scores[0]
            if recent_trend > 10:
                return "ascending"
            elif recent_trend < -5:
                return "declining"
        
        return "stable"
    
    def _calculate_learning_velocity(self, assessments: List[SkillAssessment]) -> float:
        """Calculate rate of skill development"""
        if len(assessments) < 2:
            return 5.0  # Default moderate velocity
        
        score_improvements = []
        for i in range(1, len(assessments)):
            improvement = assessments[i].overall_proficiency_score - assessments[i-1].overall_proficiency_score
            days_between = (assessments[i].assessment_date - assessments[i-1].assessment_date).days
            if days_between > 0:
                velocity = improvement / (days_between / 30)  # Points per month
                score_improvements.append(velocity)
        
        if score_improvements:
            avg_velocity = sum(score_improvements) / len(score_improvements)
            return max(0, min(10, avg_velocity + 5))  # Normalize to 0-10 scale
        
        return 5.0
    
    def _calculate_skill_diversity(self, assessment: SkillAssessment) -> float:
        """Calculate skill diversity score"""
        categories = set(self._get_skill_category(skill) for skill in assessment.skill_breakdown.keys())
        diversity_score = min(len(categories) * 25, 100)  # Max 4 categories for 100%
        return diversity_score
        def track_certification(self, request: CertificationTrackingRequest) -> Dict[str, Any]:
        """
        Track employee certifications with more precision than a transcript office!
        We catalog achievements like a hall of fame curator! 🏆📜
        """
        try:
            logger.info(f"🏆 Tracking certification '{request.certification_name}' for employee {request.employee_id}")
            
            # Calculate market value and impact
            market_value = self._calculate_certification_market_value(request.certification_name, request.certification_type)
            salary_impact = self._estimate_salary_impact(request.certification_name)
            career_value = self._assess_career_advancement_value(request.certification_name, request.certification_type)
            skill_enhancement = self._calculate_skill_enhancement_score(request.skills_covered)
            industry_recognition = self._assess_industry_recognition(request.certification_provider)
            
            # Determine renewal requirements
            renewal_info = self._determine_renewal_requirements(request.certification_name, request.certification_type)
            
            # Generate next certification recommendations
            next_cert_recommendations = self._recommend_next_certifications(request.skills_covered, request.certification_level)
            
            # Create certification tracking record
            certification = CertificationTracking(
                employee_id=request.employee_id,
                certification_name=request.certification_name,
                certification_provider=request.certification_provider,
                certification_type=request.certification_type,
                certification_level=request.certification_level,
                certification_id=request.certification_id,
                issue_date=request.issue_date,
                expiration_date=request.expiration_date,
                verification_url=request.verification_url,
                skills_covered=request.skills_covered,
                study_hours_required=request.study_hours_invested,
                market_value_score=market_value,
                industry_recognition=industry_recognition,
                salary_impact_percentage=salary_impact,
                career_advancement_value=career_value,
                digital_badge_url=request.digital_badge_url,
                renewal_required=renewal_info["required"],
                renewal_period_months=renewal_info["period_months"],
                next_renewal_date=renewal_info["next_date"]
            )
            
            self.db.add(certification)
            self.db.commit()
            self.db.refresh(certification)
            
            return {
                "certification_id": certification.id,
                "market_value_score": market_value,
                "salary_impact_estimate": salary_impact,
                "career_advancement_value": career_value,
                "skill_enhancement_score": skill_enhancement,
                "industry_recognition": industry_recognition,
                "renewal_timeline": f"Every {renewal_info['period_months']} months" if renewal_info["required"] else "No renewal required",
                "recommended_next_certifications": next_cert_recommendations,
                "achievement_humor": random.choice(self.assessment_jokes)
            }
            
        except Exception as e:
            logger.error(f"💥 Error tracking certification: {e}")
            self.db.rollback()
            raise
    
    def _calculate_certification_market_value(self, cert_name: str, cert_type: str) -> float:
        """Calculate market value of certification"""
        # Base value by type
        type_values = {
            "technical": 80,
            "professional": 75,
            "academic": 70,
            "vendor": 85,
            "industry": 78
        }
        
        base_value = type_values.get(cert_type, 70)
        
        # Popular certifications get higher value
        high_value_certs = ["aws", "google", "microsoft", "pmp", "cissp", "cfa", "cpa"]
        cert_lower = cert_name.lower()
        
        if any(high_val in cert_lower for high_val in high_value_certs):
            base_value += 15
        
        # Add some realistic variance
        market_value = base_value + random.uniform(-10, 10)
        
        return max(0, min(100, market_value))
    
    def _estimate_salary_impact(self, cert_name: str) -> float:
        """Estimate salary impact percentage"""
        cert_lower = cert_name.lower()
        
        # High-impact certifications
        if any(cert in cert_lower for cert in ["aws", "google cloud", "azure"]):
            return random.uniform(8, 15)  # 8-15% salary increase
        elif any(cert in cert_lower for cert in ["pmp", "cissp", "cfa"]):
            return random.uniform(10, 20)  # 10-20% salary increase
        elif any(cert in cert_lower for cert in ["microsoft", "oracle", "salesforce"]):
            return random.uniform(5, 12)   # 5-12% salary increase
        else:
            return random.uniform(3, 8)    # 3-8% salary increase
    
    def _assess_career_advancement_value(self, cert_name: str, cert_type: str) -> float:
        """Assess career advancement value"""
        base_value = 70
        
        if cert_type in ["professional", "industry"]:
            base_value += 15
        
        cert_lower = cert_name.lower()
        if any(term in cert_lower for term in ["management", "leadership", "architect", "expert"]):
            base_value += 10
        
        return max(0, min(100, base_value + random.uniform(-5, 10)))
    
    def _calculate_skill_enhancement_score(self, skills_covered: List[str]) -> float:
        """Calculate how much certification enhances skills"""
        if not skills_covered:
            return 50
        
        # More skills covered = higher enhancement
        base_score = min(len(skills_covered) * 15, 80)
        
        # High-demand skills boost the score
        high_demand_skills = ["python", "aws", "kubernetes", "leadership", "project_management"]
        demand_boost = sum(10 for skill in skills_covered 
                          if any(hd_skill in skill.lower() for hd_skill in high_demand_skills))
        
        total_score = base_score + min(demand_boost, 20)
        
        return max(0, min(100, total_score))
    
    def _assess_industry_recognition(self, provider: str) -> str:
        """Assess industry recognition level of certification provider"""
        provider_lower = provider.lower()
        
        high_recognition = ["amazon", "google", "microsoft", "oracle", "salesforce", "cisco", "pmi", "isaca"]
        if any(provider_name in provider_lower for provider_name in high_recognition):
            return "high"
        
        medium_recognition = ["comptia", "red hat", "vmware", "adobe", "atlassian"]
        if any(provider_name in provider_lower for provider_name in medium_recognition):
            return "medium"
        
        return "low"
    
    def _determine_renewal_requirements(self, cert_name: str, cert_type: str) -> Dict[str, Any]:
        """Determine certification renewal requirements"""
        cert_lower = cert_name.lower()
        
        # Certifications that typically require renewal
        renewal_required_certs = ["pmp", "cissp", "aws", "google", "microsoft"]
        requires_renewal = any(cert in cert_lower for cert in renewal_required_certs)
        
        if requires_renewal:
            # Typical renewal periods
            if any(cert in cert_lower for cert in ["aws", "google", "microsoft"]):
                period_months = 36  # 3 years
            elif "pmp" in cert_lower:
                period_months = 36  # 3 years
            elif "cissp" in cert_lower:
                period_months = 36  # 3 years
            else:
                period_months = 24  # 2 years default
            
            next_date = datetime.utcnow() + timedelta(days=period_months * 30)
        else:
            period_months = None
            next_date = None
        
        return {
            "required": requires_renewal,
            "period_months": period_months,
            "next_date": next_date
        }
    
    def _recommend_next_certifications(self, current_skills: List[str], current_level: Optional[str]) -> List[str]:
        """Recommend next certifications based on current skills"""
        recommendations = []
        
        # Progression recommendations based on current level
        if current_level == "foundation":
            recommendations.append("Consider Associate-level certification in same domain")
        elif current_level == "associate":
            recommendations.append("Progress to Professional-level certification")
        elif current_level == "professional":
            recommendations.append("Explore Expert or Specialty certifications")
        
        # Skill-based recommendations
        for skill in current_skills:
            skill_lower = skill.lower()
            if "aws" in skill_lower:
                recommendations.extend(["AWS Solutions Architect Professional", "AWS DevOps Engineer"])
            elif "project" in skill_lower:
                recommendations.extend(["Agile Certification", "Scrum Master"])
            elif "security" in skill_lower:
                recommendations.extend(["CISSP", "Certified Ethical Hacker"])
        
        return list(set(recommendations))[:5]  # Remove duplicates, limit to 5
        def analyze_skill_gaps(self, request: SkillGapAnalysisRequest) -> Dict[str, Any]:
        """
        Analyze skill gaps with more precision than a GPS finding the shortest route!
        We map the path to professional excellence! 🗺️🎯
        """
        try:
            logger.info(f"🔍 Analyzing skill gaps for employee {request.employee_id}")
            
            # Get current skill profile
            current_profile = self._get_current_skill_profile(request.employee_id)
            
            # Get target skill requirements
            target_profile = self._get_target_skill_requirements(request.target_role, request.target_department)
            
            # Identify skill gaps
            identified_gaps = self._identify_skill_gaps(current_profile, target_profile)
            
            # Categorize gaps by priority and severity
            critical_gaps, quick_wins, long_term_gaps = self._categorize_skill_gaps(identified_gaps)
            
            # Generate learning path
            learning_path = self._generate_comprehensive_learning_path(identified_gaps, request.career_timeline)
            
            # Estimate timeline and budget
            timeline_estimate = self._estimate_gap_closure_timeline(identified_gaps, request.career_timeline)
            budget_estimate = self._estimate_development_budget(identified_gaps)
            
            # Calculate ROI projection
            roi_projection = self._calculate_skill_development_roi(identified_gaps, request.target_role)
            
            # Assess market urgency
            market_urgency = self._assess_market_urgency(identified_gaps)
            
            # Calculate success probability
            success_probability = self._calculate_development_success_probability(request.employee_id, identified_gaps)
            
            # Create gap analysis record
            gap_analysis = SkillGapAnalysis(
                employee_id=request.employee_id,
                target_role=request.target_role,
                target_department=request.target_department,
                analysis_scope=request.analysis_scope,
                current_skill_profile=current_profile,
                target_skill_profile=target_profile,
                identified_gaps=[gap.dict() for gap in identified_gaps],
                proficiency_gaps={gap.skill_name: gap.required_level - gap.current_level for gap in identified_gaps},
                critical_gaps=critical_gaps,
                quick_wins=quick_wins,
                long_term_development=long_term_gaps,
                recommended_learning_path=learning_path,
                estimated_closure_timeline=timeline_estimate,
                budget_estimate=budget_estimate,
                priority_ranking=[gap.skill_name for gap in sorted(identified_gaps, key=lambda x: x.development_priority)],
                roi_analysis=roi_projection,
                market_urgency=market_urgency,
                success_metrics=self._generate_success_metrics(identified_gaps),
                analysis_confidence=random.uniform(0.85, 0.95)
            )
            
            self.db.add(gap_analysis)
            self.db.commit()
            self.db.refresh(gap_analysis)
            
            return {
                "analysis_id": gap_analysis.id,
                "identified_gaps": identified_gaps,
                "critical_gaps": critical_gaps,
                "quick_wins": quick_wins,
                "long_term_development": long_term_gaps,
                "recommended_learning_path": learning_path,
                "estimated_timeline": timeline_estimate,
                "budget_estimate": budget_estimate,
                "roi_projection": roi_projection,
                "market_urgency": market_urgency,
                "success_probability": success_probability,
                "analysis_confidence": gap_analysis.analysis_confidence,
                "next_review_date": datetime.utcnow() + timedelta(days=90),
                "motivational_message": random.choice(self.assessment_jokes)
            }
            
        except Exception as e:
            logger.error(f"💥 Error analyzing skill gaps: {e}")
            self.db.rollback()
            raise
    
    def _get_current_skill_profile(self, employee_id: int) -> Dict[str, float]:
        """Get employee's current skill profile"""
        # Get latest assessment
        latest_assessment = self.db.query(SkillAssessment).filter(
            SkillAssessment.employee_id == employee_id
        ).order_by(desc(SkillAssessment.assessment_date)).first()
        
        if latest_assessment:
            return latest_assessment.skill_breakdown
        
        # If no assessment, return basic profile
        return {
            "communication": random.uniform(60, 80),
            "teamwork": random.uniform(65, 85),
            "problem_solving": random.uniform(55, 75),
            "technical_skills": random.uniform(50, 70)
        }
    
    def _get_target_skill_requirements(self, target_role: Optional[str], target_department: Optional[str]) -> Dict[str, float]:
        """Get target skill requirements for role/department"""
        # Simplified target requirements (in production would be from job descriptions/role definitions)
        role_requirements = {
            "senior_developer": {
                "python": 85, "javascript": 80, "sql": 75, "aws": 70,
                "leadership": 70, "communication": 80, "problem_solving": 85
            },
            "team_lead": {
                "leadership": 90, "communication": 85, "project_management": 80,
                "technical_skills": 75, "mentoring": 85, "strategic_thinking": 80
            },
            "data_scientist": {
                "python": 90, "machine_learning": 85, "sql": 80, "statistics": 85,
                "data_visualization": 75, "communication": 80
            },
            "product_manager": {
                "product_strategy": 85, "communication": 90, "leadership": 80,
                "data_analysis": 75, "market_research": 80, "project_management": 85
            }
        }
        
        if target_role and target_role.lower().replace(" ", "_") in role_requirements:
            return role_requirements[target_role.lower().replace(" ", "_")]
        
        # Default requirements
        return {
            "communication": 75,
            "teamwork": 75,
            "problem_solving": 80,
            "leadership": 70,
            "technical_skills": 75
        }
    
    def _identify_skill_gaps(self, current_profile: Dict[str, float], target_profile: Dict[str, float]) -> List[SkillGap]:
        """Identify skill gaps between current and target profiles"""
        gaps = []
        
        for skill, target_level in target_profile.items():
            current_level = current_profile.get(skill, 0)
            gap_size = target_level - current_level
            
            if gap_size > 5:  # Only significant gaps
                # Determine gap severity
                if gap_size >= 30:
                    severity = "critical"
                    priority = 1
                elif gap_size >= 20:
                    severity = "high"
                    priority = 2
                elif gap_size >= 10:
                    severity = "medium"
                    priority = 3
                else:
                    severity = "low"
                    priority = 4
                
                # Estimate development time
                if gap_size >= 25:
                    dev_time = "6-12 months"
                elif gap_size >= 15:
                    dev_time = "3-6 months"
                else:
                    dev_time = "1-3 months"
                
                # Generate recommended approach
                approach = self._generate_development_approach(skill, gap_size)
                
                gap = SkillGap(
                    skill_name=skill,
                    current_level=current_level,
                    required_level=target_level,
                    gap_severity=severity,
                    development_priority=priority,
                    estimated_development_time=dev_time,
                    recommended_approach=approach,
                    resource_requirements=self._identify_resource_requirements(skill),
                    success_metrics=self._generate_skill_success_metrics(skill)
                )
                
                gaps.append(gap)
        
        return sorted(gaps, key=lambda x: x.development_priority)
    
    def _generate_development_approach(self, skill: str, gap_size: float) -> List[str]:
        """Generate development approach for specific skill"""
        approaches = []
        
        skill_lower = skill.lower()
        
        # Basic approaches based on gap size
        if gap_size >= 25:
            approaches.append("Comprehensive formal training program")
            approaches.append("Mentorship with senior expert")
            approaches.append("Hands-on project assignments")
        elif gap_size >= 15:
            approaches.append("Structured online courses")
            approaches.append("Practical workshops and seminars")
            approaches.append("Peer learning and study groups")
        else:
            approaches.append("Self-directed learning resources")
            approaches.append("Short-term skill-building exercises")
            approaches.append("On-the-job practice opportunities")
        
        # Skill-specific approaches
        if "leadership" in skill_lower:
            approaches.append("Leadership development program")
            approaches.append("Cross-functional team leadership")
        elif "technical" in skill_lower or any(tech in skill_lower for tech in ["python", "aws", "sql"]):
            approaches.append("Technical certification pathway")
            approaches.append("Open-source project contributions")
        elif "communication" in skill_lower:
            approaches.append("Public speaking practice")
            approaches.append("Written communication workshops")
        
        return approaches[:4]  # Limit to 4 approaches
    
    def _categorize_skill_gaps(self, gaps: List[SkillGap]) -> tuple:
        """Categorize gaps into critical, quick wins, and long-term"""
        critical_gaps = [gap.skill_name for gap in gaps if gap.gap_severity == "critical"]
        
        quick_wins = [gap.skill_name for gap in gaps 
                     if gap.gap_severity in ["low", "medium"] and "1-3 months" in gap.estimated_development_time]
        
        long_term_gaps = [gap.skill_name for gap in gaps 
                         if "6-12 months" in gap.estimated_development_time]
        
        return critical_gaps, quick_wins, long_term_gaps
        def _generate_comprehensive_learning_path(self, gaps: List[SkillGap], career_timeline: str) -> Dict[str, Any]:
        """Generate comprehensive learning path for gap closure"""
        timeline_months = {"6_months": 6, "1_year": 12, "2_years": 24, "5_years": 60}
        available_months = timeline_months.get(career_timeline, 12)
        
        # Prioritize gaps
        critical_gaps = [gap for gap in gaps if gap.gap_severity == "critical"]
        high_gaps = [gap for gap in gaps if gap.gap_severity == "high"]
        other_gaps = [gap for gap in gaps if gap.gap_severity in ["medium", "low"]]
        
        learning_path = {
            "phase_1_critical": {
                "duration_months": min(available_months // 3, 6),
                "focus_skills": [gap.skill_name for gap in critical_gaps[:3]],
                "learning_methods": ["Intensive training", "Mentorship", "Practical projects"],
                "success_criteria": "Achieve 70%+ proficiency in critical skills"
            },
            "phase_2_high_priority": {
                "duration_months": min(available_months // 3, 4),
                "focus_skills": [gap.skill_name for gap in high_gaps[:3]],
                "learning_methods": ["Structured courses", "Workshops", "Peer learning"],
                "success_criteria": "Reach target proficiency in high-priority skills"
            },
            "phase_3_comprehensive": {
                "duration_months": available_months - min(available_months // 3 * 2, 10),
                "focus_skills": [gap.skill_name for gap in other_gaps[:4]],
                "learning_methods": ["Self-directed learning", "On-job practice", "Continuous improvement"],
                "success_criteria": "Maintain and enhance all developed skills"
            }
        }
        
        return learning_path
    
    def _estimate_gap_closure_timeline(self, gaps: List[SkillGap], career_timeline: str) -> str:
        """Estimate timeline for closing all skill gaps"""
        total_gap_months = sum(self._estimate_skill_development_months(gap.skill_name, gap.required_level - gap.current_level) for gap in gaps)
        
        timeline_mapping = {"6_months": 6, "1_year": 12, "2_years": 24, "5_years": 60}
        available_months = timeline_mapping.get(career_timeline, 12)
        
        if total_gap_months <= available_months:
            return f"All gaps closable within {career_timeline.replace('_', ' ')}"
        else:
            return f"Estimated {total_gap_months} months for complete gap closure"
    
    def _estimate_skill_development_months(self, skill_name: str, gap_size: float) -> int:
        """Estimate months needed to develop a skill"""
        skill_info = self._get_skill_info(skill_name)
        learning_curve = skill_info.get("learning_curve", "moderate")
        
        base_months = gap_size / 10  # 10 points per month baseline
        
        curve_multipliers = {"easy": 0.7, "moderate": 1.0, "steep": 1.5}
        multiplier = curve_multipliers.get(learning_curve, 1.0)
        
        return max(1, int(base_months * multiplier))
    
    def _estimate_development_budget(self, gaps: List[SkillGap]) -> float:
        """Estimate budget for skill development"""
        total_budget = 0
        
        for gap in gaps:
            # Base cost per skill gap
            if gap.gap_severity == "critical":
                skill_cost = random.uniform(2000, 5000)
            elif gap.gap_severity == "high":
                skill_cost = random.uniform(1000, 3000)
            else:
                skill_cost = random.uniform(500, 1500)
            
            total_budget += skill_cost
        
        return round(total_budget, 2)
    
    def _calculate_skill_development_roi(self, gaps: List[SkillGap], target_role: Optional[str]) -> Dict[str, float]:
        """Calculate ROI for skill development"""
        # Simplified ROI calculation
        development_cost = self._estimate_development_budget(gaps)
        
        # Estimate salary impact
        role_salary_impact = {
            "senior_developer": 15,
            "team_lead": 25,
            "data_scientist": 20,
            "product_manager": 18
        }
        
        salary_increase_percent = role_salary_impact.get(target_role, 12) if target_role else 12
        
        # Assume average salary for calculation
        average_salary = 75000
        annual_increase = average_salary * (salary_increase_percent / 100)
        
        # Simple ROI calculation
        roi_years = development_cost / annual_increase if annual_increase > 0 else 5
        
        return {
            "estimated_salary_increase_percent": salary_increase_percent,
            "estimated_annual_increase": annual_increase,
            "payback_period_years": round(roi_years, 1),
            "five_year_roi": round(((annual_increase * 5) - development_cost) / development_cost * 100, 1)
        }
    
    def _assess_market_urgency(self, gaps: List[SkillGap]) -> Dict[str, str]:
        """Assess market urgency for skill development"""
        urgency_mapping = {}
        
        for gap in gaps:
            skill_info = self._get_skill_info(gap.skill_name)
            demand = skill_info.get("market_demand", "medium")
            
            if demand == "critical":
                urgency = "immediate"
            elif demand == "high":
                urgency = "high"
            elif demand == "medium":
                urgency = "moderate"
            else:
                urgency = "low"
            
            urgency_mapping[gap.skill_name] = urgency
        
        return urgency_mapping
    
    def _calculate_development_success_probability(self, employee_id: int, gaps: List[SkillGap]) -> float:
        """Calculate probability of successful skill development"""
        success_factors = []
        
        # Number of gaps (fewer gaps = higher success probability)
        gap_factor = max(0.3, 1.0 - (len(gaps) * 0.1))
        success_factors.append(gap_factor)
        
        # Gap severity (less severe = higher success)
        severity_scores = {"low": 0.9, "medium": 0.8, "high": 0.6, "critical": 0.4}
        avg_severity_score = sum(severity_scores.get(gap.gap_severity, 0.7) for gap in gaps) / len(gaps)
        success_factors.append(avg_severity_score)
        
        # Historical learning performance (simulated)
        historical_performance = random.uniform(0.7, 0.9)
        success_factors.append(historical_performance)
        
        # Overall success probability
        success_probability = sum(success_factors) / len(success_factors)
        
        return round(success_probability, 3)
    
    def _generate_success_metrics(self, gaps: List[SkillGap]) -> List[str]:
        """Generate success metrics for gap closure"""
        metrics = []
        
        for gap in gaps:
            metrics.append(f"Achieve {gap.required_level}% proficiency in {gap.skill_name}")
            
        # Overall metrics
        metrics.extend([
            "Complete all recommended learning activities",
            "Demonstrate skills through practical projects",
            "Receive peer validation of skill improvements",
            "Apply skills successfully in work environment"
        ])
        
        return metrics[:8]  # Limit to 8 metrics
    
    def _identify_resource_requirements(self, skill: str) -> List[str]:
        """Identify resource requirements for skill development"""
        resources = ["Time allocation for learning", "Manager support and guidance"]
        
        skill_lower = skill.lower()
        
        if any(tech in skill_lower for tech in ["python", "aws", "javascript"]):
            resources.extend(["Development environment access", "Practice projects", "Technical mentorship"])
        elif "leadership" in skill_lower:
            resources.extend(["Leadership opportunities", "Executive coaching", "Cross-functional projects"])
        elif "communication" in skill_lower:
            resources.extend(["Presentation opportunities", "Communication training", "Public speaking practice"])
        
        return resources[:5]  # Limit to 5 resources
    
    def _generate_skill_success_metrics(self, skill: str) -> List[str]:
        """Generate success metrics for individual skill"""
        base_metrics = [
            f"Demonstrate competency in {skill} through practical application",
            f"Complete formal assessment with 70%+ score in {skill}",
            f"Receive positive peer feedback on {skill} performance"
        ]
        
        skill_lower = skill.lower()
        if "leadership" in skill_lower:
            base_metrics.append("Successfully lead a team project")
        elif any(tech in skill_lower for tech in ["python", "javascript", "aws"]):
            base_metrics.append("Complete technical project showcasing skill")
        
        return base_metrics[:4]  # Limit to 4 metrics
    
    def get_comprehensive_skill_profile(self, employee_id: int, include_recommendations: bool, include_market_analysis: bool) -> Optional[Dict]:
        """Get comprehensive skill profile for employee"""
        try:
            # Get latest assessment
            latest_assessment = self.db.query(SkillAssessment).filter(
                SkillAssessment.employee_id == employee_id
            ).order_by(desc(SkillAssessment.assessment_date)).first()
            
            if not latest_assessment:
                return None
            
            # Get all assessments for trend analysis
            all_assessments = self.db.query(SkillAssessment).filter(
                SkillAssessment.employee_id == employee_id
            ).order_by(SkillAssessment.assessment_date).all()
            
            # Get certifications
            certifications = self.db.query(CertificationTracking).filter(
                CertificationTracking.employee_id == employee_id
            ).all()
            
            # Calculate profile metrics
            profile = {
                "employee_id": employee_id,
                "profile_completeness": self._calculate_profile_completeness(latest_assessment),
                "total_skills_assessed": len(latest_assessment.skill_breakdown),
                "average_proficiency": latest_assessment.overall_proficiency_score,
                "skill_categories": self._calculate_category_proficiencies(latest_assessment),
                "top_skills": self._identify_top_skills(latest_assessment),
                "emerging_skills": latest_assessment.recommended_learning_paths,
                "certifications_earned": len([c for c in certifications if hasattr(c, 'certification_status') and c.certification_status == "active"]),
                "certifications_pending": len([c for c in certifications if hasattr(c, 'certification_status') and c.certification_status == "pending"]),
                "market_competitiveness": latest_assessment.market_relevance_score or 75,
                "career_trajectory": self._determine_career_trajectory(all_assessments),
                "learning_velocity": self._calculate_learning_velocity(all_assessments),
                "skill_diversity_score": self._calculate_skill_diversity(latest_assessment),
                "specialization_depth": self._calculate_specialization_depth(latest_assessment),
                "future_readiness": latest_assessment.future_skill_potential or 70,
                "development_recommendations": latest_assessment.recommended_learning_paths or [],
                "last_assessment_date": latest_assessment.assessment_date,
                "next_assessment_due": latest_assessment.next_assessment_date
            }
            
            return profile
            
        except Exception as e:
            logger.error(f"💥 Error retrieving skill profile: {e}")
            raise
    
    def _calculate_specialization_depth(self, assessment: SkillAssessment) -> float:
        """Calculate specialization depth score"""
        if not assessment.skill_breakdown:
            return 0
        
        scores = list(assessment.skill_breakdown.values())
        max_score = max(scores)
        
        # Specialization is having some skills significantly higher than others
        high_skills = [s for s in scores if s >= 80]
        specialization_score = (len(high_skills) / len(scores)) * max_score
        
        return min(100, specialization_score)
