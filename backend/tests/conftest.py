# File: backend/tests/conftest.py
"""
🧪🎸 N3EXTPATH - LEGENDARY TEST CONFIGURATION & FIXTURES 🎸🧪
Professional test setup with Swiss precision
Built: 2025-08-06 01:03:28 UTC by RICKROLL187
Email: letstalktech010@gmail.com
WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
"""

import pytest
import asyncio
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, AsyncGenerator, Generator
from unittest.mock import Mock, patch
import os
import tempfile
from pathlib import Path

# FastAPI and testing imports
from fastapi.testclient import TestClient
from httpx import AsyncClient
import asyncpg

# SQLAlchemy and database imports
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Import legendary application
from main import app
from database.models import Base, User, LegendaryMetrics
from database.connection import get_db_session, legendary_db_manager
from config.settings import settings
from auth.security import create_access_token, get_password_hash

# =====================================
# 🎸 LEGENDARY TEST ENVIRONMENT SETUP 🎸
# =====================================

# Override settings for testing
os.environ.update({
    "TESTING": "true",
    "ENVIRONMENT": "test",
    "DATABASE_URL": "sqlite:///./test_legendary.db",
    "SECRET_KEY": "legendary-test-secret-key-swiss-precision-2025",
    "LEGENDARY_MODE": "true",
    "SWISS_PRECISION_ENABLED": "true",
    "CODE_BRO_ENERGY_LEVEL": "infinite",
    "FOUNDER_USERNAME": "rickroll187",
    "EMAIL_BACKEND": "console",
    "ENABLE_BACKGROUND_TASKS": "false"
})

# =====================================
# 🗄️ DATABASE TEST FIXTURES 🗄️
# =====================================

