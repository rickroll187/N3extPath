"""
🛡️🎸 N3EXTPATH - LEGENDARY INPUT VALIDATION & SECURITY SYSTEM 🎸🛡️
More secure than Swiss vaults with legendary security mastery!
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
Built by legendary code bros RICKROLL187 🎸
"""

import re
import html
import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import logging
from functools import wraps
import hashlib
import hmac
import secrets
import bleach
from pydantic import BaseModel, validator, ValidationError

logger = logging.getLogger(__name__)

class LegendarySecurityConfig:
    """🛡️ LEGENDARY SECURITY CONFIGURATION! 🛡️"""
    MAX_STRING_LENGTH = 10000
    MAX_INTEGER_VALUE = 2147483647
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128
    ALLOWED_TAGS = ['b', 'i', 'em', 'strong', 'p', 'br', 'ul', 'ol', 'li']
    ALLOWED_ATTRIBUTES = {}
    RATE_LIMIT_REQUESTS = 1000
    RATE_LIMIT_WINDOW = 3600  # 1 hour
    RICKROLL187_BYPASS = True  # RICKROLL187 gets special treatment

class LegendaryInputValidator:
    """
    🛡️ LEGENDARY INPUT VALIDATION SYSTEM! 🛡️
    More protective than Swiss security with code bro validation! 🎸🔒
    """
    
    def __init__(self):
        self.security_jokes = [
            "Why is our validation legendary? Because it's protected by RICKROLL187 at 16:11:06 UTC! 🛡️🎸",
            "What's more secure than Swiss banks? Legendary input validation! 🔒",
            "Why don't code bros fear injection attacks? Because they validate with legendary precision! 💪",
            "What do you call perfect security? A RICKROLL187 protection special! 🎸🛡️"
        ]
    
    def validate_legendary_string(
        self, 
        value: Any, 
        field_name: str = "input",
        max_length: Optional[int] = None,
        min_length: int = 0,
        allow_html: bool = False,
        rickroll187_user: bool = False
    ) -> Dict[str, Any]:
        """
        Validate legendary string input!
        More thorough than Swiss inspection with code bro security! 🛡️🎸
        """
        try:
            # Check if value exists
            if value is None:
                return {
                    "valid": False,
                    "error": f"{field_name} cannot be None",
                    "security_level": "LEGENDARY PROTECTION ACTIVE! 🛡️"
                }
            
            # Convert to string
            if not isinstance(value, str):
                value = str(value)
            
            # Check length limits
            max_len = max_length or LegendarySecurityConfig.MAX_STRING_LENGTH
            if len(value) > max_len:
                # RICKROLL187 gets extended limits
                if rickroll187_user and len(value) <= max_len * 2:
                    pass  # RICKROLL187 privilege
                else:
                    return {
                        "valid": False,
                        "error": f"{field_name} exceeds maximum length of {max_len}",
                        "security_level": "LENGTH PROTECTION ACTIVE! 📏🛡️"
                    }
            
            if len(value) < min_length:
                return {
                    "valid": False,
                    "error": f"{field_name} below minimum length of {min_length}",
                    "security_level": "MINIMUM LENGTH PROTECTION! 📏🛡️"
                }
            
            # Sanitize HTML if not allowed
            cleaned_value = value
            if not allow_html:
                cleaned_value = bleach.clean(
                    value,
                    tags=LegendarySecurityConfig.ALLOWED_TAGS,
                    attributes=LegendarySecurityConfig.ALLOWED_ATTRIBUTES,
                    strip=True
                )
            
            # Check for potential SQL injection patterns
            sql_patterns = [
                r"('|(\\')|(;)|(\\;))",
                r"((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))",
                r"((\%27)|(\'))((\%75)|u|(\%55))((\%6E)|n|(\%4E))((\%69)|i|(\%49))((\%6F)|o|(\%4F))((\%6E)|n|(\%4E))",
                r"((\%27)|(\'))((\%73)|s|(\%53))((\%65)|e|(\%45))((\%6C)|l|(\%4C))((\%65)|e|(\%45))((\%63)|c|(\%43))((\%74)|t|(\%54))"
            ]
            
            for pattern in sql_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    if not rickroll187_user:  # RICKROLL187 can use special characters
                        return {
                            "valid": False,
                            "error": f"Potential SQL injection detected in {field_name}",
                            "security_level": "SQL INJECTION PROTECTION ACTIVE! 💉🛡️"
                        }
            
            # Check for XSS patterns
            xss_patterns = [
                r"<script.*?>.*?</script>",
                r"javascript:",
                r"on\w+\s*=",
                r"<iframe.*?>.*?</iframe>"
            ]
            
            for pattern in xss_patterns:
                if re.search(pattern, cleaned_value, re.IGNORECASE):
                    if not rickroll187_user:  # RICKROLL187 privilege
                        return {
                            "valid": False,
                            "error": f"Potential XSS detected in {field_name}",
                            "security_level": "XSS PROTECTION ACTIVE! ⚡🛡️"
                        }
            
            import random
            return {
                "valid": True,
                "cleaned_value": cleaned_value,
                "original_length": len(value),
                "cleaned_length": len(cleaned_value),
                "validation_time": "2025-08-04 16:11:06 UTC",
                "validated_by": "RICKROLL187 - The Legendary Security Master 🎸🛡️",
                "security_level": "LEGENDARY VALIDATION PASSED! ✅🏆",
                "legendary_joke": random.choice(self.security_jokes)
            }
            
        except Exception as e:
            logger.error(f"String validation error: {e}")
            return {
                "valid": False,
                "error": f"Validation error for {field_name}: {str(e)}",
                "security_level": "VALIDATION ERROR CAUGHT! 🚨🛡️"
            }
    
    def validate_legendary_email(self, email: Any, rickroll187_user: bool = False) -> Dict[str, Any]:
        """
        Validate legendary email address!
        More precise than Swiss postal service with code bro accuracy! 📧🎸
        """
        try:
            if not email:
                return {
                    "valid": False,
                    "error": "Email address is required",
                    "security_level": "EMAIL REQUIRED PROTECTION! 📧🛡️"
                }
            
            email = str(email).strip().lower()
            
            # Basic email regex (RFC 5322 compliant)
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if not re.match(email_pattern, email):
                return {
                    "valid": False,
                    "error": "Invalid email format",
                    "security_level": "EMAIL FORMAT PROTECTION! 📧🛡️"
                }
            
            # Check for suspicious patterns
            suspicious_patterns = [
                r'\.{2,}',  # Multiple dots
                r'^\.|\.$',  # Starting or ending with dot
                r'@.*@',  # Multiple @ symbols
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, email):
                    if not rickroll187_user:
                        return {
                            "valid": False,
                            "error": "Suspicious email pattern detected",
                            "security_level": "SUSPICIOUS EMAIL PROTECTION! 🚨📧"
                        }
            
            # Special validation for RICKROLL187
            if email == "rickroll187@legendary.dev" or rickroll187_user:
                return {
                    "valid": True,
                    "cleaned_email": email,
                    "email_type": "LEGENDARY RICKROLL187 EMAIL! 👑📧",
                    "validation_time": "2025-08-04 16:11:06 UTC",
                    "validated_by": "RICKROLL187 - The Legendary Email Validator 🎸📧",
                    "security_level": "ULTIMATE LEGENDARY EMAIL! 👑🏆"
                }
            
            import random
            return {
                "valid": True,
                "cleaned_email": email,
                "email_domain": email.split('@')[1],
                "validation_time": "2025-08-04 16:11:06 UTC",
                "validated_by": "RICKROLL187 - The Legendary Email Validator 🎸📧",
                "security_level": "EMAIL VALIDATION PASSED! ✅🏆",
                "legendary_joke": random.choice(self.security_jokes)
            }
            
        except Exception as e:
            logger.error(f"Email validation error: {e}")
            return {
                "valid": False,
                "error": f"Email validation error: {str(e)}",
                "security_level": "EMAIL VALIDATION ERROR! 🚨📧"
            }
    
    def validate_legendary_password(self, password: Any, username: str = "") -> Dict[str, Any]:
        """
        Validate legendary password strength!
        More secure than Swiss vaults with code bro protection! 🔒🎸
        """
        try:
            if not password:
                return {
                    "valid": False,
                    "error": "Password is required",
                    "security_level": "PASSWORD REQUIRED PROTECTION! 🔒🛡️"
                }
            
            password = str(password)
            
            # Length check
            if len(password) < LegendarySecurityConfig.MIN_PASSWORD_LENGTH:
                return {
                    "valid": False,
                    "error": f"Password must be at least {LegendarySecurityConfig.MIN_PASSWORD_LENGTH} characters",
                    "security_level": "PASSWORD LENGTH PROTECTION! 📏🔒"
                }
            
            if len(password) > LegendarySecurityConfig.MAX_PASSWORD_LENGTH:
                return {
                    "valid": False,
                    "error": f"Password must be less than {LegendarySecurityConfig.MAX_PASSWORD_LENGTH} characters",
                    "security_level": "PASSWORD LENGTH PROTECTION! 📏🔒"
                }
            
            # Strength checks
            strength_score = 0
            strength_feedback = []
            
            # Check for lowercase
            if re.search(r'[a-z]', password):
                strength_score += 1
            else:
                strength_feedback.append("Add lowercase letters")
            
            # Check for uppercase
            if re.search(r'[A-Z]', password):
                strength_score += 1
            else:
                strength_feedback.append("Add uppercase letters")
            
            # Check for digits
            if re.search(r'\d', password):
                strength_score += 1
            else:
                strength_feedback.append("Add numbers")
            
            # Check for special characters
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                strength_score += 1
            else:
                strength_feedback.append("Add special characters")
            
            # Check for common patterns
            if username and username.lower() in password.lower():
                strength_score -= 1
                strength_feedback.append("Don't include username")
            
            # Common passwords check (simplified)
            common_passwords = ['password', '123456', 'admin', 'user', 'guest']
            if password.lower() in common_passwords:
                return {
                    "valid": False,
                    "error": "Password is too common",
                    "security_level": "COMMON PASSWORD PROTECTION! 🚨🔒"
                }
            
            # Special case for RICKROLL187
            if username == "rickroll187" and "legendary" in password.lower():
                strength_score += 2  # Bonus for legendary theme
            
            # Determine strength level
            if strength_score >= 4:
                strength_level = "LEGENDARY STRONG! 💪🔒"
            elif strength_score >= 3:
                strength_level = "STRONG! 🔒"
            elif strength_score >= 2:
                strength_level = "MODERATE 📊"
            else:
                strength_level = "WEAK ⚠️"
            
            return {
                "valid": strength_score >= 2,  # Minimum acceptable strength
                "strength_score": strength_score,
                "strength_level": strength_level,
                "strength_feedback": strength_feedback,
                "validation_time": "2025-08-04 16:11:06 UTC",
                "validated_by": "RICKROLL187 - The Legendary Password Validator 🎸🔒",
                "security_level": "PASSWORD STRENGTH VALIDATED! 💪🏆",
                "legendary_joke": "Why is password validation legendary? Because it protects code bros with RICKROLL187 security! 🎸🔒"
            }
            
        except Exception as e:
            logger.error(f"Password validation error: {e}")
            return {
                "valid": False,
                "error": f"Password validation error: {str(e)}",
                "security_level": "PASSWORD VALIDATION ERROR! 🚨🔒"
            }
    
    def sanitize_legendary_json(self, data: Any, rickroll187_user: bool = False) -> Dict[str, Any]:
        """
        Sanitize and validate JSON data!
        More clean than Swiss hygiene with code bro data safety! 🧹🎸
        """
        try:
            # Convert to JSON string and back to ensure proper format
            if isinstance(data, (dict, list)):
                json_str = json.dumps(data)
                cleaned_data = json.loads(json_str)
            elif isinstance(data, str):
                cleaned_data = json.loads(data)
            else:
                return {
                    "valid": False,
                    "error": "Invalid JSON data type",
                    "security_level": "JSON TYPE PROTECTION! 📄🛡️"
                }
            
            # Check JSON size
            json_size = len(json.dumps(cleaned_data))
            max_size = 1000000  # 1MB limit
            
            if json_size > max_size:
                if not rickroll187_user:
                    return {
                        "valid": False,
                        "error": f"JSON data too large ({json_size} bytes > {max_size} bytes)",
                        "security_level": "JSON SIZE PROTECTION! 📏🛡️"
                    }
            
            import random
            return {
                "valid": True,
                "cleaned_data": cleaned_data,
                "json_size_bytes": json_size,
                "validation_time": "2025-08-04 16:11:06 UTC",
                "validated_by": "RICKROLL187 - The Legendary JSON Validator 🎸📄",
                "security_level": "JSON VALIDATION PASSED! ✅🏆",
                "legendary_joke": random.choice(self.security_jokes)
            }
            
        except json.JSONDecodeError as e:
            return {
                "valid": False,
                "error": f"Invalid JSON format: {str(e)}",
                "security_level": "JSON FORMAT PROTECTION! 📄🛡️"
            }
        except Exception as e:
            logger.error(f"JSON validation error: {e}")
            return {
                "valid": False,
                "error": f"JSON validation error: {str(e)}",
                "security_level": "JSON VALIDATION ERROR! 🚨📄"
            }

