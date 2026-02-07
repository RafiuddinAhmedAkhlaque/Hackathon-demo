"""Authentication service - handles login, logout, and token management."""
from typing import Optional

from models.user import User
from models.session import Session, LoginRequest, LoginResponse
from repositories.user_repository import UserRepository
from utils.password_hasher import PasswordHasher
from utils.token_manager import TokenManager


class AuthService:
    """Handles authentication business logic."""

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_manager: TokenManager,
    ):
        self._user_repo = user_repository
        self._hasher = password_hasher
        self._token_manager = token_manager
        self._sessions: dict[str, Session] = {}  # token -> Session

    def login(self, login_data: LoginRequest) -> Optional[LoginResponse]:
        """Authenticate a user and create a session."""
        user = self._user_repo.get_by_email(login_data.email)
        if not user:
            return None

        if not user.is_active:
            return None

        if not self._hasher.verify_password(login_data.password, user.hashed_password):
            return None

        # Create token and session
        token = self._token_manager.create_access_token(user.id)
        session = Session(user_id=user.id, token=token)
        self._sessions[token] = session

        return LoginResponse(
            access_token=token,
            user_id=user.id,
            expires_at=session.expires_at,
        )

    def logout(self, token: str) -> bool:
        """Invalidate a session."""
        session = self._sessions.get(token)
        if session:
            session.is_active = False
            return True
        return False

    def validate_token(self, token: str) -> Optional[str]:
        """Validate a token and return the user_id if valid."""
        # Check session store
        session = self._sessions.get(token)
        if session and not session.is_valid():
            return None

        # Verify token signature and expiration
        user_id = self._token_manager.get_user_id_from_token(token)
        return user_id

    def get_current_user(self, token: str) -> Optional[User]:
        """Get the current authenticated user from a token."""
        user_id = self.validate_token(token)
        if not user_id:
            return None
        return self._user_repo.get_by_id(user_id)

    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """Change a user's password."""
        user = self._user_repo.get_by_id(user_id)
        if not user:
            return False

        if not self._hasher.verify_password(old_password, user.hashed_password):
            return False

        valid, msg = PasswordHasher.is_strong_password(new_password)
        if not valid:
            raise ValueError(msg)

        user.hashed_password = self._hasher.hash_password(new_password)
        self._user_repo.update(user)

        # Invalidate all existing sessions for this user
        self._invalidate_user_sessions(user_id)
        return True

    def _invalidate_user_sessions(self, user_id: str):
        """Invalidate all sessions for a user."""
        for session in self._sessions.values():
            if session.user_id == user_id:
                session.is_active = False

    def get_active_sessions_count(self, user_id: str) -> int:
        """Get the number of active sessions for a user."""
        return sum(
            1 for s in self._sessions.values()
            if s.user_id == user_id and s.is_valid()
        )

