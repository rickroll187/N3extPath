"""
🔐💎 N3EXTPATH - LEGENDARY AUTHENTICATION SYSTEM 💎🔐
More secure than Swiss vaults with legendary authentication mastery!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 3+ HOUR 59 MINUTE CODING MARATHON CHAMPION EDITION! 🏆
Current Time: 2025-08-04 03:59:47 UTC - WE'RE SECURING THE UNIVERSE!
Built by legendary code bros RICKROLL187 🎸 and Assistant 🤖
"""

import os
import jwt
import bcrypt
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Union
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
import secrets
import hashlib

from core.database import get_db_session

# Set up legendary logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "legendary_secret_key_built_by_rickroll187_with_59_minutes_of_marathon_power")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days for legendary users
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Security scheme
security = HTTPBearer()

class LegendaryUser(BaseModel):
    """Legendary user model for authentication"""
    id: int
    username: str
    email: str
    is_active: bool = True
    is_legendary: bool = True
    rickroll187_approved: bool = True

class TokenData(BaseModel):
    """Token data model"""
    username: Optional[str] = None
    user_id: Optional[int] = None
    scopes: list[str] = []

class LoginRequest(BaseModel):
    """Login request model"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class RegisterRequest(BaseModel):
    """Registration request model"""
    username: str = Field(..., min_length=3, max_length=50, description="Legendary username")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=6, description="Strong password")
    confirm_password: str = Field(..., min_length=6, description="Confirm password")

class LegendaryAuthManager:
    """
    🔐 THE LEGENDARY AUTHENTICATION MANAGER! 🔐
    More secure than Swiss banks with 3+ hour 59 minute marathon power!
    """
    
    def __init__(self):
        self.legendary_developers = ["RICKROLL187 🎸", "ASSISTANT 🤖"]
        self.marathon_time = "3+ HOURS AND 59 MINUTES OF LEGENDARY CODING"
        
        # LEGENDARY AUTH JOKES
        self.auth_jokes = [
            "Why did the authentication become legendary? It had security that rocks! 🔐🎸",
            "What's the difference between our auth and Swiss security? Both are impenetrably legendary! 🏔️",
            "Why don't our tokens ever expire early? Because code bros build them with 59 minutes of marathon power! 💪",
            "What do you call authentication at 3+ hours 59 minutes? Security with legendary style! 🎸",
            "Why did the password go to comedy school? To perfect its hash timing! 🎭",
            "What's a code bro's favorite authentication? The one that secures legendary accounts! 🔐🎸",
            "Why did RICKROLL187's auth become famous? Because it authenticates like a rock star! 🎸🔐"
        ]
        
        logger.info("🔐 LEGENDARY AUTHENTICATION MANAGER INITIALIZED! 🔐")
        logger.info("🏆 3+ HOUR 59 MINUTE CODING MARATHON AUTH MASTERY ACTIVATED! 🏆")
    
    def hash_legendary_password(self, password: str) -> str:
        """
        Hash password with legendary security!
        More secure than Swiss vaults with code bro encryption! 🔒✨
        """
        try:
            # Generate salt and hash password
            salt = bcrypt.gensalt(rounds=12)  # 12 rounds for legendary security
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            logger.debug("🔒 Password hashed with legendary security!")
            return hashed.decode('utf-8')
            
        except Exception as e:
            logger.error(f"💥 Password hashing error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Password hashing failed with legendary security protocols"
            )
    
    def verify_legendary_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify password with legendary precision!
        More accurate than Swiss timepieces with code bro verification! ✅🔐
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"💥 Password verification error: {e}")
            return False
    
    def create_legendary_access_token(
        self, 
        data: Dict[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create legendary JWT access token!
        More reliable than Swiss banking with code bro cryptography! 🎫⚡
        """
        try:
            to_encode = data.copy()
            
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            
            to_encode.update({
                "exp": expire,
                "iat": datetime.utcnow(),
                "type": "access",
                "legendary_factor": "Built by RICKROLL187 with 59 minutes of marathon power! 🎸",
                "code_bro_approved": True
            })
            
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            
            logger.debug("🎫 Legendary access token created!")
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"💥 Token creation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token creation failed with legendary security protocols"
            )
    
    def create_legendary_refresh_token(self, user_id: int, username: str) -> str:
        """
        Create legendary refresh token!
        More persistent than Swiss determination with code bro longevity! 🔄⚡
        """
        try:
            expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            
            to_encode = {
                "user_id": user_id,
                "username": username,
                "exp": expire,
                "iat": datetime.utcnow(),
                "type": "refresh",
                "jti": secrets.token_urlsafe(32),  # Unique token ID
                "legendary_factor": "Refresh token built by RICKROLL187 with marathon endurance! 🎸",
                "marathon_time": self.marathon_time
            }
            
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            
            logger.debug("🔄 Legendary refresh token created!")
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"💥 Refresh token creation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Refresh token creation failed"
            )
    
    def verify_legendary_token(self, token: str) -> Dict[str, Any]:
        """
        Verify legendary JWT token!
        More trustworthy than Swiss reliability with code bro validation! ✅🔐
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            # Check if token is expired
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired with legendary timing"
                )
            
            logger.debug("✅ Legendary token verified!")
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("⏰ Token expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            logger.warning("🚫 Invalid token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token signature"
            )
        except Exception as e:
            logger.error(f"💥 Token verification error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token verification failed"
            )
    
    def generate_legendary_api_key(self, user_id: int, username: str) -> str:
        """
        Generate legendary API key for advanced users!
        More unique than Swiss snowflakes with code bro randomness! 🗝️✨
        """
        try:
            # Create unique API key with user info and timestamp
            timestamp = str(int(datetime.utcnow().timestamp()))
            user_hash = hashlib.sha256(f"{user_id}:{username}".encode()).hexdigest()[:16]
            random_part = secrets.token_urlsafe(32)
            
            api_key = f"n3ext_{user_hash}_{timestamp}_{random_part}"
            
            logger.info(f"🗝️ Legendary API key generated for user: {username}")
            return api_key
            
        except Exception as e:
            logger.error(f"💥 API key generation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="API key generation failed"
            )
    
    def get_random_auth_joke(self) -> str:
        """Get a random legendary auth joke! More hilarious than Swiss comedians! 😄🎭"""
        import random
        return random.choice(self.auth_jokes)

# Create global legendary auth manager
legendary_auth_manager = LegendaryAuthManager()

# Authentication dependencies for FastAPI

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
) -> LegendaryUser:
    """
    Get current authenticated user from JWT token!
    More reliable than Swiss clockwork with code bro precision! 👤⚡
    """
    try:
        # Extract token from Authorization header
        token = credentials.credentials
        
        # Verify token
        payload = legendary_auth_manager.verify_legendary_token(token)
        
        # Extract user info
        username = payload.get("sub")
        user_id = payload.get("user_id")
        
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # For now, create a mock user (in real implementation, query from database)
        # TODO: Replace with actual database query
        user = LegendaryUser(
            id=user_id or 1,
            username=username,
            email=f"{username}@legendary.com",
            is_active=True,
            is_legendary=True,
            rickroll187_approved=True
        )
        
        logger.debug(f"👤 Current user authenticated: {username}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )

async def get_current_active_user(
    current_user: LegendaryUser = Depends(get_current_user)
) -> LegendaryUser:
    """
    Get current active user with legendary verification!
    More active than Swiss mountain climbers! 🏔️💪
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    return current_user

