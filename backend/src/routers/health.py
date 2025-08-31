from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, status
from pydantic import BaseModel

from ..config import settings


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str
    timestamp: datetime
    version: str = "1.0.0"
    environment: Dict[str, Any]


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check the health status of the Backend service",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint required by Docker health checks.
    
    Returns:
        HealthResponse: Current health status and system information
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        environment={
            "debug_mode": settings.DEBUG_MODE,
            "guest_mode": settings.GUEST_MODE,
            "timezone": settings.TZ,
            "log_level": settings.LOG_LEVEL,
        }
    )


@router.get(
    "/health/ready",
    status_code=status.HTTP_200_OK,
    summary="Readiness Check",
    description="Check if the service is ready to accept requests",
)
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check endpoint for Kubernetes-style health checks.
    
    Returns:
        Dict[str, str]: Simple ready status
    """
    return {"status": "ready"}


@router.get(
    "/health/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness Check", 
    description="Check if the service is alive and responsive",
)
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check endpoint for Kubernetes-style health checks.
    
    Returns:
        Dict[str, str]: Simple alive status
    """
    return {"status": "alive"}
