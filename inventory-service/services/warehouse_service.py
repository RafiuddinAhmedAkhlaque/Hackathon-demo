"""Warehouse service - business logic for warehouse management."""
from datetime import datetime
from typing import List, Optional

from models.warehouse import Warehouse
from repositories.warehouse_repository import WarehouseRepository
from repositories.stock_repository import StockRepository


class WarehouseService:
    def __init__(self, warehouse_repo: WarehouseRepository, stock_repo: StockRepository):
        self._warehouse_repo = warehouse_repo
        self._stock_repo = stock_repo

    def create_warehouse(self, name: str, code: str, address: str,
                         city: str, state: str, country: str = "US",
                         capacity: int = 10000) -> Warehouse:
        if not name or not name.strip():
            raise ValueError("Warehouse name is required")
        if not code or not code.strip():
            raise ValueError("Warehouse code is required")
        if len(code) > 20:
            raise ValueError("Warehouse code must be 20 characters or less")

        existing = self._warehouse_repo.find_by_code(code)
        if existing:
            raise ValueError(f"Warehouse with code '{code}' already exists")

        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        warehouse = Warehouse(
            name=name,
            code=code,
            address=address,
            city=city,
            state=state,
            country=country,
            capacity=capacity,
        )
        return self._warehouse_repo.save(warehouse)

    def get_warehouse(self, warehouse_id: str) -> Optional[Warehouse]:
        return self._warehouse_repo.find_by_id(warehouse_id)

    def get_warehouse_by_code(self, code: str) -> Optional[Warehouse]:
        return self._warehouse_repo.find_by_code(code)

    def list_warehouses(self, active_only: bool = False) -> List[Warehouse]:
        if active_only:
            return self._warehouse_repo.find_active()
        return self._warehouse_repo.get_all()

    def update_warehouse(self, warehouse_id: str, **kwargs) -> Optional[Warehouse]:
        warehouse = self._warehouse_repo.find_by_id(warehouse_id)
        if not warehouse:
            return None

        for key, value in kwargs.items():
            if value is not None and hasattr(warehouse, key):
                setattr(warehouse, key, value)

        warehouse.updated_at = datetime.utcnow()
        return self._warehouse_repo.save(warehouse)

    def deactivate_warehouse(self, warehouse_id: str) -> bool:
        warehouse = self._warehouse_repo.find_by_id(warehouse_id)
        if not warehouse:
            return False

        # Check if warehouse has stock
        items = self._stock_repo.find_by_warehouse(warehouse_id)
        items_with_stock = [i for i in items if i.quantity > 0]
        if items_with_stock:
            raise ValueError("Cannot deactivate warehouse with existing stock")

        warehouse.is_active = False
        warehouse.updated_at = datetime.utcnow()
        self._warehouse_repo.save(warehouse)
        return True

    def activate_warehouse(self, warehouse_id: str) -> bool:
        warehouse = self._warehouse_repo.find_by_id(warehouse_id)
        if not warehouse:
            return False
        warehouse.is_active = True
        warehouse.updated_at = datetime.utcnow()
        self._warehouse_repo.save(warehouse)
        return True

    def get_warehouse_utilization(self, warehouse_id: str) -> dict:
        warehouse = self._warehouse_repo.find_by_id(warehouse_id)
        if not warehouse:
            raise ValueError(f"Warehouse '{warehouse_id}' not found")

        items = self._stock_repo.find_by_warehouse(warehouse_id)
        total_stock = sum(item.quantity for item in items)
        utilization = (total_stock / warehouse.capacity * 100) if warehouse.capacity > 0 else 0

        return {
            "warehouse_id": warehouse_id,
            "warehouse_name": warehouse.name,
            "capacity": warehouse.capacity,
            "total_stock": total_stock,
            "item_count": len(items),
            "utilization_percent": round(utilization, 2),
        }

    def delete_warehouse(self, warehouse_id: str) -> bool:
        items = self._stock_repo.find_by_warehouse(warehouse_id)
        if items:
            raise ValueError("Cannot delete warehouse with inventory items")
        return self._warehouse_repo.delete(warehouse_id)

