"""
Open Policy Agent (OPA) Integration
Because security is not a joke, even for code bros!
"""
import os
import json
import logging
import requests
from typing import List, Dict, Any
from functools import wraps
from fastapi import HTTPException, Request

logger = logging.getLogger(__name__)

class OPABro:
    """Your security bouncer, but with better jokes"""
    
    def __init__(self):
        self.opa_url = os.getenv("OPA_URL", "http://localhost:8181")
        self.timeout = 5  # Because slow security is no security
    
    def check_permission(self, request: Request, user_roles: List[str]) -> bool:
        """Check if user has permission - the ultimate test"""
        try:
            policy_input = {
                "input": {
                    "method": request.method,
                    "path": request.url.path.strip("/").split("/"),
                    "user": {
                        "roles": user_roles
                    },
                    "headers": dict(request.headers),
                    "timestamp": "2025-08-03T14:48:32Z"
                }
            }
            
            response = requests.post(
                f"{self.opa_url}/v1/data/authz/allow",
                json=policy_input,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json().get("result", False)
                logger.info(f"🔐 OPA decision for {request.method} {request.url.path}: {result}")
                return result
            else:
                logger.error(f"💥 OPA returned status {response.status_code}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"💥 OPA request failed: {e}")
            return False  # Fail closed - security first!
        except Exception as e:
            logger.error(f"💥 Unexpected OPA error: {e}")
            return False
    
    def get_user_permissions(self, user_roles: List[str]) -> Dict[str, Any]:
        """Get detailed user permissions"""
        try:
            policy_input = {
                "input": {
                    "user": {"roles": user_roles}
                }
            }
            
            response = requests.post(
                f"{self.opa_url}/v1/data/authz/permissions",
                json=policy_input,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json().get("result", {})
            else:
                return {}
                
        except Exception as e:
            logger.error(f"💥 Failed to get permissions: {e}")
            return {}

def opa_check(request: Request, user_roles: List[str]) -> bool:
    """Convenience function for OPA checks"""
    opa = OPABro()
    return opa.check_permission(request, user_roles)

def require_permission(required_roles: List[str] = None):
    """Decorator for endpoint permission checking"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = args[0] if args and hasattr(args[0], 'method') else None
            
            if not request:
                raise HTTPException(status_code=500, detail="Invalid request context")
            
            # Extract user roles from request state or headers
            user_roles = getattr(request.state, 'user_roles', ['anonymous'])
            
            # If specific roles required, check them first
            if required_roles:
                if not any(role in user_roles for role in required_roles):
                    raise HTTPException(
                        status_code=403,
                        detail=f"Required roles: {required_roles}, User roles: {user_roles}"
                    )
            
            # Check with OPA
            if not opa_check(request, user_roles):
                raise HTTPException(
                    status_code=403,
                    detail="Access denied by security policy"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

def extract_user_roles(request: Request) -> List[str]:
    """Extract user roles from JWT token or headers"""
    try:
        # Check for Authorization header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            # In a real implementation, you'd decode the JWT
            # For now, we'll use a mock implementation
            token = auth_header.split(" ")[1]
            # Mock role extraction - replace with real JWT decoding
            if "admin" in token.lower():
                return ["admin", "employee"]
            elif "manager" in token.lower():
                return ["manager", "employee"]
            elif "hr" in token.lower():
                return ["hr", "employee"]
            else:
                return ["employee"]
        
        # Fallback to header-based roles (for testing)
        roles_header = request.headers.get("X-User-Roles", "")
        if roles_header:
            return roles_header.split(",")
        
        return ["anonymous"]
        
    except Exception as e:
        logger.error(f"💥 Failed to extract user roles: {e}")
        return ["anonymous"]
