"""User model definitions."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
import uuid


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    username: str
    hashed_password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

