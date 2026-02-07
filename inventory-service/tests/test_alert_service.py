"""Tests for AlertService."""
import pytest
from models.inventory_item import InventoryItem


class TestCheckStockLevels:
    def test_detect_low_stock(self, alert_service, stock_repo, sample_warehouse):
        item = InventoryItem(product_id="p1", sku="SKU-001", warehouse_id=sample_warehouse.id,
                             quantity=5, reorder_point=10)
        stock_repo.save(item)
        alerts = alert_service.check_stock_levels()
        assert len(alerts) == 1
        assert alerts[0].alert_type == "low_stock"

    def test_detect_out_of_stock(self, alert_service, stock_repo, sample_warehouse):
        item = InventoryItem(product_id="p1", sku="SKU-001", warehouse_id=sample_warehouse.id,
                             quantity=0, reorder_point=10)
        stock_repo.save(item)
        alerts = alert_service.check_stock_levels()
        assert len(alerts) == 1
        assert alerts[0].alert_type == "out_of_stock"

    def test_no_alerts_for_healthy_stock(self, alert_service, stock_repo, sample_warehouse):
        item = InventoryItem(product_id="p1", sku="SKU-001", warehouse_id=sample_warehouse.id,
                             quantity=100, reorder_point=10)
        stock_repo.save(item)
        alerts = alert_service.check_stock_levels()
        assert len(alerts) == 0

    def test_detect_overstock(self, alert_service, stock_repo, sample_warehouse):
        item = InventoryItem(product_id="p1", sku="SKU-001", warehouse_id=sample_warehouse.id,
                             quantity=1500, max_quantity=1000, reorder_point=10)
        stock_repo.save(item)
        alerts = alert_service.check_stock_levels()
        assert any(a.alert_type == "overstock" for a in alerts)


class TestAlertManagement:
    def test_acknowledge_alert(self, alert_service, stock_repo, sample_warehouse):
        item = InventoryItem(product_id="p1", sku="SKU-001", warehouse_id=sample_warehouse.id,
                             quantity=3, reorder_point=10)
        stock_repo.save(item)
        alerts = alert_service.check_stock_levels()
        assert alert_service.acknowledge_alert(alerts[0].id) is True
        acknowledged = alert_service.get_alerts(acknowledged=True)
        assert len(acknowledged) == 1

    def test_filter_by_type(self, alert_service, stock_repo, sample_warehouse):
        item1 = InventoryItem(product_id="p1", sku="SKU-001", warehouse_id=sample_warehouse.id,
                              quantity=0, reorder_point=10)
        item2 = InventoryItem(product_id="p2", sku="SKU-002", warehouse_id=sample_warehouse.id,
                              quantity=5, reorder_point=10)
        stock_repo.save(item1)
        stock_repo.save(item2)
        alert_service.check_stock_levels()
        oos_alerts = alert_service.get_alerts(alert_type="out_of_stock")
        assert len(oos_alerts) == 1


class TestReorderSuggestions:
    def test_generates_suggestions(self, alert_service, stock_repo, sample_warehouse):
        item = InventoryItem(product_id="p1", sku="SKU-001", warehouse_id=sample_warehouse.id,
                             quantity=3, reorder_point=10, reorder_quantity=50)
        stock_repo.save(item)
        suggestions = alert_service.get_reorder_suggestions()
        assert len(suggestions) == 1
        assert suggestions[0]["suggested_order_quantity"] == 50

    def test_prioritizes_out_of_stock(self, alert_service, stock_repo, sample_warehouse):
        item1 = InventoryItem(product_id="p1", sku="SKU-001", warehouse_id=sample_warehouse.id,
                              quantity=0, reorder_point=10)
        item2 = InventoryItem(product_id="p2", sku="SKU-002", warehouse_id=sample_warehouse.id,
                              quantity=5, reorder_point=10)
        stock_repo.save(item1)
        stock_repo.save(item2)
        suggestions = alert_service.get_reorder_suggestions()
        assert suggestions[0]["priority"] == "high"
        assert suggestions[1]["priority"] == "medium"

