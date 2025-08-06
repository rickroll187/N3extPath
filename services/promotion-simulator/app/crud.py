"""
CRUD Operations for Promotion Simulator Service
Where promotion algorithms meet database reality - and magic happens! ✨
"""
import logging
import random
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from app.models import PromotionSimulation, PromotionCriteria, EmployeeProfile, PromotionBenchmark
from app.schemas import (
    PromotionSimulationRequest, PromotionSimulationResponse, 
    PromotionFactor, DevelopmentAction
)

logger = logging.getLogger(__name__)

class PromotionSimulatorCRUD:
    """CRUD operations for promotion simulation - the crystal ball of HR! 🔮"""
    
    def __init__(self, db: Session):
        self.db = db
        
        # Mock promotion criteria for different positions
        self.promotion_criteria = {
            "senior_software_engineer": {
                "minimum_performance_score": 75.0,
                "minimum_years_experience": 3.0,
                "required_skills": ["programming", "system_design", "code_review"],
                "success_factors": ["technical_excellence", "mentoring", "project_leadership"],
                "average_promotion_time": 3.5
            },
            "tech_lead": {
                "minimum_performance_score": 80.0,
                "minimum_years_experience": 4.0,
                "required_skills": ["architecture", "leadership", "team_management"],
                "success_factors": ["technical_vision", "team_building", "cross_functional_collaboration"],
                "average_promotion_time": 4.0
            },
            "engineering_manager": {
                "minimum_performance_score": 85.0,
                "minimum_years_experience": 5.0,
                "required_skills": ["people_management", "strategic_thinking", "budget_management"],
                "success_factors": ["leadership", "communication", "business_impact"],
                "average_promotion_time": 5.0
            },
            "senior_manager": {
                "minimum_performance_score": 88.0,
                "minimum_years_experience": 7.0,
                "required_skills": ["strategic_planning", "organizational_leadership", "executive_presence"],
                "success_factors": ["vision", "influence", "results_delivery"],
                "average_promotion_time": 6.0
            }
        }
        
        # Mock benchmark data
        self.benchmark_data = {
            "software_engineer_to_senior": {"success_rate": 75.0, "avg_time": 3.2},
            "senior_to_lead": {"success_rate": 65.0, "avg_time": 4.1},
            "lead_to_manager": {"success_rate": 55.0, "avg_time": 5.3},
            "manager_to_senior_manager": {"success_rate": 45.0, "avg_time": 6.8}
        }
    
    def simulate_promotion(self, request: PromotionSimulationRequest) -> PromotionSimulationResponse:
        """
        Run promotion simulation using advanced algorithms 
        (and a healthy dose of code bro magic) ✨
        """
        try:
            logger.info(f"🔮 Running promotion simulation for employee {request.employee_id}")
            
            # Get promotion criteria for target position
            position_key = request.target_position.lower().replace(" ", "_")
            criteria = self.promotion_criteria.get(
                position_key, 
                self.promotion_criteria.get("senior_software_engineer")  # Default
            )
            
            # Analyze promotion factors
            factors_analysis = self._analyze_promotion_factors(request, criteria)
            
            # Calculate promotion probability using our proprietary algorithm™
            promotion_probability = self._calculate_promotion_probability(factors_analysis, criteria)
            
            # Generate recommendation
            recommendation = self._generate_recommendation(promotion_probability, factors_analysis)
            
            # Generate development plan if requested
            development_plan = None
            if request.include_development_plan:
                development_plan = self._generate_development_plan(factors_analysis, criteria)
            
            # Get benchmark comparison
            benchmark_comparison = self._get_benchmark_comparison(request, promotion_probability)
            
            # Determine confidence level
            confidence_level = self._calculate_confidence_level(factors_analysis)
            
            # Estimate readiness timeline
            estimated_timeline = self._estimate_readiness_timeline(factors_analysis, criteria)
            
            # Save simulation to database
            simulation = PromotionSimulation(
                employee_id=request.employee_id,
                target_position=request.target_position,
                current_performance_score=request.current_performance_score,
                years_in_current_role=request.years_in_current_role,
                years_with_company=request.years_with_company,
                promotion_probability=promotion_probability,
                recommendation=recommendation,
                factors_analysis=[factor.dict() for factor in factors_analysis],
                development_plan=[action.dict() for action in development_plan] if development_plan else None,
                simulation_algorithm=request.simulation_algorithm or "monte_carlo"
            )
            
            self.db.add(simulation)
            self.db.commit()
            self.db.refresh(simulation)
            
            response = PromotionSimulationResponse(
                simulation_id=simulation.id,
                employee_id=request.employee_id,
                target_position=request.target_position,
                promotion_probability=promotion_probability,
                recommendation=recommendation,
                confidence_level=confidence_level,
                factors_analysis=factors_analysis,
                development_plan=development_plan,
                estimated_readiness_timeline=estimated_timeline,
                benchmark_comparison=benchmark_comparison,
                simulation_algorithm=simulation.simulation_algorithm,
                simulation_timestamp=simulation.simulation_date
            )
            
            logger.info(f"✅ Simulation completed with {promotion_probability}% probability")
            return response
            
        except Exception as e:
            logger.error(f"💥 Error in promotion simulation: {e}")
            self.db.rollback()
            raise
    
    def _analyze_promotion_factors(self, request: PromotionSimulationRequest, criteria: Dict) -> List[PromotionFactor]:
        """Analyze factors affecting promotion probability"""
        factors = []
        
        # Performance factor
        performance_factor = PromotionFactor(
            factor_name="performance_score",
            current_value=request.current_performance_score,
            target_value=criteria["minimum_performance_score"],
            weight=0.35,
            impact_score=min(request.current_performance_score / criteria["minimum_performance_score"], 1.0) * 100,
            improvement_needed=self._calculate_improvement_needed(
                request.current_performance_score, criteria["minimum_performance_score"]
            )
        )
        factors.append(performance_factor)
        
        # Experience factor
        experience_factor = PromotionFactor(
            factor_name="years_experience",
            current_value=request.years_in_current_role,
            target_value=criteria["minimum_years_experience"],
            weight=0.25,
            impact_score=min(request.years_in_current_role / criteria["minimum_years_experience"], 1.0) * 100,
            improvement_needed=self._calculate_improvement_needed(
                request.years_in_current_role, criteria["minimum_years_experience"]
            )
        )
        factors.append(experience_factor)
        
        # Skills factor (simulated)
        skills_score = random.uniform(60, 95)  # Mock skills assessment
        skills_factor = PromotionFactor(
            factor_name="skills_assessment",
            current_value=skills_score,
            target_value=80.0,  # Target skills score
            weight=0.20,
            impact_score=min(skills_score / 80.0, 1.0) * 100,
            improvement_needed=self._calculate_improvement_needed(skills_score, 80.0)
        )
        factors.append(skills_factor)
        
        # Leadership potential (simulated)
        leadership_score = random.uniform(50, 90)
        leadership_factor = PromotionFactor(
            factor_name="leadership_potential",
            current_value=leadership_score,
            target_value=75.0,
            weight=0.15,
            impact_score=min(leadership_score / 75.0, 1.0) * 100,
            improvement_needed=self._calculate_improvement_needed(leadership_score, 75.0)
        )
        factors.append(leadership_factor)
        
        # Company tenure factor
        tenure = request.years_with_company or request.years_in_current_role * 1.2
        tenure_factor = PromotionFactor(
            factor_name="company_tenure",
            current_value=tenure,
            target_value=2.0,  # Minimum company tenure
            weight=0.05,
            impact_score=min(tenure / 2.0, 1.0) * 100,
            improvement_needed=self._calculate_improvement_needed(tenure, 2.0)
        )
        factors.append(tenure_factor)
        
        return factors
    
    def _calculate_improvement_needed(self, current_value: float, target_value: float) -> str:
        """Calculate how much improvement is needed"""
        if current_value >= target_value:
            return "none"
        
        gap_percentage = (target_value - current_value) / target_value * 100
        
        if gap_percentage <= 10:
            return "low"
        elif gap_percentage <= 25:
            return "medium"
        elif gap_percentage <= 50:
            return "high"
        else:
            return "critical"
    
    def _calculate_promotion_probability(self, factors: List[PromotionFactor], criteria: Dict) -> float:
        """
        Calculate promotion probability using our proprietary algorithm™
        (Actually just weighted scoring, but it sounds cooler this way)
        """
        weighted_score = 0.0
        
        for factor in factors:
            # Calculate factor contribution
            factor_score = (factor.impact_score / 100) * factor.weight
            weighted_score += factor_score
        
        # Convert to percentage
        base_probability = weighted_score * 100
        
        # Add some randomness for realism (Monte Carlo simulation vibes)
        random_factor = random.uniform(-5, 5)
        final_probability = max(0, min(100, base_probability + random_factor))
        
        return round(final_probability, 2)
    
    def _generate_recommendation(self, probability: float, factors: List[PromotionFactor]) -> str:
        """Generate promotion recommendation based on probability and factors"""
        critical_gaps = len([f for f in factors if f.improvement_needed == "critical"])
        high_gaps = len([f for f in factors if f.improvement_needed == "high"])
        
        if probability >= 80 and critical_gaps == 0:
            return "promote"
        elif probability >= 60 and critical_gaps <= 1:
            return "develop"
        else:
            return "maintain"
    
    def _generate_development_plan(self, factors: List[PromotionFactor], criteria: Dict) -> List[DevelopmentAction]:
        """Generate personalized development plan"""
        actions = []
        
        for factor in factors:
            if factor.improvement_needed in ["medium", "high", "critical"]:
                action = self._create_development_action(factor)
                actions.append(action)
        
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        actions.sort(key=lambda x: priority_order.get(x.priority, 3))
        
        return actions
    
    def _create_development_action(self, factor: PromotionFactor) -> DevelopmentAction:
        """Create specific development action for a factor"""
        action_templates = {
            "performance_score": {
                "action_type": "performance",
                "description": "Focus on exceeding performance targets and delivering high-impact projects",
                "timeline": "3-6 months",
                "metrics": ["Quarterly performance rating", "Project completion rate", "Stakeholder feedback"]
            },
            "years_experience": {
                "action_type": "experience",
                "description": "Gain additional experience in current role while taking on stretch assignments",
                "timeline": "6-12 months",
                "metrics": ["Project leadership roles", "Cross-functional collaboration", "Skill demonstrations"]
            },
            "skills_assessment": {
                "action_type": "skill",
                "description": "Complete targeted skill development in key technical and soft skills",
                "timeline": "3-9 months",
                "metrics": ["Certification completion", "Skill assessment scores", "Peer feedback"]
            },
            "leadership_potential": {
                "action_type": "leadership",
                "description": "Develop leadership skills through mentoring, team leadership, and executive visibility",
                "timeline": "6-12 months",
                "metrics": ["Mentoring relationships", "Team project leadership", "360-degree feedback"]
            },
            "company_tenure": {
                "action_type": "experience",
                "description": "Build deeper company knowledge and cross-functional relationships",
                "timeline": "ongoing",
                "metrics": ["Cross-team collaboration", "Company culture contributions", "Network building"]
            }
        }
        
        template = action_templates.get(factor.factor_name, action_templates["skills_assessment"])
        
        # Determine priority based on improvement needed
        priority_map = {"critical": "critical", "high": "high", "medium": "medium", "low": "low"}
        priority = priority_map.get(factor.improvement_needed, "medium")
        
        return DevelopmentAction(
            action_type=template["action_type"],
            description=template["description"],
            priority=priority,
            estimated_timeline=template["timeline"],
            success_metrics=template["metrics"]
        )
    
    def _get_benchmark_comparison(self, request: PromotionSimulationRequest, probability: float) -> Dict[str, Any]:
        """Get benchmark comparison data"""
        # Simulate benchmark data
        avg_probability = random.uniform(55, 75)
        
        return {
            "employee_probability": probability,
            "benchmark_average": avg_probability,
            "percentile": min(95, max(5, (probability / avg_probability) * 50)),
            "comparison": "above_average" if probability > avg_probability else "below_average",
            "sample_size": random.randint(50, 200)
        }
    
    def _calculate_confidence_level(self, factors: List[PromotionFactor]) -> str:
        """Calculate confidence level of the simulation"""
        high_confidence_factors = len([f for f in factors if f.impact_score >= 80])
        total_factors = len(factors)
        
        confidence_ratio = high_confidence_factors / total_factors
        
        if confidence_ratio >= 0.8:
            return "high"
        elif confidence_ratio >= 0.6:
            return "medium"
        else:
            return "low"
    
    def _estimate_readiness_timeline(self, factors: List[PromotionFactor], criteria: Dict) -> str:
        """Estimate when employee might be ready for promotion"""
        critical_gaps = len([f for f in factors if f.improvement_needed == "critical"])
        high_gaps = len([f for f in factors if f.improvement_needed == "high"])
        medium_gaps = len([f for f in factors if f.improvement_needed == "medium"])
        
        if critical_gaps == 0 and high_gaps == 0:
            return "ready_now"
        elif critical_gaps == 0 and high_gaps <= 1:
            return "3-6_months"
        elif critical_gaps <= 1:
            return "6-12_months"
        else:
            return "12+_months"
    
    def get_employee_simulation_history(self, employee_id: int) -> List[Dict]:
        """Get simulation history for an employee"""
        simulations = self.db.query(PromotionSimulation).filter(
            PromotionSimulation.employee_id == employee_id
        ).order_by(desc(PromotionSimulation.simulation_date)).all()
        
        return [simulation.to_dict() for simulation in simulations]
    
    def get_simulation_by_id(self, simulation_id: int) -> Optional[Dict]:
        """Get specific simulation by ID"""
        simulation = self.db.query(PromotionSimulation).filter(
            PromotionSimulation.id == simulation_id
        ).first()
        
        return simulation.to_dict() if simulation else None
