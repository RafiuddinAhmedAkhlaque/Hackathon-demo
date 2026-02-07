"""In-memory user repository."""
from typing import Dict, List, Optional
from models.user import User


class UserRepository:
    """Repository for user data access with in-memory storage."""

    def __init__(self):
        self._users: Dict[str, User] = {}
        self._email_index: Dict[str, str] = {}  # email -> user_id
        self._username_index: Dict[str, str] = {}  # username -> user_id

    def create(self, user: User) -> User:
        if user.email in self._email_index:
            raise ValueError(f"User with email '{user.email}' already exists")
        if user.username in self._username_index:
            raise ValueError(f"User with username '{user.username}' already exists")

        self._users[user.id] = user
        self._email_index[user.email] = user.id
        self._username_index[user.username] = user.id
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        user_id = self._email_index.get(email)
        if user_id:
            return self._users.get(user_id)
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        user_id = self._username_index.get(username)
        if user_id:
            return self._users.get(user_id)
        return None

    def update(self, user: User) -> User:
        if user.id not in self._users:
            raise ValueError(f"User with id '{user.id}' not found")

        old_user = self._users[user.id]

        # Update indexes if email or username changed
        if old_user.email != user.email:
            del self._email_index[old_user.email]
            self._email_index[user.email] = user.id

        if old_user.username != user.username:
            del self._username_index[old_user.username]
            self._username_index[user.username] = user.id

        self._users[user.id] = user
        return user

    def delete(self, user_id: str) -> bool:
        user = self._users.get(user_id)
        if not user:
            return False

        del self._email_index[user.email]
        del self._username_index[user.username]
        del self._users[user_id]
        return True

    def list_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        users = list(self._users.values())
        return users[skip: skip + limit]

    def count(self) -> int:
        return len(self._users)

