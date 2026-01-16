"""Request tracing middleware."""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import logging

logger = logging.getLogger(__name__)


class TracingMiddleware(BaseHTTPMiddleware):
    """Add unique trace ID to each request for debugging."""
    
    async def dispatch(self, request: Request, call_next):
        # Generate or extract trace ID
        trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
        
        # Store in request state
        request.state.trace_id = trace_id
        
        # Log request
        logger.info(
            f"[{trace_id}] {request.method} {request.url.path}",
            extra={"trace_id": trace_id}
        )
        
        # Process request
        response = await call_next(request)
        
        # Add trace ID to response headers
        response.headers["X-Trace-ID"] = trace_id
        
        # Log response
        logger.info(
            f"[{trace_id}] Response: {response.status_code}",
            extra={"trace_id": trace_id}
        )
        
        return response
