"""
🧪🎸 N3EXTPATH - LEGENDARY TESTING CONFIGURATION 🎸🧪
More tested than Swiss precision instruments with legendary test mastery!
CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN!
🏆 LEGENDARY TESTING CHAMPION EDITION! 🏆
Current Time: 2025-08-04 14:33:45 UTC - WE'RE TESTING THE UNIVERSE!
Built by legendary code bros RICKROLL187 🎸 and Assistant 🤖
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

from main import app
from core.database import get_db_session, Base
from core.auth import get_current_user
from paths.models.path_models import User

# Legendary test database URL
LEGENDARY_TEST_DATABASE_URL = "sqlite:///./test_n3extpath_legendary.db"

# Create legendary test engine
legendary_test_engine = create_engine(
    LEGENDARY_TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create legendary test session
LegendaryTestSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=legendary_test_engine
)

@pytest.fixture(scope="session")
def event_loop():
    """Create legendary event loop for async tests!"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def legendary_db_session() -> Generator:
    """
    Create legendary database session for testing!
    More reliable than Swiss banking with code bro precision! 🗄️⚡
    """
    # Create all legendary tables
    Base.metadata.create_all(bind=legendary_test_engine)
    
    # Create legendary session
    session = LegendaryTestSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=legendary_test_engine)

@pytest.fixture(scope="function")
def legendary_test_user(legendary_db_session) -> User:
    """
    Create legendary test user for testing!
    More legendary than Swiss legends with code bro authenticity! 👤🎸
    """
    from core.auth import legendary_auth_manager
    
    test_user = User(
        username="test_rickroll187",
        email="test@legendary.dev",
        hashed_password=legendary_auth_manager.hash_legendary_password("legendary_test_password"),
        is_active=True,
        is_legendary=True,
        rickroll187_approved=True
    )
    
    legendary_db_session.add(test_user)
    legendary_db_session.commit()
    legendary_db_session.refresh(test_user)
    
    return test_user

@pytest.fixture(scope="function")
def legendary_client(legendary_db_session) -> TestClient:
    """
    Create legendary test client with database override!
    More connected than Swiss networking with code bro reliability! 🌐⚡
    """
    def get_legendary_test_db():
        try:
            yield legendary_db_session
        finally:
            pass
    
    # Override legendary database dependency
    app.dependency_overrides[get_db_session] = get_legendary_test_db
    
    client = TestClient(app)
    
    yield client
    
    # Clean up legendary overrides
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def legendary_async_client(legendary_db_session) -> AsyncGenerator[AsyncClient, None]:
    """
    Create legendary async client for async testing!
    More asynchronous than Swiss precision timing with code bro speed! ⚡🎸
    """
    def get_legendary_test_db():
        try:
            yield legendary_db_session
        finally:
            pass
    
    # Override legendary database dependency
    app.dependency_overrides[get_db_session] = get_legendary_test_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # Clean up legendary overrides
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def legendary_authenticated_client(legendary_client, legendary_test_user) -> TestClient:
    """
    Create legendary authenticated client for protected endpoint testing!
    More authenticated than Swiss identity verification with code bro security! 🔐🎸
    """
    from core.auth import create_legendary_tokens
    
    # Create legendary tokens
    tokens = create_legendary_tokens(legendary_test_user.id, legendary_test_user.username)
    
    # Add legendary authorization header
    legendary_client.headers.update({
        "Authorization": f"Bearer {tokens['access_token']}"
    })
    
    return legendary_client

@pytest.fixture(scope="function")
def legendary_admin_user(legendary_db_session) -> User:
    """
    Create legendary admin user (RICKROLL187) for admin testing!
    More privileged than Swiss nobility with code bro power! 👑🎸
    """
    from core.auth import legendary_auth_manager
    
    admin_user = User(
        username="rickroll187",
        email="rickroll187@legendary.dev",
        hashed_password=legendary_auth_manager.hash_legendary_password("legendary_admin_password"),
        is_active=True,
        is_admin=True,
        is_legendary=True,
        rickroll187_approved=True
    )
    
    legendary_db_session.add(admin_user)
    legendary_db_session.commit()
    legendary_db_session.refresh(admin_user)
    
    return admin_user