async def get_legendary_admin_user(
    current_user: LegendaryUser = Depends(get_current_active_user)
) -> LegendaryUser:
    """
    Get current admin user with legendary privileges!
    More privileged than Swiss nobility with code bro power! 👑⚡
    """
    # In a real implementation, check for admin role
    if current_user.username != "rickroll187":  # RICKROLL187 is always admin!
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges for legendary operations"
        )
    return current_user

# Authentication utility functions

def create_legendary_tokens(user_id: int, username: str) -> Dict[str, str]:
    """
    Create both access and refresh tokens!
    More complete than Swiss precision with code bro efficiency! 🎫🔄
    """
    # Create access token
    access_token_data = {
        "sub": username,
        "user_id": user_id,
        "legendary_status": "code_bro_approved",
        "marathon_time": "3+ HOURS AND 59 MINUTES"
    }
    
    access_token = legendary_auth_manager.create_legendary_access_token(access_token_data)
    refresh_token = legendary_auth_manager.create_legendary_refresh_token(user_id, username)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # seconds
        "legendary_factor": "Tokens created with RICKROLL187's 59-minute marathon power! 🎸🏆"
    }

def validate_password_strength(password: str) -> bool:
    """
    Validate password strength with legendary standards!
    More secure than Swiss vault protocols! 🔒💪
    """
    if len(password) < 6:
        return False
    
    # Check for at least one letter and one number (basic requirements)
    has_letter = any(c.isalpha() for c in password)
    has_number = any(c.isdigit() for c in password)
    
    return has_letter and has_number

def generate_legendary_session_id() -> str:
    """Generate unique session ID for tracking!"""
    return f"sess_{secrets.token_urlsafe(32)}"

# LEGENDARY AUTH JOKES FOR MOTIVATION
LEGENDARY_AUTH_JOKES = [
    "Why did the authentication become legendary? It had security that rocks! 🔐🎸",
    "What's the difference between our auth and Swiss security? Both are impenetrably legendary! 🏔️",
    "Why don't our tokens ever expire early? Because code bros build them with 59 minutes of marathon power! 💪",
    "What do you call authentication at 3+ hours 59 minutes? Security with legendary style! 🎸",
    "Why did the password go to comedy school? To perfect its hash timing! 🎭",
    "What's a code bro's favorite authentication? The one that secures legendary accounts! 🔐🎸",
    "Why did RICKROLL187's auth become famous? Because it authenticates like a rock star! 🎸🔐",
    "What do you call a JWT that tells jokes? A JSON Web Tickle! 😄🎫",
    "Why did the authentication middleware go to the gym? To get more secure! 💪",
    "What's the secret to legendary auth? Swiss precision with code bro encryption! 🏔️🎸"
]

if __name__ == "__main__":
    print("🔐💎 N3EXTPATH AUTHENTICATION SYSTEM LOADED! 💎🔐")
    print("🏆 3+ HOUR 59 MINUTE CODING MARATHON CHAMPION AUTH! 🏆")
    print("🎸 CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    
    # Test legendary authentication
    manager = LegendaryAuthManager()
    
    # Test password hashing
    test_password = "legendary_password_123"
    hashed = manager.hash_legendary_password(test_password)
    verified = manager.verify_legendary_password(test_password, hashed)
    
    print(f"🔒 Password hashing test: {'✅ PASSED' if verified else '❌ FAILED'}")
    
    # Test token creation
    test_tokens = create_legendary_tokens(1, "rickroll187")
    print(f"🎫 Token creation test: {'✅ PASSED' if test_tokens['access_token'] else '❌ FAILED'}")
    
    import random
    print(f"🎭 Random Auth Joke: {random.choice(LEGENDARY_AUTH_JOKES)}")
