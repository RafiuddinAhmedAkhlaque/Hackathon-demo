"""In-memory address repository."""
from typing import Dict, List, Optional
from models.address import Address


class AddressRepository:
    """Repository for address data access with in-memory storage."""

    def __init__(self):
        self._addresses: Dict[str, Address] = {}
        self._user_addresses: Dict[str, List[str]] = {}  # user_id -> [address_ids]

    def create(self, address: Address) -> Address:
        self._addresses[address.id] = address

        if address.user_id not in self._user_addresses:
            self._user_addresses[address.user_id] = []
        self._user_addresses[address.user_id].append(address.id)

        # If this is set as default, unset other defaults for this user
        if address.is_default:
            self._unset_other_defaults(address.user_id, address.id)

        return address

    def get_by_id(self, address_id: str) -> Optional[Address]:
        return self._addresses.get(address_id)

    def get_by_user_id(self, user_id: str) -> List[Address]:
        address_ids = self._user_addresses.get(user_id, [])
        return [self._addresses[aid] for aid in address_ids if aid in self._addresses]

    def get_default_for_user(self, user_id: str) -> Optional[Address]:
        addresses = self.get_by_user_id(user_id)
        for addr in addresses:
            if addr.is_default:
                return addr
        return None

    def update(self, address: Address) -> Address:
        if address.id not in self._addresses:
            raise ValueError(f"Address with id '{address.id}' not found")

        if address.is_default:
            self._unset_other_defaults(address.user_id, address.id)

        self._addresses[address.id] = address
        return address

    def delete(self, address_id: str) -> bool:
        address = self._addresses.get(address_id)
        if not address:
            return False

        if address.user_id in self._user_addresses:
            self._user_addresses[address.user_id] = [
                aid for aid in self._user_addresses[address.user_id] if aid != address_id
            ]

        del self._addresses[address_id]
        return True

    def delete_all_for_user(self, user_id: str) -> int:
        address_ids = self._user_addresses.get(user_id, [])
        count = 0
        for aid in address_ids:
            if aid in self._addresses:
                del self._addresses[aid]
                count += 1
        self._user_addresses[user_id] = []
        return count

    def _unset_other_defaults(self, user_id: str, exclude_id: str):
        addresses = self.get_by_user_id(user_id)
        for addr in addresses:
            if addr.id != exclude_id and addr.is_default:
                addr.is_default = False
                self._addresses[addr.id] = addr

