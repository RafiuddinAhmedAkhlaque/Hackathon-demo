"""Alert service - monitors stock levels and generates alerts."""
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, field
import uuid

from models.inventory_item import InventoryItem
from repositories.stock_repository import StockRepository


@dataclass
class StockAlert:
    item_id: str
    product_id: str
    sku: str
    warehouse_id: str
    alert_type: str  # "low_stock", "out_of_stock", "overstock"
    current_quantity: int
    threshold: int
    message: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    acknowledged: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "item_id": self.item_id,
            "product_id": self.product_id,
            "sku": self.sku,
            "warehouse_id": self.warehouse_id,
            "alert_type": self.alert_type,
            "current_quantity": self.current_quantity,
            "threshold": self.threshold,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
            "acknowledged": self.acknowledged,
        }


class AlertService:
    def __init__(self, stock_repo: StockRepository):
        self._stock_repo = stock_repo
        self._alerts: Dict[str, StockAlert] = {}

    def check_stock_levels(self) -> List[StockAlert]:
        """Scan all inventory and generate alerts for low/out of stock items."""
        new_alerts = []

        all_items = self._stock_repo.get_all()
        for item in all_items:
            if item.is_out_of_stock:
                alert = self._create_alert(
                    item,
                    "out_of_stock",
                    f"CRITICAL: {item.sku} is out of stock in warehouse {item.warehouse_id}",
                )
                new_alerts.append(alert)
            elif item.is_low_stock:
                alert = self._create_alert(
                    item,
                    "low_stock",
                    f"WARNING: {item.sku} is low on stock ({item.available_quantity} remaining) "
                    f"in warehouse {item.warehouse_id}. Reorder point: {item.reorder_point}",
                )
                new_alerts.append(alert)

            if item.quantity > item.max_quantity:
                alert = self._create_alert(
                    item,
                    "overstock",
                    f"INFO: {item.sku} exceeds max quantity ({item.quantity}/{item.max_quantity}) "
                    f"in warehouse {item.warehouse_id}",
                )
                new_alerts.append(alert)

        return new_alerts

    def get_alerts(self, alert_type: str = None, acknowledged: bool = None) -> List[StockAlert]:
        alerts = list(self._alerts.values())
        if alert_type:
            alerts = [a for a in alerts if a.alert_type == alert_type]
        if acknowledged is not None:
            alerts = [a for a in alerts if a.acknowledged == acknowledged]
        return alerts

    def acknowledge_alert(self, alert_id: str) -> bool:
        alert = self._alerts.get(alert_id)
        if not alert:
            return False
        alert.acknowledged = True
        return True

    def get_reorder_suggestions(self) -> List[dict]:
        """Generate reorder suggestions for low stock items."""
        suggestions = []
        low_stock = self._stock_repo.find_low_stock()

        for item in low_stock:
            suggestions.append({
                "item_id": item.id,
                "product_id": item.product_id,
                "sku": item.sku,
                "warehouse_id": item.warehouse_id,
                "current_quantity": item.available_quantity,
                "reorder_point": item.reorder_point,
                "suggested_order_quantity": item.reorder_quantity,
                "priority": "high" if item.is_out_of_stock else "medium",
            })

        # Sort by priority
        suggestions.sort(key=lambda s: 0 if s["priority"] == "high" else 1)
        return suggestions

    def _create_alert(self, item: InventoryItem, alert_type: str, message: str) -> StockAlert:
        alert = StockAlert(
            item_id=item.id,
            product_id=item.product_id,
            sku=item.sku,
            warehouse_id=item.warehouse_id,
            alert_type=alert_type,
            current_quantity=item.available_quantity,
            threshold=item.reorder_point,
            message=message,
        )
        self._alerts[alert.id] = alert
        return alert

