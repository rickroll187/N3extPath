# File: tests/integration/test_api_integration.py
"""
🧪🎸 N3EXTPATH - LEGENDARY API INTEGRATION TESTS 🎸🧪
Professional API integration testing with Swiss precision
Built: 2025-08-05 19:17:18 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import asyncio
import pytest
import httpx
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import uuid

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_USER_DATA = {
    "username": "test_user_integration",
    "email": "test@n3extpath.com",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User",
    "department": "Engineering",
    "role": "employee"
}

LEGENDARY_USER_DATA = {
    "username": "rickroll187",
    "email": "rickroll187@n3extpath.com",
    "password": "LegendaryPassword123!",
    "first_name": "RICKROLL",
    "last_name": "187",
    "department": "Legendary",
    "role": "founder",
    "is_legendary": True
}

class LegendaryAPITestClient:
    """Legendary API test client with Swiss precision"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.access_token: Optional[str] = None
        self.legendary_mode = False
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login and store access token"""
        response = await self.client.post(
            f"{self.base_url}/api/auth/login",
            json={
                "username": username,
                "password": password,
                "remember_me": False
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            
            # Check if legendary user
            if data.get("user", {}).get("is_legendary"):
                self.legendary_mode = True
                print("🎸 LEGENDARY MODE ACTIVATED IN TESTS! 🎸")
            
            return data
        else:
            raise Exception(f"Login failed: {response.text}")
    
    async def authenticated_request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Make authenticated request"""
        headers = kwargs.get("headers", {})
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
            
        # Add legendary headers if in legendary mode
        if self.legendary_mode:
            headers.update({
                "X-Legendary-User": "true",
                "X-Swiss-Precision": "maximum",
                "X-Code-Bro-Energy": "infinite"
            })
        
        kwargs["headers"] = headers
        
        return await self.client.request(method, f"{self.base_url}{endpoint}", **kwargs)

@pytest.fixture
async def api_client():
    """Create API test client"""
    async with LegendaryAPITestClient() as client:
        yield client

@pytest.fixture
async def authenticated_client(api_client):
    """Create authenticated API client"""
    await api_client.login(TEST_USER_DATA["username"], TEST_USER_DATA["password"])
    yield api_client

@pytest.fixture
async def legendary_client(api_client):
    """Create legendary authenticated client for RICKROLL187"""
    await api_client.login(LEGENDARY_USER_DATA["username"], LEGENDARY_USER_DATA["password"])
    yield api_client

class TestHealthAndInfo:
    """Test health and info endpoints"""
    
    async def test_health_check(self, api_client):
        """Test health check endpoint"""
        response = await api_client.client.get(f"{BASE_URL}/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "legendary"
        assert data["legendary_founder"] == "rickroll187"
        assert data["swiss_precision"] is True
        assert "timestamp" in data
        
    async def test_root_endpoint(self, api_client):
        """Test root endpoint"""
        response = await api_client.client.get(f"{BASE_URL}/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "N3EXTPATH HR Platform" in data["message"]
        assert data["built_by"] == "rickroll187"
        assert "WE ARE CODE BROS" in data["motto"]

class TestAuthentication:
    """Test authentication endpoints"""
    
    async def test_user_registration(self, api_client):
        """Test user registration"""
        unique_username = f"test_user_{uuid.uuid4().hex[:8]}"
        unique_email = f"test_{uuid.uuid4().hex[:8]}@n3extpath.com"
        
        registration_data = {
            **TEST_USER_DATA,
            "username": unique_username,
            "email": unique_email
        }
        
        response = await api_client.client.post(
            f"{BASE_URL}/api/auth/register",
            json=registration_data
        )
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["user"]["username"] == unique_username
        assert data["user"]["email"] == unique_email
        assert data["user"]["is_active"] is True
        
    async def test_user_login(self, api_client):
        """Test user login"""
        login_data = await api_client.login(TEST_USER_DATA["username"], TEST_USER_DATA["password"])
        
        assert "access_token" in login_data
        assert "refresh_token" in login_data
        assert "user" in login_data
        assert login_data["user"]["username"] == TEST_USER_DATA["username"]
        
    async def test_legendary_login(self, api_client):
        """Test legendary user login"""
        login_data = await api_client.login(LEGENDARY_USER_DATA["username"], LEGENDARY_USER_DATA["password"])
        
        assert "access_token" in login_data
        assert login**

