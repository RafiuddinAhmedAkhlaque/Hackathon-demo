"""Tests for quantity calculator utilities."""
import pytest
from utils.quantity_calculator import (
    calculate_reorder_quantity,
    calculate_days_of_stock,
    calculate_stock_value,
    calculate_turnover_rate,
    calculate_fill_rate,
)
from models.inventory_item import InventoryItem


def make_item(quantity=100, reorder_quantity=50, reorder_point=10):
    return InventoryItem(
        product_id="p1", sku="SKU-001", warehouse_id="wh-1",
        quantity=quantity, reorder_quantity=reorder_quantity,
        reorder_point=reorder_point,
    )


class TestReorderQuantity:
    def test_basic_reorder(self):
        item = make_item(quantity=5)
        qty = calculate_reorder_quantity(item, avg_daily_sales=10, lead_time_days=7)
        assert qty >= item.reorder_quantity

    def test_high_stock_still_returns_minimum(self):
        item = make_item(quantity=500)
        qty = calculate_reorder_quantity(item, avg_daily_sales=5, lead_time_days=7)
        assert qty == item.reorder_quantity


class TestDaysOfStock:
    def test_normal_sales(self):
        item = make_item(quantity=100)
        days = calculate_days_of_stock(item, avg_daily_sales=10)
        assert days == 10.0

    def test_zero_sales(self):
        item = make_item(quantity=100)
        days = calculate_days_of_stock(item, avg_daily_sales=0)
        assert days == float('inf')


class TestStockValue:
    def test_calculate_value(self):
        items = [make_item(quantity=10), make_item(quantity=20)]
        items[0].product_id = "p1"
        items[1].product_id = "p2"
        prices = {"p1": 25.00, "p2": 10.00}
        value = calculate_stock_value(items, prices)
        assert value == 450.00

    def test_missing_price(self):
        items = [make_item(quantity=10)]
        value = calculate_stock_value(items, {})
        assert value == 0.0


class TestTurnoverRate:
    def test_normal_turnover(self):
        rate = calculate_turnover_rate(1000, 200)
        assert rate == 5.0

    def test_zero_inventory(self):
        rate = calculate_turnover_rate(100, 0)
        assert rate == 0.0


class TestFillRate:
    def test_perfect_fill(self):
        rate = calculate_fill_rate(100, 100)
        assert rate == 100.0

    def test_partial_fill(self):
        rate = calculate_fill_rate(80, 100)
        assert rate == 80.0

    def test_no_orders(self):
        rate = calculate_fill_rate(0, 0)
        assert rate == 100.0

