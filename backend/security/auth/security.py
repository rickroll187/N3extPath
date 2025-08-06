# File: backend/auth/security.py
"""
🔐🎸 N3EXTPATH - LEGENDARY AUTHENTICATION SECURITY SYSTEM 🎸🔐
Professional JWT authentication with legendary user detection
Built: 2025-08-05 22:15:56 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Union, List
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
import asyncio
from functools import wraps

# Database and configuration
from config.settings import settings
from database.connection import legendary_db_manager, get_db_session
from sqlalchemy import text
from sqlalchemy.orm import Session

# Configure logging
logger = logging.getLogger(__name__)

# =====================================
# 🎸 LEGENDARY SECURITY CONFIGURATION 🎸
# =====================================

# Password hashing context with legendary strength
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12 if settings.LEGENDARY_MODE else 10  # Extra rounds for legendary security
)

# JWT Security scheme
security_scheme = HTTPBearer(
    scheme_name="LegendaryJWT",
    description="🎸 Legendary JWT Authentication with Swiss precision 🎸"
)

# Legendary constants
LEGENDARY_USERS = ["rickroll187"]
SWISS_PRECISION_TOKEN_LIFETIME = 3600  # 1 hour for Swiss precision
CODE_BRO_ENERGY_BOOST = 1.5  # Energy multiplier for legendary users

# =====================================
# 🔐 PASSWORD SECURITY FUNCTIONS 🔐
# =====================================

def hash_password(password: str, legendary_mode: bool = False) -> str:
    """
    Hash password with legendary security
    """
    try:
        # Extra salt rounds for legendary users
        if legendary_mode or settings.LEGENDARY_MODE:
            # Use maximum security for legendary users
            salt_rounds = 14
            salt = bcrypt.gensalt(rounds=salt_rounds)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        else:
            # Standard security for regular users
            return pwd_context.hash(password)
            
    except Exception as e:
        logger.error(f"🚨 Password hashing failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password security error"
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password with legendary precision
    """
    try:
        # Handle both bcrypt and passlib hashes
        if hashed_password.startswith('$2b$'):
            # Direct bcrypt hash (legendary users)
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        else:
            # Passlib hash (standard users)
            return pwd_context.verify(plain_password, hashed_password)
            
    except Exception as e:
        logger.error(f"🚨 Password verification failed: {str(e)}")
        return False

def generate_legendary_salt() -> str:
    """
    Generate legendary salt for maximum security
    """
    return secrets.token_urlsafe(32)

def validate_password_strength(password: str, is_legendary: bool = False) -> Dict[str, Any]:
    """
    Validate password strength with legendary standards
    """
    validation = {
        "valid": True,
        "score": 0,
        "requirements": [],
        "legendary_approved": False
    }
    
    # Basic requirements
    if len(password) < 8:
        validation["valid"] = False
        validation["requirements"].append("Minimum 8 characters")
    else:
        validation["score"] += 1
    
    if not any(c.isupper() for c in password):
        validation["valid"] = False
        validation["requirements"].append("At least one uppercase letter")
    else:
        validation["score"] += 1
    
    if not any(c.islower() for c in password):
        validation["valid"] = False
        validation["requirements"].append("At least one lowercase letter")
    else:
        validation["score"] += 1
    
    if not any(c.isdigit() for c in password):
        validation["valid"] = False
        validation["requirements"].append("At least one number")
    else:
        validation["score"] += 1
    
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        validation["valid"] = False
        validation["requirements"].append("At least one special character")
    else:
        validation["score"] += 1
    
    # Legendary requirements
    if is_legendary:
        if len(password) < 12:
            validation["valid"] = False
            validation["requirements"].append("Legendary users need minimum 12 characters")
        else:
            validation["score"] += 2
        
        if not any(c in "🎸⚡💪🏆🚀" for c in password):
            validation["requirements"].append("Consider adding legendary emojis for maximum code bro energy! 🎸")
            validation["legendary_approved"] = False
        else:
            validation["legendary_approved"] = True
            validation["score"] += 3
    
    return validation

# =====================================
# 🎯 JWT TOKEN FUNCTIONS 🎯
# =====================================

