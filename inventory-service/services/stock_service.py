"""Stock service - business logic for inventory management."""
from datetime import datetime
from typing import List, Optional

from models.inventory_item import InventoryItem
from models.stock_movement import StockMovement, MovementType
from repositories.stock_repository import StockRepository
from repositories.warehouse_repository import WarehouseRepository


class StockService:
    def __init__(self, stock_repo: StockRepository, warehouse_repo: WarehouseRepository):
        self._stock_repo = stock_repo
        self._warehouse_repo = warehouse_repo
        self._movements: List[StockMovement] = []

    def add_inventory_item(self, product_id: str, sku: str, warehouse_id: str,
                           quantity: int = 0, reorder_point: int = 10) -> InventoryItem:
        warehouse = self._warehouse_repo.find_by_id(warehouse_id)
        if not warehouse:
            raise ValueError(f"Warehouse '{warehouse_id}' not found")
        if not warehouse.is_active:
            raise ValueError(f"Warehouse '{warehouse_id}' is not active")

        existing = self._stock_repo.find_by_sku_and_warehouse(sku, warehouse_id)
        if existing:
            raise ValueError(f"SKU '{sku}' already exists in warehouse '{warehouse_id}'")

        if quantity < 0:
            raise ValueError("Initial quantity cannot be negative")

        item = InventoryItem(
            product_id=product_id,
            sku=sku,
            warehouse_id=warehouse_id,
            quantity=quantity,
            reorder_point=reorder_point,
        )
        return self._stock_repo.save(item)

    def receive_stock(self, item_id: str, quantity: int, reference_id: str = "") -> InventoryItem:
        if quantity <= 0:
            raise ValueError("Receive quantity must be positive")

        item = self._stock_repo.find_by_id(item_id)
        if not item:
            raise ValueError(f"Inventory item '{item_id}' not found")

        if item.quantity + quantity > item.max_quantity:
            raise ValueError(f"Would exceed max quantity ({item.max_quantity})")

        item.quantity += quantity
        item.updated_at = datetime.utcnow()

        movement = StockMovement(
            inventory_item_id=item_id,
            warehouse_id=item.warehouse_id,
            movement_type=MovementType.INBOUND,
            quantity=quantity,
            reference_id=reference_id,
        )
        self._movements.append(movement)

        return self._stock_repo.save(item)

    def ship_stock(self, item_id: str, quantity: int, reference_id: str = "") -> InventoryItem:
        if quantity <= 0:
            raise ValueError("Ship quantity must be positive")

        item = self._stock_repo.find_by_id(item_id)
        if not item:
            raise ValueError(f"Inventory item '{item_id}' not found")

        if quantity > item.available_quantity:
            raise ValueError(
                f"Insufficient stock. Available: {item.available_quantity}, Requested: {quantity}"
            )

        item.quantity -= quantity
        item.updated_at = datetime.utcnow()

        movement = StockMovement(
            inventory_item_id=item_id,
            warehouse_id=item.warehouse_id,
            movement_type=MovementType.OUTBOUND,
            quantity=quantity,
            reference_id=reference_id,
        )
        self._movements.append(movement)

        return self._stock_repo.save(item)

    def reserve_stock(self, item_id: str, quantity: int) -> InventoryItem:
        if quantity <= 0:
            raise ValueError("Reserve quantity must be positive")

        item = self._stock_repo.find_by_id(item_id)
        if not item:
            raise ValueError(f"Inventory item '{item_id}' not found")

        if quantity > item.available_quantity:
            raise ValueError(
                f"Insufficient available stock. Available: {item.available_quantity}, Requested: {quantity}"
            )

        item.reserved_quantity += quantity
        item.updated_at = datetime.utcnow()
        return self._stock_repo.save(item)

    def release_reservation(self, item_id: str, quantity: int) -> InventoryItem:
        if quantity <= 0:
            raise ValueError("Release quantity must be positive")

        item = self._stock_repo.find_by_id(item_id)
        if not item:
            raise ValueError(f"Inventory item '{item_id}' not found")

        if quantity > item.reserved_quantity:
            raise ValueError("Cannot release more than reserved quantity")

        item.reserved_quantity -= quantity
        item.updated_at = datetime.utcnow()
        return self._stock_repo.save(item)

    def adjust_stock(self, item_id: str, new_quantity: int, notes: str = "") -> InventoryItem:
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")

        item = self._stock_repo.find_by_id(item_id)
        if not item:
            raise ValueError(f"Inventory item '{item_id}' not found")

        old_quantity = item.quantity
        item.quantity = new_quantity
        item.updated_at = datetime.utcnow()

        movement = StockMovement(
            inventory_item_id=item_id,
            warehouse_id=item.warehouse_id,
            movement_type=MovementType.ADJUSTMENT,
            quantity=new_quantity - old_quantity,
            notes=notes,
        )
        self._movements.append(movement)

        return self._stock_repo.save(item)

    def get_item(self, item_id: str) -> Optional[InventoryItem]:
        return self._stock_repo.find_by_id(item_id)

    def get_stock_by_product(self, product_id: str) -> List[InventoryItem]:
        return self._stock_repo.find_by_product(product_id)

    def get_stock_by_warehouse(self, warehouse_id: str) -> List[InventoryItem]:
        return self._stock_repo.find_by_warehouse(warehouse_id)

    def get_total_available(self, product_id: str) -> int:
        return self._stock_repo.get_total_quantity(product_id)

    def get_low_stock_items(self) -> List[InventoryItem]:
        return self._stock_repo.find_low_stock()

    def get_out_of_stock_items(self) -> List[InventoryItem]:
        return self._stock_repo.find_out_of_stock()

    def get_movements(self, item_id: str = None) -> List[StockMovement]:
        if item_id:
            return [m for m in self._movements if m.inventory_item_id == item_id]
        return self._movements

