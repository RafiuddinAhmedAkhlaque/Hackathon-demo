"""In-memory stock repository."""
from typing import Dict, List, Optional
from models.inventory_item import InventoryItem


class StockRepository:
    def __init__(self):
        self._items: Dict[str, InventoryItem] = {}
        self._product_idx: Dict[str, List[str]] = {}
        self._warehouse_idx: Dict[str, List[str]] = {}
        self._sku_warehouse_idx: Dict[str, str] = {}  # "sku:warehouse_id" -> item_id

    def save(self, item: InventoryItem) -> InventoryItem:
        key = f"{item.sku}:{item.warehouse_id}"
        if key in self._sku_warehouse_idx and self._sku_warehouse_idx[key] != item.id:
            raise ValueError(f"Item with SKU '{item.sku}' already exists in warehouse '{item.warehouse_id}'")

        self._items[item.id] = item
        self._sku_warehouse_idx[key] = item.id

        if item.product_id not in self._product_idx:
            self._product_idx[item.product_id] = []
        if item.id not in self._product_idx[item.product_id]:
            self._product_idx[item.product_id].append(item.id)

        if item.warehouse_id not in self._warehouse_idx:
            self._warehouse_idx[item.warehouse_id] = []
        if item.id not in self._warehouse_idx[item.warehouse_id]:
            self._warehouse_idx[item.warehouse_id].append(item.id)

        return item

    def find_by_id(self, item_id: str) -> Optional[InventoryItem]:
        return self._items.get(item_id)

    def find_by_product(self, product_id: str) -> List[InventoryItem]:
        ids = self._product_idx.get(product_id, [])
        return [self._items[i] for i in ids if i in self._items]

    def find_by_warehouse(self, warehouse_id: str) -> List[InventoryItem]:
        ids = self._warehouse_idx.get(warehouse_id, [])
        return [self._items[i] for i in ids if i in self._items]

    def find_by_sku_and_warehouse(self, sku: str, warehouse_id: str) -> Optional[InventoryItem]:
        key = f"{sku}:{warehouse_id}"
        item_id = self._sku_warehouse_idx.get(key)
        if item_id:
            return self._items.get(item_id)
        return None

    def find_low_stock(self) -> List[InventoryItem]:
        return [item for item in self._items.values() if item.is_low_stock]

    def find_out_of_stock(self) -> List[InventoryItem]:
        return [item for item in self._items.values() if item.is_out_of_stock]

    def delete(self, item_id: str) -> bool:
        item = self._items.get(item_id)
        if not item:
            return False
        del self._items[item_id]
        key = f"{item.sku}:{item.warehouse_id}"
        self._sku_warehouse_idx.pop(key, None)
        return True

    def get_all(self) -> List[InventoryItem]:
        return list(self._items.values())

    def get_total_quantity(self, product_id: str) -> int:
        items = self.find_by_product(product_id)
        return sum(item.available_quantity for item in items)

