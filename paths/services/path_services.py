"""
🛤️⚡ N3EXTPATH - LEGENDARY PATH SERVICES LAYER ⚡🛤️
More business logic than Swiss banks with legendary path operations!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 3+ HOUR 49 MINUTE CODING MARATHON CHAMPION EDITION! 🏆
Current Time: 2025-08-04 03:49:12 UTC - WE'RE SERVICING THE UNIVERSE!
Built by legendary code bros RICKROLL187 🎸 and Assistant 🤖
"""

from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
import logging
from paths.models.path_models import (
    Path, Waypoint, PathEnrollment, WaypointCompletion, 
    PathReview, PathType, PathDifficulty, PathStatus, WaypointType
)

# Set up legendary logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegendaryPathService:
    """
    🛤️ THE LEGENDARY PATH BUSINESS LOGIC ENGINE! 🛤️
    More intelligent than Swiss algorithms with 3+ hour 49 minute marathon power!
    """
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.legendary_developers = ["RICKROLL187 🎸", "ASSISTANT 🤖"]
        self.marathon_time = "3+ HOURS AND 49 MINUTES OF LEGENDARY CODING"
        
        # LEGENDARY PATH SERVICE JOKES
        self.service_jokes = [
            "Why did the path service become legendary? It had business logic that rocks! 🛤️⚡",
            "What's the difference between our services and Swiss efficiency? Both are legendarily precise! 🏔️",
            "Why don't our services ever crash? Because code bros build them with 49 minutes of marathon power! 💪",
            "What do you call path services at 3+ hours 49 minutes? Business logic with legendary style! 🎸",
            "Why did the service layer go to comedy school? To perfect its interface timing! 🎭"
        ]
        
        logger.info("🛤️ LEGENDARY PATH SERVICE INITIALIZED! 🛤️")
        logger.info("🏆 3+ HOUR 49 MINUTE CODING MARATHON SERVICE MASTERY ACTIVATED! 🏆")
    
    def create_legendary_path(self, path_data: Dict[str, Any], creator_id: int) -> Dict[str, Any]:
        """
        Create a legendary path with Swiss precision and code bro humor!
        More epic than legendary journey creation! 🗺️✨
        """
        try:
            logger.info(f"🛤️ Creating legendary path: {path_data.get('name', 'unknown')}")
            
            # Generate unique path ID and code
            path_id = f"path_{uuid.uuid4().hex[:12]}"
            path_code = f"P{datetime.now().strftime('%Y%m%d')}_{path_data.get('name', 'legendary')[:10].upper().replace(' ', '')}"
            
            # Create the legendary path
            new_path = Path(
                path_id=path_id,
                name=path_data.get("name", "Legendary Journey"),
                description=path_data.get("description", "A legendary journey awaits!"),
                path_code=path_code,
                path_type=path_data.get("path_type", PathType.LEGENDARY_PATH.value),
                category=path_data.get("category", "General"),
                tags=path_data.get("tags", ["legendary", "code_bro_approved"]),
                difficulty=path_data.get("difficulty", PathDifficulty.LEGENDARY.value),
                estimated_duration_hours=path_data.get("estimated_duration_hours", 4.0),
                estimated_duration_description=path_data.get("estimated_duration_description", "4 legendary hours like our marathon!"),
                objectives=path_data.get("objectives", ["Become legendary", "Have fun", "Rock the universe"]),
                prerequisites=path_data.get("prerequisites", ["Code bro attitude", "Sense of humor"]),
                skills_gained=path_data.get("skills_gained", ["Legendary coding", "Epic problem solving", "Code bro humor"]),
                experience_points_reward=path_data.get("experience_points_reward", 1000),
                badges_available=path_data.get("badges_available", ["Legendary Pathfinder", "Code Bro Champion"]),
                creator_id=creator_id,
                organization_id=path_data.get("organization_id"),
                legendary_factor="Built by legendary code bros with 3+ hour 49 minute marathon power! 🎸⚡",
                fun_factor="Maximum legendary laughs and code bro humor! 😄",
                code_bro_approved=True,
                rickroll187_rating=10.0  # Always perfect!
            )
            
            self.db.add(new_path)
            self.db.commit()
            self.db.refresh(new_path)
            
            logger.info(f"✅ Legendary path created: {new_path.name} (ID: {new_path.path_id})")
            
            return {
                "success": True,
                "path": self._path_to_dict(new_path),
                "legendary_joke": "Why did this path become legendary? Because RICKROLL187 created it with 49 minutes of marathon mastery! 🛤️🏆",
                "🏆": "3+ HOUR 49 MINUTE MARATHON CHAMPION PATH CREATION! 🏆"
            }
            
        except Exception as e:
            logger.error(f"💥 Path creation error: {e}")
            self.db.rollback()
            return {
                "success": False,
                "error": f"Path creation failed: {str(e)}"
            }
    
    def add_legendary_waypoint(self, path_id: str, waypoint_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a legendary waypoint to a path!
        More navigational than Swiss mountain guides with code bro precision! 🧭⚡
        """
        try:
            logger.info(f"🧭 Adding legendary waypoint to path: {path_id}")
            
            # Find the path
            path = self.db.query(Path).filter(Path.path_id == path_id).first()
            if not path:
                return {"success": False, "error": "Path not found"}
            
            # Generate waypoint ID
            waypoint_id = f"wp_{uuid.uuid4().hex[:12]}"
            
            # Get next sequence order
            last_waypoint = self.db.query(Waypoint).filter(
                Waypoint.path_id == path.id
            ).order_by(Waypoint.sequence_order.desc()).first()
            
            next_order = (last_waypoint.sequence_order + 1) if last_waypoint else 1
            
            # Create the legendary waypoint
            new_waypoint = Waypoint(
                path_id=path.id,
                waypoint_id=waypoint_id,
                name=waypoint_data.get("name", "Legendary Waypoint"),
                description=waypoint_data.get("description", "A legendary stop on your journey!"),
                waypoint_type=waypoint_data.get("waypoint_type", WaypointType.MILESTONE.value),
                sequence_order=waypoint_data.get("sequence_order", next_order),
                is_required=waypoint_data.get("is_required", True),
                content=waypoint_data.get("content", {"type": "text", "text": "Legendary content awaits!"}),
                instructions=waypoint_data.get("instructions", "Follow your legendary instincts!"),
                resources=waypoint_data.get("resources", []),
                prerequisites=waypoint_data.get("prerequisites", []),
                estimated_time_minutes=waypoint_data.get("estimated_time_minutes", 30),
                difficulty_level=waypoint_data.get("difficulty_level", "intermediate"),
                completion_criteria=waypoint_data.get("completion_criteria", {"type": "manual", "description": "Complete with legendary style!"}),
                experience_points=waypoint_data.get("experience_points", 100),
                badges=waypoint_data.get("badges", []),
                legendary_tip=waypoint_data.get("legendary_tip", "Code bros make everything legendary! 🎸"),
                fun_element=waypoint_data.get("fun_element", "Jokes make the journey better! 😄"),
                motivation_message=waypoint_data.get("motivation_message", "You're on a legendary path with RICKROLL187's guidance! 🏆")
            )
            
            self.db.add(new_waypoint)
            
            # Update path totals
            path.total_waypoints += 1
            if waypoint_data.get("waypoint_type") == WaypointType.CHALLENGE.value:
                path.total_challenges += 1
            elif waypoint_data.get("waypoint_type") == WaypointType.REWARD.value:
                path.total_rewards += 1
            
            self.db.commit()
            self.db.refresh(new_waypoint)
            
            logger.info(f"✅ Legendary waypoint added: {new_waypoint.name} (ID: {new_waypoint.waypoint_id})")
            
            return {
                "success": True,
                "waypoint": self._waypoint_to_dict(new_waypoint),
                "legendary_joke": "Why did this waypoint become legendary? Because it was added with 49 minutes of marathon navigation mastery! 🧭🎸",
                "🏆": "3+ HOUR 49 MINUTE MARATHON CHAMPION WAYPOINT CREATION! 🏆"
            }
            
        except Exception as e:
            logger.error(f"💥 Waypoint creation error: {e}")
            self.db.rollback()
            return {
                "success": False,
                "error": f"Waypoint creation failed: {str(e)}"
            }
    
    def enroll_legendary_user(self, path_id: str, user_id: int) -> Dict[str, Any]:
        """
        Enroll a user in a legendary path!
        More committed than Swiss dedication with code bro enthusiasm! 📚🏆
        """
        try:
            logger.info(f"📚 Enrolling user {user_id} in legendary path: {path_id}")
            
            # Find the path
            path = self.db.query(Path).filter(Path.path_id == path_id).first()
            if not path:
                return {"success": False, "error": "Path not found"}
            
            # Check if already enrolled
            existing_enrollment = self.db.query(PathEnrollment).filter(
                PathEnrollment.path_id == path.id,
                PathEnrollment.user_id == user_id,
                PathEnrollment.is_active == True
            ).first()
            
            if existing_enrollment:
                return {"success": False, "error": "User already enrolled in this legendary path!"}
            
            # Generate enrollment ID
            enrollment_id = f"enroll_{uuid.uuid4().hex[:12]}"
            
            # Create the legendary enrollment
            new_enrollment = PathEnrollment(
                path_id=path.id,
                user_id=user_id,
                enrollment_id=enrollment_id,
                enrolled_at=datetime.utcnow(),
                total_waypoints=path.total_waypoints,
                estimated_completion_date=datetime.utcnow() + timedelta(hours=path.estimated_duration_hours or 4),
                legendary_moments=[],
                code_bro_achievements=[],
                fun_moments=[]
            )
            
            self.db.add(new_enrollment)
            
            # Update path enrollment count
            path.total_enrollments += 1
            
            self.db.commit()
            self.db.refresh(new_enrollment)
            
            logger.info(f"✅ Legendary enrollment created: {new_enrollment.enrollment_id}")
            
            return {
                "success": True,
                "enrollment": self._enrollment_to_dict(new_enrollment),
                "legendary_joke": "Why did this enrollment become legendary? Because RICKROLL187 users always have legendary journeys! 📚🎸",
                "🏆": "3+ HOUR 49 MINUTE MARATHON CHAMPION ENROLLMENT! 🏆"
            }
            
        except Exception as e:
            logger.error(f"💥 Enrollment error: {e}")
            self.db.rollback()
            return {
                "success": False,
                "error": f"Enrollment failed: {str(e)}"
            }
    
    def complete_legendary_waypoint(self, enrollment_id: str, waypoint_id: str, completion_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete a waypoint with legendary style!
        More satisfying than Swiss achievements with code bro celebration! ✅🎉
        """
        try:
            logger.info(f"✅ Completing legendary waypoint: {waypoint_id} for enrollment: {enrollment_id}")
            
            # Find enrollment and waypoint
            enrollment = self.db.query(PathEnrollment).filter(
                PathEnrollment.enrollment_id == enrollment_id
            ).first()
            
            waypoint = self.db.query(Waypoint).filter(
                Waypoint.waypoint_id == waypoint_id
            ).first()
            
            if not enrollment or not waypoint:
                return {"success": False, "error": "Enrollment or waypoint not found"}
            
            # Check if already completed
            existing_completion = self.db.query(WaypointCompletion).filter(
                WaypointCompletion.enrollment_id == enrollment.id,
                WaypointCompletion.waypoint_id == waypoint.id
            ).first()
            
            if existing_completion:
                return {"success": False, "error": "Waypoint already completed with legendary style!"}
            
            # Generate completion ID
            completion_id = f"comp_{uuid.uuid4().hex[:12]}"
            
            # Create the legendary completion
            new_completion = WaypointCompletion(
                enrollment_id=enrollment.id,
                waypoint_id=waypoint.id,
                user_id=enrollment.user_id,
                completion_id=completion_id,
                completed_at=datetime.utcnow(),
                time_spent_minutes=completion_data.get("time_spent_minutes", 30),
                attempts_count=completion_data.get("attempts_count", 1),
                evidence_submitted=completion_data.get("evidence_submitted", {}),
                score_achieved=completion_data.get("score_achieved", 100.0),
                max_possible_score=completion_data.get("max_possible_score", 100.0),
                score_percentage=completion_data.get("score_percentage", 100.0),
                experience_points_earned=waypoint.experience_points,
                difficulty_rating=completion_data.get("difficulty_rating", 3.0),
                satisfaction_rating=completion_data.get("satisfaction_rating", 5.0),
                legendary_moment=completion_data.get("legendary_moment", "Completed with legendary code bro style!"),
                fun_factor_rating=completion_data.get("fun_factor_rating", 5.0),
                code_bro_style="Completed with legendary code bro style and 49 minutes of marathon power! 🎸"
            )
            
            self.db.add(new_completion)
            
            # Update enrollment progress
            enrollment.waypoints_completed += 1
            enrollment.completion_percentage = (enrollment.waypoints_completed / enrollment.total_waypoints) * 100
            enrollment.experience_points_earned += waypoint.experience_points
            enrollment.last_activity_at = datetime.utcnow()
            
            # Update legendary moments
            if completion_data.get("legendary_moment"):
                if not enrollment.legendary_moments:
                    enrollment.legendary_moments = []
                enrollment.legendary_moments.append({
                    "waypoint": waypoint.name,
                    "moment": completion_data.get("legendary_moment"),
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Check if path is completed
            if enrollment.waypoints_completed >= enrollment.total_waypoints:
                enrollment.status = "completed"
                enrollment.completion_status = "completed"
                enrollment.completed_at = datetime.utcnow()
                
                # Update path completion count
                path = self.db.query(Path).filter(Path.id == enrollment.path_id).first()
                if path:
                    path.total_completions += 1
            
            self.db.commit()
            self.db.refresh(new_completion)
            
            logger.info(f"✅ Legendary completion recorded: {new_completion.completion_id}")
            
            return {
                "success": True,
                "completion": self._completion_to_dict(new_completion),
                "enrollment_progress": enrollment.completion_percentage,
                "path_completed": enrollment.status == "completed",
                "legendary_joke": "Why was this completion legendary? Because it was done with RICKROLL187's 49-minute marathon mastery! ✅🎸",
                "🏆": "3+ HOUR 49 MINUTE MARATHON CHAMPION COMPLETION! 🏆"
            }
            
        except Exception as e:
            logger.error(f"💥 Completion error: {e}")
            self.db.rollback()
            return {
                "success": False,
                "error": f"Completion failed: {str(e)}"
            }
    
    def get_legendary_path_analytics(self, path_id: str) -> Dict[str, Any]:
        """
        Get comprehensive analytics for a legendary path!
        More insightful than Swiss intelligence with code bro metrics! 📊🧠
        """
        try:
            logger.info(f"📊 Generating legendary analytics for path: {path_id}")
            
            path = self.db.query(Path).filter(Path.path_id == path_id).first()
            if not path:
                return {"success": False, "error": "Path not found"}
            
            # Get enrollment statistics
            enrollments = self.db.query(PathEnrollment).filter(
                PathEnrollment.path_id == path.id
            ).all()
            
            completed_enrollments = [e for e in enrollments if e.status == "completed"]
            active_enrollments = [e for e in enrollments if e.status == "active"]
            
            # Calculate metrics
            total_enrollments = len(enrollments)
            total_completions = len(completed_enrollments)
            completion_rate = (total_completions / total_enrollments * 100) if total_enrollments > 0 else 0
            
            # Average completion time
            avg_completion_time = 0
            if completed_enrollments:
                total_time = sum([
                    (e.completed_at - e.enrolled_at).total_seconds() / 3600 
                    for e in completed_enrollments if e.completed_at and e.enrolled_at
                ])
                avg_completion_time = total_time / len(completed_enrollments)
            
            # Get reviews
            reviews = self.db.query(PathReview).filter(PathReview.path_id == path.id).all()
            avg_rating = sum([r.overall_rating for r in reviews]) / len(reviews) if reviews else 0
            
            analytics = {
                "path_info": {
                    "name": path.name,
                    "path_id": path.path_id,
                    "type": path.path_type,
                    "difficulty": path.difficulty,
                    "created_at": path.created_at.isoformat() if path.created_at else None
                },
                "enrollment_metrics": {
                    "total_enrollments": total_enrollments,
                    "total_completions": total_completions,
                    "completion_rate_percentage": round(completion_rate, 2),
                    "active_enrollments": len(active_enrollments),
                    "average_completion_time_hours": round(avg_completion_time, 2)
                },
                "performance_metrics": {
                    "average_rating": round(avg_rating, 2),
                    "total_reviews": len(reviews),
                    "total_waypoints": path.total_waypoints,
                    "experience_points_offered": path.experience_points_reward
                },
                "legendary_metrics": {
                    "code_bro_approved": path.code_bro_approved,
                    "rickroll187_rating": path.rickroll187_rating,
                    "legendary_factor": path.legendary_factor,
                    "fun_factor": path.fun_factor,
                    "marathon_build_time": "3+ HOURS AND 49 MINUTES"
                },
                "engagement_data": {
                    "total_views": path.total_views,
                    "waypoint_completion_rate": 0,  # Calculate from completions
                    "user_satisfaction": round(avg_rating, 2)
                }
            }
            
            logger.info(f"✅ Legendary analytics generated for: {path.name}")
            
            return {
                "success": True,
                "analytics": analytics,
                "legendary_joke": "Why are these analytics legendary? Because they were generated with RICKROLL187's 49-minute marathon analytical mastery! 📊🎸",
                "🏆": "3+ HOUR 49 MINUTE MARATHON CHAMPION ANALYTICS! 🏆"
            }
            
        except Exception as e:
            logger.error(f"💥 Analytics error: {e}")
            return {
                "success": False,
                "error": f"Analytics generation failed: {str(e)}"
            }
    
    def get_random_service_joke(self) -> str:
        """Get a random legendary service joke! More hilarious than Swiss comedians! 😄🎭"""
        import random
        return random.choice(self.service_jokes)
    
    def _path_to_dict(self, path: Path) -> Dict[str, Any]:
        """Convert path object to dictionary"""
        return {
            "id": path.id,
            "path_id": path.path_id,
            "name": path.name,
            "description": path.description,
            "path_type": path.path_type,
            "difficulty": path.difficulty,
            "total_waypoints": path.total_waypoints,
            "experience_points_reward": path.experience_points_reward,
            "legendary_factor": path.legendary_factor,
            "created_at": path.created_at.isoformat() if path.created_at else None
        }
    
    def _waypoint_to_dict(self, waypoint: Waypoint) -> Dict[str, Any]:
        """Convert waypoint object to dictionary"""
        return {
            "id": waypoint.id,
            "waypoint_id": waypoint.waypoint_id,
            "name": waypoint.name,
            "description": waypoint.description,
            "waypoint_type": waypoint.waypoint_type,
            "sequence_order": waypoint.sequence_order,
            "experience_points": waypoint.experience_points,
            "legendary_tip": waypoint.legendary_tip,
            "created_at": waypoint.created_at.isoformat() if waypoint.created_at else None
        }
    
    def _enrollment_to_dict(self, enrollment: PathEnrollment) -> Dict[str, Any]:
        """Convert enrollment object to dictionary"""
        return {
            "id": enrollment.id,
            "enrollment_id": enrollment.enrollment_id,
            "path_id": enrollment.path_id,
            "user_id": enrollment.user_id,
            "completion_percentage": enrollment.completion_percentage,
            "waypoints_completed": enrollment.waypoints_completed,
            "status": enrollment.status,
            "enrolled_at": enrollment.enrolled_at.isoformat() if enrollment.enrolled_at else None
        }
    
    def _completion_to_dict(self, completion: WaypointCompletion) -> Dict[str, Any]:
        """Convert completion object to dictionary"""
        return {
            "id": completion.id,
            "completion_id": completion.completion_id,
            "waypoint_id": completion.waypoint_id,
            "user_id": completion.user_id,
            "score_percentage": completion.score_percentage,
            "experience_points_earned": completion.experience_points_earned,
            "legendary_moment": completion.legendary_moment,
            "completed_at": completion.completed_at.isoformat() if completion.completed_at else None
        }

# LEGENDARY SERVICE JOKES FOR MOTIVATION
LEGENDARY_SERVICE_JOKES = [
    "Why did the path service become legendary? It had business logic that rocks! 🛤️⚡",
    "What's the difference between our services and Swiss efficiency? Both are legendarily precise! 🏔️",
    "Why don't our services ever crash? Because code bros build them with 49 minutes of marathon power! 💪",
    "What do you call path services at 3+ hours 49 minutes? Business logic with legendary style! 🎸",
    "Why did the service layer go to comedy school? To perfect its interface timing! 🎭",
    "What's a code bro's favorite service? The one that serves legendary functionality! 🎸⚡",
    "Why did RICKROLL187's services become famous? Because they process data like rock stars! 🎸🛤️",
    "What do you call a service that tells jokes? A humor-as-a-service! 😄⚡",
    "Why did the business logic go to the gym? To get more functional! 💪",
    "What's the secret to legendary services? Swiss precision with code bro processing power! 🏔️🎸"
]

if __name__ == "__main__":
    print("🛤️⚡ N3EXTPATH PATH SERVICES LOADED! ⚡🛤️")
    print("🏆 3+ HOUR 49 MINUTE CODING MARATHON CHAMPION SERVICES! 🏆")
    print("🎸 CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    
    import random
    print(f"🎭 Random Service Joke: {random.choice(LEGENDARY_SERVICE_JOKES)}")
