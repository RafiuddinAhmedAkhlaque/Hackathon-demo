"""Tests for AddressService."""
import pytest
from models.user import User
from models.address import AddressCreate, AddressUpdate
from utils.password_hasher import PasswordHasher


def _create_user(user_repository):
    """Helper to create a test user in the repository."""
    hasher = PasswordHasher()
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=hasher.hash_password("SecurePass1!"),
        first_name="Test",
        last_name="User",
    )
    user_repository.create(user)
    return user


class TestAddressServiceAdd:
    def test_add_address_success(self, address_service, user_repository):
        user = _create_user(user_repository)
        data = AddressCreate(
            label="Home",
            street_line1="123 Main St",
            city="Springfield",
            state="IL",
            postal_code="62701",
            country="US",
        )
        result = address_service.add_address(user.id, data)
        assert result.label == "Home"
        assert result.street_line1 == "123 Main St"
        assert result.is_default is True  # First address becomes default

    def test_add_address_user_not_found(self, address_service):
        data = AddressCreate(
            label="Home",
            street_line1="123 Main St",
            city="Springfield",
            state="IL",
            postal_code="62701",
        )
        with pytest.raises(ValueError, match="not found"):
            address_service.add_address("nonexistent", data)

    def test_add_second_address_not_default(self, address_service, user_repository):
        user = _create_user(user_repository)
        first = AddressCreate(
            label="Home",
            street_line1="123 Main St",
            city="Springfield",
            state="IL",
            postal_code="62701",
        )
        address_service.add_address(user.id, first)

        second = AddressCreate(
            label="Work",
            street_line1="456 Office Blvd",
            city="Springfield",
            state="IL",
            postal_code="62702",
        )
        result = address_service.add_address(user.id, second)
        assert result.is_default is False

    def test_add_address_invalid_postal_code(self, address_service, user_repository):
        user = _create_user(user_repository)
        data = AddressCreate(
            label="Home",
            street_line1="123 Main St",
            city="Springfield",
            state="IL",
            postal_code="INVALID",
            country="US",
        )
        with pytest.raises(ValueError, match="postal code"):
            address_service.add_address(user.id, data)


class TestAddressServiceGet:
    def test_get_address(self, address_service, user_repository):
        user = _create_user(user_repository)
        data = AddressCreate(
            label="Home",
            street_line1="123 Main St",
            city="Springfield",
            state="IL",
            postal_code="62701",
        )
        created = address_service.add_address(user.id, data)
        result = address_service.get_address(user.id, created.id)
        assert result is not None
        assert result.id == created.id

    def test_get_address_wrong_user(self, address_service, user_repository):
        user = _create_user(user_repository)
        data = AddressCreate(
            label="Home",
            street_line1="123 Main St",
            city="Springfield",
            state="IL",
            postal_code="62701",
        )
        created = address_service.add_address(user.id, data)
        result = address_service.get_address("wrong-user", created.id)
        assert result is None

    def test_list_addresses(self, address_service, user_repository):
        user = _create_user(user_repository)
        for label in ["Home", "Work"]:
            data = AddressCreate(
                label=label,
                street_line1=f"{label} St",
                city="Springfield",
                state="IL",
                postal_code="62701",
            )
            address_service.add_address(user.id, data)
        addresses = address_service.list_addresses(user.id)
        assert len(addresses) == 2

    def test_get_default_address(self, address_service, user_repository):
        user = _create_user(user_repository)
        data = AddressCreate(
            label="Home",
            street_line1="123 Main St",
            city="Springfield",
            state="IL",
            postal_code="62701",
        )
        address_service.add_address(user.id, data)
        default = address_service.get_default_address(user.id)
        assert default is not None
        assert default.label == "Home"


class TestAddressServiceUpdate:
    def test_update_address(self, address_service, user_repository):
        user = _create_user(user_repository)
        data = AddressCreate(
            label="Home",
            street_line1="123 Main St",
            city="Springfield",
            state="IL",
            postal_code="62701",
        )
        created = address_service.add_address(user.id, data)
        update = AddressUpdate(label="Primary Home", city="Chicago")
        result = address_service.update_address(user.id, created.id, update)
        assert result.label == "Primary Home"
        assert result.city == "Chicago"
        assert result.street_line1 == "123 Main St"  # Unchanged

    def test_update_address_not_found(self, address_service, user_repository):
        user = _create_user(user_repository)
        update = AddressUpdate(label="Updated")
        result = address_service.update_address(user.id, "nonexistent", update)
        assert result is None


class TestAddressServiceDelete:
    def test_delete_address(self, address_service, user_repository):
        user = _create_user(user_repository)
        data = AddressCreate(
            label="Home",
            street_line1="123 Main St",
            city="Springfield",
            state="IL",
            postal_code="62701",
        )
        created = address_service.add_address(user.id, data)
        result = address_service.delete_address(user.id, created.id)
        assert result is True
        assert address_service.get_address(user.id, created.id) is None

    def test_delete_address_wrong_user(self, address_service, user_repository):
        user = _create_user(user_repository)
        data = AddressCreate(
            label="Home",
            street_line1="123 Main St",
            city="Springfield",
            state="IL",
            postal_code="62701",
        )
        created = address_service.add_address(user.id, data)
        result = address_service.delete_address("wrong-user", created.id)
        assert result is False


class TestAddressServiceSetDefault:
    def test_set_default_address(self, address_service, user_repository):
        user = _create_user(user_repository)
        first = AddressCreate(
            label="Home",
            street_line1="123 Main St",
            city="Springfield",
            state="IL",
            postal_code="62701",
        )
        address_service.add_address(user.id, first)

        second = AddressCreate(
            label="Work",
            street_line1="456 Office Blvd",
            city="Springfield",
            state="IL",
            postal_code="62702",
        )
        second_created = address_service.add_address(user.id, second)

        result = address_service.set_default_address(user.id, second_created.id)
        assert result is not None
        assert result.is_default is True