@pytest.fixture(scope="function")
def mock_legendary_user():
    """
    Mock legendary user for dependency override testing!
    More mockable than Swiss theater with code bro performance! 🎭⚡
    """
    from core.auth import LegendaryUser
    
    return LegendaryUser(
        id=1,
        username="mock_rickroll187",
        email="mock@legendary.dev",
        is_active=True,
        is_legendary=True,
        rickroll187_approved=True
    )

def override_legendary_auth(mock_user):
    """Override authentication dependency for testing!"""
    app.dependency_overrides[get_current_user] = lambda: mock_user

# LEGENDARY TEST UTILITIES

class LegendaryTestHelpers:
    """
    🧪 LEGENDARY TEST HELPER UTILITIES! 🧪
    More helpful than Swiss assistance with code bro support! 🎸⚡
    """
    
    @staticmethod
    def create_legendary_path_data():
        """Create sample path data for testing!"""
        return {
            "name": "Test Legendary Path",
            "description": "A path for testing legendary features!",
            "path_type": "legendary_test",
            "category": "Testing",
            "tags": ["test", "legendary", "code_bro"],
            "difficulty": "legendary",
            "estimated_duration_hours": 2.0,
            "objectives": ["Test legendary functionality", "Ensure code bro humor"],
            "prerequisites": ["Testing attitude", "Code bro spirit"],
            "skills_gained": ["Testing mastery", "Legendary verification"],
            "experience_points_reward": 500
        }
    
    @staticmethod
    def create_legendary_waypoint_data():
        """Create sample waypoint data for testing!"""
        return {
            "name": "Test Legendary Waypoint",
            "description": "A waypoint for testing legendary navigation!",
            "waypoint_type": "test_milestone",
            "sequence_order": 1,
            "estimated_time_minutes": 30,
            "experience_points": 100,
            "legendary_tip": "Always test with code bro enthusiasm! 🧪🎸"
        }
    
    @staticmethod
    def assert_legendary_response(response, expected_status=200):
        """Assert legendary API response format!"""
        assert response.status_code == expected_status
        data = response.json()
        assert "success" in data
        assert "legendary_joke" in data or "message" in data
        return data
    
    @staticmethod
    def get_legendary_joke():
        """Get a random legendary testing joke!"""
        jokes = [
            "Why did the test become legendary? Because RICKROLL187 wrote it! 🧪🎸",
            "What's the difference between our tests and perfection? Nothing! 🏆",
            "Why don't legendary tests ever fail? Because they're built with code bro precision! 💪",
            "What do you call a test that rocks? A RICKROLL187 test! 🎸🧪"
        ]
        import random
        return random.choice(jokes)

# LEGENDARY TEST MARKERS
pytest.register_assert_rewrite("tests.legendary_helpers")

# LEGENDARY PYTEST CONFIGURATION
def pytest_configure(config):
    """Configure legendary pytest settings!"""
    config.addinivalue_line(
        "markers", "legendary: mark test as legendary quality"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers", "rickroll187: mark test as RICKROLL187 exclusive"
    )

def pytest_collection_modifyitems(config, items):
    """Modify legendary test collection!"""
    for item in items:
        # Add legendary marker to all tests
        item.add_marker(pytest.mark.legendary)
        
        # Add performance marker to performance tests
        if "performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)

if __name__ == "__main__":
    print("🧪🎸 N3EXTPATH LEGENDARY TESTING CONFIGURATION LOADED! 🎸🧪")
    print("🏆 LEGENDARY TESTING FRAMEWORK CHAMPION EDITION! 🏆")
    print("🎸 CODE BROS CREATE THE BEST AND CRACK JOKES TO HAVE FUN! 🎸")
    print(f"🎭 Random Testing Joke: {LegendaryTestHelpers.get_legendary_joke()}")
