# Backend

This folder contains the FastAPI backend service that provides the core API functionality for the invoicer application. The service is containerized using Docker with multi-stage builds for optimal performance and security.

## Technology Stack

- **FastAPI** - Modern, fast Python web framework
- **Python 3.10.14** - Programming language (slim-bookworm base image)
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server implementation
- **pytest** - Testing framework
- **Docker** - Multi-stage containerization

## Project Structure

```
backend/
├── src/
│   └── main.py        # FastAPI application entry point
├── test/              # Test files
├── requirements.txt   # Python dependencies
├── Dockerfile         # Multi-stage Docker build
└── README.md          # This file
```

## Docker Architecture

The service uses a **multi-stage Docker build**:

1. **Builder Stage**: 
   - Creates Python virtual environment
   - Installs dependencies with pip caching
   - Uses wheel-based installations for faster builds

2. **Runtime Stage**:
   - Lightweight Python slim image
   - Non-root user execution (appuser:10001)
   - Health check endpoint monitoring
   - Exposes port 8080

## Key Features

- **RESTful API**: Clean, well-documented REST endpoints
- **Type Safety**: Full Pydantic validation for request/response data
- **Auto Documentation**: Swagger/OpenAPI documentation generation
- **Security**: Non-root container execution
- **Health Monitoring**: Built-in health check endpoint (`/health`)
- **Performance**: Optimized Docker builds with dependency caching
- **Error Handling**: Comprehensive error responses
- **Logging**: Structured logging for monitoring and debugging

## Development Guidelines

- Use type hints throughout the codebase
- Write comprehensive tests for all endpoints
- Follow FastAPI best practices
- Use Pydantic models for data validation
- Implement proper error handling and logging
- Document all API endpoints with docstrings
- Ensure `/health` endpoint is always available for container health checks

## Container Configuration

The service runs on **port 8080** inside the container and is designed to be deployed with:

- **Non-root execution**: Runs as `appuser` (UID: 10001) for security
- **Health monitoring**: Automatic health checks via HTTP endpoint
- **Environment isolation**: Virtual environment for dependency management
- **Optimized builds**: Multi-stage Docker builds with caching

## Environment Variables

Configure the service using environment variables:

- `DEBUG_MODE` - Enable debug mode (default: 1 in development)
- `GUEST_MODE` - Enable guest access (default: 1 in development)
- `TZ` - Timezone setting (default: Europe/Bratislava)
