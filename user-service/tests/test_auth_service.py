"""Tests for AuthService."""
import pytest
from models.user import User, UserCreate
from models.session import LoginRequest
from utils.password_hasher import PasswordHasher


class TestAuthServiceLogin:
    def _create_test_user(self, auth_service, password_hasher):
        """Helper to create a test user directly in the repository."""
        hashed = password_hasher.hash_password("SecurePass1!")
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=hashed,
            first_name="Test",
            last_name="User",
        )
        auth_service._user_repo.create(user)
        return user

    def test_login_success(self, auth_service, password_hasher):
        user = self._create_test_user(auth_service, password_hasher)
        login_data = LoginRequest(email="test@example.com", password="SecurePass1!")
        result = auth_service.login(login_data)
        assert result is not None
        assert result.user_id == user.id
        assert result.access_token is not None

    def test_login_wrong_password(self, auth_service, password_hasher):
        self._create_test_user(auth_service, password_hasher)
        login_data = LoginRequest(email="test@example.com", password="WrongPass1!")
        result = auth_service.login(login_data)
        assert result is None

    def test_login_wrong_email(self, auth_service, password_hasher):
        self._create_test_user(auth_service, password_hasher)
        login_data = LoginRequest(email="wrong@example.com", password="SecurePass1!")
        result = auth_service.login(login_data)
        assert result is None

    def test_login_inactive_user(self, auth_service, password_hasher):
        user = self._create_test_user(auth_service, password_hasher)
        user.is_active = False
        auth_service._user_repo.update(user)
        login_data = LoginRequest(email="test@example.com", password="SecurePass1!")
        result = auth_service.login(login_data)
        assert result is None


class TestAuthServiceLogout:
    def test_logout_success(self, auth_service, password_hasher):
        hashed = password_hasher.hash_password("SecurePass1!")
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=hashed,
            first_name="Test",
            last_name="User",
        )
        auth_service._user_repo.create(user)
        login_data = LoginRequest(email="test@example.com", password="SecurePass1!")
        login_result = auth_service.login(login_data)
        result = auth_service.logout(login_result.access_token)
        assert result is True

    def test_logout_invalid_token(self, auth_service):
        result = auth_service.logout("invalid-token")
        assert result is False


class TestAuthServiceTokenValidation:
    def test_validate_valid_token(self, auth_service, password_hasher):
        hashed = password_hasher.hash_password("SecurePass1!")
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=hashed,
            first_name="Test",
            last_name="User",
        )
        auth_service._user_repo.create(user)
        login_data = LoginRequest(email="test@example.com", password="SecurePass1!")
        login_result = auth_service.login(login_data)
        user_id = auth_service.validate_token(login_result.access_token)
        assert user_id == user.id

    def test_validate_invalid_token(self, auth_service):
        user_id = auth_service.validate_token("invalid-token")
        assert user_id is None

    def test_get_current_user(self, auth_service, password_hasher):
        hashed = password_hasher.hash_password("SecurePass1!")
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=hashed,
            first_name="Test",
            last_name="User",
        )
        auth_service._user_repo.create(user)
        login_data = LoginRequest(email="test@example.com", password="SecurePass1!")
        login_result = auth_service.login(login_data)
        current = auth_service.get_current_user(login_result.access_token)
        assert current is not None
        assert current.id == user.id


class TestAuthServiceChangePassword:
    def test_change_password_success(self, auth_service, password_hasher):
        hashed = password_hasher.hash_password("SecurePass1!")
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=hashed,
            first_name="Test",
            last_name="User",
        )
        auth_service._user_repo.create(user)
        result = auth_service.change_password(user.id, "SecurePass1!", "NewSecure2@")
        assert result is True

    def test_change_password_wrong_old(self, auth_service, password_hasher):
        hashed = password_hasher.hash_password("SecurePass1!")
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=hashed,
            first_name="Test",
            last_name="User",
        )
        auth_service._user_repo.create(user)
        result = auth_service.change_password(user.id, "WrongPass1!", "NewSecure2@")
        assert result is False

    def test_change_password_weak_new(self, auth_service, password_hasher):
        hashed = password_hasher.hash_password("SecurePass1!")
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=hashed,
            first_name="Test",
            last_name="User",
        )
        auth_service._user_repo.create(user)
        with pytest.raises(ValueError, match="Password"):
            auth_service.change_password(user.id, "SecurePass1!", "weak")

