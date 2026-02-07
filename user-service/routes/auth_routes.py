"""Authentication route handlers."""
from fastapi import APIRouter, HTTPException, Header
from typing import Optional

from models.session import LoginRequest, LoginResponse
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from utils.password_hasher import PasswordHasher
from utils.token_manager import TokenManager

router = APIRouter()

# Initialize dependencies (in production, use proper DI)
_user_repo = UserRepository()
_hasher = PasswordHasher()
_token_manager = TokenManager()
_auth_service = AuthService(_user_repo, _hasher, _token_manager)


def get_auth_service() -> AuthService:
    return _auth_service


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest):
    """Authenticate a user and return an access token."""
    result = _auth_service.login(login_data)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return result


@router.post("/logout")
def logout(authorization: Optional[str] = Header(None)):
    """Invalidate the current session."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")

    token = authorization.replace("Bearer ", "")
    success = _auth_service.logout(token)
    if not success:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": "Successfully logged out"}


@router.post("/change-password")
def change_password(
    old_password: str,
    new_password: str,
    authorization: Optional[str] = Header(None),
):
    """Change the current user's password."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")

    token = authorization.replace("Bearer ", "")
    user_id = _auth_service.validate_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    try:
        success = _auth_service.change_password(user_id, old_password, new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not success:
        raise HTTPException(status_code=400, detail="Invalid old password")
    return {"message": "Password changed successfully"}

