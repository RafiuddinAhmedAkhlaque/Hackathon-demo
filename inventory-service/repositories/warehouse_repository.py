"""In-memory warehouse repository."""
from typing import Dict, List, Optional
from models.warehouse import Warehouse


class WarehouseRepository:
    def __init__(self):
        self._warehouses: Dict[str, Warehouse] = {}
        self._code_idx: Dict[str, str] = {}

    def save(self, warehouse: Warehouse) -> Warehouse:
        if warehouse.code in self._code_idx and self._code_idx[warehouse.code] != warehouse.id:
            raise ValueError(f"Warehouse with code '{warehouse.code}' already exists")
        self._warehouses[warehouse.id] = warehouse
        self._code_idx[warehouse.code] = warehouse.id
        return warehouse

    def find_by_id(self, warehouse_id: str) -> Optional[Warehouse]:
        return self._warehouses.get(warehouse_id)

    def find_by_code(self, code: str) -> Optional[Warehouse]:
        wid = self._code_idx.get(code)
        if wid:
            return self._warehouses.get(wid)
        return None

    def find_active(self) -> List[Warehouse]:
        return [w for w in self._warehouses.values() if w.is_active]

    def get_all(self) -> List[Warehouse]:
        return list(self._warehouses.values())

    def delete(self, warehouse_id: str) -> bool:
        wh = self._warehouses.get(warehouse_id)
        if not wh:
            return False
        del self._warehouses[warehouse_id]
        self._code_idx.pop(wh.code, None)
        return True

    def count(self) -> int:
        return len(self._warehouses)

