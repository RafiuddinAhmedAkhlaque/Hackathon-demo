"""Warehouse model."""
from datetime import datetime
from dataclasses import dataclass, field
import uuid


@dataclass
class Warehouse:
    name: str
    code: str  # unique short code, e.g. "WH-EAST-01"
    address: str
    city: str
    state: str
    country: str = "US"
    capacity: int = 10000
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "capacity": self.capacity,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

