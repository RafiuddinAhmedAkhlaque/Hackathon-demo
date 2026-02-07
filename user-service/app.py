"""User Service - Main Application Entry Point"""
import json
import logging
import time
from datetime import datetime, timezone
from fastapi import FastAPI, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.address_routes import router as address_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration_ms = round((time.time() - start_time) * 1000, 2)
        
        log_data = {
            "method": request.method,
            "path": str(request.url.path),
            "status": response.status_code,
            "duration_ms": duration_ms,
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
        
        logger.info(json.dumps(log_data))
        return response


def create_app() -> FastAPI:
    app = FastAPI(
        title="User Service",
        description="Handles user registration, authentication, profile management, and address book.",
        version="1.0.0",
    )

    # Add logging middleware
    app.add_middleware(LoggingMiddleware)

    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(user_router, prefix="/users", tags=["Users"])
    app.include_router(address_router, prefix="/users/{user_id}/addresses", tags=["Addresses"])

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "user-service"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

