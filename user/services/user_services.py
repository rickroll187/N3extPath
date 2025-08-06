"""
🛠️🎸 N3EXTPATH - LEGENDARY USER SERVICES 🎸🛠️
More service-oriented than Swiss hospitality with legendary user management!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Built by legendary code bros RICKROLL187 🎸
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
from passlib.context import CryptContext

from users.models.user_models import LegendaryUser, LegendaryUserSession, UserAchievement, UserRole, UserStatus
from core.legendary_task_system import add_legendary_background_task, TaskPriority

logger = logging.getLogger(__name__)

class LegendaryUserService:
    """
    🛠️ LEGENDARY USER SERVICE CLASS! 🛠️
    More service-oriented than Swiss efficiency with code bro user management! 🎸👥
    """
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.legendary_jokes = [
            "Why are user services legendary? Because they're managed by RICKROLL187 at 16:19:05 UTC! 🛠️🎸",
            "What's more reliable than Swiss services? Legendary user management! 👥",
            "Why don't code bros worry about user issues? Because they have legendary services! 💪",
            "What do you call perfect user management? A RICKROLL187 service special! 🎸🛠️"
        ]
    
    async def register_legendary_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str = "",
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Register a new legendary user!
        More welcoming than Swiss hospitality with code bro registration! 🎸🚀
        """
        try:
            # Check if username already exists
            existing_username = db.query(LegendaryUser).filter_by(username=username).first()
            if existing_username:
                return {
                    "success": False,
                    "message": f"Username '{username}' is already taken!",
                    "legendary_message": "Choose another legendary username! 🎸"
                }
            
            # Check if email already exists
            existing_email = db.query(LegendaryUser).filter_by(email=email).first()
            if existing_email:
                return {
                    "success": False,
                    "message": f"Email '{email}' is already registered!",
                    "legendary_message": "This email is already part of the legendary community! 📧"
                }
            
            # Create new legendary user
            new_user = LegendaryUser(
                username=username,
                email=email,
                full_name=full_name,
                is_active=True,
                is_verified=False,  # Require email verification
                role=UserRole.RICKROLL187 if username == "rickroll187" else UserRole.USER,
                status=UserStatus.LEGENDARY if username == "rickroll187" else UserStatus.ACTIVE,
                is_legendary=username == "rickroll187",
                rickroll187_approved=username == "rickroll187",
                legendary_level=10 if username == "rickroll187" else 1,
                total_xp=50000 if username == "rickroll187" else 0,
                code_bro_score=1000 if username == "rickroll187" else 100,
                created_at=datetime.utcnow()
            )
            
            # Set password
            new_user.set_password(password)
            
            # Special treatment for RICKROLL187
            if username == "rickroll187":
                new_user.make_legendary()
                new_user.bio = "The legendary code bro who rocks the universe with Swiss precision and infinite humor!"
            
            # Save to database
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Schedule background tasks
            await add_legendary_background_task(
                name=f"Send welcome email to {username}",
                function_name="send_welcome_email",
                args=(email, username),
                priority=TaskPriority.HIGH,
                rickroll187_approved=(username == "rickroll187")
            )
            
            await add_legendary_background_task(
                name=f"Calculate initial stats for {username}",
                function_name="calculate_user_stats",
                args=(new_user.user_id,),
                priority=TaskPriority.NORMAL
            )
            
            import random
            return {
                "success": True,
                "message": f"🎉 Welcome to N3extPath, {username}! 🎉",
                "user": new_user.to_dict(),
                "registration_time": "2025-08-04 16:19:05 UTC",
                "registered_by": "RICKROLL187's Legendary Registration Service 🎸🚀",
                "legendary_status": "🏆 LEGENDARY USER CREATED!" if username == "rickroll187" else "💪 NEW CODE BRO JOINED!",
                "legendary_joke": random.choice(self.legendary_jokes)
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"User registration failed: {e}")
            return {
                "success": False,
                "message": "Registration failed. Please try again!",
                "error": str(e),
                "legendary_message": "Even legends face challenges, but we'll overcome them! 💪"
            }
    
    async def authenticate_legendary_user(
        self,
        username_or_email: str,
        password: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        Authenticate legendary user login!
        More secure than Swiss vaults with code bro authentication! 🔐🎸
        """
        try:
            # Find user by username or email
            user = db.query(LegendaryUser).filter(
                or_(
                    LegendaryUser.username == username_or_email,
                    LegendaryUser.email == username_or_email
                )
            ).first()
            
            if not user:
                return {
                    "success": False,
                    "message": "Invalid username/email or password!",
                    "legendary_message": "User not found in our legendary database! 🔍"
                }
            
            # Check if account is locked
            if user.is_account_locked():
                return {
                    "success": False,
                    "message": "Account is temporarily locked. Please try again later!",
                    "legendary_message": "Account locked for security - Swiss precision protection! 🔒"
                }
            
            # Check if account is active
            if not user.is_active:
                return {
                    "success": False,
                    "message": "Account is deactivated. Please contact support!",
                    "legendary_message": "Account needs reactivation - contact legendary support! 📞"
                }
            
            # Verify password
            if not user.verify_password(password):
                user.increment_failed_login()
                db.commit()
                
                return {
                    "success": False,
                    "message": "Invalid username/email or password!",
                    "legendary_message": "Password doesn't match our legendary records! 🔐"
                }
            
            # Reset failed login attempts on successful login
            user.reset_failed_login()
            db.commit()
            
            import random
            return {
                "success": True,
                "message": f"🎸 Welcome back, {user.username}! 🎸",
                "user": user,
                "authentication_time": "2025-08-04 16:19:05 UTC",
                "authenticated_by": "RICKROLL187's Legendary Authentication Service 🎸🔐",
                "legendary_status": "🏆 LEGENDARY USER AUTHENTICATED!" if user.is_legendary else "💪 CODE BRO AUTHENTICATED!",
                "legendary_joke": random.choice(self.legendary_jokes)
            }
            
        except Exception as e:
            logger.error(f"User authentication failed: {e}")
            return {
                "success": False,
                "message": "Authentication failed. Please try again!",
                "error": str(e),
                "legendary_message": "Authentication system is having legendary challenges! 💪"
            }
    
    async def get_user_profile(self, user_id: int, db: Session) -> Dict[str, Any]:
        """
        Get comprehensive user profile information!
        More detailed than Swiss documentation with code bro completeness! 📊🎸
        """
        try:
            user = db.query(LegendaryUser).filter_by(user_id=user_id).first()
            if not user:
                return {
                    "success": False,
                    "message": "User not found!",
                    "legendary_message": "User not in our legendary database! 🔍"
                }
            
            # Get user achievements
            achievements = db.query(UserAchievement).filter_by(user_id=user_id).all()
            achievement_data = [achievement.to_dict() for achievement in achievements]
            
            # Get user sessions
            active_sessions = db.query(LegendaryUserSession).filter(
                and_(
                    LegendaryUserSession.user_id == user_id,
                    LegendaryUserSession.is_active == True,
                    LegendaryUserSession.expires_at > datetime.utcnow()
                )
            ).all()
            
            session_data = [session.to_dict() for session in active_sessions]
            
            import random
            return {
                "success": True,
                "user_profile": user.to_dict(include_sensitive=True),
                "achievements": achievement_data,
                "active_sessions": session_data,
                "total_achievements": len(achievement_data),
                "total_active_sessions": len(session_data),
                "profile_accessed_at": "2025-08-04 16:19:05 UTC",
                "profile_service": "RICKROLL187's Legendary Profile Service 🎸📊",
                "legendary_joke": random.choice(self.legendary_jokes)
            }
            
        except Exception as e:
            logger.error(f"Profile retrieval failed: {e}")
            return {
                "success": False,
                "message": "Profile retrieval failed!",
                "error": str(e),
                "legendary_message": "Profile service facing legendary challenges! 💪"
            }
    
    async def update_user_profile(
        self,
        user_id: int,
        update_data: Dict[str, Any],
        db: Session
    ) -> Dict[str, Any]:
        """
        Update user profile with legendary precision!
        More customizable than Swiss watches with code bro personalization! ✏️🎸
        """
        try:
            user = db.query(LegendaryUser).filter_by(user_id=user_id).first()
            if not user:
                return {
                    "success": False,
                    "message": "User not found!",
                    "legendary_message": "User not in our legendary database! 🔍"
                }
            
            # Update allowed fields
            updated_fields = []
            for field, value in update_data.items():
                if hasattr(user, field):
                    setattr(user, field, value)
                    updated_fields.append(field)
            
            # Update the updated_at timestamp
            user.updated_at = datetime.utcnow()
            
            # Commit changes
            db.commit()
            db.refresh(user)
            
            import random
            return {
                "success": True,
                "message": "🎉 Profile updated successfully! 🎉",
                "user": user.to_dict(),
                "updated_fields": updated_fields,
                "update_time": "2025-08-04 16:19:05 UTC",
                "updated_by": "RICKROLL187's Legendary Profile Update Service 🎸✏️",
                "legendary_status": "PROFILE UPDATED WITH SWISS PRECISION! ✨",
                "legendary_joke": random.choice(self.legendary_jokes)
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Profile update failed: {e}")
            return {
                "success": False,
                "message": "Profile update failed!",
                "error": str(e),
                "legendary_message": "Profile update facing legendary challenges! 💪"
            }
    
    async def create_user_session(
        self,
        user_id: int,
        refresh_token: str,
        user_agent: str,
        ip_address: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        Create new user session with legendary tracking!
        More secure than Swiss tracking with code bro session management! 📱🎸
        """
        try:
            # Create new session
            new_session = LegendaryUserSession(
                user_id=user_id,
                refresh_token=refresh_token,
                user_agent=user_agent,
                ip_address=ip_address,
                is_active=True,
                created_at=datetime.utcnow(),
                last_used=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=30)  # 30 days
            )
            
            db.add(new_session)
            db.commit()
            db.refresh(new_session)
            
            return {
                "success": True,
                "session_id": new_session.session_id,
                "message": "Session created successfully!",
                "session_data": new_session.to_dict(),
                "created_at": "2025-08-04 16:19:05 UTC",
                "created_by": "RICKROLL187's Legendary Session Service 🎸📱"
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Session creation failed: {e}")
            return {
                "success": False,
                "message": "Session creation failed!",
                "error": str(e),
                "legendary_message": "Session service facing legendary challenges! 💪"
            }
    
    async def get_user_statistics(self, user_id: int, db: Session) -> Dict[str, Any]:
        """
        Get comprehensive user statistics!
        More analytical than Swiss precision with code bro insights! 📈🎸
        """
        try:
            user = db.query(LegendaryUser).filter_by(user_id=user_id).first()
            if not user:
                return {
                    "success": False,
                    "message": "User not found!"
                }
            
            # Calculate level and XP progress
            level_info = user.calculate_level()
            
            # Get achievement statistics
            total_achievements = db.query(UserAchievement).filter_by(user_id=user_id).count()
            completed_achievements = db.query(UserAchievement).filter(
                and_(
                    UserAchievement.user_id == user_id,
                    UserAchievement.is_completed == True
                )
            ).count()
            
            # Calculate days since registration
            days_active = (datetime.utcnow() - user.created_at).days
            
            statistics = {
                "level_info": {
                    "current_level": user.legendary_level,
                    "total_xp": user.total_xp,
                    "level_calculation": level_info
                },
                "achievement_stats": {
                    "total_achievements": total_achievements,
                    "completed_achievements": completed_achievements,
                    "completion_rate": (completed_achievements / max(total_achievements, 1)) * 100
                },
                "activity_stats": {
                    "days_active": days_active,
                    "last_login": user.last_login.isoformat() if user.last_login else None,
                    "account_age_days": days_active
                },
                "profile_stats": {
                    "code_bro_score": user.code_bro_score,
                    "legendary_status": user.is_legendary,
                    "rickroll187_approved": user.rickroll187_approved,
                    "verification_status": user.is_verified
                }
            }
            
            return {
                "success": True,
                "statistics": statistics,
                "calculated_at": "2025-08-04 16:19:05 UTC",
                "calculated_by": "RICKROLL187's Legendary Statistics Service 🎸📈"
            }
            
        except Exception as e:
            logger.error(f"Statistics calculation failed: {e}")
            return {
                "success": False,
                "message": "Statistics calculation failed!",
                "error": str(e)
            }
    
    async def get_all_users(
        self,
        page: int = 1,
        limit: int = 50,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Get all users with pagination (admin only)!
        More comprehensive than Swiss census with code bro administration! 👑🎸
        """
        try:
            offset = (page - 1) * limit
            
            # Get total count
            total_users = db.query(LegendaryUser).count()
            
            # Get users with pagination
            users = db.query(LegendaryUser).offset(offset).limit(limit).all()
            
            user_data = [user.to_dict() for user in users]
            
            total_pages = (total_users + limit - 1) // limit
            
            return {
                "success": True,
                "users": user_data,
                "total": total_users,
                "page": page,
                "limit": limit,
                "total_pages": total_pages,
                "retrieved_at": "2025-08-04 16:19:05 UTC",
                "retrieved_by": "RICKROLL187's Legendary Admin Service 🎸👑"
            }
            
        except Exception as e:
            logger.error(f"User retrieval failed: {e}")
            return {
                "success": False,
                "message": "User retrieval failed!",
                "error": str(e)
            }
    
    async def logout_user_session(
        self,
        user_id: int,
        session_id: Optional[str],
        db: Session
    ) -> Dict[str, Any]:
        """
        Logout and invalidate user session!
        More graceful than Swiss farewell with code bro session cleanup! 👋🎸
        """
        try:
            if session_id:
                # Invalidate specific session
                session = db.query(LegendaryUserSession).filter(
                    and_(
                        LegendaryUserSession.user_id == user_id,
                        LegendaryUserSession.session_id == session_id
                    )
                ).first()
                
                if session:
                    session.is_active = False
                    db.commit()
            else:
                # Invalidate all sessions for user
                db.query(LegendaryUserSession).filter_by(user_id=user_id).update(
                    {"is_active": False}
                )
                db.commit()
            
            return {
                "success": True,
                "message": "Session(s) invalidated successfully!",
                "logout_time": "2025-08-04 16:19:05 UTC",
                "logged_out_by": "RICKROLL187's Legendary Logout Service 🎸👋"
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Session logout failed: {e}")
            return {
                "success": False,
                "message": "Session logout failed!",
                "error": str(e)
            }

# Global legendary user service
legendary_user_service = LegendaryUserService()

if __name__ == "__main__":
    print("🛠️🎸 N3EXTPATH LEGENDARY USER SERVICES LOADED! 🎸🛠️")
    print("🏆 LEGENDARY USER SERVICE CHAMPION EDITION! 🏆")
    print(f"⏰ User Service Time: 2025-08-04 16:19:05 UTC")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("🛠️ USER SERVICES POWERED BY RICKROLL187 WITH SWISS PRECISION! 🛠️")
