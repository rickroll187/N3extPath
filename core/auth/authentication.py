"""
LEGENDARY AUTHENTICATION FORTRESS 🔐🏰
More secure than Fort Knox with trust issues and a CS degree!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import logging
import secrets
import hashlib
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List, Union
from passlib.context import CryptContext
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import pyotp
import qrcode
from io import BytesIO
import base64
from email.mime.text import MIMEText
import smtplib
import re

logger = logging.getLogger(__name__)

class AuthConfig:
    """
    Authentication configuration that's more secure than a paranoid programmer!
    Settings so tight they make security experts weep with joy! 🛡️😄
    """
    
    def __init__(self):
        # AUTHENTICATION JOKES FOR SUNDAY MORNING MOTIVATION
        self.auth_jokes = [
            "Why did the password go to therapy? It had security issues! 🔒😄",
            "What's the difference between our auth and a bouncer? Both check IDs but ours is more polite! 🚪",
            "Why don't hackers crack our passwords? Because they're having trust issues! 💪",
            "What do you call authentication at midnight? Night security with style! 🌙",
            "Why did the JWT token become a comedian? It had great timing! ⏰"
        ]
        
        # JWT Configuration
        self.secret_key = secrets.token_urlsafe(32)  # In production, use env variable
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7
        self.reset_token_expire_minutes = 15
        
        # Password Security
        self.min_password_length = 8
        self.require_special_chars = True
        self.require_numbers = True
        self.require_uppercase = True
        self.require_lowercase = True
        self.password_history_count = 5
        self.max_failed_attempts = 5
        self.lockout_duration_minutes = 30
        
        # Two-Factor Authentication
        self.enable_2fa = True
        self.totp_issuer = "HR Empire"
        self.backup_codes_count = 10
        
        # Session Management
        self.max_concurrent_sessions = 3
        self.session_timeout_minutes = 480  # 8 hours
        
        logger.info("🔐 Legendary Authentication Config initialized - Security level: MAXIMUM")

class PasswordValidator:
    """
    Password validation that's stricter than a drill sergeant!
    More thorough than a security audit with OCD! 💪🔍
    """
    
    def __init__(self, config: AuthConfig):
        self.config = config
        
        # Common weak passwords (in production, load from external source)
        self.weak_passwords = {
            "password", "123456", "password123", "admin", "qwerty",
            "letmein", "welcome", "monkey", "dragon", "password1",
            "123456789", "welcome123", "admin123", "root", "toor"
        }
    
    def validate_password(self, password: str, user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Validate password strength with more precision than a Swiss watch!
        Returns validation results that are more detailed than a forensic report! 🎯
        """
        try:
            errors = []
            warnings = []
            score = 0
            
            # Length check
            if len(password) < self.config.min_password_length:
                errors.append(f"Password must be at least {self.config.min_password_length} characters long")
            else:
                score += 20
                if len(password) >= 12:
                    score += 10
                if len(password) >= 16:
                    score += 10
            
            # Character requirements
            if self.config.require_lowercase and not re.search(r'[a-z]', password):
                errors.append("Password must contain at least one lowercase letter")
            elif re.search(r'[a-z]', password):
                score += 10
            
            if self.config.require_uppercase and not re.search(r'[A-Z]', password):
                errors.append("Password must contain at least one uppercase letter")
            elif re.search(r'[A-Z]', password):
                score += 10
            
            if self.config.require_numbers and not re.search(r'\d', password):
                errors.append("Password must contain at least one number")
            elif re.search(r'\d', password):
                score += 10
            
            if self.config.require_special_chars and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                errors.append("Password must contain at least one special character")
            elif re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                score += 10
            
            # Advanced checks
            if password.lower() in self.weak_passwords:
                errors.append("Password is too common and easily guessable")
            else:
                score += 15
            
            # Check for personal information (if provided)
            if user_info:
                personal_data = [
                    user_info.get('first_name', '').lower(),
                    user_info.get('last_name', '').lower(),
                    user_info.get('username', '').lower(),
                    user_info.get('email', '').split('@')[0].lower() if user_info.get('email') else ''
                ]
                
                for data in personal_data:
                    if data and len(data) > 2 and data in password.lower():
                        warnings.append(f"Password should not contain personal information")
                        score -= 10
                        break
            
            # Pattern analysis
            if re.search(r'(.)\1{2,}', password):  # Repeated characters
                warnings.append("Avoid repeating characters more than twice")
                score -= 5
            
            if re.search(r'(012|123|234|345|456|567|678|789|890)', password):  # Sequential numbers
                warnings.append("Avoid sequential numbers")
                score -= 5
            
            if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
                warnings.append("Avoid sequential letters")
                score -= 5
            
            # Calculate final score
            score = max(0, min(100, score))
            
            # Determine strength
            if score >= 90:
                strength = "LEGENDARY"
                strength_emoji = "🏆"
            elif score >= 80:
                strength = "EXCELLENT"
                strength_emoji = "💎"
            elif score >= 70:
                strength = "STRONG"
                strength_emoji = "💪"
            elif score >= 60:
                strength = "GOOD"
                strength_emoji = "👍"
            elif score >= 40:
                strength = "WEAK"
                strength_emoji = "⚠️"
            else:
                strength = "VERY_WEAK"
                strength_emoji = "❌"
            
            validation_result = {
                "is_valid": len(errors) == 0,
                "strength": strength,
                "strength_emoji": strength_emoji,
                "score": score,
                "errors": errors,
                "warnings": warnings,
                "suggestions": self._generate_password_suggestions(),
                "validation_timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"🔍 Password validation complete - Strength: {strength} ({score}/100)")
            return validation_result
            
        except Exception as e:
            logger.error(f"💥 Password validation error: {e}")
            return {
                "is_valid": False,
                "strength": "UNKNOWN",
                "score": 0,
                "errors": [f"Validation error: {str(e)}"],
                "warnings": [],
                "suggestions": []
            }
    
    def _generate_password_suggestions(self) -> List[str]:
        """Generate helpful password suggestions"""
        return [
            "Use a mix of uppercase and lowercase letters",
            "Include numbers and special characters",
            "Consider using a passphrase with random words",
            "Avoid personal information like names or birthdays",
            "Use a password manager for complex passwords",
            "Make it at least 12 characters long for better security"
        ]

class LegendaryAuthenticator:
    """
    The most secure authenticator in the galaxy!
    More reliable than a loyal dog with a cybersecurity degree! 🐕💻🔐
    """
    
    def __init__(self, config: AuthConfig = None):
        self.config = config or AuthConfig()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.password_validator = PasswordValidator(self.config)
        
        logger.info("🚀 Legendary Authenticator initialized - Ready to secure the empire!")
    
    def hash_password(self, password: str) -> str:
        """
        Hash password with more security than a Swiss bank!
        More protected than classified documents! 🔒📄
        """
        try:
            hashed = self.pwd_context.hash(password)
            logger.debug("🔐 Password hashed successfully")
            return hashed
        except Exception as e:
            logger.error(f"💥 Password hashing error: {e}")
            raise
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify password with precision of a Swiss timepiece!
        More accurate than a sniper with perfect vision! 🎯
        """
        try:
            result = self.pwd_context.verify(plain_password, hashed_password)
            logger.debug(f"🔍 Password verification: {'SUCCESS' if result else 'FAILED'}")
            return result
        except Exception as e:
            logger.error(f"💥 Password verification error: {e}")
            return False
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token more secure than a vault!
        More trustworthy than a best friend with a security clearance! 🎫🔐
        """
        try:
            to_encode = data.copy()
            
            if expires_delta:
                expire = datetime.now(timezone.utc) + expires_delta
            else:
                expire = datetime.now(timezone.utc) + timedelta(minutes=self.config.access_token_expire_minutes)
            
            to_encode.update({
                "exp": expire,
                "iat": datetime.now(timezone.utc),
                "type": "access",
                "jti": secrets.token_hex(16)  # JWT ID for tracking
            })
            
            encoded_jwt = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)
            
            logger.debug(f"🎫 Access token created - Expires: {expire}")
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"💥 Token creation error: {e}")
            raise
    
    def create_refresh_token(self, user_id: int) -> str:
        """
        Create refresh token for long-term authentication!
        More persistent than a determined programmer debugging at 3 AM! 🔄
        """
        try:
            expire = datetime.now(timezone.utc) + timedelta(days=self.config.refresh_token_expire_days)
            
            to_encode = {
                "user_id": user_id,
                "exp": expire,
                "iat": datetime.now(timezone.utc),
                "type": "refresh",
                "jti": secrets.token_hex(16)
            }
            
            encoded_jwt = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)
            
            logger.debug(f"🔄 Refresh token created - User: {user_id}")
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"💥 Refresh token creation error: {e}")
            raise
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """
        Verify JWT token with more precision than a forensic lab!
        More thorough than a security audit with trust issues! 🔍🎯
        """
        try:
            payload = jwt.decode(token, self.config.secret_key, algorithms=[self.config.algorithm])
            
            # Verify token type
            if payload.get("type") != token_type:
                logger.warning(f"🚨 Token type mismatch: expected {token_type}, got {payload.get('type')}")
                return None
            
            # Check expiration
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
                logger.warning("⏰ Token has expired")
                return None
            
            logger.debug(f"✅ Token verified successfully - Type: {token_type}")
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("⏰ Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"🚨 Invalid token: {e}")
            return None
        except Exception as e:
            logger.error(f"💥 Token verification error: {e}")
            return None
    
    def generate_2fa_secret(self, user_email: str) -> Dict[str, Any]:
        """
        Generate 2FA secret with more security than a military base!
        More protected than state secrets! 🛡️🔐
        """
        try:
            secret = pyotp.random_base32()
            
            # Create TOTP URI for QR code
            totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
                name=user_email,
                issuer_name=self.config.totp_issuer
            )
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(totp_uri)
            qr.make(fit=True)
            
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64 for easy transmission
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            # Generate backup codes
            backup_codes = [secrets.token_hex(4).upper() for _ in range(self.config.backup_codes_count)]
            
            result = {
                "secret": secret,
                "qr_code_uri": totp_uri,
                "qr_code_base64": qr_code_base64,
                "backup_codes": backup_codes,
                "setup_instructions": [
                    "1. Install an authenticator app (Google Authenticator, Authy, etc.)",
                    "2. Scan the QR code or manually enter the secret",
                    "3. Save the backup codes in a secure location",
                    "4. Enter a code from your app to verify setup"
                ]
            }
            
            logger.info(f"🔐 2FA secret generated for: {user_email}")
            return result
            
        except Exception as e:
            logger.error(f"💥 2FA secret generation error: {e}")
            raise
    
    def verify_2fa_token(self, secret: str, token: str) -> bool:
        """
        Verify 2FA token with Swiss precision!
        More accurate than a atomic clock! ⏰🎯
        """
        try:
            totp = pyotp.TOTP(secret)
            is_valid = totp.verify(token, valid_window=1)  # Allow 1 window (30 seconds) tolerance
            
            logger.debug(f"🔍 2FA token verification: {'SUCCESS' if is_valid else 'FAILED'}")
            return is_valid
            
        except Exception as e:
            logger.error(f"💥 2FA verification error: {e}")
            return False
    
    def generate_password_reset_token(self, user_id: int, email: str) -> str:
        """
        Generate secure password reset token!
        More secure than a vault with trust issues! 🔑🔐
        """
        try:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.config.reset_token_expire_minutes)
            
            to_encode = {
                "user_id": user_id,
                "email": email,
                "exp": expire,
                "iat": datetime.now(timezone.utc),
                "type": "password_reset",
                "jti": secrets.token_hex(16)
            }
            
            token = jwt.encode(to_encode, self.config.secret_key, algorithm=self.config.algorithm)
            
            logger.info(f"🔑 Password reset token generated for user: {user_id}")
            return token
            
        except Exception as e:
            logger.error(f"💥 Password reset token generation error: {e}")
            raise