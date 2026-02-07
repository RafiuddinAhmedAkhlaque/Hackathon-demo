"""Shared test fixtures for user-service tests."""
import sys
import os
import pytest

# Add the service root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from repositories.user_repository import UserRepository
from repositories.address_repository import AddressRepository
from utils.password_hasher import PasswordHasher
from utils.token_manager import TokenManager
from services.user_service import UserService
from services.auth_service import AuthService
from services.address_service import AddressService
from models.user import UserCreate


@pytest.fixture
def user_repository():
    return UserRepository()


@pytest.fixture
def address_repository():
    return AddressRepository()


@pytest.fixture
def password_hasher():
    return PasswordHasher()


@pytest.fixture
def token_manager():
    return TokenManager(secret_key="test-secret-key")


@pytest.fixture
def user_service(user_repository, password_hasher):
    return UserService(user_repository, password_hasher)


@pytest.fixture
def auth_service(user_repository, password_hasher, token_manager):
    return AuthService(user_repository, password_hasher, token_manager)


@pytest.fixture
def address_service(address_repository, user_repository):
    return AddressService(address_repository, user_repository)


@pytest.fixture
def sample_user_data():
    return UserCreate(
        email="john@example.com",
        username="johndoe",
        password="SecurePass1!",
        first_name="John",
        last_name="Doe",
        phone="+1234567890",
    )


@pytest.fixture
def created_user(user_service, sample_user_data):
    return user_service.create_user(sample_user_data)

