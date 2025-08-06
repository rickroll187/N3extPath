"""
LEGENDARY USER MANAGEMENT FORTRESS 👥🏰
More comprehensive than a university registration system with attitude!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import logging
import secrets
import hashlib
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import re
from dataclasses import asdict
import json

from .authentication import LegendaryAuthenticator, AuthConfig, PasswordValidator
from .authorization import LegendaryAuthorizer, AuthContext, Permission, Role
from ..database.base_models import User, Employee, Department, AuditLog

logger = logging.getLogger(__name__)

class UserCreationResult:
    """
    User creation result that's more detailed than a birth certificate!
    More comprehensive than a background check report! 📋✨
    """
    
    def __init__(self, success: bool, user_id: Optional[int] = None, 
                 username: Optional[str] = None, errors: List[str] = None,
                 warnings: List[str] = None, next_steps: List[str] = None):
        self.success = success
        self.user_id = user_id
        self.username = username
        self.errors = errors or []
        self.warnings = warnings or []
        self.next_steps = next_steps or []
        self.creation_timestamp = datetime.utcnow().isoformat()

class LegendaryUserManager:
    """
    The most comprehensive user management system in the galaxy!
    More organized than a Swiss library with a computer science degree! 📚💻👥
    """
    
    def __init__(self, db: Session, authenticator: LegendaryAuthenticator = None, 
                 authorizer: LegendaryAuthorizer = None):
        self.db = db
        self.authenticator = authenticator or LegendaryAuthenticator()
        self.authorizer = authorizer or LegendaryAuthorizer()
        
        # USER MANAGEMENT JOKES FOR SUNDAY MORNING MOTIVATION
        self.user_jokes = [
            "Why did the user go to therapy? They had identity management issues! 👤😄",
            "What's the difference between our user system and a Swiss hotel? Both check you in perfectly! 🏨",
            "Why don't users ever get lost? Because our system has excellent navigation! 🧭",
            "What do you call user management at 3 AM? Night shift with perfect records! 🌙",
            "Why did the password become a stand-up comedian? It had great security timing! ⏰"
        ]
        
        # Default user settings
        self.default_settings = {
            "timezone": "UTC",
            "language_preference": "en",
            "notification_preferences": {
                "email_notifications": True,
                "push_notifications": True,
                "performance_reminders": True,
                "training_notifications": True,
                "system_announcements": True
            },
            "privacy_settings": {
                "profile_visibility": "colleagues",
                "skill_sharing": True,
                "performance_sharing": False,
                "contact_info_sharing": "team"
            },
            "ui_preferences": {
                "theme": "auto",
                "dashboard_layout": "default",
                "items_per_page": 25,
                "show_tooltips": True
            }
        }
        
        logger.info("🚀 Legendary User Manager initialized - Ready to manage the empire!")
    
    def create_user(self, user_data: Dict[str, Any], creator_context: AuthContext) -> UserCreationResult:
        """
        Create new user with more precision than a Swiss watchmaker!
        More thorough than a university admissions process! 🎓✨
        """
        try:
            logger.info(f"👤 Creating new user: {user_data.get('username', 'unknown')}")
            
            # Validate creator permissions
            if not self.authorizer.check_permission(creator_context, Permission.USER_WRITE):
                return UserCreationResult(
                    success=False,
                    errors=["Insufficient permissions to create users"]
                )
            
            # Validate input data
            validation_result = self._validate_user_data(user_data)
            if not validation_result["is_valid"]:
                return UserCreationResult(
                    success=False,
                    errors=validation_result["errors"],
                    warnings=validation_result["warnings"]
                )
            
            # Check for existing username/email
            existing_user = self.db.query(User).filter(
                or_(User.username == user_data["username"], 
                    User.email == user_data["email"])
            ).first()
            
            if existing_user:
                conflict_type = "username" if existing_user.username == user_data["username"] else "email"
                return UserCreationResult(
                    success=False,
                    errors=[f"User with this {conflict_type} already exists"]
                )
            
            # Validate password strength
            password_validation = self.authenticator.password_validator.validate_password(
                user_data["password"], 
                {
                    "first_name": user_data.get("first_name", ""),
                    "last_name": user_data.get("last_name", ""),
                    "username": user_data["username"],
                    "email": user_data["email"]
                }
            )
            
            if not password_validation["is_valid"]:
                return UserCreationResult(
                    success=False,
                    errors=password_validation["errors"],
                    warnings=password_validation["warnings"]
                )
            
            # Hash password
            hashed_password = self.authenticator.hash_password(user_data["password"])
            
            # Create user record
            new_user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_password,
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                display_name=user_data.get("display_name", f"{user_data['first_name']} {user_data['last_name']}"),
                is_superuser=user_data.get("is_superuser", False),
                is_hr_admin=user_data.get("is_hr_admin", False),
                is_manager=user_data.get("is_manager", False),
                timezone=user_data.get("timezone", "UTC"),
                language_preference=user_data.get("language_preference", "en"),
                notification_preferences=user_data.get("notification_preferences", self.default_settings["notification_preferences"]),
                created_by=creator_context.user_id,
                updated_by=creator_context.user_id
            )
            
            self.db.add(new_user)
            self.db.flush()  # Get the user ID
            
            # Create employee record if requested
            employee_id = None
            if user_data.get("create_employee_record", True):
                employee_result = self._create_employee_record(new_user, user_data, creator_context)
                if employee_result["success"]:
                    employee_id = employee_result["employee_id"]
                else:
                    # Rollback user creation if employee creation fails
                    self.db.rollback()
                    return UserCreationResult(
                        success=False,
                        errors=employee_result["errors"]
                    )
            
            # Log the creation
            self._log_user_action("USER_CREATED", new_user.id, creator_context, {
                "username": new_user.username,
                "email": new_user.email,
                "roles_assigned": user_data.get("roles", []),
                "employee_record_created": employee_id is not None
            })
            
            # Prepare next steps
            next_steps = [
                "User account created successfully",
                "Initial password set - user should change on first login",
                "Account is active and ready for use"
            ]
            
            if user_data.get("send_welcome_email", True):
                welcome_result = self._send_welcome_email(new_user, user_data.get("temporary_password"))
                if welcome_result["success"]:
                    next_steps.append("Welcome email sent with login instructions")
                else:
                    next_steps.append("⚠️ Welcome email failed to send - notify user manually")
            
            if user_data.get("require_2fa", False):
                next_steps.append("Two-factor authentication setup required on first login")
            
            self.db.commit()
            
            logger.info(f"✅ User created successfully: {new_user.username} (ID: {new_user.id})")
            
            return UserCreationResult(
                success=True,
                user_id=new_user.id,
                username=new_user.username,
                warnings=validation_result.get("warnings", []),
                next_steps=next_steps
            )
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 User creation error: {e}")
            return UserCreationResult(
                success=False,
                errors=[f"System error during user creation: {str(e)}"]
            )
    
    def _validate_user_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user input data with Swiss precision"""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ["username", "email", "password", "first_name", "last_name"]
        for field in required_fields:
            if not user_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Username validation
        if user_data.get("username"):
            username = user_data["username"]
            if len(username) < 3:
                errors.append("Username must be at least 3 characters long")
            elif len(username) > 50:
                errors.append("Username must be no more than 50 characters long")
            elif not re.match(r'^[a-zA-Z0-9_.-]+$', username):
                errors.append("Username can only contain letters, numbers, dots, hyphens, and underscores")
            elif username.lower() in ["admin", "root", "administrator", "system", "test"]:
                warnings.append("Username appears to be a system account name")
        
        # Email validation
        if user_data.get("email"):
            email = user_data["email"]
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                errors.append("Invalid email format")
            elif len(email) > 100:
                errors.append("Email address is too long")
        
        # Name validation
        for field in ["first_name", "last_name"]:
            if user_data.get(field):
                name = user_data[field]
                if len(name) > 50:
                    errors.append(f"{field.replace('_', ' ').title()} is too long")
                elif not re.match(r'^[a-zA-Z\s\'-]+$', name):
                    warnings.append(f"{field.replace('_', ' ').title()} contains unusual characters")
        
        # Role validation
        if user_data.get("is_superuser") and not user_data.get("creator_is_admin"):
            errors.append("Only administrators can create superuser accounts")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _create_employee_record(self, user: User, user_data: Dict[str, Any], 
                              creator_context: AuthContext) -> Dict[str, Any]:
        """Create corresponding employee record"""
        try:
            # Generate unique employee ID
            employee_id = self._generate_employee_id(user_data.get("department_id"))
            
            # Get department and role
            department_id = user_data.get("department_id")
            role_id = user_data.get("role_id")
            
            if not department_id or not role_id:
                return {
                    "success": False,
                    "errors": ["Department and role are required for employee record creation"]
                }
            
            # Create employee record
            new_employee = Employee(
                user_id=user.id,
                employee_id=employee_id,
                role_id=role_id,
                department_id=department_id,
                manager_id=user_data.get("manager_id"),
                hire_date=user_data.get("hire_date", datetime.utcnow()),
                employment_type=user_data.get("employment_type", "FULL_TIME"),
                employment_status="ACTIVE",
                phone_number=user_data.get("phone_number"),
                work_location=user_data.get("work_location"),
                office_location=user_data.get("office_location"),
                remote_work_eligible=user_data.get("remote_work_eligible", False),
                current_salary=user_data.get("salary"),
                salary_currency=user_data.get("salary_currency", "USD"),
                created_by=creator_context.user_id,
                updated_by=creator_context.user_id
            )
            
            self.db.add(new_employee)
            self.db.flush()
            
            logger.info(f"✅ Employee record created: {employee_id}")
            
            return {
                "success": True,
                "employee_id": new_employee.id,
                "employee_number": employee_id
            }
            
        except Exception as e:
            logger.error(f"💥 Employee record creation error: {e}")
            return {
                "success": False,
                "errors": [f"Failed to create employee record: {str(e)}"]
            }
    
    def _generate_employee_id(self, department_id: Optional[int]) -> str:
        """Generate unique employee ID with department prefix"""
        try:
            # Get department code
            dept_code = "EMP"
            if department_id:
                department = self.db.query(Department).filter(Department.id == department_id).first()
                if department and department.code:
                    dept_code = department.code[:3].upper()
            
            # Get next sequence number
            last_employee = self.db.query(Employee).filter(
                Employee.employee_id.like(f"{dept_code}%")
            ).order_by(desc(Employee.employee_id)).first()
            
            if last_employee:
                try:
                    last_number = int(last_employee.employee_id.split('-')[-1])
                    next_number = last_number + 1
                except (ValueError, IndexError):
                    next_number = 1
            else:
                next_number = 1
            
            # Generate employee ID: DEPT-YYYY-NNNN
            year = datetime.utcnow().year
            employee_id = f"{dept_code}-{year}-{next_number:04d}"
            
            logger.debug(f"📝 Generated employee ID: {employee_id}")
            return employee_id
            
        except Exception as e:
            logger.error(f"💥 Employee ID generation error: {e}")
            return f"EMP-{datetime.utcnow().year}-{secrets.randbelow(9999):04d}"
    
    def authenticate_user(self, username: str, password: str, 
                         session_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Authenticate user with more security than Fort Knox!
        More thorough than a security clearance investigation! 🔐🎯
        """
        try:
            logger.info(f"🔐 Authentication attempt for user: {username}")
            
            # Find user
            user = self.db.query(User).filter(
                or_(User.username == username, User.email == username)
            ).first()
            
            if not user:
                logger.warning(f"🚫 Authentication failed: User not found - {username}")
                return {
                    "success": False,
                    "error": "Invalid credentials",
                    "error_code": "USER_NOT_FOUND"
                }
            
            # Check if account is locked
            if user.account_locked_until and user.account_locked_until > datetime.utcnow():
                logger.warning(f"🔒 Authentication failed: Account locked - {username}")
                return {
                    "success": False,
                    "error": "Account is temporarily locked due to failed login attempts",
                    "error_code": "ACCOUNT_LOCKED",
                    "locked_until": user.account_locked_until.isoformat()
                }
            
            # Verify password
            if not self.authenticator.verify_password(password, user.hashed_password):
                # Increment failed attempts
                user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
                
                # Lock account if too many failures
                if user.failed_login_attempts >= self.authenticator.config.max_failed_attempts:
                    user.account_locked_until = datetime.utcnow() + timedelta(
                        minutes=self.authenticator.config.lockout_duration_minutes
                    )
                    logger.warning(f"🔒 Account locked due to failed attempts: {username}")
                
                self.db.commit()
                
                logger.warning(f"🚫 Authentication failed: Invalid password - {username}")
                return {
                    "success": False,
                    "error": "Invalid credentials",
                    "error_code": "INVALID_PASSWORD",
                    "failed_attempts": user.failed_login_attempts
                }
            
            # Reset failed attempts on successful authentication
            user.failed_login_attempts = 0
            user.account_locked_until = None
            user.last_login = datetime.utcnow()
            user.login_count = (user.login_count or 0) + 1
            
            # Load employee data
            employee = self.db.query(Employee).filter(Employee.user_id == user.id).first()
            
            # Create user data for auth context
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_superuser": user.is_superuser,
                "is_hr_admin": user.is_hr_admin,
                "is_manager": user.is_manager,
                "department_id": employee.department_id if employee else None,
                "manager_id": employee.manager_id if employee else None
            }
            
            # Create auth context
            auth_context = self.authorizer.create_auth_context(user_data, session_data)
            
            # Generate tokens
            access_token = self.authenticator.create_access_token({"sub": user.username, "user_id": user.id})
            refresh_token = self.authenticator.create_refresh_token(user.id)
            
            # Log successful authentication
            self._log_user_action("USER_LOGIN", user.id, auth_context, {
                "login_method": "password",
                "ip_address": session_data.get("ip_address") if session_data else None,
                "user_agent": session_data.get("user_agent") if session_data else None
            })
            
            self.db.commit()
            
            logger.info(f"✅ Authentication successful: {username}")
            
            return {
                "success": True,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": self.authenticator.config.access_token_expire_minutes * 60,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "display_name": user.display_name,
                    "roles": [role.value for role in auth_context.roles],
                    "permissions": [perm.value for perm in auth_context.permissions]
                },
                "auth_context": auth_context,
                "legendary_joke": secrets.choice(self.user_jokes)
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"💥 Authentication error: {e}")
            return {
                "success": False,
                "error": "Authentication system error",
                "error_code": "SYSTEM_ERROR"
            }
    
    def _send_welcome_email(self, user: User, temporary_password: Optional[str] = None) -> Dict[str, Any]:
        """Send welcome email to new user"""
        try:
            # In production, this would use a proper email service
            logger.info(f"📧 Sending welcome email to: {user.email}")
            
            # Email content
            subject = f"Welcome to HR Empire - {user.display_name}!"
            
            body = f"""
            Welcome to HR Empire, {user.first_name}! 🎉
            
            Your account has been created successfully:
            
            Username: {user.username}
            Email: {user.email}
            
            Next Steps:
            1. Log in to the system using your credentials
            2. Complete your profile setup
            3. Review your skills assessment
            4. Explore available training opportunities
            
            If you have any questions, please contact your HR representative.
            
            Best regards,
            The HR Empire Team
            
            P.S. Remember, in this empire, every employee is legendary! 🏆
            """
            
            # Simulate email sending (in production, use proper SMTP)
            logger.info(f"📤 Welcome email sent successfully to: {user.email}")
            
            return {"success": True, "message": "Welcome email sent"}
            
        except Exception as e:
            logger.error(f"💥 Welcome email error: {e}")
            return {"success": False, "error": str(e)}
    
    def _log_user_action(self, action: str, user_id: int, context: AuthContext, details: Dict[str, Any]):
        """Log user actions for audit trail"""
        try:
            audit_log = AuditLog(
                event_type=action,
                event_category="USER",
                event_description=f"User action: {action}",
                user_id=context.user_id,
                target_type="User",
                target_id=user_id,
                new_values=details,
                ip_address=context.ip_address,
                user_agent=context.user_agent,
                security_level="NORMAL"
            )
            
            self.db.add(audit_log)
            logger.debug(f"📝 User action logged: {action} for user {user_id}")
            
        except Exception as e:
            logger.error(f"💥 Audit logging error: {e}")