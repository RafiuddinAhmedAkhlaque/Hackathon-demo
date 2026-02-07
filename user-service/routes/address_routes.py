"""Address route handlers."""
from fastapi import APIRouter, HTTPException
from typing import List

from models.address import AddressCreate, AddressUpdate, AddressResponse
from services.address_service import AddressService
from repositories.address_repository import AddressRepository
from repositories.user_repository import UserRepository

router = APIRouter()

# Initialize dependencies
_address_repo = AddressRepository()
_user_repo = UserRepository()
_address_service = AddressService(_address_repo, _user_repo)


def get_address_service() -> AddressService:
    return _address_service


@router.post("/", response_model=AddressResponse, status_code=201)
def add_address(user_id: str, address_data: AddressCreate):
    """Add a new address for a user."""
    try:
        return _address_service.add_address(user_id, address_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[AddressResponse])
def list_addresses(user_id: str):
    """List all addresses for a user."""
    return _address_service.list_addresses(user_id)


@router.get("/default", response_model=AddressResponse)
def get_default_address(user_id: str):
    """Get the default address for a user."""
    address = _address_service.get_default_address(user_id)
    if not address:
        raise HTTPException(status_code=404, detail="No default address found")
    return address


@router.get("/{address_id}", response_model=AddressResponse)
def get_address(user_id: str, address_id: str):
    """Get a specific address."""
    address = _address_service.get_address(user_id, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.put("/{address_id}", response_model=AddressResponse)
def update_address(user_id: str, address_id: str, update_data: AddressUpdate):
    """Update an existing address."""
    try:
        address = _address_service.update_address(user_id, address_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.delete("/{address_id}", status_code=204)
def delete_address(user_id: str, address_id: str):
    """Delete an address."""
    success = _address_service.delete_address(user_id, address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")


@router.post("/{address_id}/set-default", response_model=AddressResponse)
def set_default_address(user_id: str, address_id: str):
    """Set an address as the default."""
    address = _address_service.set_default_address(user_id, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

