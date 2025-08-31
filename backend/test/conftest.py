import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_headers():
    """Sample headers for testing."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
