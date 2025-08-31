import time
import logging
from fastapi import Request, Response


logger = logging.getLogger(__name__)


async def logging_middleware(request: Request, call_next) -> Response:
    """
    Log request details and response time.
    
    Args:
        request: The incoming request
        call_next: The next middleware/endpoint to call
        
    Returns:
        Response: The response from the next middleware/endpoint
    """
    start_time = time.time()
    
    # Log the incoming request
    logger.info(
        f"Incoming request: {request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client_ip": request.client.host if request.client else None,
        }
    )
    
    # Process the request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log the response
    logger.info(
        f"Request processed: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - Time: {process_time:.4f}s",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
        }
    )
    
    # Add response headers
    response.headers["X-Process-Time"] = str(process_time)
    
    return response
