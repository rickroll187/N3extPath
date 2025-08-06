# File: backend/tests/test_api_endpoints.py
"""
🧪🎸 N3EXTPATH - LEGENDARY API ENDPOINT TESTS 🎸🧪
Professional API testing with Swiss precision
Built: 2025-08-06 01:03:28 UTC by RICKROLL187
Email: letstalktech010@gmail.com
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone
import json

# =====================================
# 🎸 LEGENDARY ROOT ENDPOINT TESTS 🎸
# =====================================

@pytest.mark.api
@pytest.mark.fast
def test_legendary_root_endpoint(client, assert_legendary_response):
    """
    Test legendary root endpoint with Swiss precision
    """
    response = client.get("/")
    data = assert_legendary_response(response)
    
    assert data["platform"] == "N3EXTPATH"
    assert data["built_by"] == "RICKROLL187"
    assert "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!" in data["philosophy"]
    assert data["features"]["swiss_precision"] == "enabled"
    assert data["features"]["code_bro_energy"] == "infinite"
    assert data["features"]["founder_access"] == "rickroll187"

@pytest.mark.api
@pytest.mark.fast
def test_health_check_endpoint(client, assert_legendary_response):
    """
    Test legendary health check with Swiss precision monitoring
    """
    response = client.get("/health")
    data = assert_legendary_response(response)
    
    assert data["status"] == "healthy"
    assert data["platform"] == "N3EXTPATH"
    assert data["swiss_precision"] == "maximum"
    assert data["code_bro_energy"] == "infinite"
    assert "legendary_features" in data
    assert data["legendary_features"]["authentication"] == "active"
    assert data["health_score"] >= 85.0
    assert data["grade"] in ["A+", "A", "B+"]

@pytest.mark.api
@pytest.mark.fast
def test_metrics_endpoint(client, assert_legendary_response):
    """
    Test legendary metrics endpoint
    """
    response = client.get("/metrics")
    data = assert_legendary_response(response)
    
    assert "platform_metrics" in data
    assert "legendary_metrics" in data
    assert data["legendary_metrics"]["code_bro_energy_level"] == "infinite"
    assert data["legendary_metrics"]["founder_oversight"] == "rickroll187"
    assert data["performance_grade"] == "A+"

@pytest.mark.api
@pytest.mark.legendary
def test_legendary_status_endpoint(client, assert_legendary_response):
    """
    Test legendary status endpoint
    """
    response = client.get("/legendary")
    data = assert_legendary_response(response)
    
    assert data["legendary_platform"] == "N3EXTPATH"
    assert data["founder"] == "RICKROLL187"
    assert "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!" in data["philosophy"]
    assert len(data["legendary_features"]) >= 7
    assert data["platform_status"] == "legendary"

@pytest.mark.api
@pytest.mark.rickroll187
def test_founder_info_endpoint(client, assert_legendary_response):
    """
    Test RICKROLL187 founder information endpoint
    """
    response = client.get("/founder")
    data = assert_legendary_response(response)
    
    assert data["founder"]["username"] == "rickroll187"
    assert data["founder"]["status"] == "legendary_founder"
    assert data["founder"]["legendary_level"] == "infinite"
    assert data["founder"]["swiss_precision_master"] == True
    assert data["platform_vision"]["mission"]
    assert data["contact"]["email"] == "letstalktech010@gmail.com"

# =====================================
# 🔐 AUTHENTICATION ENDPOINT TESTS 🔐
# =====================================

@pytest.mark.api
@pytest.mark.auth
def test_login_endpoint_success(client, rickroll187_user, assert_legendary_response):
    """
    Test successful login with legendary founder
    """
    login_data = {
        "username": "rickroll187",
        "password": "LegendaryPassword2025!"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    data = assert_legendary_response(response)
    
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user_info"]["username"] == "rickroll187"
    assert data["user_info"]["is_legendary"] == True
    assert data["user_info"]["role"] == "founder"
    assert data["legendary_features"]["infinite_access"] == True

@pytest.mark.api
@pytest.mark.auth
def test_login_endpoint_failure(client, assert_legendary_response):
    """
    Test login failure with Swiss precision error handling
    """
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
    
    data = response.json()
    assert "detail" in data

@pytest.mark.api
@pytest.mark.auth
def test_register_endpoint(client, mock_email_backend, assert_legendary_response):
    """
    Test user registration with legendary features
    """
    register_data = {
        "username": "new_code_bro",
        "email": "newbro@n3extpath.com",
        "password": "NewCodeBro2025!",
        "first_name": "New",
        "last_name": "CodeBro",
        "job_title": "Software Engineer",
        "department": "Engineering"
    }
    
    response = client.post("/api/v1/auth/register", json=register_data)
    data = assert_legendary_response(response, expected_status=201)
    
    assert data["user"]["username"] == "new_code_bro"
    assert data["user"]["email"] == "newbro@n3extpath.com"
    assert data["user"]["is_active"] == True
    assert data["legendary_features"]["swiss_precision_enabled"] == True
    assert mock_email_backend.called

@pytest.mark.api
@pytest.mark.auth
@pytest.mark.legendary
def test_protected_endpoint_access(authenticated_client, assert_legendary_response):
    """
    Test access to protected endpoints with legendary token
    """
    response = authenticated_client.get("/api/v1/users/me")
    data = assert_legendary_response(response)
    
    assert data["username"] == "rickroll187"
    assert data["is_legendary"] == True
    assert data["role"] == "founder"
    assert data["swiss_precision_certified"] == True
    assert data["code_bro_energy_level"] == "infinite"

# =====================================
# 👤 USER MANAGEMENT ENDPOINT TESTS 👤
# =====================================

@pytest.mark.api
@pytest.mark.unit
def test_get_user_profile(authenticated_client, assert_legendary_response):
    """
    Test get user profile with legendary features
    """
    response = authenticated_client.get("/api/v1/users/me")
    data = assert_legendary_response(response)
    
    assert data["username"] == "rickroll187"
    assert data["email"] == "letstalktech010@gmail.com"
    assert data["job_title"] == "Legendary Founder & Chief Code Bro"
    assert data["department"] == "Executive Leadership"
    assert data["is_legendary"] == True
    assert data["legendary_metrics"]["swiss_precision_score"] == 100.0
    assert data["legendary_metrics"]["code_bro_rating"] == 10

@pytest.mark.api
@pytest.mark.rickroll187
def test_list_users_founder_access(authenticated_client, sample_employee, regular_user, assert_legendary_response):
    """
    Test list users with RICKROLL187 founder access
    """
    response = authenticated_client.get("/api/v1/users/")
    data = assert_legendary_response(response)
    
    assert data["total_count"] >= 3  # founder + sample_employee + regular_user
    assert data["legendary_users"] >= 2  # founder + sample_employee
    
    # Check founder appears in list
    founder_user = next((user for user in data["users"] if user["username"] == "rickroll187"), None)
    assert founder_user is not None
    assert founder_user["is_legendary"] == True
    assert founder_user["role"] == "founder"

@pytest.mark.api
@pytest.mark.integration
def test_update_user_profile(authenticated_client, assert_legendary_response):
    """
    Test update user profile with Swiss precision
    """
    update_data = {
        "phone": "+1-555-LEGEND-NEW",
        "location": "Legendary Silicon Valley, CA",
        "bio": "🎸👑 Updated legendary founder bio with maximum code bro energy! 👑🎸"
    }
    
    response = authenticated_client.put("/api/v1/users/me", json=update_data)
    data = assert_legendary_response(response)
    
    assert data["phone"] == "+1-555-LEGEND-NEW"
    assert data["location"] == "Legendary Silicon Valley, CA"
    assert "maximum code bro energy" in data["profile"]["bio"]

# =====================================
# 📊 PERFORMANCE ENDPOINT TESTS 📊
# =====================================

@pytest.mark.api
@pytest.mark.integration
def test_create_performance_review(authenticated_client, sample_employee, performance_review_data, assert_legendary_response):
    """
    Test create performance review with legendary features
    """
    review_data = {
        "reviewee_id": str(sample_employee.user_id),
        "review_period_start": "2025-07-01T00:00:00Z",
        "review_period_end": "2025-09-30T23:59:59Z",
        **performance_review_data
    }
    
    response = authenticated_client.post("/api/v1/performance/reviews", json=review_data)
    data = assert_legendary_response(response, expected_status=201)
    
    assert data["overall_score"] == 4.5
    assert data["swiss_precision_score"] == 88.5
    assert data["is_legendary"] == True
    assert "legendary" in data["code_bro_energy_notes"].lower()
    assert data["reviewer"]["username"] == "rickroll187"

@pytest.mark.api
@pytest.mark.swiss_precision
def test_get_performance_analytics(employee_client, assert_legendary_response):
    """
    Test performance analytics with Swiss precision
    """
    response = employee_client.get("/api/v1/performance/analytics/me")
    data = assert_legendary_response(response)
    
    assert "performance_summary" in data
    assert "swiss_precision_analysis" in data
    assert "code_bro_energy_trend" in data
    assert "legendary_potential" in data
    assert data["swiss_precision_analysis"]["current_score"] >= 0

# =====================================
# 🎯 OKR ENDPOINT TESTS 🎯
# =====================================

@pytest.mark.api
@pytest.mark.integration
def test_create_legendary_okr(authenticated_client, okr_data, assert_legendary_response):
    """
    Test create legendary OKR with Swiss precision
    """
    okr_request = {
        **okr_data,
        "start_date": "2025-08-01T00:00:00Z",
        "end_date": "2025-10-31T23:59:59Z"
    }
    
    response = authenticated_client.post("/api/v1/okr/", json=okr_request)
    data = assert_legendary_response(response, expected_status=201)
    
    assert data["title"] == "Achieve Legendary Code Bro Status"
    assert data["is_legendary"] == True
    assert data["swiss_precision_mode"] == True
    assert data["code_bro_energy_goal"] == True
    assert len(data["key_results"]) == 2
    assert data["key_results"][0]["legendary_stretch_goal"] == True

@pytest.mark.api
@pytest.mark.legendary
def test_update_okr_progress(authenticated_client, assert_legendary_response):
    """
    Test update OKR progress with legendary tracking
    """
    # First create an OKR
    okr_data = {
        "title": "Test Progress Update",
        "description": "Test OKR for progress updates",
        "cycle": "quarterly",
        "start_date": "2025-08-01T00:00:00Z",
        "end_date": "2025-10-31T23:59:59Z",
        "is_legendary": True
    }
    
    create_response = authenticated_client.post("/api/v1/okr/", json=okr_data)
    created_okr = assert_legendary_response(create_response, expected_status=201)
    
    # Update progress
    progress_data = {
        "progress": 75.0,
        "confidence_level": 8,
        "progress_notes": "Making legendary progress with Swiss precision!"
    }
    
    response = authenticated_client.put(f"/api/v1/okr/{created_okr['okr_id']}/progress", json=progress_data)
    data = assert_legendary_response(response)
    
    assert data["progress"] == 75.0
    assert data["confidence_level"] == 8
    assert "legendary progress" in data["progress_notes"]

# =====================================
# 🔔 NOTIFICATION ENDPOINT TESTS 🔔
# =====================================

@pytest.mark.api
@pytest.mark.integration
def test_send_legendary_notification(authenticated_client, sample_employee, assert_legendary_response):
    """
    Test send legendary notification with Swiss precision delivery
    """
    notification_data = {
        "title": "🎸 Legendary Achievement Unlocked! 🎸",
        "message": "Congratulations on your legendary performance with Swiss precision!",
        "notification_type": "achievement",
        "priority": "legendary",
        "recipient_ids": [str(sample_employee.user_id)],
        "legendary_styling": True,
        "swiss_precision_delivery": True,
        "code_bro_energy_boost": True,
        "founder_message": True
    }
    
    response = authenticated_client.post("/api/v1/notifications/", json=notification_data)
    data = assert_legendary_response(response)
    
    assert data["recipient_count"] == 1
    assert data["sender"] == "rickroll187"
    assert data["legendary_delivery"] == True
    assert data["swiss_precision"] == True

@pytest.mark.api
@pytest.mark.fast
def test_get_notifications(employee_client, assert_legendary_response):
    """
    Test get notifications with legendary filtering
    """
    response = employee_client.get("/api/v1/notifications/")
    data = assert_legendary_response(response)
    
    assert "notifications" in data
    assert "total_count" in data
    assert "unread_count" in data
    assert data["total_count"] >= 0

# =====================================
# 📈 ANALYTICS ENDPOINT TESTS 📈
# =====================================

@pytest.mark.api
@pytest.mark.legendary
def test_personal_dashboard(authenticated_client, assert_legendary_response):
    """
    Test personal dashboard with legendary analytics
    """
    response = authenticated_client.get("/api/v1/analytics/dashboard")
    data = assert_legendary_response(response)
    
    assert data["dashboard_type"] == "legendary"
    assert data["user_name"]
    assert data["is_legendary_dashboard"] == True
    assert data["code_bro_energy_level"] == "infinite"
    assert "key_metrics" in data
    assert "legendary_achievements" in data
    assert len(data["legendary_achievements"]) >= 0

@pytest.mark.api
@pytest.mark.rickroll187
def test_company_analytics_founder_access(authenticated_client, assert_legendary_response):
    """
    Test company analytics with RICKROLL187 founder access
    """
    response = authenticated_client.get("/api/v1/analytics/company")
    data = assert_legendary_response(response)
    
    assert data["company_name"] == "N3EXTPATH"
    assert data["generated_by"] == "rickroll187"
    assert "founder_insights" in data
    assert data["founder_insights"] is not None
    assert "legendary_adoption" in data["founder_insights"]

@pytest.mark.api
@pytest.mark.rickroll187
def test_founder_exclusive_analytics(authenticated_client, assert_legendary_response):
    """
    Test RICKROLL187 exclusive founder analytics
    """
    response = authenticated_client.get("/api/v1/analytics/founder")
    data = assert_legendary_response(response)
    
    assert data["founder_status"] == "rickroll187"
    assert data["infinite_privileges"]["system_administration"] == True
    assert data["platform_impact"]["users_inspired"] == "all"
    assert data["platform_impact"]["code_bro_energy_generated"] == "infinite"
    assert "WE ARE CODE BROS" in data["founder_message"]

# =====================================
# 🎸 ERROR HANDLING TESTS 🎸
# =====================================

@pytest.mark.api
@pytest.mark.fast
def test_404_error_handling(client):
    """
    Test 404 error handling with legendary styling
    """
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404
    
    data = response.json()
    assert "Endpoint not found" in data["error"]
    assert "legendary platform" in data["message"]
    assert data["platform"] == "N3EXTPATH"
    assert data["contact"] == "letstalktech010@gmail.com"

@pytest.mark.api
@pytest.mark.auth
def test_401_unauthorized_access(client):
    """
    Test 401 unauthorized access with legendary error message
    """
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    
    data = response.json()
    assert "detail" in data

@pytest.mark.api
@pytest.mark.auth
def test_403_forbidden_access(regular_client):
    """
    Test 403 forbidden access with legendary privilege information
    """
    response = regular_client.get("/api/v1/analytics/founder")
    assert response.status_code == 403
    
    data = response.json()
    assert "Access forbidden" in data["error"]
    assert "legendary privileges" in data["message"]
    assert data["platform"] == "N3EXTPATH"

# =====================================
# 🎸 LEGENDARY TEST COMPLETION 🎸
# =====================================

@pytest.mark.api
@pytest.mark.legendary
@pytest.mark.swiss_precision
def test_legendary_platform_integration(authenticated_client, assert_legendary_response):
    """
    Comprehensive integration test for legendary platform features
    """
    # Test root endpoint
    root_response = authenticated_client.get("/")
    root_data = assert_legendary_response(root_response)
    assert root_data["features"]["legendary_status"] == "active"
    
    # Test health check
    health_response = authenticated_client.get("/health")
    health_data = assert_legendary_response(health_response)
    assert health_data["health_score"] >= 85.0
    
    # Test user profile
    profile_response = authenticated_client.get("/api/v1/users/me")
    profile_data = assert_legendary_response(profile_response)
    assert profile_data["is_legendary"] == True
    
    # Test legendary status
    legendary_response = authenticated_client.get("/legendary")
    legendary_data = assert_legendary_response(legendary_response)
    assert legendary_data["platform_status"] == "legendary"
    
    # Test founder access
    founder_response = authenticated_client.get("/founder")
    founder_data = assert_legendary_response(founder_response)
    assert founder_data["founder"]["username"] == "rickroll187"
    
    print("🎸🎸🎸 LEGENDARY PLATFORM INTEGRATION TEST PASSED! 🎸🎸🎸")
    print("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    print("All legendary features tested with Swiss precision!")
