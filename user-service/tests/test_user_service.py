"""Tests for UserService."""
import pytest
from models.user import UserCreate, UserUpdate


class TestUserServiceCreate:
    def test_create_user_success(self, user_service, sample_user_data):
        result = user_service.create_user(sample_user_data)
        assert result.email == "john@example.com"
        assert result.username == "johndoe"
        assert result.first_name == "John"
        assert result.last_name == "Doe"
        assert result.is_active is True
        assert result.is_verified is False

    def test_create_user_duplicate_email(self, user_service, sample_user_data):
        user_service.create_user(sample_user_data)
        duplicate = UserCreate(
            email="john@example.com",
            username="different",
            password="SecurePass1!",
            first_name="Jane",
            last_name="Doe",
        )
        with pytest.raises(ValueError, match="already exists"):
            user_service.create_user(duplicate)

    def test_create_user_duplicate_username(self, user_service, sample_user_data):
        user_service.create_user(sample_user_data)
        duplicate = UserCreate(
            email="different@example.com",
            username="johndoe",
            password="SecurePass1!",
            first_name="Jane",
            last_name="Doe",
        )
        with pytest.raises(ValueError, match="already exists"):
            user_service.create_user(duplicate)

    def test_create_user_invalid_email(self, user_service):
        data = UserCreate(
            email="not-an-email",
            username="testuser",
            password="SecurePass1!",
            first_name="Test",
            last_name="User",
        )
        with pytest.raises(ValueError, match="Invalid email"):
            user_service.create_user(data)

    def test_create_user_weak_password(self, user_service):
        data = UserCreate(
            email="test@example.com",
            username="testuser",
            password="weak",
            first_name="Test",
            last_name="User",
        )
        with pytest.raises(ValueError, match="Password"):
            user_service.create_user(data)

    def test_create_user_short_username(self, user_service):
        data = UserCreate(
            email="test@example.com",
            username="ab",
            password="SecurePass1!",
            first_name="Test",
            last_name="User",
        )
        with pytest.raises(ValueError, match="at least 3"):
            user_service.create_user(data)


class TestUserServiceGet:
    def test_get_user_by_id(self, user_service, created_user):
        result = user_service.get_user(created_user.id)
        assert result is not None
        assert result.id == created_user.id

    def test_get_user_not_found(self, user_service):
        result = user_service.get_user("nonexistent-id")
        assert result is None

    def test_get_user_by_email(self, user_service, created_user):
        result = user_service.get_user_by_email("john@example.com")
        assert result is not None
        assert result.email == "john@example.com"


class TestUserServiceUpdate:
    def test_update_user_name(self, user_service, created_user):
        update = UserUpdate(first_name="Jonathan")
        result = user_service.update_user(created_user.id, update)
        assert result is not None
        assert result.first_name == "Jonathan"
        assert result.last_name == "Doe"  # unchanged

    def test_update_user_email(self, user_service, created_user):
        update = UserUpdate(email="newemail@example.com")
        result = user_service.update_user(created_user.id, update)
        assert result is not None
        assert result.email == "newemail@example.com"

    def test_update_user_not_found(self, user_service):
        update = UserUpdate(first_name="Ghost")
        result = user_service.update_user("nonexistent", update)
        assert result is None

    def test_update_user_invalid_email(self, user_service, created_user):
        update = UserUpdate(email="bad-email")
        with pytest.raises(ValueError, match="Invalid email"):
            user_service.update_user(created_user.id, update)


class TestUserServiceLifecycle:
    def test_deactivate_user(self, user_service, created_user):
        result = user_service.deactivate_user(created_user.id)
        assert result is True
        user = user_service.get_user(created_user.id)
        assert user.is_active is False

    def test_activate_user(self, user_service, created_user):
        user_service.deactivate_user(created_user.id)
        result = user_service.activate_user(created_user.id)
        assert result is True
        user = user_service.get_user(created_user.id)
        assert user.is_active is True

    def test_verify_user(self, user_service, created_user):
        result = user_service.verify_user(created_user.id)
        assert result is True
        user = user_service.get_user(created_user.id)
        assert user.is_verified is True

    def test_delete_user(self, user_service, created_user):
        result = user_service.delete_user(created_user.id)
        assert result is True
        assert user_service.get_user(created_user.id) is None

    def test_list_users(self, user_service, sample_user_data):
        user_service.create_user(sample_user_data)
        second = UserCreate(
            email="jane@example.com",
            username="janedoe",
            password="SecurePass1!",
            first_name="Jane",
            last_name="Doe",
        )
        user_service.create_user(second)
        users = user_service.list_users()
        assert len(users) == 2

