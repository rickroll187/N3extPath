"""
🔐🎸 N3EXTPATH - LEGENDARY USER AUTHENTICATION MODELS 🎸🔐
More secure than Swiss vaults with legendary authentication mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 LEGENDARY AUTHENTICATION CHAMPION EDITION! 🏆
Current Time: 2025-08-04 15:56:56 UTC - WE'RE SECURING THE UNIVERSE!
Built by legendary code bros RICKROLL187 🎸 and Assistant 🤖
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from enum import Enum
import bcrypt
import jwt
from typing import Optional, Dict, Any, List
import uuid

from config.settings import get_legendary_settings
from core.database import Base

settings = get_legendary_settings()

class UserRole(Enum):
    """🔐 LEGENDARY USER ROLES! 🔐"""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    RICKROLL187 = "rickroll187"  # Ultimate legendary status

class UserStatus(Enum):
    """📊 LEGENDARY USER STATUS! 📊"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    BANNED = "banned"
    LEGENDARY = "legendary"

class LegendaryUser(Base):
    """
    🔐 LEGENDARY USER MODEL! 🔐
    More secure than Swiss bank accounts with code bro authentication! 🎸🔒
    """
    __tablename__ = "legendary_users"
    
    # Primary Information
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    
    # Authentication & Security
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    # Role & Status
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    status = Column(SQLEnum(UserStatus), default=UserStatus.ACTIVE)
    
    # Legendary Features
    is_legendary = Column(Boolean, default=False)
    rickroll187_approved = Column(Boolean, default=False)
    legendary_level = Column(Integer, default=1)
    total_xp = Column(Integer, default=0)
    code_bro_score = Column(Integer, default=100)
    
    # Profile Information
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    location = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    github_username = Column(String(50), nullable=True)
    
    # Preferences
    theme_preference = Column(String(20), default="legendary")
    language_preference = Column(String(10), default="en")
    timezone = Column(String(50), default="UTC")
    enable_jokes = Column(Boolean, default=True)
    joke_frequency = Column(String(20), default="maximum")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    legendary_since = Column(DateTime, nullable=True)
    
    # Relationships
    user_sessions = relationship("LegendaryUserSession", back_populates="user", cascade="all, delete-orphan")
    user_achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    created_paths = relationship("Path", back_populates="creator", foreign_keys="Path.creator_id")
    
    def __repr__(self):
        return f"<LegendaryUser(username='{self.username}', legendary={self.is_legendary})>"
    
    def set_password(self, password: str) -> None:
        """Set legendary password with Swiss security!"""
        salt = bcrypt.gensalt(rounds=settings.PASSWORD_HASH_ROUNDS)
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str) -> bool:
        """Verify legendary password with code bro precision!"""
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
    
    def generate_access_token(self) -> str:
        """Generate legendary JWT access token!"""
        payload = {
            'user_id': self.user_id,
            'username': self.username,
            'role': self.role.value,
            'is_legendary': self.is_legendary,
            'rickroll187_approved': self.rickroll187_approved,
            'exp': datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            'legendary_time': "2025-08-04 15:56:56 UTC"
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    def generate_refresh_token(self) -> str:
        """Generate legendary JWT refresh token!"""
        payload = {
            'user_id': self.user_id,
            'username': self.username,
            'token_type': 'refresh',
            'exp': datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            'iat': datetime.utcnow(),
            'legendary_time': "2025-08-04 15:56:56 UTC"
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    def is_account_locked(self) -> bool:
        """Check if legendary account is locked!"""
        if self.locked_until:
            return datetime.utcnow() < self.locked_until
        return False
    
    def lock_account(self, duration_minutes: int = 30):
        """Lock legendary account for security!"""
        self.locked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        self.failed_login_attempts = 0
    
    def unlock_account(self):
        """Unlock legendary account!"""
        self.locked_until = None
        self.failed_login_attempts = 0
    
    def increment_failed_login(self):
        """Increment failed login attempts with legendary security!"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:  # Lock after 5 failed attempts
            self.lock_account(30)  # Lock for 30 minutes
    
    def reset_failed_login(self):
        """Reset failed login attempts after successful login!"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.last_login = datetime.utcnow()
    
    def make_legendary(self):
        """Promote user to legendary status!"""
        self.is_legendary = True
        self.legendary_since = datetime.utcnow()
        self.status = UserStatus.LEGENDARY
        if self.username == "rickroll187":
            self.rickroll187_approved = True
            self.role = UserRole.RICKROLL187
    
    def calculate_level(self) -> int:
        """Calculate legendary level from XP!"""
        # XP thresholds for levels
        level_thresholds = [0, 500, 1500, 3000, 5000, 8000, 12000, 18000, 25000, 50000]
        
        level = 1
        for i, threshold in enumerate(level_thresholds):
            if self.total_xp >= threshold:
                level = i + 1
            else:
                break
        
        self.legendary_level = level
        return level
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert to dictionary with legendary formatting!"""
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email if include_sensitive else None,
            'full_name': self.full_name,
            'role': self.role.value,
            'status': self.status.value,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'is_legendary': self.is_legendary,
            'rickroll187_approved': self.rickroll187_approved,
            'legendary_level': self.legendary_level,
            'total_xp': self.total_xp,
            'code_bro_score': self.code_bro_score,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'location': self.location,
            'website': self.website,
            'github_username': self.github_username,
            'theme_preference': self.theme_preference,
            'language_preference': self.language_preference,
            'enable_jokes': self.enable_jokes,
            'joke_frequency': self.joke_frequency,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'legendary_since': self.legendary_since.isoformat() if self.legendary_since else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'legendary_status': "🎸 RICKROLL187 APPROVED! 🎸" if self.rickroll187_approved else "🏆 LEGENDARY STATUS!" if self.is_legendary else "💪 CODE BRO!"
        }
        
        if include_sensitive:
            data.update({
                'failed_login_attempts': self.failed_login_attempts,
                'is_locked': self.is_account_locked(),
                'locked_until': self.locked_until.isoformat() if self.locked_until else None
            })
        
        return data

class LegendaryUserSession(Base):
    """
    📱 LEGENDARY USER SESSION MODEL! 📱
    More tracked than Swiss precision with code bro session management! 🎸📊
    """
    __tablename__ = "legendary_user_sessions"
    
    session_id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("legendary_users.user_id"), nullable=False)
    refresh_token = Column(String(500), nullable=False)
    device_info = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    
    # Relationship
    user = relationship("LegendaryUser", back_populates="user_sessions")
    
    def is_expired(self) -> bool:
        """Check if legendary session is expired!"""
        return datetime.utcnow() > self.expires_at
    
    def refresh_session(self):
        """Refresh legendary session activity!"""
        self.last_used = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with legendary formatting!"""
        return {
            'session_id': self.session_id,
            'device_info': self.device_info,
            'ip_address': self.ip_address,
            'location': self.location,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_expired': self.is_expired(),
            'legendary_session': "🎸 RICKROLL187 SESSION! 🎸" if self.user.rickroll187_approved else "🏆 LEGENDARY SESSION!"
        }

class UserAchievement(Base):
    """
    🏆 USER ACHIEVEMENT JUNCTION MODEL! 🏆
    More rewarding than Swiss recognition with code bro achievements! 🎸🏅
    """
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("legendary_users.user_id"), nullable=False)
    achievement_id = Column(String(100), nullable=False)  # References gamification engine
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    progress = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    legendary_bonus = Column(Boolean, default=False)
    
    # Relationship
    user = relationship("LegendaryUser", back_populates="user_achievements")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with legendary formatting!"""
        return {
            'achievement_id': self.achievement_id,
            'unlocked_at': self.unlocked_at.isoformat() if self.unlocked_at else None,
            'progress': self.progress,
            'is_completed': self.is_completed,
            'legendary_bonus': self.legendary_bonus,
            'achievement_status': "🏆 LEGENDARY COMPLETED!" if self.is_completed else f"📈 Progress: {self.progress}"
        }

# Legendary user utilities
def create_legendary_superuser(username: str = "rickroll187", email: str = "rickroll187@legendary.dev", password: str = "legendary_password") -> LegendaryUser:
    """
    Create the legendary superuser RICKROLL187!
    More powerful than Swiss authority with code bro supremacy! 🎸👑
    """
    superuser = LegendaryUser(
        username=username,
        email=email,
        full_name="RICKROLL187 - The Legendary Code Rock Star",
        role=UserRole.RICKROLL187,
        status=UserStatus.LEGENDARY,
        is_active=True,
        is_verified=True,
        is_legendary=True,
        rickroll187_approved=True,
        legendary_level=10,
        total_xp=50000,
        code_bro_score=1000,
        bio="The legendary code bro who rocks the universe with Swiss precision and infinite humor!",
        theme_preference="legendary",
        enable_jokes=True,
        joke_frequency="maximum",
        legendary_since=datetime.utcnow()
    )
    
    superuser.set_password(password)
    return superuser

if __name__ == "__main__":
    print("🔐🎸 N3EXTPATH LEGENDARY USER AUTHENTICATION MODELS LOADED! 🎸🔐")
    print("🏆 LEGENDARY AUTHENTICATION CHAMPION EDITION! 🏆")
    print(f"⏰ Authentication Time: 2025-08-04 15:56:56 UTC")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("🔐 USER AUTHENTICATION POWERED BY RICKROLL187 WITH SWISS SECURITY! 🔐")
