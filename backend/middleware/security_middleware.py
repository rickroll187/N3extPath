# File: backend/middleware/security_middleware.py
"""
🛡️🎸 N3EXTPATH - LEGENDARY SECURITY MIDDLEWARE 🎸🛡️
Professional security middleware with Swiss precision protection
Built: 2025-08-05 18:09:21 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import time
import json
import hashlib
import secrets
from typing import Callable, Dict, Any, Optional, List
from fastapi import Request, Response, HTTPException, status
from fastapi.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import logging
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import ASGIApp
import redis
from datetime import datetime, timedelta, timezone
import ipaddress
import re
from urllib.parse import urlparse
import jwt

class LegendarySecurityMiddleware(BaseHTTPMiddleware):
    """Professional Security Middleware with Legendary Protection"""
    
    def __init__(self, app: ASGIApp, redis_client: redis.Redis = None):
        super().__init__(app)
        self.redis_client = redis_client
        self.logger = logging.getLogger(__name__)
        
        # Security configuration
        self.security_config = {
            "rate_limiting": {
                "enabled": True,
                "default_limit": 100,  # requests per window
                "window_seconds": 60,
                "legendary_multiplier": 5.0,  # 5x rate limit for RICKROLL187
                "burst_threshold": 150
            },
            "ip_filtering": {
                "enabled": True,
                "blocked_ips": set(),
                "allowed_ips": set(),
                "legendary_whitelist": True
            },
            "request_validation": {
                "max_request_size": 50 * 1024 * 1024,  # 50MB
                "max_url_length": 2048,
                "max_header_count": 50,
                "blocked_user_agents": [
                    "bot", "crawler", "spider", "scraper"
                ]
            },
            "content_security": {
                "sanitize_headers": True,
                "validate_content_type": True,
                "check_malicious_patterns": True,
                "legendary_protection": True
            },
            "ddos_protection": {
                "enabled": True,
                "connection_limit": 1000,
                "request_burst_limit": 50,
                "suspicious_threshold": 200
            }
        }
        
        # Security headers to add
        self.security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
            "X-Legendary-Security": "maximum",
            "X-Swiss-Precision": "enabled",
            "X-Built-By": "rickroll187"
        }
        
        # Malicious patterns to detect
        self.malicious_patterns = [
            # SQL Injection patterns
            r"(\b(union|select|insert|update|delete|drop|create|alter|exec|execute)\b)",
            r"(';|--|\||\*)",
            r"(\b(or|and)\b\s*\d+\s*[=<>]\s*\d+)",
            
            # XSS patterns
            r"(<script|</script|javascript:|vbscript:|onload=|onerror=)",
            r"(<iframe|<object|<embed|<applet)",
            
            # Path traversal
            r"(\.\./|\.\.\\|%2e%2e%2f|%2e%2e%5c)",
            
            # Command injection
            r"([;&|`$(){}[\]\\])",
            
            # File inclusion
            r"(file://|ftp://|php://|data://)",
        ]
        
        # Compile regex patterns for performance
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.malicious_patterns]
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Main security middleware dispatch"""
        
        start_time = time.time()
        
        try:
            # Pre-request security checks
            security_check_result = await self._perform_security_checks(request)
            
            if not security_check_result["allowed"]:
                return JSONResponse(
                    status_code=security_check_result["status_code"],
                    content={"detail": security_check_result["message"]},
                    headers={"X-Security-Block": "true"}
                )
            
            # Add request metadata
            request.state.security_metadata = {
                "client_ip": self._get_client_ip(request),
                "user_agent": request.headers.get("user-agent", ""),
                "request_id": secrets.token_hex(8),
                "is_legendary": security_check_result.get("is_legendary", False),
                "security_level": security_check_result.get("security_level", "standard")
            }
            
            # Process request
            response = await call_next(request)
            
            # Post-request security enhancements
            response = await self._enhance_response_security(request, response)
            
            # Log security metrics
            await self._log_security_metrics(request, response, time.time() - start_time)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Security middleware error: {e}")
            
            # Return secure error response
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal security error"},
                headers=self.security_headers
            )
    
    async def _perform_security_checks(self, request: Request) -> Dict[str, Any]:
        """Perform comprehensive security checks"""
        
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "")
        path = request.url.path
        method = request.method
        
        # Check if this is a legendary user
        is_legendary = await self._check_legendary_user(request)
        
        # IP filtering check
        if not await self._check_ip_allowed(client_ip, is_legendary):
            return {
                "allowed": False,
                "status_code": 403,
                "message": "IP address blocked",
                "reason": "ip_blocked"
            }
        
        # Rate limiting check
        if not await self._check_rate_limit(client_ip, is_legendary):
            return {
                "allowed": False,
                "status_code": 429,
                "message": "Rate limit exceeded",
                "reason": "rate_limited"
            }
        
        # Request size validation
        if not await self._check_request_size(request):
            return {
                "allowed": False,
                "status_code": 413,
                "message": "Request too large",
                "reason": "request_too_large"
            }
        
        # URL validation
        if not self._check_url_validity(request):
            return {
                "allowed": False,
                "status_code": 400,
                "message": "Invalid URL format",
                "reason": "invalid_url"
            }
        
        # User agent validation
        if not self._check_user_agent(user_agent, is_legendary):
            return {
                "allowed": False,
                "status_code": 403,
                "message": "Blocked user agent",
                "reason": "blocked_user_agent"
            }
        
        # Malicious pattern detection
        if not await self._check_malicious_patterns(request):
            return {
                "allowed": False,
                "status_code": 400,
                "message": "Malicious content detected",
                "reason": "malicious_content"
            }
        
        # DDoS protection check
        if not await self._check_ddos_protection(client_ip):
            return {
                "allowed": False,
                "status_code": 503,
                "message": "Service temporarily unavailable",
                "reason": "ddos_protection"
            }
        
        return {
            "allowed": True,
            "is_legendary": is_legendary,
            "security_level": "legendary" if is_legendary else "standard"
        }
    
    def _get_client_ip(self, request: Request) -> str:
        """Get real client IP address"""
        
        # Check for forwarded headers
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        forwarded = request.headers.get("forwarded")
        if forwarded:
            # Parse forwarded header
            for item in forwarded.split(";"):
                if item.strip().startswith("for="):
                    return item.split("=")[1].strip().strip('"')
        
        # Fallback to client host
        return request.client.host if request.client else "unknown"
    
    async def _check_legendary_user(self, request: Request) -> bool:
        """Check if request is from legendary user RICKROLL187"""
        
        # Check Authorization header for JWT
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            try:
                token = auth_header.split(" ")[1]
                # This would integrate with your JWT verification
                # For now, return basic check
                return "rickroll187" in str(token).lower()
            except:
                pass
        
        # Check for legendary API key
        api_key = request.headers.get("x-legendary-key")
        if api_key:
            return await self._verify_legendary_api_key(api_key)
        
        return False
    
    async def _verify_legendary_api_key(self, api_key: str) -> bool:
        """Verify legendary API key"""
        # This would check against stored legendary API keys
        legendary_keys = [
            "legendary_rickroll187_master_key",
            "swiss_precision_founder_key",
            "code_bro_ultimate_access"
        ]
        return api_key in legendary_keys
    
    async def _check_ip_allowed(self, client_ip: str, is_legendary: bool) -> bool:
        """Check if IP address is allowed"""
        
        if not self.security_config["ip_filtering"]["enabled"]:
            return True
        
        # Legendary users bypass IP restrictions
        if is_legendary and self.security_config["ip_filtering"]["legendary_whitelist"]:
            return True
        
        # Check blocked IPs
        if client_ip in self.security_config["ip_filtering"]["blocked_ips"]:
            return False
        
        # Check allowed IPs (if whitelist is configured)
        allowed_ips = self.security_config["ip_filtering"]["allowed_ips"]
        if allowed_ips and client_ip not in allowed_ips:
            return False
        
        # Check for private IP ranges in production
        try:
            ip_obj = ipaddress.ip_address(client_ip)
            if ip_obj.is_private and not is_legendary:
                # Log private IP access
                self.logger.warning(f"Private IP access attempt: {client_ip}")
        except:
            pass
        
        return True
    
    async def _check_rate_limit(self, client_ip: str, is_legendary: bool) -> bool:
        """Check rate limiting"""
        
        if not self.security_config["rate_limiting"]["enabled"] or not self.redis_client:
            return True
        
        rate_config = self.security_config["rate_limiting"]
        
        # Get rate limit for this IP
        base_limit = rate_config["default_limit"]
        if is_legendary:
            limit = int(base_limit * rate_config["legendary_multiplier"])
        else:
            limit = base_limit
        
        window = rate_config["window_seconds"]
        
        # Redis key for rate limiting
        rate_key = f"rate_limit:{client_ip}"
        
        try:
            # Get current count
            current_count = self.redis_client.get(rate_key)
            if current_count is None:
                # First request in window
                pipeline = self.redis_client.pipeline()
                pipeline.set(rate_key, 1, ex=window)
                pipeline.execute()
                return True
            
            current_count = int(current_count)
            
            # Check if over limit
            if current_count >= limit:
                # Log rate limit violation
                self.logger.warning(f"Rate limit exceeded for IP: {client_ip}, count: {current_count}, limit: {limit}")
                return False
            
            # Increment counter
            self.redis_client.incr(rate_key)
            return True
            
        except Exception as e:
            self.logger.error(f"Rate limiting error: {e}")
            return True  # Fail open
    
    async def _check_request_size(self, request: Request) -> bool:
        """Check request size limits"""
        
        max_size = self.security_config["request_validation"]["max_request_size"]
        
        # Check Content-Length header
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                size = int(content_length)
                if size > max_size:
                    return False
            except ValueError:
                return False
        
        return True
    
    def _check_url_validity(self, request: Request) -> bool:
        """Check URL validity and safety"""
        
        url = str(request.url)
        path = request.url.path
        
        # Check URL length
        max_length = self.security_config["request_validation"]["max_url_length"]
        if len(url) > max_length:
            return False
        
        # Check for dangerous characters
        dangerous_chars = ["<", ">", "\"", "'", "&", "%00", "%0a", "%0d"]
        for char in dangerous_chars:
            if char in url:
                return False
        
        # Check for path traversal
        if ".." in path or "%2e%2e" in path.lower():
            return False
        
        return True
    
    def _check_user_agent(self, user_agent: str, is_legendary: bool) -> bool:
        """Check user agent validity"""
        
        if not user_agent:
            return True  # Allow empty user agents
        
        # Legendary users bypass user agent checks
        if is_legendary:
            return True
        
        user_agent_lower = user_agent.lower()
        
        # Check for blocked user agents
        blocked_agents = self.security_config["request_validation"]["blocked_user_agents"]
        for blocked in blocked_agents:
            if blocked in user_agent_lower:
                return False
        
        return True
    
    async def _check_malicious_patterns(self, request: Request) -> bool:
        """Check for malicious patterns in request"""
        
        if not self.security_config["content_security"]["check_malicious_patterns"]:
            return True
        
        # Check URL path
        path = request.url.path
        for pattern in self.compiled_patterns:
            if pattern.search(path):
                self.logger.warning(f"Malicious pattern detected in path: {path}")
                return False
        
        # Check query parameters
        query = str(request.query_params)
        for pattern in self.compiled_patterns:
            if pattern.search(query):
                self.logger.warning(f"Malicious pattern detected in query: {query}")
                return False
        
        # Check headers
        for header_name, header_value in request.headers.items():
            for pattern in self.compiled_patterns:
                if pattern.search(header_value):
                    self.logger.warning(f"Malicious pattern detected in header {header_name}: {header_value}")
                    return False
        
        return True
    
    async def _check_ddos_protection(self, client_ip: str) -> bool:
        """Check DDoS protection measures"""
        
        if not self.security_config["ddos_protection"]["enabled"] or not self.redis_client:
            return True
        
        ddos_config = self.security_config["ddos_protection"]
        
        # Check connection count
        connection_key = f"ddos_connections:{client_ip}"
        
        try:
            current_connections = self.redis_client.get(connection_key)
            if current_connections and int(current_connections) > ddos_config["connection_limit"]:
                return False
            
            # Increment and set expiry
            pipeline = self.redis_client.pipeline()
            pipeline.incr(connection_key)
            pipeline.expire(connection_key, 60)  # 1 minute window
            pipeline.execute()
            
            return True
            
        except Exception as e:
            self.logger.error(f"DDoS protection error: {e}")
            return True  # Fail open
    
    async def _enhance_response_security(self, request: Request, response: Response) -> Response:
        """Add security headers and enhancements to response"""
        
        # Add security headers
        for header_name, header_value in self.security_headers.items():
            response.headers[header_name] = header_value
        
        # Add request-specific security headers
        if hasattr(request.state, "security_metadata"):
            metadata = request.state.security_metadata
            
            response.headers["X-Request-ID"] = metadata["request_id"]
            
            if metadata["is_legendary"]:
                response.headers["X-Legendary-User"] = "true"
                response.headers["X-Code-Bro-Status"] = "maximum"
        
        # Add timing header (for performance monitoring)
        response.headers["X-Response-Time"] = str(int(time.time() * 1000))
        
        return response
    
    async def _log_security_metrics(self, request: Request, response: Response, processing_time: float):
        """Log security metrics and events"""
        
        client_ip = self._get_client_ip(request)
        
        security_log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "client_ip": client_ip,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "processing_time": processing_time,
            "user_agent": request.headers.get("user-agent", ""),
            "content_length": response.headers.get("content-length", "0"),
            "is_legendary": getattr(request.state, "security_metadata", {}).get("is_legendary", False)
        }
        
        # Log based on response code
        if response.status_code >= 400:
            if response.status_code in [403, 429]:
                self.logger.warning(f"Security block: {json.dumps(security_log)}")
            else:
                self.logger.error(f"Security error: {json.dumps(security_log)}")
        elif getattr(request.state, "security_metadata", {}).get("is_legendary", False):
            self.logger.info(f"🎸 Legendary request: {json.dumps(security_log)} 🎸")
        
        # Store metrics in Redis for monitoring
        if self.redis_client:
            try:
                metrics_key = f"security_metrics:{datetime.now().strftime('%Y%m%d%H')}"
                self.redis_client.lpush(metrics_key, json.dumps(security_log))
                self.redis_client.expire(metrics_key, 86400)  # 24 hours
            except Exception as e:
                self.logger.error(f"Failed to store security metrics: {e}")

