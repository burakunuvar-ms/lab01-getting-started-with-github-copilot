"""
Pytest configuration and fixtures for backend tests.

Provides:
  - client: TestClient for making requests to the FastAPI app
  - reset_activities: Fixture that restores the activities dict to its original state after each test
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app


# Store the original activities state for restoration during tests
_original_activities = None


@pytest.fixture(scope="function")
def client():
    """
    Fixture that provides a TestClient for the FastAPI application.
    
    Scope: function (fresh client for each test)
    """
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def reset_activities():
    """
    Fixture that resets the in-memory activities dictionary to its original state
    before and after each test to ensure test isolation.
    
    Scope: function (runs before/after each test)
    Autouse: True (automatically applies without explicit import)
    
    This fixture ensures that participant list modifications in one test
    do not affect subsequent tests.
    """
    import src.app as app_module
    
    global _original_activities
    
    # Store original state on first run
    if _original_activities is None:
        _original_activities = copy.deepcopy(app_module.activities)
    
    # Arrange: Reset activities to known state before test
    app_module.activities = copy.deepcopy(_original_activities)
    
    # Test runs here (yield point)
    yield
    
    # Cleanup: Reset activities after test
    app_module.activities = copy.deepcopy(_original_activities)
