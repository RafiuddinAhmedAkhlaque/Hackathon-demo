"""User route handlers."""
from fastapi import APIRouter, HTTPException, Query
from typing import List

from models.user import UserCreate, UserUpdate, UserResponse
from services.user_service import UserService
from repositories.user_repository import UserRepository
from utils.password_hasher import PasswordHasher

router = APIRouter()

# Initialize dependencies
_user_repo = UserRepository()
_hasher = PasswordHasher()
_user_service = UserService(_user_repo, _hasher)


def get_user_service() -> UserService:
    return _user_service


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate):
    """Register a new user."""
    try:
        return _user_service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[UserResponse])
def list_users(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    """List all users with pagination."""
    return _user_service.list_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    """Get a user by ID."""
    user = _user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, update_data: UserUpdate):
    """Update a user's profile."""
    try:
        user = _user_service.update_user(user_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str):
    """Delete a user."""
    success = _user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/{user_id}/deactivate")
def deactivate_user(user_id: str):
    """Deactivate a user account."""
    success = _user_service.deactivate_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deactivated"}


@router.post("/{user_id}/activate")
def activate_user(user_id: str):
    """Activate a user account."""
    success = _user_service.activate_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User activated"}


@router.post("/{user_id}/verify")
def verify_user(user_id: str):
    """Mark a user as verified."""
    success = _user_service.verify_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User verified"}