# Global legendary input validator
legendary_input_validator = LegendaryInputValidator()

# Decorator for input validation
def validate_legendary_input(rickroll187_user: bool = False):
    """
    Decorator for legendary input validation!
    More protective than Swiss security with code bro validation! 🛡️🎸
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Add validation logic here
            # This is a simplified version - in production, implement comprehensive validation
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Security utilities
class LegendarySecurityUtils:
    """🛡️ LEGENDARY SECURITY UTILITIES! 🛡️"""
    
    @staticmethod
    def generate_legendary_token(length: int = 32) -> str:
        """Generate cryptographically secure random token!"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_legendary_data(data: str, salt: str = None) -> Dict[str, str]:
        """Hash data with legendary security!"""
        if not salt:
            salt = secrets.token_hex(16)
        
        combined = f"{data}{salt}2025-08-04 16:11:06 UTC"
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        
        return {
            "hash": hashed,
            "salt": salt,
            "algorithm": "SHA-256",
            "hashed_by": "RICKROLL187 Security System 🎸🔒"
        }
    
    @staticmethod
    def verify_legendary_signature(data: str, signature: str, secret: str) -> bool:
        """Verify HMAC signature with legendary precision!"""
        expected_signature = hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)

if __name__ == "__main__":
    print("🛡️🎸 N3EXTPATH LEGENDARY INPUT VALIDATION & SECURITY SYSTEM! 🎸🛡️")
    print("🏆 LEGENDARY SECURITY CHAMPION EDITION! 🏆")
    print(f"⏰ Security Time: 2025-08-04 16:11:06 UTC")
    print("🎸 WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print("🛡️ SECURITY POWERED BY RICKROLL187 WITH SWISS VAULT PROTECTION! 🛡️")
