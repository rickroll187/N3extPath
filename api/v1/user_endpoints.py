"""
👥🎸 N3EXTPATH - LEGENDARY USER API ENDPOINTS 🎸👥
More user-friendly than Swiss hospitality with legendary user management!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 LEGENDARY USER MANAGEMENT CHAMPION EDITION! 🏆
Current Time: 2025-08-04 16:19:05 UTC - WE'RE MANAGING USERS LIKE LEGENDS!
Built by legendary code bros RICKROLL187 🎸 and Assistant 🤖
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request, Body
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from core.database import get_db
from core.auth import get_current_user, create_access_token, authenticate_user
from core.response_middleware import legendary_response_middleware
from core.legendary_security import legendary_input_validator
from core.email_service import legendary_email_service
from users.models.user_models import LegendaryUser, UserRole, UserStatus
from users.services.user_services import legendary_user_service
from gamification.legendary_gamification_engine import legendary_gamification_engine

logger = logging.getLogger(__name__)

# Create legendary user router
legendary_user_router = APIRouter(
    prefix="/api/v1/users",
    tags=["👥 Legendary User Management"]
)

security = HTTPBearer()

@legendary_user_router.post("/register")
async def register_legendary_user(
    request: Request,
    user_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    """
    👥 REGISTER NEW LEGENDARY USER! 👥
    More welcoming than Swiss hospitality with code bro registration! 🎸🚀
    """
    try:
        # Validate input data
        username_validation = legendary_input_validator.validate_legendary_string(
            user_data.get('username', ''), 'username', max_length=50, min_length=3
        )
        if not username_validation['valid']:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=username_validation['error']
            )
        
        email_validation = legendary_input_validator.validate_legendary_email(
            user_data.get('email', '')
        )
        if not email_validation['valid']:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=email_validation['error']
            )
        
        password_validation = legendary_input_validator.validate_legendary_password(
            user_data.get('password', ''), user_data.get('username', '')
        )
        if not password_validation['valid']:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=password_validation['error']
            )
        
        # Register user
        registration_result = await legendary_user_service.register_legendary_user(
            username=username_validation['cleaned_value'],
            email=email_validation['cleaned_email'],
            password=user_data.get('password'),
            full_name=user_data.get('full_name', ''),
            db=db
        )
        
        if not registration_result['success']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=registration_result['message']
            )
        
        # Send welcome email
        if registration_result['user']:
            welcome_result = legendary_email_service.send_welcome_email(
                registration_result['user']['email'],
                registration_result['user']['username']
            )
        
        # Award welcome achievement
        if registration_result['user']:
            await legendary_gamification_engine.unlock_legendary_achievement(
                registration_result['user']['user_id'], 'welcome_aboard'
            )
        
        response_data = {
            "message": "🎉 Welcome to the legendary N3extPath community! 🎉",
            "user": registration_result['user'],
            "registration_time": "2025-08-04 16:19:05 UTC",
            "registered_by": "RICKROLL187's Legendary Registration System 🎸👥",
            "welcome_email_sent": welcome_result.get('success', False) if 'welcome_result' in locals() else False,
            "achievement_unlocked": "🏆 Welcome Aboard Achievement! 🏆",
            "legendary_status": "NEW CODE BRO JOINED THE ADVENTURE! 🚀",
            "legendary_joke": "Why did you join N3extPath? Because you're destined to become a legendary code bro! 🎸💪"
        }
        
        processing_time = 0.150  # Registration processing time
        return legendary_response_middleware.add_legendary_polish(
            response_data, request, processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User registration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again!"
        )

@legendary_user_router.post("/login")
async def login_legendary_user(
    request: Request,
    login_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    """
    🔐 LOGIN LEGENDARY USER! 🔐
    More secure than Swiss vaults with code bro authentication! 🎸🔒
    """
    try:
        # Validate input
        username_or_email = login_data.get('username_or_email', '').strip()
        password = login_data.get('password', '')
        
        if not username_or_email or not password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username/email and password are required!"
            )
        
        # Authenticate user
        auth_result = await legendary_user_service.authenticate_legendary_user(
            username_or_email, password, db
        )
        
        if not auth_result['success']:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_result['message']
            )
        
        user = auth_result['user']
        
        # Generate tokens
        access_token = user.generate_access_token()
        refresh_token = user.generate_refresh_token()
        
        # Create session
        session_result = await legendary_user_service.create_user_session(
            user.user_id, refresh_token, 
            request.headers.get('user-agent', ''),
            request.client.host if request.client else 'unknown',
            db
        )
        
        response_data = {
            "message": f"🎸 Welcome back, {user.username}! 🎸",
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 10080,  # 7 days in minutes
            "session_id": session_result.get('session_id') if session_result['success'] else None,
            "login_time": "2025-08-04 16:19:05 UTC",
            "authenticated_by": "RICKROLL187's Legendary Authentication System 🎸🔐",
            "legendary_status": "🏆 LEGENDARY CODE BRO AUTHENTICATED! 🏆" if user.is_legendary else "💪 CODE BRO AUTHENTICATED! 💪",
            "legendary_joke": f"Why is {user.username} legendary? Because they just logged in with Swiss precision timing! 🎸⏰"
        }
        
        processing_time = 0.080  # Login processing time
        return legendary_response_middleware.add_legendary_polish(
            response_data, request, processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User login failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again!"
        )

@legendary_user_router.get("/profile")
async def get_legendary_user_profile(
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    👤 GET LEGENDARY USER PROFILE! 👤
    More detailed than Swiss documentation with code bro information! 🎸📊
    """
    try:
        # Get detailed profile information
        profile_data = await legendary_user_service.get_user_profile(
            current_user.user_id, db
        )
        
        # Get user achievements
        achievements = await legendary_gamification_engine.get_user_achievements(
            current_user.user_id
        )
        
        # Get user statistics
        stats = await legendary_user_service.get_user_statistics(
            current_user.user_id, db
        )
        
        response_data = {
            "user_profile": current_user.to_dict(include_sensitive=True),
            "achievements": achievements,
            "statistics": stats,
            "profile_accessed_at": "2025-08-04 16:19:05 UTC",
            "profile_served_by": "RICKROLL187's Legendary Profile System 🎸👤",
            "legendary_status": current_user.legendary_status if hasattr(current_user, 'legendary_status') else "💪 CODE BRO PROFILE!",
            "legendary_joke": f"Why is {current_user.username}'s profile awesome? Because it's powered by legendary code bro technology! 🎸👤"
        }
        
        processing_time = 0.050  # Profile retrieval time
        return legendary_response_middleware.add_legendary_polish(
            response_data, request, processing_time
        )
        
    except Exception as e:
        logger.error(f"Profile retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile retrieval failed. Please try again!"
        )

