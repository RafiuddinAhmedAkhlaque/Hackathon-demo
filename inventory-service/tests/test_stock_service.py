"""Tests for StockService."""
import pytest


class TestAddInventoryItem:
    def test_add_item_success(self, stock_service, sample_warehouse):
        item = stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=100)
        assert item.product_id == "prod-1"
        assert item.sku == "SKU-001"
        assert item.quantity == 100

    def test_add_item_invalid_warehouse(self, stock_service):
        with pytest.raises(ValueError, match="not found"):
            stock_service.add_inventory_item("prod-1", "SKU-001", "bad-wh")

    def test_add_duplicate_sku_in_warehouse(self, stock_service, sample_warehouse):
        stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id)
        with pytest.raises(ValueError, match="already exists"):
            stock_service.add_inventory_item("prod-2", "SKU-001", sample_warehouse.id)

    def test_add_item_negative_quantity(self, stock_service, sample_warehouse):
        with pytest.raises(ValueError, match="negative"):
            stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=-5)


class TestReceiveStock:
    def test_receive_stock(self, stock_service, sample_warehouse):
        item = stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=10)
        updated = stock_service.receive_stock(item.id, 50)
        assert updated.quantity == 60

    def test_receive_zero_quantity(self, stock_service, sample_warehouse):
        item = stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id)
        with pytest.raises(ValueError, match="positive"):
            stock_service.receive_stock(item.id, 0)

    def test_receive_exceeds_max(self, stock_service, sample_warehouse):
        item = stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=990)
        with pytest.raises(ValueError, match="max quantity"):
            stock_service.receive_stock(item.id, 50)


class TestShipStock:
    def test_ship_stock(self, stock_service, sample_warehouse):
        item = stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=100)
        updated = stock_service.ship_stock(item.id, 30)
        assert updated.quantity == 70

    def test_ship_insufficient_stock(self, stock_service, sample_warehouse):
        item = stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=10)
        with pytest.raises(ValueError, match="Insufficient"):
            stock_service.ship_stock(item.id, 20)

    def test_ship_respects_reservations(self, stock_service, sample_warehouse):
        item = stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=20)
        stock_service.reserve_stock(item.id, 15)
        with pytest.raises(ValueError, match="Insufficient"):
            stock_service.ship_stock(item.id, 10)


class TestReserveStock:
    def test_reserve_stock(self, stock_service, sample_warehouse):
        item = stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=100)
        updated = stock_service.reserve_stock(item.id, 30)
        assert updated.reserved_quantity == 30
        assert updated.available_quantity == 70

    def test_reserve_exceeds_available(self, stock_service, sample_warehouse):
        item = stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=10)
        with pytest.raises(ValueError, match="Insufficient"):
            stock_service.reserve_stock(item.id, 20)

    def test_release_reservation(self, stock_service, sample_warehouse):
        item = stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=100)
        stock_service.reserve_stock(item.id, 30)
        updated = stock_service.release_reservation(item.id, 20)
        assert updated.reserved_quantity == 10
        assert updated.available_quantity == 90


class TestStockQueries:
    def test_get_total_available(self, stock_service, sample_warehouse, warehouse_repo):
        from models.warehouse import Warehouse
        wh2 = Warehouse(name="West WH", code="WH-WEST-01", address="456 St", city="LA", state="CA")
        warehouse_repo.save(wh2)

        stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=50)
        stock_service.add_inventory_item("prod-1", "SKU-001W", wh2.id, quantity=30)
        total = stock_service.get_total_available("prod-1")
        assert total == 80

    def test_get_low_stock_items(self, stock_service, sample_warehouse):
        stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=5, reorder_point=10)
        stock_service.add_inventory_item("prod-2", "SKU-002", sample_warehouse.id, quantity=100, reorder_point=10)
        low = stock_service.get_low_stock_items()
        assert len(low) == 1
        assert low[0].sku == "SKU-001"

    def test_get_movements(self, stock_service, sample_warehouse):
        item = stock_service.add_inventory_item("prod-1", "SKU-001", sample_warehouse.id, quantity=10)
        stock_service.receive_stock(item.id, 50)
        stock_service.ship_stock(item.id, 20)
        movements = stock_service.get_movements(item.id)
        assert len(movements) == 2

