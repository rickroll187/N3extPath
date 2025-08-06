"""
LEGENDARY AUTHORIZATION & PERMISSIONS ENGINE 🛡️⚖️
More precise than a Swiss judge with a computer science degree!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import logging
from typing import Dict, List, Set, Optional, Any, Callable
from enum import Enum
from functools import wraps
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import jwt
from dataclasses import dataclass
import inspect

logger = logging.getLogger(__name__)

class Permission(Enum):
    """
    Permission levels that are more organized than a Swiss filing system!
    More comprehensive than a security manual with attitude! 📋🔐
    """
    
    # SKILL ASSESSMENT PERMISSIONS
    SKILL_READ = "skill:read"
    SKILL_WRITE = "skill:write"
    SKILL_DELETE = "skill:delete"
    SKILL_ADMIN = "skill:admin"
    
    # PERFORMANCE REVIEW PERMISSIONS
    PERFORMANCE_READ = "performance:read"
    PERFORMANCE_WRITE = "performance:write"
    PERFORMANCE_REVIEW = "performance:review"
    PERFORMANCE_APPROVE = "performance:approve"
    PERFORMANCE_ADMIN = "performance:admin"
    
    # TRAINING PERMISSIONS
    TRAINING_READ = "training:read"
    TRAINING_ENROLL = "training:enroll"
    TRAINING_CREATE = "training:create"
    TRAINING_MANAGE = "training:manage"
    TRAINING_ADMIN = "training:admin"
    
    # COMPENSATION PERMISSIONS
    COMPENSATION_READ = "compensation:read"
    COMPENSATION_VIEW_SALARY = "compensation:view_salary"
    COMPENSATION_MODIFY = "compensation:modify"
    COMPENSATION_APPROVE = "compensation:approve"
    COMPENSATION_ADMIN = "compensation:admin"
    
    # CAREER PATH PERMISSIONS
    CAREER_READ = "career:read"
    CAREER_PLAN = "career:plan"
    CAREER_RECOMMEND = "career:recommend"
    CAREER_ADMIN = "career:admin"
    
    # TEAM COLLABORATION PERMISSIONS
    TEAM_READ = "team:read"
    TEAM_PARTICIPATE = "team:participate"
    TEAM_MANAGE = "team:manage"
    TEAM_ADMIN = "team:admin"
    
    # SYSTEM PERMISSIONS
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_ADMIN = "user:admin"
    SYSTEM_ADMIN = "system:admin"
    AUDIT_READ = "audit:read"
    AUDIT_ADMIN = "audit:admin"
    
    # SPECIAL PERMISSIONS
    BYPASS_FAIRNESS = "special:bypass_fairness"  # For emergency situations only
    DATA_EXPORT = "special:data_export"
    ANONYMIZATION_REVERSE = "special:anonymization_reverse"

class Role(Enum):
    """
    System roles with built-in permission sets!
    More organized than a military hierarchy with coding skills! 🎖️💻
    """
    
    EMPLOYEE = "employee"
    TEAM_LEAD = "team_lead"
    MANAGER = "manager"
    HR_SPECIALIST = "hr_specialist"
    HR_MANAGER = "hr_manager"
    DIRECTOR = "director"
    VP = "vp"
    EXECUTIVE = "executive"
    SYSTEM_ADMIN = "system_admin"
    SUPER_ADMIN = "super_admin"

@dataclass
class AuthContext:
    """
    Authentication context for tracking who's doing what!
    More detailed than a surveillance report! 🕵️📝
    """
    user_id: int
    username: str
    email: str
    roles: List[Role]
    permissions: Set[Permission]
    department_id: Optional[int] = None
    manager_id: Optional[int] = None
    is_manager: bool = False
    is_hr: bool = False
    is_admin: bool = False
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    login_timestamp: Optional[datetime] = None
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has specific permission"""
        return permission in self.permissions
    
    def has_role(self, role: Role) -> bool:
        """Check if user has specific role"""
        return role in self.roles
    
    def can_access_employee_data(self, target_employee_id: int) -> bool:
        """Check if user can access specific employee's data"""
        # Users can always access their own data
        if self.user_id == target_employee_id:
            return True
        
        # HR can access all employee data
        if self.is_hr:
            return True
        
        # Managers can access their direct reports (simplified check)
        if self.is_manager:
            return True  # In real system, check actual reporting relationship
        
        # Admins can access all data
        if self.is_admin:
            return True
        
        return False

