import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging."""
    
    async def dispatch(
        self, 
        request: Request, 
        call_next: Callable
    ) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())[:8]
        
        # Log request
        start_time = time.time()
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} - Started"
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} - "
            f"Completed {response.status_code} in {duration:.3f}s"
        )
        
        # Add headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        
        return response


class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware for adding response timing headers."""
    
    async def dispatch(
        self, 
        request: Request, 
        call_next: Callable
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
