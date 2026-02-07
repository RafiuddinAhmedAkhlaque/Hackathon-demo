"""Address service - business logic for managing user addresses."""
from datetime import datetime
from typing import List, Optional

from models.address import Address, AddressCreate, AddressUpdate, AddressResponse
from repositories.address_repository import AddressRepository
from repositories.user_repository import UserRepository
from utils.validators import validate_postal_code, validate_name


class AddressService:
    """Handles address-related business logic."""

    MAX_ADDRESSES_PER_USER = 10

    def __init__(self, address_repository: AddressRepository, user_repository: UserRepository):
        self._address_repo = address_repository
        self._user_repo = user_repository

    def add_address(self, user_id: str, address_data: AddressCreate) -> AddressResponse:
        """Add a new address for a user."""
        # Verify user exists
        user = self._user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User '{user_id}' not found")

        # Check address limit
        existing = self._address_repo.get_by_user_id(user_id)
        if len(existing) >= self.MAX_ADDRESSES_PER_USER:
            raise ValueError(
                f"Maximum number of addresses ({self.MAX_ADDRESSES_PER_USER}) reached"
            )

        # Validate postal code
        valid, msg = validate_postal_code(address_data.postal_code, address_data.country)
        if not valid:
            raise ValueError(msg)

        # Validate label
        valid, msg = validate_name(address_data.label, "Address label")
        if not valid:
            raise ValueError(msg)

        # If this is the first address, make it default
        is_default = address_data.is_default
        if len(existing) == 0:
            is_default = True

        address = Address(
            user_id=user_id,
            label=address_data.label,
            street_line1=address_data.street_line1,
            street_line2=address_data.street_line2,
            city=address_data.city,
            state=address_data.state,
            postal_code=address_data.postal_code,
            country=address_data.country,
            is_default=is_default,
        )

        created = self._address_repo.create(address)
        return self._to_response(created)

    def get_address(self, user_id: str, address_id: str) -> Optional[AddressResponse]:
        """Get a specific address."""
        address = self._address_repo.get_by_id(address_id)
        if address and address.user_id == user_id:
            return self._to_response(address)
        return None

    def list_addresses(self, user_id: str) -> List[AddressResponse]:
        """List all addresses for a user."""
        addresses = self._address_repo.get_by_user_id(user_id)
        return [self._to_response(a) for a in addresses]

    def update_address(
        self, user_id: str, address_id: str, update_data: AddressUpdate
    ) -> Optional[AddressResponse]:
        """Update an existing address."""
        address = self._address_repo.get_by_id(address_id)
        if not address or address.user_id != user_id:
            return None

        if update_data.label is not None:
            valid, msg = validate_name(update_data.label, "Address label")
            if not valid:
                raise ValueError(msg)
            address.label = update_data.label

        if update_data.street_line1 is not None:
            address.street_line1 = update_data.street_line1
        if update_data.street_line2 is not None:
            address.street_line2 = update_data.street_line2
        if update_data.city is not None:
            address.city = update_data.city
        if update_data.state is not None:
            address.state = update_data.state
        if update_data.country is not None:
            address.country = update_data.country

        if update_data.postal_code is not None:
            country = update_data.country or address.country
            valid, msg = validate_postal_code(update_data.postal_code, country)
            if not valid:
                raise ValueError(msg)
            address.postal_code = update_data.postal_code

        if update_data.is_default is not None:
            address.is_default = update_data.is_default

        address.updated_at = datetime.utcnow()
        updated = self._address_repo.update(address)
        return self._to_response(updated)

    def delete_address(self, user_id: str, address_id: str) -> bool:
        """Delete an address."""
        address = self._address_repo.get_by_id(address_id)
        if not address or address.user_id != user_id:
            return False
        return self._address_repo.delete(address_id)

    def get_default_address(self, user_id: str) -> Optional[AddressResponse]:
        """Get the default address for a user."""
        address = self._address_repo.get_default_for_user(user_id)
        if address:
            return self._to_response(address)
        return None

    def set_default_address(self, user_id: str, address_id: str) -> Optional[AddressResponse]:
        """Set an address as the default."""
        address = self._address_repo.get_by_id(address_id)
        if not address or address.user_id != user_id:
            return None

        address.is_default = True
        address.updated_at = datetime.utcnow()
        updated = self._address_repo.update(address)
        return self._to_response(updated)

    @staticmethod
    def _to_response(address: Address) -> AddressResponse:
        return AddressResponse(
            id=address.id,
            user_id=address.user_id,
            label=address.label,
            street_line1=address.street_line1,
            street_line2=address.street_line2,
            city=address.city,
            state=address.state,
            postal_code=address.postal_code,
            country=address.country,
            is_default=address.is_default,
            created_at=address.created_at,
            updated_at=address.updated_at,
        )

