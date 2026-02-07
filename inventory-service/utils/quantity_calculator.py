"""Utility for calculating reorder quantities and stock metrics."""
from typing import List
from models.inventory_item import InventoryItem


def calculate_reorder_quantity(item: InventoryItem, avg_daily_sales: float = 5.0,
                                lead_time_days: int = 7) -> int:
    """Calculate optimal reorder quantity using Economic Order Quantity simplified model."""
    safety_stock = int(avg_daily_sales * lead_time_days * 0.5)
    demand_during_lead = int(avg_daily_sales * lead_time_days)
    reorder_qty = demand_during_lead + safety_stock - item.available_quantity

    return max(reorder_qty, item.reorder_quantity)


def calculate_days_of_stock(item: InventoryItem, avg_daily_sales: float = 5.0) -> float:
    """Estimate how many days the current stock will last."""
    if avg_daily_sales <= 0:
        return float('inf')
    return round(item.available_quantity / avg_daily_sales, 1)


def calculate_stock_value(items: List[InventoryItem], unit_prices: dict) -> float:
    """Calculate total stock value across items."""
    total = 0.0
    for item in items:
        price = unit_prices.get(item.product_id, 0.0)
        total += item.quantity * price
    return round(total, 2)


def calculate_turnover_rate(total_sold: int, average_inventory: float) -> float:
    """Calculate inventory turnover rate."""
    if average_inventory <= 0:
        return 0.0
    return round(total_sold / average_inventory, 2)


def calculate_fill_rate(fulfilled_orders: int, total_orders: int) -> float:
    """Calculate order fill rate as a percentage."""
    if total_orders <= 0:
        return 100.0
    return round((fulfilled_orders / total_orders) * 100, 2)

