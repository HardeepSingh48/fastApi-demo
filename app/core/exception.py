"""Exception handling for the application."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers."""
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        """Handle Pydantic validation errors."""
        trace_id = getattr(request.state, "trace_id", "unknown")
        
        # Convert errors to JSON-serializable format
        errors = []
        for error in exc.errors():
            error_dict = {
                "loc": list(error.get("loc", [])),
                "msg": str(error.get("msg", "")),
                "type": str(error.get("type", ""))
            }
            # Handle context if it exists
            if "ctx" in error:
                error_dict["ctx"] = {k: str(v) for k, v in error["ctx"].items()}
            errors.append(error_dict)
        
        logger.error(
            f"[{trace_id}] Validation error: {errors}",
            extra={"trace_id": trace_id}
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": errors,
                "trace_id": trace_id
            }
        )
    
    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(
        request: Request,
        exc: IntegrityError
    ):
        """Handle database integrity errors."""
        trace_id = getattr(request.state, "trace_id", "unknown")
        
        logger.error(
            f"[{trace_id}] Database integrity error: {str(exc)}",
            extra={"trace_id": trace_id}
        )
        
        # Parse error message
        error_str = str(exc).lower()
        if "unique constraint" in error_str:
            detail = "Resource already exists"
        elif "foreign key constraint" in error_str:
            detail = "Referenced resource not found"
        else:
            detail = "Database constraint violation"
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": detail,
                "trace_id": trace_id
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception
    ):
        """Handle all other exceptions."""
        trace_id = getattr(request.state, "trace_id", "unknown")
        
        logger.exception(
            f"[{trace_id}] Unhandled exception: {str(exc)}",
            extra={"trace_id": trace_id}
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error",
                "trace_id": trace_id
            }
        )
