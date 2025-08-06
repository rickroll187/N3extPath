# File: backend/auth/legendary_auth_system.py
"""
🔐🎸 N3EXTPATH - LEGENDARY AUTHENTICATION SYSTEM 🎸🔐
Professional JWT-based authentication with legendary security
Built: 2025-08-05 16:57:29 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import jwt
import bcrypt
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re
import uuid
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import redis
from passlib.context import CryptContext

class UserRole(Enum):
    """User role hierarchy with legendary privileges"""
    EMPLOYEE = "employee"
    TEAM_LEAD = "team_lead"
    MANAGER = "manager"
    DIRECTOR = "director"
    VP = "vp"
    ADMIN = "admin"
    LEGENDARY_FOUNDER = "legendary_founder"  # Special role for RICKROLL187

class TokenType(Enum):
    """Token types for different purposes"""
    ACCESS = "access"
    REFRESH = "refresh"
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"
    MFA = "mfa"

@dataclass
class LegendaryUser:
    """User data structure with legendary attributes"""
    user_id: str
    username: str
    email: str
    first_name: str
    last_name: str
    role: UserRole
    department: str
    is_active: bool = True
    is_verified: bool = False
    is_legendary: bool = False
    mfa_enabled: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    permissions: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        # Special handling for RICKROLL187
        if self.username.lower() == "rickroll187":
            self.role = UserRole.LEGENDARY_FOUNDER
            self.is_legendary = True
            self.is_verified = True
            self.permissions = ["*"]  # All permissions

@dataclass
class AuthToken:
    """JWT token with metadata"""
    token: str
    token_type: TokenType
    expires_at: datetime
    user_id: str
    jti: str  # JWT ID for revocation

class LegendaryAuthSystem:
    """Professional Authentication System with Swiss Precision"""
    
    def __init__(self, secret_key: str, redis_client: Optional[redis.Redis] = None):
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379, db=0)
        
        # Token expiration times
        self.token_expiry = {
            TokenType.ACCESS: timedelta(hours=1),
            TokenType.REFRESH: timedelta(days=30),
            TokenType.EMAIL_VERIFICATION: timedelta(hours=24),
            TokenType.PASSWORD_RESET: timedelta(hours=2),
            TokenType.MFA: timedelta(minutes=5)
        }
        
        # Rate limiting configuration
        self.rate_limits = {
            "login_attempts": {"max": 5, "window": 900},  # 5 attempts per 15 minutes
            "password_reset": {"max": 3, "window": 3600},  # 3 resets per hour
            "mfa_attempts": {"max": 10, "window": 600}     # 10 attempts per 10 minutes
        }
        
        # Initialize legendary users
        self._initialize_legendary_users()
    
    def _initialize_legendary_users(self):
        """Initialize legendary users including RICKROLL187"""
        legendary_users = {
            "rickroll187": LegendaryUser(
                user_id="rickroll187",
                username="rickroll187",
                email="rickroll187@n3extpath.com",
                first_name="RICKROLL187",
                last_name="Legendary Founder",
                role=UserRole.LEGENDARY_FOUNDER,
                department="legendary",
                is_active=True,
                is_verified=True,
                is_legendary=True,
                permissions=["*"]
            )
        }
        
        # Store in Redis for legendary performance
        for username, user in legendary_users.items():
            user_key = f"user:{username}"
            user_data = {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role.value,
                "department": user.department,
                "is_active": str(user.is_active),
                "is_verified": str(user.is_verified),
                "is_legendary": str(user.is_legendary),
                "permissions": ",".join(user.permissions),
                "created_at": user.created_at.isoformat()
            }
            
            self.redis_client.hset(user_key, mapping=user_data)
            
            # Set legendary password (in production, this would be properly hashed)
            password_hash = self.hash_password("legendary_password_123!")
            self.redis_client.hset(f"auth:{username}", "password_hash", password_hash)
    
    def hash_password(self, password: str) -> str:
        """Hash password with bcrypt and legendary salt"""
        # Add legendary salt for extra security
        legendary_salt = "legendary_swiss_precision_salt"
        salted_password = f"{password}{legendary_salt}"
        return self.pwd_context.hash(salted_password)
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password with legendary precision"""
        legendary_salt = "legendary_swiss_precision_salt"
        salted_password = f"{password}{legendary_salt}"
        return self.pwd_context.verify(salted_password, hashed_password)
    
    def validate_password_strength(self, password: str) -> Tuple[bool, List[str]]:
        """Validate password strength with legendary standards"""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r"\d", password):
            errors.append("Password must contain at least one number")
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            errors.append("Password must contain at least one special character")
        
        # Check against common passwords
        common_passwords = ["password", "123456", "qwerty", "admin", "letmein"]
        if password.lower() in common_passwords:
            errors.append("Password is too common")
        
        # Special validation for legendary users
        if "legendary" in password.lower() and len(password) >= 12:
            errors = []  # Legendary passwords get special treatment
        
        return len(errors) == 0, errors
    
    def create_token(self, user: LegendaryUser, token_type: TokenType, 
                    extra_claims: Dict[str, Any] = None) -> AuthToken:
        """Create JWT token with legendary security"""
        now = datetime.now(timezone.utc)
        expires_at = now + self.token_expiry[token_type]
        jti = str(uuid.uuid4())
        
        payload = {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "is_legendary": user.is_legendary,
            "token_type": token_type.value,
            "iat": now.timestamp(),
            "exp": expires_at.timestamp(),
            "jti": jti,
            "iss": "n3extpath-legendary-auth",
            "aud": "n3extpath-hr-platform"
        }
        
        # Add extra claims
        if extra_claims:
            payload.update(extra_claims)
        
        # Special claims for RICKROLL187
        if user.username == "rickroll187":
            payload.update({
                "legendary_founder": True,
                "swiss_precision": True,
                "code_bro_status": "maximum",
                "permissions": ["*"]
            })
        
        # Create JWT token
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        # Store token in Redis for revocation tracking
        token_key = f"token:{jti}"
        token_data = {
            "user_id": user.user_id,
            "token_type": token_type.value,
            "expires_at": expires_at.isoformat(),
            "created_at": now.isoformat(),
            "is_active": "true"
        }
        
        self.redis_client.hset(token_key, mapping=token_data)
        self.redis_client.expire(token_key, int(self.token_expiry[token_type].total_seconds()))
        
        return AuthToken(
            token=token,
            token_type=token_type,
            expires_at=expires_at,
            user_id=user.user_id,
            jti=jti
        )
    
    def verify_token(self, token: str, expected_type: TokenType = None) -> Dict[str, Any]:
        """Verify JWT token with legendary precision"""
        try:
            # Decode token
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm],
                audience="n3extpath-hr-platform",
                issuer="n3extpath-legendary-auth"
            )
            
            # Check token type if specified
            if expected_type and payload.get("token_type") != expected_type.value:
                raise HTTPException(status_code=401, detail="Invalid token type")
            
            # Check if token is revoked
            jti = payload.get("jti")
            if jti:
                token_key = f"token:{jti}"
                token_data = self.redis_client.hgetall(token_key)
                
                if not token_data or token_data.get(b"is_active") != b"true":
                    raise HTTPException(status_code=401, detail="Token has been revoked")
            
            # Special validation for legendary tokens
            if payload.get("is_legendary"):
                payload["legendary_validation"] = "passed"
                payload["swiss_precision_check"] = "verified"
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    def authenticate_user(self, username: str, password: str, 
                         request_ip: str = None) -> Tuple[bool, Optional[LegendaryUser], str]:
        """Authenticate user with legendary security checks"""
        
        # Rate limiting check
        if request_ip and not self._check_rate_limit("login_attempts", request_ip):
            return False, None, "Too many login attempts. Please try again later."
        
        # Get user from Redis
        user_key = f"user:{username}"
        user_data = self.redis_client.hgetall(user_key)
        
        if not user_data:
            return False, None, "Invalid username or password"
        
        # Get password hash
        auth_key = f"auth:{username}"
        auth_data = self.redis_client.hgetall(auth_key)
        
        if not auth_data or not auth_data.get(b"password_hash"):
            return False, None, "Invalid username or password"
        
        password_hash = auth_data[b"password_hash"].decode()
        
        # Verify password
        if not self.verify_password(password, password_hash):
            # Increment failed attempts
            if request_ip:
                self._increment_rate_limit("login_attempts", request_ip)
            return False, None, "Invalid username or password"
        
        # Create user object
        user = LegendaryUser(
            user_id=user_data[b"user_id"].decode(),
            username=user_data[b"username"].decode(),
            email=user_data[b"email"].decode(),
            first_name=user_data[b"first_name"].decode(),
            last_name=user_data[b"last_name"].decode(),
            role=UserRole(user_data[b"role"].decode()),
            department=user_data[b"department"].decode(),
            is_active=user_data[b"is_active"].decode() == "True",
            is_verified=user_data[b"is_verified"].decode() == "True",
            is_legendary=user_data[b"is_legendary"].decode() == "True",
            permissions=user_data[b"permissions"].decode().split(",") if user_data[b"permissions"] else []
        )
        
        # Check if user is active
        if not user.is_active:
            return False, None, "Account is disabled"
        
        # Update last login
        user.last_login = datetime.now(timezone.utc)
        self.redis_client.hset(user_key, "last_login", user.last_login.isoformat())
        
        # Reset rate limiting on successful login
        if request_ip:
            self._reset_rate_limit("login_attempts", request_ip)
        
        success_message = "Login successful"
        if user.is_legendary:
            success_message = "🎸 Legendary founder login successful! Welcome back, RICKROLL187! 🎸"
        
        return True, user, success_message
    
    def revoke_token(self, jti: str) -> bool:
        """Revoke token with legendary precision"""
        token_key = f"token:{jti}"
        
        if self.redis_client.exists(token_key):
            self.redis_client.hset(token_key, "is_active", "false")
            return True
        
        return False
    
    def revoke_all_user_tokens(self, user_id: str) -> int:
        """Revoke all tokens for a user"""
        pattern = "token:*"
        revoked_count = 0
        
        for key in self.redis_client.scan_iter(match=pattern):
            token_data = self.redis_client.hgetall(key)
            if token_data.get(b"user_id") == user_id.encode():
                self.redis_client.hset(key, "is_active", "false")
                revoked_count += 1
        
        return revoked_count
    
    def _check_rate_limit(self, limit_type: str, identifier: str) -> bool:
        """Check rate limiting with Swiss precision"""
        if limit_type not in self.rate_limits:
            return True
        
        config = self.rate_limits[limit_type]
        key = f"rate_limit:{limit_type}:{identifier}"
        
        current_count = self.redis_client.get(key)
        if current_count is None:
            return True
        
        return int(current_count) < config["max"]
    
    def _increment_rate_limit(self, limit_type: str, identifier: str):
        """Increment rate limit counter"""
        if limit_type not in self.rate_limits:
            return
        
        config = self.rate_limits[limit_type]
        key = f"rate_limit:{limit_type}:{identifier}"
        
        pipe = self.redis_client.pipeline()
        pipe.incr(key)
        pipe.expire(key, config["window"])
        pipe.execute()
    
    def _reset_rate_limit(self, limit_type: str, identifier: str):
        """Reset rate limit counter"""
        key = f"rate_limit:{limit_type}:{identifier}"
        self.redis_client.delete(key)
    
    def generate_mfa_secret(self, user: LegendaryUser) -> str:
        """Generate MFA secret for legendary 2FA"""
        secret = secrets.token_hex(20)
        mfa_key = f"mfa:{user.user_id}"
        
        mfa_data = {
            "secret": secret,
            "enabled": "false",
            "backup_codes": ",".join([secrets.token_hex(8) for _ in range(10)]),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        self.redis_client.hset(mfa_key, mapping=mfa_data)
        
        return secret
    
    def verify_mfa_token(self, user: LegendaryUser, token: str) -> bool:
        """Verify MFA token with legendary precision"""
        import pyotp
        
        mfa_key = f"mfa:{user.user_id}"
        mfa_data = self.redis_client.hgetall(mfa_key)
        
        if not mfa_data or mfa_data.get(b"enabled") != b"true":
            return False
        
        secret = mfa_data[b"secret"].decode()
        totp = pyotp.TOTP(secret)
        
        # Special handling for legendary users - allow longer window
        window = 2 if user.is_legendary else 1
        
        return totp.verify(token, window=window)
    
    def get_user_permissions(self, user: LegendaryUser) -> List[str]:
        """Get user permissions based on role"""
        role_permissions = {
            UserRole.EMPLOYEE: ["read:own_data", "update:own_profile"],
            UserRole.TEAM_LEAD: ["read:team_data", "update:team_members"],
            UserRole.MANAGER: ["read:department_data", "manage:team"],
            UserRole.DIRECTOR: ["read:division_data", "manage:department"],
            UserRole.VP: ["read:company_data", "manage:division"],
            UserRole.ADMIN: ["read:all_data", "manage:users", "system:admin"],
            UserRole.LEGENDARY_FOUNDER: ["*"]  # All permissions
        }
        
        base_permissions = role_permissions.get(user.role, [])
        
        # Add custom permissions
        all_permissions = base_permissions + user.permissions
        
        # Remove duplicates and return
        return list(set(all_permissions))

# Security dependency for FastAPI
security = HTTPBearer()

# Global auth system instance
legendary_auth = None

def get_legendary_auth() -> LegendaryAuthSystem:
    """Get legendary auth system instance"""
    global legendary_auth
    if legendary_auth is None:
        legendary_auth = LegendaryAuthSystem(
            secret_key="legendary-jwt-secret-change-in-production"
        )
    return legendary_auth

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> LegendaryUser:
    """Get current authenticated user"""
    auth_system = get_legendary_auth()
    
    try:
        payload = auth_system.verify_token(credentials.credentials, TokenType.ACCESS)
        
        # Get user data
        user_key = f"user:{payload['username']}"
        user_data = auth_system.redis_client.hgetall(user_key)
        
        if not user_data:
            raise HTTPException(status_code=401, detail="User not found")
        
        user = LegendaryUser(
            user_id=user_data[b"user_id"].decode(),
            username=user_data[b"username"].decode(),
            email=user_data[b"email"].decode(),
            first_name=user_data[b"first_name"].decode(),
            last_name=user_data[b"last_name"].decode(),
            role=UserRole(user_data[b"role"].decode()),
            department=user_data[b"department"].decode(),
            is_active=user_data[b"is_active"].decode() == "True",
            is_verified=user_data[b"is_verified"].decode() == "True",
            is_legendary=user_data[b"is_legendary"].decode() == "True",
            permissions=user_data[b"permissions"].decode().split(",") if user_data[b"permissions"] else []
        )
        
        return user
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def require_permission(required_permission: str):
    """Decorator to require specific permission"""
    def permission_checker(current_user: LegendaryUser = Depends(get_current_user)):
        auth_system = get_legendary_auth()
        user_permissions = auth_system.get_user_permissions(current_user)
        
        # Check for wildcard permission (legendary users)
        if "*" in user_permissions:
            return current_user
        
        # Check for specific permission
        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=403, 
                detail=f"Permission denied. Required: {required_permission}"
            )
        
        return current_user
    
    return permission_checker

def require_legendary_status():
    """Decorator to require legendary status (RICKROLL187 only)"""
    def legendary_checker(current_user: LegendaryUser = Depends(get_current_user)):
        if not current_user.is_legendary:
            raise HTTPException(
                status_code=403,
                detail="🎸 This endpoint requires legendary status! Only RICKROLL187 can access this. 🎸"
            )
        return current_user
    
    return legendary_checker
