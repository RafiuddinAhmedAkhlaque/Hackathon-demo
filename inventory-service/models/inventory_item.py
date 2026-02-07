"""Inventory item model."""
from datetime import datetime
from dataclasses import dataclass, field
import uuid


@dataclass
class InventoryItem:
    product_id: str
    sku: str
    warehouse_id: str
    quantity: int = 0
    reserved_quantity: int = 0
    reorder_point: int = 10
    reorder_quantity: int = 50
    max_quantity: int = 1000
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def available_quantity(self) -> int:
        return max(0, self.quantity - self.reserved_quantity)

    @property
    def is_low_stock(self) -> bool:
        return self.available_quantity <= self.reorder_point

    @property
    def is_out_of_stock(self) -> bool:
        return self.available_quantity <= 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "sku": self.sku,
            "warehouse_id": self.warehouse_id,
            "quantity": self.quantity,
            "reserved_quantity": self.reserved_quantity,
            "available_quantity": self.available_quantity,
            "reorder_point": self.reorder_point,
            "reorder_quantity": self.reorder_quantity,
            "max_quantity": self.max_quantity,
            "is_low_stock": self.is_low_stock,
            "is_out_of_stock": self.is_out_of_stock,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

