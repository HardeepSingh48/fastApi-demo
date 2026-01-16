from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exception import register_exception_handlers
from app.middlewares.cors import setup_cors
from app.core.tracing import TracingMiddleware

# Feature routers
from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.posts.routes import router as posts_router

def create_app() -> FastAPI:
    """
    Application factory pattern.
    
    Why factory pattern?
    - Easier to test (create app with different configs)
    - Can create multiple app instances
    - Clean separation of concerns
    """
    
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,  # Disable docs in prod
        redoc_url="/redoc" if settings.DEBUG else None,
    )
    
    # Register middleware (order matters!)
    app.add_middleware(TracingMiddleware)  # First: Add trace ID
    setup_cors(app)  # Second: Handle CORS
    
    # Register exception handlers
    register_exception_handlers(app)
    
    # Register routers
    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(users_router, prefix="/api/users", tags=["Users"])
    app.include_router(posts_router, prefix="/api/posts", tags=["Posts"])
    
    @app.get("/health")
    def health_check():
        """Health check endpoint for load balancers."""
        return {"status": "healthy"}
    
    return app

# Create app instance
app = create_app()

# For running with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