class LegendaryRateLimitMiddleware:
    """Simplified rate limiting middleware for specific endpoints"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.logger = logging.getLogger(__name__)
    
    async def __call__(self, request: Request, call_next):
        """Rate limit specific endpoints"""
        
        # Define endpoint-specific rate limits
        endpoint_limits = {
            "/api/auth/login": (5, 300),  # 5 attempts per 5 minutes
            "/api/auth/register": (3, 600),  # 3 attempts per 10 minutes
            "/api/password/reset": (3, 600),  # 3 resets per 10 minutes
        }
        
        path = request.url.path
        
        if path in endpoint_limits:
            limit, window = endpoint_limits[path]
            client_ip = request.client.host
            
            rate_key = f"endpoint_rate:{path}:{client_ip}"
            
            try:
                current = self.redis_client.get(rate_key)
                if current is None:
                    self.redis_client.set(rate_key, 1, ex=window)
                elif int(current) >= limit:
                    return JSONResponse(
                        status_code=429,
                        content={"detail": f"Rate limit exceeded for {path}"}
                    )
                else:
                    self.redis_client.incr(rate_key)
            except Exception as e:
                self.logger.error(f"Endpoint rate limiting error: {e}")
        
        return await call_next(request)

# Export middleware classes
__all__ = ["LegendarySecurityMiddleware", "LegendaryRateLimitMiddleware"]