@pytest.fixture(scope="session")
def engine():
    """
    Create legendary test database engine with Swiss precision
    """
    # Use in-memory SQLite for lightning-fast tests
    engine = create_engine(
        "sqlite:///",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False  # Set to True for SQL debugging
    )
    
    # Create all legendary tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Cleanup with Swiss precision
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(engine) -> Generator[Session, None, None]:
    """
    Create legendary database session for each test
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
    
    # Use nested transaction for isolation
    nested = connection.begin_nested()
    
    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()
    
    yield session
    
    # Cleanup with legendary precision
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(autouse=True)
def override_db_dependency(db_session):
    """
    Override database dependency for legendary testing
    """
    def get_test_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db_session] = get_test_db
    yield
    app.dependency_overrides.clear()

# =====================================
# 🎸 LEGENDARY USER FIXTURES 🎸
# =====================================

@pytest.fixture
def password_hash():
    """Generate legendary password hash"""
    return get_password_hash("LegendaryPassword2025!")

@pytest.fixture
def rickroll187_user(db_session, password_hash) -> User:
    """
    Create legendary RICKROLL187 founder user
    """
    user = User(
        user_id=uuid.uuid4(),
        username="rickroll187",
        email="letstalktech010@gmail.com",
        password_hash=password_hash,
        first_name="Rick",
        last_name="Roll",
        job_title="Legendary Founder & Chief Code Bro",
        department="Executive Leadership",
        role="founder",
        is_active=True,
        is_legendary=True,
        email_verified=True,
        swiss_precision_certified=True,
        code_bro_energy_level="infinite",
        legendary_certified_at=datetime.now(timezone.utc),
        hire_date=datetime.now(timezone.utc) - timedelta(days=1),
        salary=1000000.0,
        salary_currency="USD"
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Add legendary metrics
    metrics = LegendaryMetrics(
        user_id=user.user_id,
        swiss_precision_score=100.0,
        code_bro_rating=10,
        swiss_precision_level="legendary",
        code_bro_energy_level="infinite",
        quality_consistency_score=100.0,
        platform_engagement_score=100.0,
        total_achievements=4,
        legendary_achievements=4,
        last_activity_at=datetime.now(timezone.utc)
    )
    
    db_session.add(metrics)
    db_session.commit()
    
    return user

@pytest.fixture
def sample_employee(db_session, password_hash) -> User:
    """
    Create sample employee for testing
    """
    user = User(
        user_id=uuid.uuid4(),
        username="alice_legendary",
        email="alice.legendary@n3extpath.com",
        password_hash=password_hash,
        first_name="Alice",
        last_name="Legendary",
        job_title="Senior Software Engineer",
        department="Engineering",
        role="employee",
        is_active=True,
        is_legendary=True,
        email_verified=True,
        swiss_precision_certified=True,
        code_bro_energy_level="maximum",
        hire_date=datetime.now(timezone.utc) - timedelta(days=30)
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Add metrics
    metrics = LegendaryMetrics(
        user_id=user.user_id,
        swiss_precision_score=88.5,
        code_bro_rating=9,
        swiss_precision_level="high",
        code_bro_energy_level="maximum",
        quality_consistency_score=85.0,
        platform_engagement_score=90.0,
        last_activity_at=datetime.now(timezone.utc)
    )
    
    db_session.add(metrics)
    db_session.commit()
    
    return user

@pytest.fixture
def regular_user(db_session, password_hash) -> User:
    """
    Create regular user for testing
    """
    user = User(
        user_id=uuid.uuid4(),
        username="bob_standard",
        email="bob.standard@n3extpath.com",
        password_hash=password_hash,
        first_name="Bob",
        last_name="Standard",
        job_title="Software Developer",
        department="Engineering",
        role="employee",
        is_active=True,
        is_legendary=False,
        email_verified=True,
        swiss_precision_certified=False,
        code_bro_energy_level="good",
        hire_date=datetime.now(timezone.utc) - timedelta(days=60)
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user

# =====================================
# 🔐 AUTHENTICATION FIXTURES 🔐
# =====================================

@pytest.fixture
def rickroll187_token(rickroll187_user) -> str:
    """
    Generate legendary access token for RICKROLL187
    """
    token_data = {
        "sub": str(rickroll187_user.user_id),
        "username": rickroll187_user.username,
        "role": rickroll187_user.role.value,
        "is_legendary": True,
        "swiss_precision_certified": True,
        "code_bro_energy_level": "infinite"
    }
    
    return create_access_token(data=token_data)

@pytest.fixture
def employee_token(sample_employee) -> str:
    """
    Generate access token for sample employee
    """
    token_data = {
        "sub": str(sample_employee.user_id),
        "username": sample_employee.username,
        "role": sample_employee.role.value,
        "is_legendary": True,
        "swiss_precision_certified": True,
        "code_bro_energy_level": "maximum"
    }
    
    return create_access_token(data=token_data)

@pytest.fixture
def regular_token(regular_user) -> str:
    """
    Generate access token for regular user
    """
    token_data = {
        "sub": str(regular_user.user_id),
        "username": regular_user.username,
        "role": regular_user.role.value,
        "is_legendary": False,
        "swiss_precision_certified": False,
        "code_bro_energy_level": "good"
    }
    
    return create_access_token(data=token_data)

# =====================================
# 🌐 HTTP CLIENT FIXTURES 🌐
# =====================================

@pytest.fixture
def client() -> TestClient:
    """
    Create legendary test client with Swiss precision
    """
    return TestClient(app)

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Create legendary async client for advanced testing
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def authenticated_client(client, rickroll187_token) -> TestClient:
    """
    Create authenticated client for RICKROLL187
    """
    client.headers.update({"Authorization": f"Bearer {rickroll187_token}"})
    return client

@pytest.fixture
def employee_client(client, employee_token) -> TestClient:
    """
    Create authenticated client for employee
    """
    client.headers.update({"Authorization": f"Bearer {employee_token}"})
    return client

@pytest.fixture
def regular_client(client, regular_token) -> TestClient:
    """
    Create authenticated client for regular user
    """
    client.headers.update({"Authorization": f"Bearer {regular_token}"})
    return client

# =====================================
# 📊 MOCK FIXTURES 📊
# =====================================

@pytest.fixture
def mock_email_backend():
    """
    Mock email backend for legendary testing
    """
    with patch('auth.legendary_auth_system.send_verification_email') as mock_email:
        mock_email.return_value = True
        yield mock_email

@pytest.fixture
def mock_redis():
    """
    Mock Redis for legendary caching tests
    """
    with patch('redis.Redis') as mock_redis:
        mock_redis.return_value.ping.return_value = True
        mock_redis.return_value.get.return_value = None
        mock_redis.return_value.set.return_value = True
        mock_redis.return_value.delete.return_value = 1
        yield mock_redis

@pytest.fixture
def mock_openai():
    """
    Mock OpenAI API for legendary AI tests
    """
    with patch('openai.ChatCompletion.create') as mock_openai:
        mock_openai.return_value = Mock(
            choices=[Mock(
                message=Mock(
                    content="This is a legendary AI response with Swiss precision!"
                )
            )]
        )
        yield mock_openai

# =====================================
# 🎸 UTILITY FIXTURES 🎸
# =====================================

@pytest.fixture
def temp_upload_dir():
    """
    Create temporary upload directory for legendary file tests
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        upload_path = Path(temp_dir) / "uploads"
        upload_path.mkdir(exist_ok=True)
        yield upload_path