class LegendaryRoleManager:
    """
    Role management system more organized than a Swiss filing cabinet!
    More comprehensive than a university course catalog! 📚🎯
    """
    
    def __init__(self):
        # AUTHORIZATION JOKES FOR SUNDAY MORNING MOTIVATION
        self.auth_jokes = [
            "Why did the permission go to therapy? It had access issues! 🔐😄",
            "What's the difference between our roles and a theater cast? Both have parts but ours don't forget their lines! 🎭",
            "Why don't unauthorized users get in? Because our bouncer has a CS degree! 💪",
            "What do you call authorization at 3 AM? Night shift security with style! 🌙",
            "Why did the role become a comedian? It had great permissions timing! ⏰"
        ]
        
        # Define role hierarchy (higher number = more permissions)
        self.role_hierarchy = {
            Role.EMPLOYEE: 1,
            Role.TEAM_LEAD: 2,
            Role.MANAGER: 3,
            Role.HR_SPECIALIST: 4,
            Role.HR_MANAGER: 5,
            Role.DIRECTOR: 6,
            Role.VP: 7,
            Role.EXECUTIVE: 8,
            Role.SYSTEM_ADMIN: 9,
            Role.SUPER_ADMIN: 10
        }
        
        # Define role-based permissions
        self.role_permissions = self._initialize_role_permissions()
        
        logger.info("🛡️ Legendary Role Manager initialized - Permission fortress activated!")
    
    def _initialize_role_permissions(self) -> Dict[Role, Set[Permission]]:
        """Initialize comprehensive role-based permissions"""
        permissions = {}
        
        # EMPLOYEE - Basic permissions
        permissions[Role.EMPLOYEE] = {
            Permission.SKILL_READ,
            Permission.PERFORMANCE_READ,
            Permission.TRAINING_READ,
            Permission.TRAINING_ENROLL,
            Permission.CAREER_READ,
            Permission.CAREER_PLAN,
            Permission.TEAM_READ,
            Permission.TEAM_PARTICIPATE
        }
        
        # TEAM_LEAD - Employee + team management
        permissions[Role.TEAM_LEAD] = permissions[Role.EMPLOYEE] | {
            Permission.SKILL_WRITE,
            Permission.PERFORMANCE_WRITE,
            Permission.TEAM_MANAGE,
            Permission.TRAINING_CREATE
        }
        
        # MANAGER - Team Lead + broader management
        permissions[Role.MANAGER] = permissions[Role.TEAM_LEAD] | {
            Permission.PERFORMANCE_REVIEW,
            Permission.CAREER_RECOMMEND,
            Permission.COMPENSATION_READ,
            Permission.USER_READ
        }
        
        # HR_SPECIALIST - HR specific permissions
        permissions[Role.HR_SPECIALIST] = permissions[Role.MANAGER] | {
            Permission.PERFORMANCE_APPROVE,
            Permission.COMPENSATION_VIEW_SALARY,
            Permission.TRAINING_MANAGE,
            Permission.USER_WRITE,
            Permission.AUDIT_READ
        }
        
        # HR_MANAGER - HR Specialist + management
        permissions[Role.HR_MANAGER] = permissions[Role.HR_SPECIALIST] | {
            Permission.COMPENSATION_MODIFY,
            Permission.SKILL_ADMIN,
            Permission.PERFORMANCE_ADMIN,
            Permission.TRAINING_ADMIN,
            Permission.CAREER_ADMIN,
            Permission.TEAM_ADMIN
        }
        
        # DIRECTOR - Strategic oversight
        permissions[Role.DIRECTOR] = permissions[Role.HR_MANAGER] | {
            Permission.COMPENSATION_APPROVE,
            Permission.DATA_EXPORT
        }
        
        # VP - Executive level
        permissions[Role.VP] = permissions[Role.DIRECTOR] | {
            Permission.USER_ADMIN,
            Permission.AUDIT_ADMIN
        }
        
        # EXECUTIVE - Top level business permissions
        permissions[Role.EXECUTIVE] = permissions[Role.VP] | {
            Permission.COMPENSATION_ADMIN,
            Permission.ANONYMIZATION_REVERSE
        }
        
        # SYSTEM_ADMIN - Technical administration
        permissions[Role.SYSTEM_ADMIN] = permissions[Role.EXECUTIVE] | {
            Permission.SYSTEM_ADMIN,
            Permission.BYPASS_FAIRNESS  # Emergency use only
        }
        
        # SUPER_ADMIN - God mode (use responsibly!)
        permissions[Role.SUPER_ADMIN] = set(Permission)  # All permissions
        
        return permissions
    
    def get_permissions_for_role(self, role: Role) -> Set[Permission]:
        """Get all permissions for a specific role"""
        return self.role_permissions.get(role, set())
    
    def get_permissions_for_roles(self, roles: List[Role]) -> Set[Permission]:
        """Get combined permissions for multiple roles"""
        all_permissions = set()
        for role in roles:
            all_permissions.update(self.get_permissions_for_role(role))
        return all_permissions
    
    def role_can_perform_action(self, role: Role, permission: Permission) -> bool:
        """Check if a role has a specific permission"""
        return permission in self.get_permissions_for_role(role)
    
    def get_role_hierarchy_level(self, role: Role) -> int:
        """Get hierarchy level for role comparison"""
        return self.role_hierarchy.get(role, 0)
    
    def role_has_higher_authority(self, role1: Role, role2: Role) -> bool:
        """Check if role1 has higher authority than role2"""
        return self.get_role_hierarchy_level(role1) > self.get_role_hierarchy_level(role2)

