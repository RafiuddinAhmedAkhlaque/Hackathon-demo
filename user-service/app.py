"""User Service - Main Application Entry Point"""
from fastapi import FastAPI
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.address_routes import router as address_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="User Service",
        description="Handles user registration, authentication, profile management, and address book.",
        version="1.0.0",
    )

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

