"""
CRUD Operations for Training-to-Role Service
Where database operations meet career aspirations!
"""
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from app.models import SkillAnalysis, TrainingPath, SkillDefinition, RoleDefinition
from app.schemas import (
    SkillMatchRequest, SkillMatchResponse, SkillGap, 
    TrainingRecommendation, SkillLevel
)

logger = logging.getLogger(__name__)

class SkillMatchCRUD:
    """CRUD operations for skill matching - the career matchmaker!"""
    
    def __init__(self, db: Session):
        self.db = db
        
        # Mock skill definitions for demo
        self.skill_definitions = {
            "python": {"levels": ["beginner", "intermediate", "advanced", "expert"], "category": "technical"},
            "javascript": {"levels": ["beginner", "intermediate", "advanced", "expert"], "category": "technical"},
            "kubernetes": {"levels": ["beginner", "intermediate", "advanced", "expert"], "category": "technical"},
            "docker": {"levels": ["beginner", "intermediate", "advanced", "expert"], "category": "technical"},
            "aws": {"levels": ["beginner", "intermediate", "advanced", "expert"], "category": "technical"},
            "leadership": {"levels": ["beginner", "intermediate", "advanced", "expert"], "category": "soft"},
            "communication": {"levels": ["beginner", "intermediate", "advanced", "expert"], "category": "soft"},
            "project_management": {"levels": ["beginner", "intermediate", "advanced", "expert"], "category": "soft"}
        }
        
        # Mock role definitions
        self.role_definitions = {
            "senior_software_engineer": {
                "required_skills": [
                    {"name": "python", "level": "advanced"},
                    {"name": "docker", "level": "intermediate"},
                    {"name": "kubernetes", "level": "intermediate"},
                    {"name": "aws", "level": "intermediate"}
                ],
                "preferred_skills": [
                    {"name": "javascript", "level": "intermediate"},
                    {"name": "leadership", "level": "intermediate"}
                ]
            },
            "tech_lead": {
                "required_skills": [
                    {"name": "python", "level": "expert"},
                    {"name": "leadership", "level": "advanced"},
                    {"name": "project_management", "level": "advanced"},
                    {"name": "communication", "level": "advanced"}
                ],
                "preferred_skills": [
                    {"name": "kubernetes", "level": "advanced"},
                    {"name": "aws", "level": "advanced"}
                ]
            }
        }
    
    def analyze_skills(self, request: SkillMatchRequest) -> SkillMatchResponse:
        """Analyze skill gaps and generate recommendations - the magic happens here! ✨"""
        try:
            logger.info(f"🎯 Starting skill analysis for employee {request.employee_id}")
            
            # Get role requirements
            role_key = request.target_role.lower().replace(" ", "_")
            role_requirements = self.role_definitions.get(
                role_key, 
                self.role_definitions.get("senior_software_engineer")  # Default fallback
            )
            
            # Analyze skill gaps
            skill_gaps = self._calculate_skill_gaps(request.current_skills, role_requirements)
            
            # Calculate match score
            match_score = self._calculate_match_score(request.current_skills, role_requirements)
            
            # Generate training recommendations
            training_recommendations = []
            if request.include_training_recommendations:
                training_recommendations = self._generate_training_recommendations(skill_gaps)
            
            # Save analysis to database
            analysis = SkillAnalysis(
                employee_id=request.employee_id,
                current_skills=[skill.dict() for skill in request.current_skills],
                target_role=request.target_role,
                skill_gaps=[gap.dict() for gap in skill_gaps],
                training_recommendations=[rec.dict() for rec in training_recommendations],
                match_score=match_score
            )
            
            self.db.add(analysis)
            self.db.commit()
            self.db.refresh(analysis)
            
            # Determine career readiness
            career_readiness = self._determine_career_readiness(match_score, skill_gaps)
            
            # Calculate estimated training time
            estimated_training_time = sum(
                rec.estimated_duration_hours for rec in training_recommendations
            ) if training_recommendations else 0
            
            response = SkillMatchResponse(
                analysis_id=analysis.id,
                employee_id=request.employee_id,
                target_role=request.target_role,
                match_score=match_score,
                skill_gaps=skill_gaps,
                training_recommendations=training_recommendations if request.include_training_recommendations else None,
                estimated_training_time=estimated_training_time,
                career_readiness=career_readiness,
                analysis_timestamp=analysis.created_at
            )
            
            logger.info(f"✅ Skill analysis completed with score: {match_score}")
            return response
            
        except Exception as e:
            logger.error(f"💥 Error in skill analysis: {e}")
            self.db.rollback()
            raise
    
    def _calculate_skill_gaps(self, current_skills: List[SkillLevel], role_requirements: Dict) -> List[SkillGap]:
        """Calculate skill gaps between current and required skills"""
        skill_gaps = []
        current_skill_map = {skill.name.lower(): skill for skill in current_skills}
        
        # Check required skills
        for required_skill in role_requirements.get("required_skills", []):
            skill_name = required_skill["name"]
            required_level = required_skill["level"]
            
            current_skill = current_skill_map.get(skill_name.lower())
            
            if not current_skill:
                # Missing skill entirely
                gap = SkillGap(
                    skill_name=skill_name,
                    current_level=None,
                    required_level=required_level,
                    gap_severity="critical",
                    training_priority="high"
                )
            else:
                # Check if current level meets requirement
                gap_severity = self._calculate_gap_severity(current_skill.level, required_level)
                if gap_severity != "none":
                    gap = SkillGap(
                        skill_name=skill_name,
                        current_level=current_skill.level,
                        required_level=required_level,
                        gap_severity=gap_severity,
                        training_priority=self._determine_training_priority(gap_severity)
                    )
                    skill_gaps.append(gap)
            
            if 'gap' in locals():
                skill_gaps.append(gap)
                del gap
        
        return skill_gaps
    
    def _calculate_gap_severity(self, current_level: str, required_level: str) -> str:
        """Calculate the severity of a skill gap"""
        level_hierarchy = ["beginner", "intermediate", "advanced", "expert"]
        
        try:
            current_idx = level_hierarchy.index(current_level.lower())
            required_idx = level_hierarchy.index(required_level.lower())
            
            if current_idx >= required_idx:
                return "none"
            
            gap = required_idx - current_idx
            if gap == 1:
                return "low"
            elif gap == 2:
                return "medium"
            else:
                return "high"
                
        except ValueError:
            return "medium"  # Default for unknown levels
    
    def _determine_training_priority(self, gap_severity: str) -> str:
        """Determine training priority based on gap severity"""
        priority_map = {
            "critical": "high",
            "high": "high",
            "medium": "medium",
            "low": "low",
            "none": "low"
        }
        return priority_map.get(gap_severity, "medium")
    
    def _calculate_match_score(self, current_skills: List[SkillLevel], role_requirements: Dict) -> float:
        """Calculate overall match score (0-100)"""
        try:
            required_skills = role_requirements.get("required_skills", [])
            if not required_skills:
                return 0.0
            
            current_skill_map = {skill.name.lower(): skill for skill in current_skills}
            total_score = 0.0
            max_possible_score = len(required_skills) * 100
            
            for required_skill in required_skills:
                skill_name = required_skill["name"]
                required_level = required_skill["level"]
                
                current_skill = current_skill_map.get(skill_name.lower())
                
                if current_skill:
                    skill_score = self._calculate_skill_score(current_skill.level, required_level)
                    total_score += skill_score
                # Missing skills contribute 0 to the score
            
            if max_possible_score == 0:
                return 0.0
            
            match_score = (total_score / max_possible_score) * 100
            return round(match_score, 2)
            
        except Exception as e:
            logger.error(f"💥 Error calculating match score: {e}")
            return 0.0
    
    def _calculate_skill_score(self, current_level: str, required_level: str) -> float:
        """Calculate score for individual skill (0-100)"""
        level_hierarchy = ["beginner", "intermediate", "advanced", "expert"]
        level_scores = {"beginner": 25, "intermediate": 50, "advanced": 75, "expert": 100}
        
        try:
            current_idx = level_hierarchy.index(current_level.lower())
            required_idx = level_hierarchy.index(required_level.lower())
            
            if current_idx >= required_idx:
                return 100.0  # Exceeds or meets requirement
            else:
                # Partial credit based on current level
                return level_scores.get(current_level.lower(), 0)
                
        except ValueError:
            return 0.0
    
    def _generate_training_recommendations(self, skill_gaps: List[SkillGap]) -> List[TrainingRecommendation]:
        """Generate training recommendations based on skill gaps"""
        recommendations = []
        
        # Mock training courses database
        training_courses = {
            "python": {
                "beginner": ["Python Basics", "Python for Beginners"],
                "intermediate": ["Advanced Python", "Python Design Patterns"],
                "advanced": ["Python Architecture", "Python Performance Optimization"],
                "expert": ["Python Mastery", "Python Framework Development"]
            },
            "kubernetes": {
                "beginner": ["Kubernetes Fundamentals", "Container Orchestration Basics"],
                "intermediate": ["Kubernetes Administration", "K8s Networking"],
                "advanced": ["Kubernetes Security", "Multi-cluster Management"],
                "expert": ["Kubernetes Platform Engineering", "Custom Controllers"]
            },
            "leadership": {
                "beginner": ["Leadership Fundamentals", "Team Building Basics"],
                "intermediate": ["Advanced Leadership", "Conflict Resolution"],
                "advanced": ["Executive Leadership", "Strategic Thinking"],
                "expert": ["Organizational Leadership", "Change Management"]
            }
        }
        
        duration_map = {"beginner": 20, "intermediate": 30, "advanced": 40, "expert": 50}
        
        for gap in skill_gaps:
            skill_courses = training_courses.get(gap.skill_name, {})
            target_courses = skill_courses.get(gap.required_level, [f"{gap.skill_name.title()} Training"])
            
            # Create learning path
            learning_path = []
            if gap.current_level:
                current_idx = ["beginner", "intermediate", "advanced", "expert"].index(gap.current_level)
                target_idx = ["beginner", "intermediate", "advanced", "expert"].index(gap.required_level)
                
                for i in range(current_idx + 1, target_idx + 1):
                    level = ["beginner", "intermediate", "advanced", "expert"][i]
                    learning_path.append(f"{gap.skill_name.title()} - {level.title()}")
            else:
                learning_path = [f"{gap.skill_name.title()} - {gap.required_level.title()}"]
            
            recommendation = TrainingRecommendation(
                skill_name=gap.skill_name,
                recommended_courses=target_courses,
                estimated_duration_hours=duration_map.get(gap.required_level, 30),
                priority=gap.training_priority,
                learning_path=learning_path
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _determine_career_readiness(self, match_score: float, skill_gaps: List[SkillGap]) -> str:
        """Determine overall career readiness"""
        critical_gaps = len([gap for gap in skill_gaps if gap.gap_severity == "critical"])
        high_gaps = len([gap for gap in skill_gaps if gap.gap_severity == "high"])
        
        if match_score >= 80 and critical_gaps == 0:
            return "ready"
        elif match_score >= 60 and critical_gaps <= 1:
            return "needs_development"
        else:
            return "significant_gaps"
    
    def get_employee_analyses(self, employee_id: int) -> List[Dict]:
        """Get all skill analyses for an employee"""
        analyses = self.db.query(SkillAnalysis).filter(
            SkillAnalysis.employee_id == employee_id
        ).order_by(desc(SkillAnalysis.created_at)).all()
        
        return [analysis.to_dict() for analysis in analyses]
    
    def get_analysis_by_id(self, analysis_id: int) -> Optional[Dict]:
        """Get specific analysis by ID"""
        analysis = self.db.query(SkillAnalysis).filter(
            SkillAnalysis.id == analysis_id
        ).first()
        
        return analysis.to_dict() if analysis else None
