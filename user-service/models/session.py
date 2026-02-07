"""Session model definitions."""
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import uuid


class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    token: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(hours=24)
    )

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

    def is_valid(self) -> bool:
        return self.is_active and not self.is_expired()


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    expires_at: datetime


class TokenPayload(BaseModel):
    user_id: str
    exp: datetime
    iat: datetime = Field(default_factory=datetime.utcnow)