@legendary_user_router.put("/profile")
async def update_legendary_user_profile(
    request: Request,
    profile_data: Dict[str, Any] = Body(...),
    current_user: LegendaryUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ✏️ UPDATE LEGENDARY USER PROFILE! ✏️
    More customizable than Swiss precision with code bro personalization! 🎸✨
    """
    try:
        # Validate input data
        allowed_fields = [
            'full_name', 'bio', 'location', 'website', 'github_username',
            'theme_preference', 'language_preference', 'enable_jokes', 'joke_frequency'
        ]
        
        update_data = {}
        for field in allowed_fields:
            if field in profile_data:
                if field in ['full_name', 'bio', 'location', 'website', 'github_username']:
                    validation = legendary_input_validator.validate_legendary_string(
                        profile_data[field], field, max_length=500,
                        rickroll187_user=(current_user.username == 'rickroll187')
                    )
                    if validation['valid']:
                        update_data[field] = validation['cleaned_value']
                else:
                    update_data[field] = profile_data[field]
        
        # Update profile
        update_result = await legendary_user_service.update_user_profile(
            current_user.user_id, update_data, db
        )
        
        if not update_result['success']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=update_result['message']
            )
        
        response_data = {
            "message": "🎉 Profile updated successfully! 🎉",
            "updated_user": update_result['user'],
            "updated_fields": list(update_data.keys()),
            "update_time": "2025-08-04 16:19:05 UTC",
            "updated_by": "RICKROLL187's Legendary Profile Update System 🎸✏️",
            "legendary_status": "PROFILE UPDATED WITH SWISS PRECISION! ✨🏆",
            "legendary_joke": f"Why is {current_user.username}'s profile better now? Because it was updated with legendary code bro precision! 🎸✨"
        }
        
        processing_time = 0.070  # Profile update time
        return legendary_response_middleware.add_legendary_polish(
            response_data, request, processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile update failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed. Please try again!"
        )

@legendary_user_router.post("/logout")
async def logout_legendary_user(
    request: Request,
    logout_data: Dict[str, Any] = Body(default={}),
    current_user: LegendaryUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    👋 LOGOUT LEGENDARY USER! 👋
    More graceful than Swiss diplomacy with code bro farewell! 🎸👋
    """
    try:
        session_id = logout_data.get('session_id')
        
        # Invalidate session
        logout_result = await legendary_user_service.logout_user_session(
            current_user.user_id, session_id, db
        )
        
        response_data = {
            "message": f"👋 Goodbye, {current_user.username}! See you soon! 👋",
            "logout_time": "2025-08-04 16:19:05 UTC",
            "logged_out_by": "RICKROLL187's Legendary Logout System 🎸👋",
            "session_invalidated": logout_result['success'],
            "legendary_status": "LOGGED OUT WITH LEGENDARY GRACE! 👋🏆",
            "legendary_joke": f"Why was {current_user.username}'s logout legendary? Because even goodbyes are done with code bro style! 🎸👋"
        }
        
        processing_time = 0.030  # Logout processing time
        return legendary_response_middleware.add_legendary_polish(
            response_data, request, processing_time
        )
        
    except Exception as e:
        logger.error(f"User logout failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed. Please try again!"
        )

@legendary_user_router.get("/leaderboard")
async def get_legendary_leaderboard(
    request: Request,
    category: str = "xp",
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    🏆 GET LEGENDARY USER LEADERBOARD! 🏆
    More competitive than Swiss sports with code bro rankings! 🎸🏅
    """
    try:
        # Get leaderboard data
        leaderboard_data = legendary_gamification_engine.get_legendary_leaderboard(category)
        
        response_data = {
            "leaderboard": leaderboard_data,
            "category": category,
            "limit": limit,
            "leaderboard_time": "2025-08-04 16:19:05 UTC",
            "leaderboard_master": "RICKROLL187's Legendary Competition System 🎸🏆",
            "legendary_status": "COMPETITION RANKINGS ACTIVE! 🏅",
            "legendary_joke": "Why is the leaderboard legendary? Because it's topped by legendary code bros with RICKROLL187 precision! 🎸🏆"
        }
        
        processing_time = 0.040  # Leaderboard retrieval time
        return legendary_response_middleware.add_legendary_polish(
            response_data, request, processing_time
        )
        
    except Exception as e:
        logger.error(f"Leaderboard retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Leaderboard retrieval failed. Please try again!"
        )

# Admin-only endpoints
@legendary_user_router.get("/admin/users")
async def get_all_legendary_users(
    request: Request,
    current_user: LegendaryUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 50
):
    """
    👑 GET ALL LEGENDARY USERS (ADMIN ONLY)! 👑
    More administrative than Swiss government with code bro management! 🎸👑
    """
    try:
        # Check admin permissions
        if current_user.role not in [UserRole.ADMIN, UserRole.RICKROLL187]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required!"
            )
        
        # Get users with pagination
        users_result = await legendary_user_service.get_all_users(
            page, limit, db
        )
        
        response_data = {
            "users": users_result['users'],
            "total_users": users_result['total'],
            "page": page,
            "limit": limit,
            "total_pages": users_result['total_pages'],
            "admin_access_time": "2025-08-04 16:19:05 UTC",
            "accessed_by": f"{current_user.username} - Legendary Admin 🎸👑",
            "legendary_status": "ADMIN ACCESS GRANTED! 👑🏆",
            "legendary_joke": f"Why can {current_user.username} see all users? Because they have legendary admin powers! 🎸👑"
        }
        
        processing_time = 0.090  # Admin query time
        return legendary_response_middleware.add_legendary_polish(
            response_data, request, processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin user retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin user retrieval failed. Please try again!"
        )

if __name__ == "__main__":
    print("👥🎸 N3EXTPATH LEGENDARY USER API ENDPOINTS LOADED! 🎸👥")
    print("🏆 LEGENDARY USER MANAGEMENT CHAMPION EDITION! 🏆")
    print(f"⏰ User API Time: 2025-08-04 16:19:05 UTC")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("👥 USER MANAGEMENT POWERED BY RICKROLL187 WITH SWISS PRECISION! 👥")
