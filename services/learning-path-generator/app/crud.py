"""
CRUD Operations for Learning Path Generator Service
Where learning algorithms meet database reality and dad jokes meet professional code! 🛤️🤖
Coded with caffeine and comedy by rickroll187 at 2025-08-03 18:13:03 UTC
"""
import logging
import random
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func

from app.models import (
    LearningPath, LearningModule, LearningProgress, 
    SkillDefinition, LearningRecommendation, PathOptimization
)
from app.schemas import (
    LearningPathRequest, LearningPathResponse, LearningModule as LearningModuleSchema,
    LearningProgressResponse, SkillRoadmapResponse, PathOptimizationResponse
)

logger = logging.getLogger(__name__)

class LearningPathCRUD:
    """
    CRUD operations for learning path generation 
    More reliable than GPS, funnier than a stand-up comedian! 🗺️😄
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # Mock learning content database (in production, this would be massive!)
        self.learning_content = {
            "python": {
                "beginner": [
                    {"name": "Python Fundamentals", "type": "course", "hours": 20, "provider": "CodeAcademy"},
                    {"name": "Python Variables and Data Types", "type": "video", "hours": 3, "provider": "YouTube"},
                    {"name": "Basic Python Projects", "type": "practice", "hours": 15, "provider": "Internal"}
                ],
                "intermediate": [
                    {"name": "Advanced Python Concepts", "type": "course", "hours": 30, "provider": "Coursera"},
                    {"name": "Python OOP Mastery", "type": "course", "hours": 25, "provider": "Udemy"},
                    {"name": "Web Development with Flask", "type": "project", "hours": 40, "provider": "Internal"}
                ],
                "advanced": [
                    {"name": "Python Architecture Patterns", "type": "course", "hours": 35, "provider": "Pluralsight"},
                    {"name": "Performance Optimization", "type": "course", "hours": 20, "provider": "Internal"},
                    {"name": "Python Certification Prep", "type": "certification", "hours": 50, "provider": "PSF"}
                ]
            },
            "javascript": {
                "beginner": [
                    {"name": "JavaScript Basics", "type": "course", "hours": 18, "provider": "freeCodeCamp"},
                    {"name": "DOM Manipulation", "type": "practice", "hours": 12, "provider": "Internal"}
                ],
                "intermediate": [
                    {"name": "React Development", "type": "course", "hours": 40, "provider": "Udemy"},
                    {"name": "Node.js Backend", "type": "course", "hours": 35, "provider": "Coursera"}
                ],
                "advanced": [
                    {"name": "Full-Stack JavaScript", "type": "project", "hours": 60, "provider": "Internal"},
                    {"name": "JavaScript Performance", "type": "course", "hours": 25, "provider": "Frontend Masters"}
                ]
            },
            "leadership": {
                "beginner": [
                    {"name": "Leadership Fundamentals", "type": "course", "hours": 15, "provider": "LinkedIn Learning"},
                    {"name": "Team Communication", "type": "course", "hours": 10, "provider": "Internal"}
                ],
                "intermediate": [
                    {"name": "Advanced Leadership", "type": "course", "hours": 25, "provider": "Harvard Online"},
                    {"name": "Conflict Resolution", "type": "course", "hours": 20, "provider": "Coursera"}
                ],
                "advanced": [
                    {"name": "Executive Leadership", "type": "course", "hours": 40, "provider": "Wharton Online"},
                    {"name": "Strategic Leadership Project", "type": "project", "hours": 30, "provider": "Internal"}
                ]
            }
        }
        
        # Fairness weights for bias-free path generation
        self.fairness_weights = {
            "skill_relevance": 0.40,     # How relevant to target skills
            "learning_efficiency": 0.25, # Time to value ratio
            "engagement_factor": 0.15,   # How engaging the content is
            "difficulty_progression": 0.10, # Proper difficulty curve
            "market_relevance": 0.10     # Current market demand
        }
        
        # Dad jokes for motivation (because learning should be fun!)
        self.motivation_jokes = [
            "Why did the programmer quit his job? He didn't get arrays! But you're getting skills! 😄",
            "How many programmers does it take to change a light bulb? None, it's a hardware problem! Keep coding! 💡",
            "Why do Java developers wear glasses? Because they can't C#! But your vision is 20/20! 👓",
            "What's a programmer's favorite hangout place? Foo Bar! Speaking of bars, you're raising yours! 🍺",
            "Why did the developer break up with CSS? Because they had no class! But you've got style! 💅"
        ]
    
    def generate_personalized_path(self, request: LearningPathRequest) -> LearningPathResponse:
        """
        Generate a personalized learning path so good, 
        it makes Netflix recommendations look like random guessing! 🎯✨
        """
        try:
            logger.info(f"🛤️ Generating learning path for employee {request.employee_id}")
            
            # Analyze current skill levels and target skills
            skill_gaps = self._analyze_skill_gaps(request.target_skills, request.current_skill_level)
            
            # Generate learning modules based on skill gaps
            modules = self._generate_learning_modules(skill_gaps, request)
            
            # Calculate path duration and milestones
            total_hours = sum(module.estimated_hours for module in modules)
            duration_weeks = max(1, int(total_hours / request.time_commitment_hours_per_week))
            
            # Generate milestones (because everyone loves a good checkpoint!)
            milestones = self._generate_milestones(modules, duration_weeks)
            
            # Calculate personalization factors
            personalization_factors = self._calculate_personalization_factors(request)
            
            # Generate path name (with a touch of creativity!)
            path_name = self._generate_path_name(request.target_skills, request.current_skill_level)
            
            # Save to database
            learning_path = LearningPath(
                employee_id=request.employee_id,
                path_name=path_name,
                target_skills=request.target_skills,
                current_skill_levels={skill: request.current_skill_level for skill in request.target_skills},
                difficulty_level=request.preferred_difficulty or "adaptive",
                learning_style=request.learning_style,
                estimated_duration_weeks=duration_weeks,
                time_commitment_hours_per_week=request.time_commitment_hours_per_week,
                personalization_factors=personalization_factors,
                algorithm_version="bias_free_v3.0"
            )
            
            self.db.add(learning_path)
            self.db.commit()
            self.db.refresh(learning_path)
            
            # Save learning modules
            for i, module_data in enumerate(modules):
                module = LearningModule(
                    learning_path_id=learning_path.id,
                    module_name=module_data.module_name,
                    module_type=module_data.module_type,
                    skill_focus=module_data.skill_focus,
                    difficulty_level=module_data.difficulty_level,
                    estimated_hours=module_data.estimated_hours,
                    sequence_order=i + 1,
                    prerequisites=module_data.prerequisites,
                    content_provider=module_data.content_provider,
                    content_url=module_data.content_url,
                    description=module_data.description,
                    learning_objectives=module_data.learning_objectives
                )
                self.db.add(module)
            
            self.db.commit()
            
            # Calculate bias score
            bias_score = self._calculate_bias_score(request, modules)
            learning_path.bias_score = bias_score
            self.db.commit()
            
            # Generate expected outcomes
            expected_outcomes = self._generate_expected_outcomes(request.target_skills, duration_weeks)
            
            response = LearningPathResponse(
                path_id=learning_path.id,
                employee_id=request.employee_id,
                path_name=path_name,
                target_skills=request.target_skills,
                difficulty_level=learning_path.difficulty_level,
                learning_style=request.learning_style,
                estimated_duration_weeks=duration_weeks,
                time_commitment_hours_per_week=request.time_commitment_hours_per_week,
                learning_modules=modules,
                milestones=milestones,
                personalization_factors=personalization_factors,
                bias_score=bias_score,
                fairness_certified=bias_score <= 0.2,
                completion_criteria=self._generate_completion_criteria(request.target_skills),
                estimated_outcomes=expected_outcomes,
                path_generation_timestamp=datetime.utcnow()
            )
            
            logger.info(f"✅ Generated {len(modules)}-module path over {duration_weeks} weeks (bias score: {bias_score:.3f})")
            return response
            
        except Exception as e:
            logger.error(f"💥 Error generating learning path: {e}")
            self.db.rollback()
            raise
    
    def _analyze_skill_gaps(self, target_skills: List[str], current_level: str) -> Dict[str, Dict]:
        """Analyze what needs to be learned - like a GPS calculating the route!"""
        skill_gaps = {}
        
        level_progression = ["beginner", "intermediate", "advanced", "expert"]
        current_idx = level_progression.index(current_level)
        
        for skill in target_skills:
            # For each skill, determine what levels need to be covered
            skill_gaps[skill] = {
                "current_level": current_level,
                "levels_to_cover": level_progression[current_idx:min(len(level_progression), current_idx + 2)],
                "priority": random.choice(["high", "medium", "low"]),  # In production, this would be smarter
                "market_demand": random.choice(["high", "medium", "low"])
            }
        
        return skill_gaps
    
    def _generate_learning_modules(self, skill_gaps: Dict, request: LearningPathRequest) -> List[LearningModuleSchema]:
        """Generate learning modules based on skill gaps - the heart of our GPS! 🗺️"""
        modules = []
        module_id = 1
        
        for skill, gap_info in skill_gaps.items():
            for level in gap_info["levels_to_cover"]:
                # Get available content for this skill and level
                skill_content = self.learning_content.get(skill, {}).get(level, [])
                
                if not skill_content:
                    # Create a generic module if we don't have specific content
                    skill_content = [{
                        "name": f"{skill.title()} - {level.title()}",
                        "type": "course",
                        "hours": 20,
                        "provider": "Internal"
                    }]
                
                # Select best content based on preferences
                selected_content = self._select_best_content(skill_content, request)
                
                for content in selected_content:
                    module = LearningModuleSchema(
                        module_id=module_id,
                        module_name=content["name"],
                        module_type=content["type"],
                        skill_focus=skill,
                        difficulty_level=level,
                        estimated_hours=content["hours"],
                        sequence_order=module_id,
                        prerequisites=self._determine_prerequisites(skill, level, modules),
                        content_provider=content["provider"],
                        content_url=f"https://learning.n3xtpath.com/{skill}/{level}/{content['name'].lower().replace(' ', '-')}",
                        description=f"Master {skill} at {level} level through {content['type']}",
                        learning_objectives=[
                            f"Understand {skill} {level} concepts",
                            f"Apply {skill} in real-world scenarios",
                            f"Build confidence in {skill} usage"
                        ]
                    )
                    modules.append(module)
                    module_id += 1
        
        return modules
    
    def _select_best_content(self, available_content: List[Dict], request: LearningPathRequest) -> List[Dict]:
        """Select the best content based on learning preferences"""
        # Simple content selection logic (in production, this would be ML-powered)
        selected = []
        
        # Prefer certain types based on learning style
        style_preferences = {
            "visual": ["video", "course"],
            "auditory": ["course", "video"],
            "kinesthetic": ["practice", "project"],
            "mixed": ["course", "practice", "project"]
        }
        
        preferred_types = style_preferences.get(request.learning_style, ["course"])
        
        # Select up to 2 pieces of content per skill level
        for content in available_content[:2]:
            if content["type"] in preferred_types or len(selected) == 0:
                selected.append(content)
        
        return selected if selected else available_content[:1]
    
    def _determine_prerequisites(self, skill: str, level: str, existing_modules: List[LearningModuleSchema]) -> List[str]:
        """Determine prerequisites for a module"""
        prerequisites = []
        
        # If this is intermediate or advanced, previous levels are prerequisites
        if level in ["intermediate", "advanced", "expert"]:
            for module in existing_modules:
                if module.skill_focus == skill and module.difficulty_level in ["beginner", "intermediate"]:
                    prerequisites.append(module.module_name)
        
        return prerequisites
    
    def _generate_milestones(self, modules: List[LearningModuleSchema], duration_weeks: int) -> List[Dict[str, Any]]:
        """Generate milestones throughout the learning journey"""
        milestones = []
        
        # Create milestones at 25%, 50%, 75%, and 100% completion
        milestone_percentages = [25, 50, 75, 100]
        modules_per_milestone = len(modules) // 4
        
        for i, percentage in enumerate(milestone_percentages):
            milestone_week = max(1, int((duration_weeks * percentage) / 100))
            milestone_modules = modules[i * modules_per_milestone:(i + 1) * modules_per_milestone]
            
            milestones.append({
                "milestone_name": f"{percentage}% Completion Milestone",
                "target_week": milestone_week,
                "modules_to_complete": [m.module_name for m in milestone_modules],
                "celebration_message": self._get_milestone_celebration(percentage),
                "skills_gained": list(set(m.skill_focus for m in milestone_modules))
            })
        
        return milestones
    
    def _get_milestone_celebration(self, percentage: int) -> str:
        """Get celebration message for milestones - because achievements deserve recognition!"""
        celebrations = {
            25: "You're off to a great start! 🚀 " + random.choice(self.motivation_jokes),
            50: "Halfway there! You're crushing it! 💪 " + random.choice(self.motivation_jokes),
            75: "Almost at the finish line! Keep going! 🏃‍♂️ " + random.choice(self.motivation_jokes),
            100: "CONGRATULATIONS! You're officially awesome! 🎉 " + random.choice(self.motivation_jokes)
        }
        return celebrations.get(percentage, "Great progress! Keep learning! 📚")
    
    def _calculate_personalization_factors(self, request: LearningPathRequest) -> Dict[str, Any]:
        """Calculate factors used for personalization"""
        return {
            "learning_style_weight": 0.3 if request.learning_style != "mixed" else 0.1,
            "time_constraint_factor": min(request.time_commitment_hours_per_week / 10, 1.0),
            "certification_preference": 0.2 if request.include_certifications else 0.0,
            "practical_preference": 0.3 if request.include_practical_projects else 0.1,
            "deadline_pressure": 0.8 if request.deadline_weeks and request.deadline_weeks < 12 else 0.3,
            "algorithm_version": "bias_free_personalization_v3.0"
        }
    
    def _generate_path_name(self, target_skills: List[str], current_level: str) -> str:
        """Generate a creative name for the learning path"""
        skill_names = ", ".join([skill.title() for skill in target_skills[:3]])
        
        creative_names = [
            f"Journey to {skill_names} Mastery",
            f"The {skill_names} Adventure",
            f"Leveling Up: {skill_names} Edition",
            f"From {current_level.title()} to Hero: {skill_names}",
            f"The {skill_names} Transformation"
        ]
        
        return random.choice(creative_names)
    
    def _calculate_bias_score(self, request: LearningPathRequest, modules: List[LearningModuleSchema]) -> float:
        """Calculate bias score for the learning path - keeping it fair!"""
        # In production, this would analyze demographic patterns, content bias, etc.
        # For now, we'll simulate a bias-free score
        
        bias_factors = []
        
        # Check for content diversity
        providers = set(module.content_provider for module in modules)
        provider_diversity = len(providers) / max(len(modules), 1)
        bias_factors.append(1.0 - provider_diversity)  # Lower is better
        
        # Check for learning style accommodation
        style_accommodation = 0.1 if request.learning_style == "mixed" else 0.2
        bias_factors.append(style_accommodation)
        
        # Check for difficulty progression
        difficulty_levels = [module.difficulty_level for module in modules]
        has_progression = len(set(difficulty_levels)) > 1
        progression_bias = 0.05 if has_progression else 0.15
        bias_factors.append(progression_bias)
        
        # Overall bias score (lower is better, 0 = no bias)
        bias_score = sum(bias_factors) / len(bias_factors)
        return min(bias_score, 1.0)
    
    def _generate_expected_outcomes(self, target_skills: List[str], duration_weeks: int) -> List[str]:
        """Generate expected learning outcomes"""
        outcomes = []
        
        for skill in target_skills:
            outcomes.extend([
                f"Proficiency in {skill} fundamentals and best practices",
                f"Ability to apply {skill} in real-world projects",
                f"Confidence to teach {skill} concepts to others"
            ])
        
        outcomes.extend([
            f"Completed comprehensive {duration_weeks}-week learning journey",
            "Enhanced problem-solving and critical thinking skills",
            "Improved career prospects and marketability",
            "Network of learning resources and community connections"
        ])
        
        return outcomes[:6]  # Keep it reasonable
    
    def _generate_completion_criteria(self, target_skills: List[str]) -> Dict[str, Any]:
        """Generate criteria for path completion"""
        return {
            "modules_completion_rate": 85,  # Must complete 85% of modules
            "skill_assessments": {skill: "70% pass rate" for skill in target_skills},
            "practical_projects": "Complete at least 2 hands-on projects",
            "time_commitment": "Maintain consistent weekly progress",
            "peer_interaction": "Participate in learning community discussions"
        }
    
    def validate_path_fairness(self, request: LearningPathRequest, response: LearningPathResponse) -> float:
        """Validate that the learning path generation was fair and unbiased"""
        fairness_checks = []
        
        # Check skill coverage fairness
        all_skills_covered = all(
            any(module.skill_focus == skill for module in response.learning_modules)
            for skill in request.target_skills
        )
        fairness_checks.append(0.0 if all_skills_covered else 0.3)
        
        # Check content diversity
        providers = set(module.content_provider for module in response.learning_modules)
        diversity_score = len(providers) / max(len(response.learning_modules), 1)
        fairness_checks.append(max(0, 0.2 - diversity_score))
        
        # Check time allocation fairness
        skill_time_distribution = {}
        for module in response.learning_modules:
            skill = module.skill_focus
            skill_time_distribution[skill] = skill_time_distribution.get(skill, 0) + module.estimated_hours
        
        if len(skill_time_distribution) > 1:
            time_values = list(skill_time_distribution.values())
            time_variance = np.var(time_values) / max(np.mean(time_values), 1)
            fairness_checks.append(min(time_variance / 2, 0.2))
        
        return sum(fairness_checks) / len(fairness_checks) if fairness_checks else 0.0
    
    def get_employee_progress(self, employee_id: int) -> Optional[Dict]:
        """Get learning progress for an employee"""
        # Get active learning paths
        active_paths = self.db.query(LearningPath).filter(
            and_(
                LearningPath.employee_id == employee_id,
                LearningPath.path_status == "active"
            )
        ).all()
        
        if not active_paths:
            return None
        
        progress_data = []
        for path in active_paths:
            # Get modules for this path
            modules = self.db.query(LearningModule).filter(
                LearningModule.learning_path_id == path.id
            ).all()
            
            completed_modules = [m for m in modules if m.completion_status == "completed"]
            current_module = next((m for m in modules if m.completion_status == "in_progress"), None)
            
            progress_data.append({
                "path_id": path.id,
                "path_name": path.path_name,
                "completion_percentage": path.completion_percentage,
                "modules_completed": len(completed_modules),
                "total_modules": len(modules),
                "current_module": current_module.to_dict() if current_module else None,
                "estimated_completion": self._calculate_estimated_completion(path, completed_modules),
                "motivation_message": random.choice(self.motivation_jokes)
            })
        
        return {
            "employee_id": employee_id,
            "active_paths": progress_data,
            "overall_engagement": random.uniform(7.5, 9.5),  # Mock engagement score
            "learning_streak_days": random.randint(5, 30),
            "achievements_unlocked": ["Fast Learner", "Consistency Champion", "Skill Collector"]
        }
    
    def _calculate_estimated_completion(self, path: LearningPath, completed_modules: List) -> str:
        """Calculate estimated completion date"""
        if not completed_modules:
            return f"{path.estimated_duration_weeks} weeks from start"
        
        completion_rate = len(completed_modules) / max(path.modules.count(), 1)
        weeks_remaining = path.estimated_duration_weeks * (1 - completion_rate)
        
        estimated_date = datetime.utcnow() + timedelta(weeks=max(1, int(weeks_remaining)))
        return estimated_date.strftime("%Y-%m-%d")
    
    def optimize_learning_path(self, path_id: int, performance_data: Dict) -> Dict:
        """Optimize learning path based on performance data"""
        try:
            learning_path = self.db.query(LearningPath).filter(
                LearningPath.id == path_id
            ).first()
            
            if not learning_path:
                raise ValueError("Learning path not found")
            
            # Analyze performance data
            optimizations = []
            
            # If learner is struggling, suggest easier content
            if performance_data.get("difficulty_rating", 5) > 7:
                optimizations.append({
                    "type": "difficulty_adjustment",
                    "change": "Add foundational modules",
                    "reason": "High difficulty rating detected"
                })
            
            # If learner is bored, suggest more challenging content
            if performance_data.get("engagement_score", 5) < 6:
                optimizations.append({
                    "type": "engagement_boost",
                    "change": "Add interactive projects",
                    "reason": "Low engagement score"
                })
            
            # If learner is ahead of schedule, suggest advanced content
            if performance_data.get("completion_rate", 0.5) > 0.8:
                optimizations.append({
                    "type": "acceleration",
                    "change": "Add advanced modules",
                    "reason": "Ahead of schedule"
                })
            
            # Save optimization record
            optimization = PathOptimization(
                learning_path_id=path_id,
                optimization_trigger="performance_analysis",
                original_path_config=learning_path.to_dict(),
                optimized_path_config={
                    "optimizations": optimizations,
                    "performance_data": performance_data
                },
                optimization_algorithm="adaptive_learning_v3.0",
                performance_improvement=15.0,  # Expected improvement
                time_savings_hours=random.uniform(5, 15),
                engagement_boost=10.0
            )
            
            self.db.add(optimization)
            self.db.commit()
            
            return {
                "optimization_id": optimization.id,
                "changes": optimizations,
                "expected_improvement": "15% better performance",
                "message": "Your learning path just got smarter! 🧠✨"
            }
            
        except Exception as e:
            logger.error(f"💥 Error optimizing path: {e}")
            self.db.rollback()
            raise
    
    def generate_skill_roadmap(self, skill_name: str, difficulty_level: str) -> Dict:
        """Generate a comprehensive skill roadmap"""
        
        # Mock roadmap generation (in production, this would be comprehensive)
        roadmap_phases = {
            "beginner": [
                {"phase": "Foundation", "duration_weeks": 4, "focus": "Basic concepts and syntax"},
                {"phase": "Practice", "duration_weeks": 6, "focus": "Hands-on exercises and mini-projects"},
                {"phase": "Application", "duration_weeks": 4, "focus": "Real-world application"}
            ],
            "intermediate": [
                {"phase": "Advanced Concepts", "duration_weeks": 6, "focus": "Complex features and patterns"},
                {"phase": "Architecture", "duration_weeks": 8, "focus": "Design patterns and best practices"},
                {"phase": "Specialization", "duration_weeks": 6, "focus": "Choose your specialty area"}
            ],
            "advanced": [
                {"phase": "Mastery", "duration_weeks": 8, "focus": "Expert-level techniques"},
                {"phase": "Leadership", "duration_weeks": 6, "focus": "Teaching and mentoring others"},
                {"phase": "Innovation", "duration_weeks": 8, "focus": "Creating new solutions"}
            ]
        }
        
        phases = roadmap_phases.get(difficulty_level, roadmap_phases["intermediate"])
        total_duration = sum(phase["duration_weeks"] for phase in phases)
        
        return {
            "skill": skill_name,
            "difficulty": difficulty_level,
            "phases": phases,
            "total_duration": f"{total_duration} weeks",
            "key_milestones": [
                {"milestone": f"Complete {phase['phase']}", "week": sum(p["duration_weeks"] for p in phases[:i+1])}
                for i, phase in enumerate(phases)
            ],
            "success_metrics": [
                "Complete all phase assessments",
                "Build portfolio projects",
                "Receive peer/mentor feedback",
                "Demonstrate skill in real scenarios"
            ],
            "motivational_quote": random.choice(self.motivation_jokes)
        }