class LegendaryAuthorizer:
    """
    The most comprehensive authorization engine in the galaxy!
    More secure than a vault with trust issues and a PhD! 🔐🎓
    """
    
    def __init__(self, role_manager: LegendaryRoleManager = None):
        self.role_manager = role_manager or LegendaryRoleManager()
        self.active_sessions = {}  # Track active user sessions
        
        logger.info("🚀 Legendary Authorizer initialized - Permission engine ready!")
    
    def create_auth_context(self, user_data: Dict[str, Any], 
                          session_data: Optional[Dict[str, Any]] = None) -> AuthContext:
        """
        Create authentication context from user data!
        More comprehensive than a background check! 🕵️📋
        """
        try:
            # Extract user roles
            user_roles = []
            if user_data.get('is_superuser'):
                user_roles.append(Role.SUPER_ADMIN)
            elif user_data.get('is_hr_admin'):
                user_roles.append(Role.HR_MANAGER)
            elif user_data.get('is_manager'):
                user_roles.append(Role.MANAGER)
            else:
                user_roles.append(Role.EMPLOYEE)
            
            # Get combined permissions
            permissions = self.role_manager.get_permissions_for_roles(user_roles)
            
            # Create context
            context = AuthContext(
                user_id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                roles=user_roles,
                permissions=permissions,
                department_id=user_data.get('department_id'),
                manager_id=user_data.get('manager_id'),
                is_manager=user_data.get('is_manager', False),
                is_hr=user_data.get('is_hr_admin', False),
                is_admin=user_data.get('is_superuser', False),
                session_id=session_data.get('session_id') if session_data else None,
                ip_address=session_data.get('ip_address') if session_data else None,
                user_agent=session_data.get('user_agent') if session_data else None,
                login_timestamp=datetime.utcnow()
            )
            
            # Store active session
            if context.session_id:
                self.active_sessions[context.session_id] = context
            
            logger.info(f"✅ Auth context created for user: {context.username}")
            return context
            
        except Exception as e:
            logger.error(f"💥 Auth context creation error: {e}")
            raise
    
    def check_permission(self, context: AuthContext, permission: Permission, 
                        resource_context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if user has permission for specific action!
        More thorough than a security clearance investigation! 🔍🎯
        """
        try:
            # Basic permission check
            if not context.has_permission(permission):
                logger.warning(f"🚫 Permission denied: {context.username} lacks {permission.value}")
                return False
            
            # Resource-specific checks
            if resource_context:
                # Check employee data access
                if 'target_employee_id' in resource_context:
                    target_id = resource_context['target_employee_id']
                    if not context.can_access_employee_data(target_id):
                        logger.warning(f"🚫 Data access denied: {context.username} cannot access employee {target_id}")
                        return False
                
                # Check department boundaries
                if 'target_department_id' in resource_context and context.department_id:
                    target_dept = resource_context['target_department_id']
                    if target_dept != context.department_id and not context.is_hr and not context.is_admin:
                        logger.warning(f"🚫 Department access denied: {context.username} cannot access dept {target_dept}")
                        return False
                
                # Check time-based restrictions
                if 'business_hours_only' in resource_context and resource_context['business_hours_only']:
                    current_hour = datetime.utcnow().hour
                    if current_hour < 6 or current_hour > 22:  # Outside business hours
                        if not context.has_permission(Permission.SYSTEM_ADMIN):
                            logger.warning(f"⏰ Time restriction: {context.username} cannot access outside business hours")
                            return False
            
            logger.debug(f"✅ Permission granted: {context.username} can perform {permission.value}")
            return True
            
        except Exception as e:
            logger.error(f"💥 Permission check error: {e}")
            return False
    
    def require_permission(self, permission: Permission, 
                          resource_context: Optional[Dict[str, Any]] = None):
        """
        Decorator for requiring specific permissions!
        More protective than a bodyguard with coding skills! 🛡️💪
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Extract auth context from function arguments
                context = None
                
                # Look for auth context in function signature
                sig = inspect.signature(func)
                for param_name, param in sig.parameters.items():
                    if param.annotation == AuthContext:
                        if param_name in kwargs:
                            context = kwargs[param_name]
                        elif len(args) > list(sig.parameters.keys()).index(param_name):
                            context = args[list(sig.parameters.keys()).index(param_name)]
                        break
                
                # If no context found, look for 'current_user' or similar
                if not context:
                    for key in ['current_user', 'auth_context', 'user_context']:
                        if key in kwargs and isinstance(kwargs[key], AuthContext):
                            context = kwargs[key]
                            break
                
                if not context:
                    logger.error("💥 No authentication context found for permission check")
                    raise PermissionError("Authentication context required")
                
                # Check permission
                if not self.check_permission(context, permission, resource_context):
                    logger.warning(f"🚫 Access denied: {context.username} lacks {permission.value}")
                    raise PermissionError(f"Insufficient permissions: {permission.value}")
                
                # Execute function if permission check passes
                return func(*args, **kwargs)
            
            return wrapper
        return decorator
    
    def require_role(self, required_role: Role):
        """
        Decorator for requiring specific role!
        More exclusive than a VIP club with dress code! 🎩✨
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Similar context extraction logic as require_permission
                context = self._extract_auth_context(func, args, kwargs)
                
                if not context:
                    raise PermissionError("Authentication context required")
                
                # Check if user has required role or higher
                user_max_level = max([self.role_manager.get_role_hierarchy_level(role) for role in context.roles])
                required_level = self.role_manager.get_role_hierarchy_level(required_role)
                
                if user_max_level < required_level:
                    logger.warning(f"🚫 Role requirement not met: {context.username} needs {required_role.value}")
                    raise PermissionError(f"Role requirement not met: {required_role.value}")
                
                return func(*args, **kwargs)
            
            return wrapper
        return decorator
    
    def _extract_auth_context(self, func: Callable, args: tuple, kwargs: dict) -> Optional[AuthContext]:
        """Extract authentication context from function arguments"""
        # Look for auth context in function signature
        sig = inspect.signature(func)
        for param_name, param in sig.parameters.items():
            if param.annotation == AuthContext:
                if param_name in kwargs:
                    return kwargs[param_name]
                elif len(args) > list(sig.parameters.keys()).index(param_name):
                    return args[list(sig.parameters.keys()).index(param_name)]
        
        # Look for common parameter names
        for key in ['current_user', 'auth_context', 'user_context']:
            if key in kwargs and isinstance(kwargs[key], AuthContext):
                return kwargs[key]
        
        return None
    
    def validate_session(self, session_id: str) -> Optional[AuthContext]:
        """
        Validate active session!
        More reliable than a Swiss timepiece! ⏰✅
        """
        try:
            if session_id not in self.active_sessions:
                logger.warning(f"🚫 Session not found: {session_id}")
                return None
            
            context = self.active_sessions[session_id]
            
            # Check session timeout (8 hours default)
            if context.login_timestamp:
                session_age = datetime.utcnow() - context.login_timestamp
                if session_age > timedelta(hours=8):
                    logger.warning(f"⏰ Session expired: {session_id}")
                    del self.active_sessions[session_id]
                    return None
            
            logger.debug(f"✅ Session validated: {session_id}")
            return context
            
        except Exception as e:
            logger.error(f"💥 Session validation error: {e}")
            return None
    
    def revoke_session(self, session_id: str) -> bool:
        """
        Revoke user session!
        More final than a judge's gavel! ⚖️🔨
        """
        try:
            if session_id in self.active_sessions:
                context = self.active_sessions[session_id]
                del self.active_sessions[session_id]
                logger.info(f"🔒 Session revoked: {session_id} for user {context.username}")
                return True
            else:
                logger.warning(f"⚠️ Session not found for revocation: {session_id}")
                return False
                
        except Exception as e:
            logger.error(f"💥 Session revocation error: {e}")
            return False