def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None,
    is_legendary: bool = False
) -> str:
    """
    Create JWT access token with legendary features
    """
    try:
        to_encode = data.copy()
        
        # Set expiration
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
            if is_legendary:
                expire_minutes *= 2  # Longer tokens for legendary users
            expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "token_type": "access",
            "legendary": is_legendary,
            "swiss_precision": True if is_legendary else False,
            "code_bro_energy": "infinite" if is_legendary else "standard"
        })
        
        # Add legendary metadata
        if is_legendary:
            to_encode.update({
                "legendary_privileges": True,
                "swiss_precision_level": "maximum",
                "founder_access": data.get("username") == "rickroll187",
                "rate_limit_multiplier": settings.LEGENDARY_API_RATE_MULTIPLIER
            })
        
        # Encode token
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET_KEY, 
            algorithm=settings.JWT_ALGORITHM
        )
        
        logger.info(f"🎯 {'🎸 Legendary' if is_legendary else 'Standard'} access token created for: {data.get('username', 'unknown')}")
        
        return encoded_jwt
        
    except Exception as e:
        logger.error(f"🚨 Failed to create access token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token creation failed"
        )

def create_refresh_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None,
    is_legendary: bool = False
) -> str:
    """
    Create JWT refresh token with legendary durability
    """
    try:
        to_encode = data.copy()
        
        # Set expiration
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire_days = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
            if is_legendary:
                expire_days *= 2  # Longer refresh tokens for legendary users
            expire = datetime.now(timezone.utc) + timedelta(days=expire_days)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "token_type": "refresh",
            "legendary": is_legendary,
            "jti": secrets.token_urlsafe(16)  # Unique token ID
        })
        
        # Encode token
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET_KEY, 
            algorithm=settings.JWT_ALGORITHM
        )
        
        logger.info(f"🔄 {'🎸 Legendary' if is_legendary else 'Standard'} refresh token created for: {data.get('username', 'unknown')}")
        
        return encoded_jwt
        
    except Exception as e:
        logger.error(f"🚨 Failed to create refresh token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Refresh token creation failed"
        )

