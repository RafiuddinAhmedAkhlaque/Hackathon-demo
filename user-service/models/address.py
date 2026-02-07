"""Address model definitions."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid


class Address(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    label: str  # e.g., "Home", "Work", "Shipping"
    street_line1: str
    street_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = "US"
    is_default: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AddressCreate(BaseModel):
    label: str
    street_line1: str
    street_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = "US"
    is_default: bool = False


class AddressUpdate(BaseModel):
    label: Optional[str] = None
    street_line1: Optional[str] = None
    street_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    is_default: Optional[bool] = None


class AddressResponse(BaseModel):
    id: str
    user_id: str
    label: str
    street_line1: str
    street_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str
    is_default: bool
    created_at: datetime
    updated_at: datetime

