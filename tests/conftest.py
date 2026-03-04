"""
Pytest configuration and shared fixtures for FastAPI testing.

This module provides reusable fixtures for all tests, enabling the
Arrange phase of the AAA pattern across test modules.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture: Provides a TestClient connected to the FastAPI app.
    
    Used in the Arrange phase to set up the HTTP client for integration tests.
    Creates a fresh client for each test to ensure test isolation.
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture: Resets the in-memory activities database to initial state.
    
    This ensures that modifications made during one test don't affect
    subsequent tests. Yields control back to the test, then restores
    the original state after the test completes.
    """
    # Store original state
    original_state = {
        name: {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": activity["participants"].copy()
        }
        for name, activity in activities.items()
    }
    
    yield activities
    
    # Restore original state after test
    for name, activity in original_state.items():
        activities[name]["participants"] = activity["participants"].copy()


@pytest.fixture
def sample_email():
    """
    Fixture: Provides a test email address.
    
    Used in the Arrange phase to set up test data without hardcoding
    email addresses throughout test files.
    """
    return "test.student@mergington.edu"


@pytest.fixture
def valid_activity_name():
    """
    Fixture: Provides a valid activity name from the app.
    
    Used in the Arrange phase to ensure tests reference activities
    that actually exist in the system.
    """
    return "Chess Club"


@pytest.fixture
def invalid_activity_name():
    """
    Fixture: Provides an invalid activity name.
    
    Used in the Arrange phase to test error handling for non-existent
    activities without hardcoding invalid names.
    """
    return "Nonexistent Activity"