def verify_token(token: str, token_type: str = "access") -> Dict[str, Any]:
    """
    Verify JWT token with legendary precision
    """
    try:
        # Decode token
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Verify token type
        if payload.get("token_type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {token_type}"
            )
        
        # Check expiration
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        
        # Validate required fields
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Log legendary token usage
        if payload.get("legendary"):
            logger.info(f"🎸 Legendary token verified for: {username}")
        
        return payload
        
    except jwt.ExpiredSignatureError:
        logger.warning("🚨 Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError as e:
        logger.error(f"🚨 JWT error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    except Exception as e:
        logger.error(f"🚨 Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed"
        )

# =====================================
# 👤 USER AUTHENTICATION FUNCTIONS 👤
# =====================================

def authenticate_user(username: str, password: str, db: Session) -> Optional[Dict[str, Any]]:
    """
    Authenticate user with legendary detection
    """
    try:
        # Query user from database
        result = db.execute(
            text("""
                SELECT user_id, username, email, password_hash, first_name, last_name,
                       is_active, is_legendary, role, department, created_at, last_login,
                       failed_login_attempts, locked_until
                FROM users 
                WHERE username = :username OR email = :username
            """),
            {"username": username}
        ).fetchone()
        
        if not result:
            logger.warning(f"🚨 Authentication attempt for non-existent user: {username}")
            return None
        
        user_data = dict(result._mapping)
        
        # Check if account is locked
        if user_data.get("locked_until") and user_data["locked_until"] > datetime.now(timezone.utc):
            logger.warning(f"🔒 Authentication attempt for locked account: {username}")
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account is temporarily locked due to failed login attempts"
            )
        
        # Check if account is active
        if not user_data.get("is_active"):
            logger.warning(f"🚨 Authentication attempt for inactive account: {username}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated"
            )
        
        # Verify password
        if not verify_password(password, user_data["password_hash"]):
            # Increment failed attempts
            _handle_failed_login(username, db)
            logger.warning(f"🚨 Failed password verification for: {username}")
            return None
        
        # Reset failed attempts on successful login
        _reset_failed_login_attempts(username, db)
        
        # Update last login
        _update_last_login(username, db)
        
        # Detect legendary status
        is_legendary = user_data.get("is_legendary") or username in LEGENDARY_USERS
        
        if is_legendary:
            logger.info(f"🎸 LEGENDARY USER AUTHENTICATED: {username} 🎸")
        else:
            logger.info(f"✅ User authenticated: {username}")
        
        # Clean sensitive data
        user_data.pop("password_hash", None)
        user_data.pop("failed_login_attempts", None)
        user_data.pop("locked_until", None)
        
        # Add authentication metadata
        user_data.update({
            "authenticated_at": datetime.now(timezone.utc),
            "is_legendary": is_legendary,
            "swiss_precision_access": is_legendary,
            "code_bro_energy": "infinite" if is_legendary else "standard",
            "founder_access": username == "rickroll187"
        })
        
        return user_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Authentication error for {username}: {str(e)}")
        return None

def _handle_failed_login(username: str, db: Session):
    """
    Handle failed login attempts with legendary protection
    """
    try:
        # Don't lock legendary users as aggressively
        max_attempts = 10 if username in LEGENDARY_USERS else 5
        lock_duration_minutes = 15 if username in LEGENDARY_USERS else 30
        
        # Increment failed attempts
        result = db.execute(
            text("""
                UPDATE users 
                SET failed_login_attempts = COALESCE(failed_login_attempts, 0) + 1,
                    locked_until = CASE 
                        WHEN COALESCE(failed_login_attempts, 0) + 1 >= :max_attempts 
                        THEN :lock_until 
                        ELSE locked_until 
                    END
                WHERE username = :username OR email = :username
                RETURNING failed_login_attempts
            """),
            {
                "username": username,
                "max_attempts": max_attempts,
                "lock_until": datetime.now(timezone.utc) + timedelta(minutes=lock_duration_minutes)
            }
        ).fetchone()
        
        db.commit()
        
        if result and result[0] >= max_attempts:
            logger.warning(f"🔒 Account locked due to failed attempts: {username}")
        
    except Exception as e:
        logger.error(f"🚨 Error handling failed login: {str(e)}")
        db.rollback()

def _reset_failed_login_attempts(username: str, db: Session):
    """
    Reset failed login attempts on successful authentication
    """
    try:
        db.execute(
            text("""
                UPDATE users 
                SET failed_login_attempts = 0, locked_until = NULL
                WHERE username = :username OR email = :username
            """),
            {"username": username}
        )
        db.commit()
        
    except Exception as e:
        logger.error(f"🚨 Error resetting failed login attempts: {str(e)}")
        db.rollback()

def _update_last_login(username: str, db: Session):
    """
    Update last login timestamp
    """
    try:
        db.execute(
            text("""
                UPDATE users 
                SET last_login = :last_login
                WHERE username = :username OR email = :username
            """),
            {
                "username": username,
                "last_login": datetime.now(timezone.utc)
            }
        )
        db.commit()
        
    except Exception as e:
        logger.error(f"🚨 Error updating last login: {str(e)}")
        db.rollback()

# =====================================
# 🔐 AUTHENTICATION DEPENDENCIES 🔐
# =====================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Get current authenticated user with legendary detection
    """
    try:
        # Verify token
        payload = verify_token(credentials.credentials, "access")
        username = payload.get("sub")
        
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        # Get user from database
        result = db.execute(
            text("""
                SELECT user_id, username, email, first_name, last_name,
                       is_active, is_legendary, role, department, created_at, last_login
                FROM users 
                WHERE username = :username
            """),
            {"username": username}
        ).fetchone()
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        user_data = dict(result._mapping)
        
        # Check if user is still active
        if not user_data.get("is_active"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated"
            )
        
        # Add token metadata
        user_data.update({
            "token_legendary": payload.get("legendary", False),
            "swiss_precision_access": payload.get("swiss_precision", False),
            "founder_access": payload.get("founder_access", False),
            "code_bro_energy": payload.get("code_bro_energy", "standard"),
            "rate_limit_multiplier": payload.get("rate_limit_multiplier", 1.0)
        })
        
        # Ensure legendary detection
        if user_data["username"] in LEGENDARY_USERS:
            user_data["is_legendary"] = True
            user_data["swiss_precision_access"] = True
            user_data["code_bro_energy"] = "infinite"
        
        return user_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"🚨 Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

async def get_legendary_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Dependency that requires legendary user status
    """
    if not current_user.get("is_legendary") and current_user.get("username") not in LEGENDARY_USERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Legendary access required",
                "message": "🎸 This endpoint requires legendary user privileges",
                "contact": "rickroll187@n3extpath.com for legendary access"
            }
        )
    
    logger.info(f"🎸 Legendary user access granted: {current_user.get('username')} 🎸")
    return current_user

