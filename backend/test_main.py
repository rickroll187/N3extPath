# File: backend/test_main.py
"""
🧪🎸 N3EXTPATH - LEGENDARY BACKEND TEST SUITE 🎸🧪
Professional pytest test suite for backend API
Built: 2025-08-05 15:52:36 UTC by RICKROLL187
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)

class TestLegendaryEndpoints:
    """Test suite for legendary API endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns HTML"""
        response = client.get("/")
        assert response.status_code == 200
        assert "N3EXTPATH HR Platform" in response.text
        assert "RICKROLL187" in response.text
        assert "WE ARE CODE BROS" in response.text
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "legendary"
        assert "RICKROLL187" in data["built_by"]
        assert "timestamp" in data
    
    def test_get_rickroll187_user(self):
        """Test getting RICKROLL187 user (legendary founder)"""
        response = client.get("/api/v1/users/rickroll187")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["user"]["username"] == "rickroll187"
        assert data["user"]["is_legendary"] is True
        assert "legendary_status" in data["user"]
    
    def test_get_nonexistent_user(self):
        """Test getting non-existent user returns 404"""
        response = client.get("/api/v1/users/nonexistent")
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
    
    def test_get_all_users(self):
        """Test getting all users"""
        response = client.get("/api/v1/users")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["total_users"] >= 1
        assert len(data["legendary_users"]) >= 1
    
    def test_get_okrs(self):
        """Test getting all OKRs"""
        response = client.get("/api/v1/okrs")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "okrs" in data
        assert "total_okrs" in data
    
    def test_get_specific_okr(self):
        """Test getting specific OKR"""
        response = client.get("/api/v1/okrs/okr_001")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["okr"]["okr_id"] == "okr_001"
        assert "Legendary HR Platform" in data["okr"]["title"]
    
    def test_get_nonexistent_okr(self):
        """Test getting non-existent OKR returns 404"""
        response = client.get("/api/v1/okrs/nonexistent")
        assert response.status_code == 404
    
    def test_dashboard_endpoint(self):
        """Test dashboard data endpoint"""
        response = client.get("/api/v1/dashboard")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "stats" in data
        assert "recent_activities" in data
        assert "RICKROLL187" in data["built_by"]
        assert "WE ARE CODE BROS" in data["legendary_message"]
    
    def test_legendary_endpoint(self):
        """Test the secret legendary endpoint"""
        response = client.get("/api/v1/legendary")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "LEGENDARY ACCESS GRANTED" in data["message"]
        assert data["founder"] == "RICKROLL187"
        assert data["swiss_precision"] is True
        assert data["code_bro_status"] == "MAXIMUM"

class TestLegendaryPerformance:
    """Test suite for performance and load testing"""
    
    def test_concurrent_health_checks(self):
        """Test multiple concurrent health check requests"""
        import concurrent.futures
        import time
        
        def make_request():
            return client.get("/health")
        
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [future.result() for future in futures]
        
        end_time = time.time()
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
        
        # Should complete within reasonable time (legendary performance!)
        assert end_time - start_time < 2.0
    
    def test_api_response_time(self):
        """Test API response times are legendary fast"""
        import time
        
        endpoints = [
            "/health",
            "/api/v1/users",
            "/api/v1/okrs",
            "/api/v1/dashboard"
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            assert response.status_code == 200
            # Should respond within 500ms (Swiss precision!)
            assert end_time - start_time < 0.5

class TestLegendaryErrorHandling:
    """Test suite for error handling"""
    
    def test_invalid_endpoints(self):
        """Test invalid endpoints return appropriate errors"""
        invalid_endpoints = [
            "/api/v1/invalid",
            "/nonexistent",
            "/api/v2/users"
        ]
        
        for endpoint in invalid_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 404
    
    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = client.get("/health")
        
        # Should have CORS headers for frontend access
        headers = response.headers
        assert "access-control-allow-origin" in headers

# Legendary test fixtures
@pytest.fixture
def legendary_test_data():
    """Fixture providing legendary test data"""
    return {
        "legendary_user": {
            "username": "rickroll187",
            "expected_role": "founder",
            "expected_department": "legendary"
        },
        "test_okr": {
            "okr_id": "okr_001",
            "expected_owner": "rickroll187"
        }
    }

def test_legendary_integration(legendary_test_data):
    """Integration test with legendary test data"""
    # Test user exists
    user_response = client.get(f"/api/v1/users/{legendary_test_data['legendary_user']['username']}")
    assert user_response.status_code == 200
    
    user_data = user_response.json()["user"]
    assert user_data["role"] == legendary_test_data["legendary_user"]["expected_role"]
    assert user_data["department"] == legendary_test_data["legendary_user"]["expected_department"]
    
    # Test OKR exists for user
    okr_response = client.get(f"/api/v1/okrs/{legendary_test_data['test_okr']['okr_id']}")
    assert okr_response.status_code == 200
    
    okr_data = okr_response.json()["okr"]
    assert okr_data["owner"] == legendary_test_data["test_okr"]["expected_owner"]

if __name__ == "__main__":
    print("🧪 Running N3EXTPATH Legendary Test Suite 🧪")
    print("Built by RICKROLL187 - Testing with Swiss Precision!")
    print("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
