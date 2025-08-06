# File: backend/auth/legendary_oauth_system.py
"""
🔑🎸 N3EXTPATH - LEGENDARY OAUTH2 INTEGRATION SYSTEM 🎸🔑
Professional OAuth2 integration for Google, Microsoft, GitHub, LinkedIn
Built: 2025-08-05 16:57:29 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import httpx
import secrets
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlencode
import json
import uuid
from fastapi import HTTPException, Request
import redis

class OAuthProvider(Enum):
    """Supported OAuth providers"""
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    GITHUB = "github"
    LINKEDIN = "linkedin"
    SLACK = "slack"

@dataclass
class OAuthConfig:
    """OAuth provider configuration"""
    provider: OAuthProvider
    client_id: str
    client_secret: str
    authorization_url: str
    token_url: str
    user_info_url: str
    scopes: List[str]
    redirect_uri: str

@dataclass
class OAuthUserInfo:
    """User information from OAuth provider"""
    provider: OAuthProvider
    provider_id: str
    email: str
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None
    raw_data: Dict[str, Any] = None

class LegendaryOAuthSystem:
    """Professional OAuth2 Integration System"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379, db=0)
        self.providers = self._initialize_providers()
        
    def _initialize_providers(self) -> Dict[OAuthProvider, OAuthConfig]:
        """Initialize OAuth provider configurations"""
        return {
            OAuthProvider.GOOGLE: OAuthConfig(
                provider=OAuthProvider.GOOGLE,
                client_id="your-google-client-id",
                client_secret="your-google-client-secret",
                authorization_url="https://accounts.google.com/o/oauth2/v2/auth",
                token_url="https://oauth2.googleapis.com/token",
                user_info_url="https://www.googleapis.com/oauth2/v2/userinfo",
                scopes=["openid", "email", "profile"],
                redirect_uri="https://n3extpath.com/auth/callback/google"
            ),
            
            OAuthProvider.MICROSOFT: OAuthConfig(
                provider=OAuthProvider.MICROSOFT,
                client_id="your-microsoft-client-id",
                client_secret="your-microsoft-client-secret",
                authorization_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
                token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
                user_info_url="https://graph.microsoft.com/v1.0/me",
                scopes=["openid", "email", "profile"],
                redirect_uri="https://n3extpath.com/auth/callback/microsoft"
            ),
            
            OAuthProvider.GITHUB: OAuthConfig(
                provider=OAuthProvider.GITHUB,
                client_id="your-github-client-id",
                client_secret="your-github-client-secret",
                authorization_url="https://github.com/login/oauth/authorize",
                token_url="https://github.com/login/oauth/access_token",
                user_info_url="https://api.github.com/user",
                scopes=["user:email"],
                redirect_uri="https://n3extpath.com/auth/callback/github"
            ),
            
            OAuthProvider.LINKEDIN: OAuthConfig(
                provider=OAuthProvider.LINKEDIN,
                client_id="your-linkedin-client-id",
                client_secret="your-linkedin-client-secret",
                authorization_url="https://www.linkedin.com/oauth/v2/authorization",
                token_url="https://www.linkedin.com/oauth/v2/accessToken",
                user_info_url="https://api.linkedin.com/v2/people/~:(id,firstName,lastName,emailAddress,profilePicture)",
                scopes=["r_liteprofile", "r_emailaddress"],
                redirect_uri="https://n3extpath.com/auth/callback/linkedin"
            ),
            
            OAuthProvider.SLACK: OAuthConfig(
                provider=OAuthProvider.SLACK,
                client_id="your-slack-client-id",
                client_secret="your-slack-client-secret",
                authorization_url="https://slack.com/oauth/v2/authorize",
                token_url="https://slack.com/api/oauth.v2.access",
                user_info_url="https://slack.com/api/users.identity",
                scopes=["identity.basic", "identity.email"],
                redirect_uri="https://n3extpath.com/auth/callback/slack"
            )
        }
    
    def generate_authorization_url(self, provider: OAuthProvider, 
                                  state: Optional[str] = None) -> Dict[str, str]:
        """Generate OAuth authorization URL with legendary security"""
        
        if provider not in self.providers:
            raise HTTPException(status_code=400, detail=f"Unsupported OAuth provider: {provider.value}")
        
        config = self.providers[provider]
        
        # Generate state parameter for CSRF protection
        if not state:
            state = secrets.token_urlsafe(32)
        
        # Store state in Redis for verification
        state_key = f"oauth_state:{state}"
        state_data = {
            "provider": provider.value,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + 
                          datetime.timedelta(minutes=10)).isoformat()
        }
        
        self.redis_client.hset(state_key, mapping=state_data)
        self.redis_client.expire(state_key, 600)  # 10 minutes
        
        # Build authorization URL
        params = {
            "client_id": config.client_id,
            "redirect_uri": config.redirect_uri,
            "scope": " ".join(config.scopes),
            "response_type": "code",
            "state": state,
            "access_type": "offline",  # For refresh tokens
            "prompt": "consent"
        }
        
        # Provider-specific parameters
        if provider == OAuthProvider.MICROSOFT:
            params["response_mode"] = "query"
        elif provider == OAuthProvider.GITHUB:
            params["allow_signup"] = "true"
        
        authorization_url = f"{config.authorization_url}?{urlencode(params)}"
        
        return {
            "authorization_url": authorization_url,
            "state": state,
            "provider": provider.value
        }
    
    async def handle_callback(self, provider: OAuthProvider, code: str, 
                            state: str) -> Dict[str, Any]:
        """Handle OAuth callback with legendary precision"""
        
        # Verify state parameter
        if not self._verify_state(state, provider):
            raise HTTPException(status_code=400, detail="Invalid state parameter")
        
        config = self.providers[provider]
        
        # Exchange code for access token
        token_data = await self._exchange_code_for_token(config, code)
        
        # Get user information
        user_info = await self._get_user_info(config, token_data["access_token"])
        
        # Clean up state
        self.redis_client.delete(f"oauth_state:{state}")
        
        return {
            "user_info": user_info,
            "token_data": token_data,
            "provider": provider.value,
            "legendary_oauth": True if user_info.email == "rickroll187@n3extpath.com" else False
        }
    
    def _verify_state(self, state: str, provider: OAuthProvider) -> bool:
        """Verify OAuth state parameter"""
        state_key = f"oauth_state:{state}"
        state_data = self.redis_client.hgetall(state_key)
        
        if not state_data:
            return False
        
        # Check provider matches
        if state_data.get(b"provider", b"").decode() != provider.value:
            return False
        
        # Check expiration
        expires_at = datetime.fromisoformat(state_data[b"expires_at"].decode())
        if datetime.now(timezone.utc) > expires_at:
            self.redis_client.delete(state_key)
            return False
        
        return True
    
    async def _exchange_code_for_token(self, config: OAuthConfig, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        
        token_data = {
            "client_id": config.client_id,
            "client_secret": config.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": config.redirect_uri
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        # Special handling for GitHub
        if config.provider == OAuthProvider.GITHUB:
            headers["Accept"] = "application/json"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                config.token_url,
                data=token_data,
                headers=headers,
                timeout=30.0
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to exchange code for token: {response.text}"
            )
        
        return response.json()
    
    async def _get_user_info(self, config: OAuthConfig, access_token: str) -> OAuthUserInfo:
        """Get user information from OAuth provider"""
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                config.user_info_url,
                headers=headers,
                timeout=30.0
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to get user info: {response.text}"
            )
        
        user_data = response.json()
        
        # Parse user info based on provider
        return self._parse_user_info(config.provider, user_data)
    
    def _parse_user_info(self, provider: OAuthProvider, data: Dict[str, Any]) -> OAuthUserInfo:
        """Parse user information from different providers"""
        
        if provider == OAuthProvider.GOOGLE:
            return OAuthUserInfo(
                provider=provider,
                provider_id=data["id"],
                email=data["email"],
                first_name=data.get("given_name", ""),
                last_name=data.get("family_name", ""),
                avatar_url=data.get("picture"),
                raw_data=data
            )
        
        elif provider == OAuthProvider.MICROSOFT:
            return OAuthUserInfo(
                provider=provider,
                provider_id=data["id"],
                email=data["mail"] or data.get("userPrincipalName", ""),
                first_name=data.get("givenName", ""),
                last_name=data.get("surname", ""),
                avatar_url=None,
                raw_data=data
            )
        
        elif provider == OAuthProvider.GITHUB:
            return OAuthUserInfo(
                provider=provider,
                provider_id=str(data["id"]),
                email=data.get("email", ""),
                first_name=data.get("name", "").split(" ")[0] if data.get("name") else "",
                last_name=" ".join(data.get("name", "").split(" ")[1:]) if data.get("name") else "",
                avatar_url=data.get("avatar_url"),
                raw_data=data
            )
        
        elif provider == OAuthProvider.LINKEDIN:
            first_name = ""
            last_name = ""
            
            if "firstName" in data:
                first_name = data["firstName"].get("localized", {}).get("en_US", "")
            if "lastName" in data:
                last_name = data["lastName"].get("localized", {}).get("en_US", "")
            
            return OAuthUserInfo(
                provider=provider,
                provider_id=data["id"],
                email=data.get("emailAddress", ""),
                first_name=first_name,
                last_name=last_name,
                avatar_url=data.get("profilePicture", {}).get("displayImage"),
                raw_data=data
            )
        
        elif provider == OAuthProvider.SLACK:
            user = data.get("user", {})
            return OAuthUserInfo(
                provider=provider,
                provider_id=user.get("id", ""),
                email=user.get("email", ""),
                first_name=user.get("name", "").split(" ")[0] if user.get("name") else "",
                last_name=" ".join(user.get("name", "").split(" ")[1:]) if user.get("name") else "",
                avatar_url=user.get("image_512"),
                raw_data=data
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider.value}")
    
    def link_oauth_account(self, user_id: str, oauth_info: OAuthUserInfo) -> bool:
        """Link OAuth account to existing user"""
        
        oauth_key = f"oauth:{user_id}:{oauth_info.provider.value}"
        oauth_data = {
            "provider_id": oauth_info.provider_id,
            "email": oauth_info.email,
            "first_name": oauth_info.first_name,
            "last_name": oauth_info.last_name,
            "avatar_url": oauth_info.avatar_url or "",
            "linked_at": datetime.now(timezone.utc).isoformat(),
            "raw_data": json.dumps(oauth_info.raw_data or {})
        }
        
        self.redis_client.hset(oauth_key, mapping=oauth_data)
        
        # Create reverse lookup
        provider_key = f"oauth_provider:{oauth_info.provider.value}:{oauth_info.provider_id}"
        self.redis_client.set(provider_key, user_id)
        
        return True
    
    def unlink_oauth_account(self, user_id: str, provider: OAuthProvider) -> bool:
        """Unlink OAuth account from user"""
        
        oauth_key = f"oauth:{user_id}:{provider.value}"
        oauth_data = self.redis_client.hgetall(oauth_key)
        
        if oauth_data:
            # Remove reverse lookup
            provider_id = oauth_data.get(b"provider_id", b"").decode()
            if provider_id:
                provider_key = f"oauth_provider:{provider.value}:{provider_id}"
                self.redis_client.delete(provider_key)
            
            # Remove OAuth data
            self.redis_client.delete(oauth_key)
            return True
        
        return False
    
    def get_user_oauth_accounts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all OAuth accounts linked to user"""
        
        accounts = []
        
        for provider in OAuthProvider:
            oauth_key = f"oauth:{user_id}:{provider.value}"
            oauth_data = self.redis_client.hgetall(oauth_key)
            
            if oauth_data:
                accounts.append({
                    "provider": provider.value,
                    "provider_id": oauth_data.get(b"provider_id", b"").decode(),
                    "email": oauth_data.get(b"email", b"").decode(),
                    "first_name": oauth_data.get(b"first_name", b"").decode(),
                    "last_name": oauth_data.get(b"last_name", b"").decode(),
                    "avatar_url": oauth_data.get(b"avatar_url", b"").decode(),
                    "linked_at": oauth_data.get(b"linked_at", b"").decode()
                })
        
        return accounts
    
    def find_user_by_oauth(self, provider: OAuthProvider, provider_id: str) -> Optional[str]:
        """Find user by OAuth provider ID"""
        
        provider_key = f"oauth_provider:{provider.value}:{provider_id}"
        user_id = self.redis_client.get(provider_key)
        
        return user_id.decode() if user_id else None

# Global OAuth system instance
legendary_oauth = LegendaryOAuthSystem()
