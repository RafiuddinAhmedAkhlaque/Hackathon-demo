"""Stock movement model for tracking inventory changes."""
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import uuid


class MovementType(str, Enum):
    INBOUND = "inbound"          # Stock received
    OUTBOUND = "outbound"        # Stock shipped/sold
    TRANSFER = "transfer"        # Between warehouses
    ADJUSTMENT = "adjustment"    # Manual adjustment
    RETURN = "return"            # Customer return
    DAMAGED = "damaged"          # Damaged/written off


@dataclass
class StockMovement:
    inventory_item_id: str
    warehouse_id: str
    movement_type: MovementType
    quantity: int
    reference_id: str = ""  # order ID, transfer ID, etc.
    notes: str = ""
    destination_warehouse_id: str = ""  # for transfers
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "inventory_item_id": self.inventory_item_id,
            "warehouse_id": self.warehouse_id,
            "movement_type": self.movement_type.value,
            "quantity": self.quantity,
            "reference_id": self.reference_id,
            "notes": self.notes,
            "destination_warehouse_id": self.destination_warehouse_id,
            "created_at": self.created_at.isoformat(),
        }