async def verify_rickroll187(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Dependency that requires RICKROLL187 founder access
    """
    if current_user.get("username") != "rickroll187":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "Founder access required",
                "message": "👑 This endpoint is exclusive to RICKROLL187",
                "contact": "rickroll187@n3extpath.com"
            }
        )
    
    logger.info("👑 RICKROLL187 FOUNDER ACCESS GRANTED! 👑")
    return current_user

# =====================================
# 🎸 LEGENDARY AUTHENTICATION UTILITIES 🎸
# =====================================

class LegendaryAuthUtils:
    """
    Legendary authentication utilities with Swiss precision
    """
    
    @staticmethod
    def is_legendary_user(username: str) -> bool:
        """Check if user is legendary"""
        return username in LEGENDARY_USERS
    
    @staticmethod
    def get_user_rate_limit(username: str, base_limit: int) -> int:
        """Get rate limit for user with legendary multiplier"""
        if username in LEGENDARY_USERS:
            return int(base_limit * settings.LEGENDARY_API_RATE_MULTIPLIER)
        return base_limit
    
    @staticmethod
    def generate_legendary_password() -> str:
        """Generate a legendary password suggestion"""
        words = ["Swiss", "Precision", "Code", "Bro", "Energy", "Legendary", "Epic"]
        emojis = ["🎸", "⚡", "💪", "🏆", "🚀"]
        numbers = secrets.randbelow(9999)
        
        password = (
            f"{secrets.choice(words)}"
            f"{secrets.choice(words)}"
            f"{numbers:04d}"
            f"{secrets.choice(emojis)}"
            f"!"
        )
        
        return password
    
    @staticmethod
    async def log_authentication_event(
        username: str, 
        event_type: str, 
        success: bool,
        metadata: Dict[str, Any] = None
    ):
        """Log authentication events with legendary precision"""
        try:
            event_data = {
                "username": username,
                "event_type": event_type,
                "success": success,
                "timestamp": datetime.now(timezone.utc),
                "is_legendary": username in LEGENDARY_USERS,
                "metadata": metadata or {}
            }
            
            # Log to application logger
            log_level = logging.INFO if success else logging.WARNING
            emoji = "🎸" if username in LEGENDARY_USERS else "👤"
            status = "✅" if success else "🚨"
            
            logger.log(
                log_level,
                f"{emoji} {status} Auth Event: {event_type} - {username} - {'Success' if success else 'Failed'}"
            )
            
            # TODO: Store in audit log table for legendary tracking
            
        except Exception as e:
            logger.error(f"🚨 Failed to log authentication event: {str(e)}")

# Global auth utilities instance
auth_utils = LegendaryAuthUtils()

# =====================================
# 🎸 LEGENDARY EXPORTS 🎸
# =====================================

__all__ = [
    "hash_password",
    "verify_password", 
    "generate_legendary_salt",
    "validate_password_strength",
    "create_access_token",
    "create_refresh_token",
    "verify_token",
    "authenticate_user",
    "get_current_user",
    "get_legendary_user",
    "verify_rickroll187",
    "LegendaryAuthUtils",
    "auth_utils",
    "pwd_context",
    "security_scheme"
]

# =====================================
# 🎸 LEGENDARY COMPLETION MESSAGE 🎸
# =====================================

if __name__ == "__main__":
    print("🎸🎸🎸 LEGENDARY AUTHENTICATION SECURITY SYSTEM LOADED! 🎸🎸🎸")
    print("Built with Swiss precision by RICKROLL187!")
    print("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    print(f"Authentication system loaded at: 2025-08-05 22:15:56 UTC")
    print("🔐 JWT tokens with legendary detection: ACTIVE")
    print("🎸 RICKROLL187 founder privileges: ENABLED")
    print("⚡ Swiss precision security: MAXIMUM")
    print("💪 Code bro energy authentication: INFINITE")
    print("🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸")
