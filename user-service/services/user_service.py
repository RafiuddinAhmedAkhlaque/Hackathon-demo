"""User service - business logic for user management."""
from datetime import datetime
from typing import List, Optional

from models.user import User, UserCreate, UserUpdate, UserResponse
from repositories.user_repository import UserRepository
from utils.password_hasher import PasswordHasher
from utils.validators import validate_email, validate_username, validate_phone, validate_name


class UserService:
    """Handles user-related business logic."""

    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher):
        self._repo = user_repository
        self._hasher = password_hasher

    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Register a new user."""
        # Validate input
        valid, msg = validate_email(user_data.email)
        if not valid:
            raise ValueError(msg)

        valid, msg = validate_username(user_data.username)
        if not valid:
            raise ValueError(msg)

        valid, msg = validate_name(user_data.first_name, "First name")
        if not valid:
            raise ValueError(msg)

        valid, msg = validate_name(user_data.last_name, "Last name")
        if not valid:
            raise ValueError(msg)

        if user_data.phone:
            valid, msg = validate_phone(user_data.phone)
            if not valid:
                raise ValueError(msg)

        valid, msg = PasswordHasher.is_strong_password(user_data.password)
        if not valid:
            raise ValueError(msg)

        # Check uniqueness
        if self._repo.get_by_email(user_data.email):
            raise ValueError(f"User with email '{user_data.email}' already exists")

        if self._repo.get_by_username(user_data.username):
            raise ValueError(f"User with username '{user_data.username}' already exists")

        # Create user
        hashed_pw = self._hasher.hash_password(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_pw,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
        )

        created = self._repo.create(user)
        return self._to_response(created)

    def get_user(self, user_id: str) -> Optional[UserResponse]:
        """Get a user by ID."""
        user = self._repo.get_by_id(user_id)
        if user:
            return self._to_response(user)
        return None

    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get a user by email."""
        user = self._repo.get_by_email(email)
        if user:
            return self._to_response(user)
        return None

    def update_user(self, user_id: str, update_data: UserUpdate) -> Optional[UserResponse]:
        """Update user profile information."""
        user = self._repo.get_by_id(user_id)
        if not user:
            return None

        if update_data.email is not None:
            valid, msg = validate_email(update_data.email)
            if not valid:
                raise ValueError(msg)
            existing = self._repo.get_by_email(update_data.email)
            if existing and existing.id != user_id:
                raise ValueError(f"Email '{update_data.email}' is already taken")
            user.email = update_data.email

        if update_data.first_name is not None:
            valid, msg = validate_name(update_data.first_name, "First name")
            if not valid:
                raise ValueError(msg)
            user.first_name = update_data.first_name

        if update_data.last_name is not None:
            valid, msg = validate_name(update_data.last_name, "Last name")
            if not valid:
                raise ValueError(msg)
            user.last_name = update_data.last_name

        if update_data.phone is not None:
            valid, msg = validate_phone(update_data.phone)
            if not valid:
                raise ValueError(msg)
            user.phone = update_data.phone

        user.updated_at = datetime.utcnow()
        updated = self._repo.update(user)
        return self._to_response(updated)

    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user account."""
        user = self._repo.get_by_id(user_id)
        if not user:
            return False
        user.is_active = False
        user.updated_at = datetime.utcnow()
        self._repo.update(user)
        return True

    def activate_user(self, user_id: str) -> bool:
        """Activate a user account."""
        user = self._repo.get_by_id(user_id)
        if not user:
            return False
        user.is_active = True
        user.updated_at = datetime.utcnow()
        self._repo.update(user)
        return True

    def verify_user(self, user_id: str) -> bool:
        """Mark a user as verified."""
        user = self._repo.get_by_id(user_id)
        if not user:
            return False
        user.is_verified = True
        user.updated_at = datetime.utcnow()
        self._repo.update(user)
        return True

    def list_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """List all users with pagination."""
        users = self._repo.list_all(skip=skip, limit=limit)
        return [self._to_response(u) for u in users]

    def delete_user(self, user_id: str) -> bool:
        """Permanently delete a user."""
        return self._repo.delete(user_id)

    @staticmethod
    def _to_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