@pytest.fixture
def sample_image_file():
    """
    Create sample image file for legendary upload tests
    """
    import io
    from PIL import Image
    
    # Create a legendary test image
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return ("test_image.png", img_bytes, "image/png")

@pytest.fixture
def performance_review_data():
    """
    Sample performance review data for legendary testing
    """
    return {
        "review_cycle": "quarterly",
        "overall_score": 4.5,
        "technical_skills": 4.8,
        "communication": 4.3,
        "leadership": 4.0,
        "collaboration": 4.7,
        "innovation": 4.6,
        "reliability": 4.4,
        "problem_solving": 4.9,
        "achievements": "Delivered legendary features with Swiss precision!",
        "strengths": "Exceptional code bro energy and Swiss precision execution",
        "improvement_areas": "Continue legendary journey toward infinite code bro energy",
        "goals_next_period": "Achieve legendary status with maximum Swiss precision",
        "swiss_precision_score": 88.5,
        "is_legendary": True,
        "code_bro_energy_notes": "Maximum energy level with infinite potential!"
    }

@pytest.fixture
def okr_data():
    """
    Sample OKR data for legendary testing
    """
    return {
        "title": "Achieve Legendary Code Bro Status",
        "description": "Master Swiss precision and infinite code bro energy",
        "cycle": "quarterly",
        "is_legendary": True,
        "swiss_precision_mode": True,
        "code_bro_energy_goal": True,
        "key_results": [
            {
                "title": "Complete 10 legendary features",
                "type": "numeric",
                "target_value": 10.0,
                "unit": "features",
                "swiss_precision_target": True,
                "legendary_stretch_goal": True
            },
            {
                "title": "Achieve 95% Swiss precision score",
                "type": "percentage",
                "target_value": 95.0,
                "unit": "percent",
                "swiss_precision_target": True
            }
        ]
    }

# =====================================
# 🎸 LEGENDARY TEST UTILITIES 🎸
# =====================================

@pytest.fixture
def assert_legendary_response():
    """
    Utility for asserting legendary API responses
    """
    def _assert_legendary_response(response, expected_status=200):
        """Assert legendary response with Swiss precision"""
        assert response.status_code == expected_status
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for legendary headers
            assert "X-Swiss-Precision" in response.headers
            assert "X-Code-Bro-Energy" in response.headers
            assert "X-Built-By" in response.headers
            assert response.headers["X-Built-By"] == "RICKROLL187"
            
            return data
        
        return response.json() if response.content else None
    
    return _assert_legendary_response

@pytest.fixture
def legendary_test_data():
    """
    Collection of legendary test data
    """
    return {
        "founder_motto": "WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!",
        "swiss_precision_threshold": 85.0,
        "legendary_threshold": 95.0,
        "code_bro_energy_levels": ["standard", "good", "high", "maximum", "infinite"],
        "founder_email": "letstalktech010@gmail.com",
        "founder_username": "rickroll187",
        "platform_name": "N3EXTPATH",
        "test_timestamp": "2025-08-06T01:03:28Z"
    }

# =====================================
# 🧪 ASYNC TEST UTILITIES 🧪
# =====================================

@pytest.fixture(scope="session")
def event_loop():
    """
    Create event loop for legendary async tests
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# =====================================
# 🎸 LEGENDARY MARKERS 🎸
# =====================================

def pytest_configure(config):
    """
    Configure legendary pytest markers
    """
    config.addinivalue_line(
        "markers", "legendary: Tests for legendary-specific features"
    )
    config.addinivalue_line(
        "markers", "swiss_precision: Tests for Swiss precision standards"
    )
    config.addinivalue_line(
        "markers", "code_bro_energy: Tests for code bro energy features"
    )
    config.addinivalue_line(
        "markers", "rickroll187: Founder-exclusive feature tests"
    )

# =====================================
# 🎸 LEGENDARY COMPLETION MESSAGE 🎸
# =====================================

if __name__ == "__main__":
    print("🎸🎸🎸 LEGENDARY TEST CONFIGURATION LOADED! 🎸🎸🎸")
    print("Built with Swiss precision by RICKROLL187!")
    print("Email: letstalktech010@gmail.com")
    print("WE ARE CODE BROS THE CREATE THE BEST AND CRACK JOKES TO HAVE FUN!")
    print(f"Test configuration loaded at: 2025-08-06 01:03:28 UTC")
    print("🧪 Comprehensive test fixtures: LEGENDARY QUALITY")
    print("🎸 RICKROLL187 founder fixtures: EXCLUSIVE ACCESS")
    print("⚙️ Swiss precision test utilities: MAXIMUM RELIABILITY")
    print("💪 Code bro energy test data: INFINITE POTENTIAL")
    print("🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸🎸")
