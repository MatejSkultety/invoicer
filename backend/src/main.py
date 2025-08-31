from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .config import settings
from .routers import health
from .middleware import logging_middleware
from . import logging_config  # Initialize logging configuration


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="Backend API",
        description="Backend service",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG_MODE else None,
        redoc_url="/redoc" if settings.DEBUG_MODE else None,
    )

    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    if not settings.DEBUG_MODE:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS
        )
    
    # Add custom middleware
    app.middleware("http")(logging_middleware)

    # Include routers
    app.include_router(health.router, tags=["Health"])

    return app


# Create the application instance
app = create_app()
