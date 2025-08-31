import pytest
from fastapi import status


class TestHealthEndpoints:
    """Test cases for health check endpoints."""

    def test_health_check(self, client):
        """Test the main health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert "environment" in data
        
        # Check environment data
        env_data = data["environment"]
        assert "debug_mode" in env_data
        assert "guest_mode" in env_data
        assert "timezone" in env_data
        assert "log_level" in env_data

    def test_readiness_check(self, client):
        """Test the readiness check endpoint."""
        response = client.get("/health/ready")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["status"] == "ready"

    def test_liveness_check(self, client):
        """Test the liveness check endpoint."""
        response = client.get("/health/live")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["status"] == "alive"

    def test_health_response_time(self, client):
        """Test that health check responds quickly."""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check for process time header (added by middleware)
        assert "X-Process-Time" in response.headers
        
        # Should be very fast (less than 1 second)
        process_time = float(response.headers["X-Process-Time"])
        assert process_time < 1.0
