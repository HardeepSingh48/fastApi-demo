"""CORS middleware configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware.
    
    Production-safe configuration that only allows specific origins.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,  # Specific origins only!
        allow_credentials=True,  # Allow cookies
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],  # Allow all headers
        expose_headers=["X-Trace-ID"],  # Expose custom headers
    )
