"""Tests for WarehouseService."""
import pytest


class TestCreateWarehouse:
    def test_create_success(self, warehouse_service):
        wh = warehouse_service.create_warehouse("East WH", "WH-EAST", "123 St", "Newark", "NJ")
        assert wh.name == "East WH"
        assert wh.code == "WH-EAST"
        assert wh.is_active is True

    def test_create_duplicate_code(self, warehouse_service):
        warehouse_service.create_warehouse("East WH", "WH-EAST", "123 St", "Newark", "NJ")
        with pytest.raises(ValueError, match="already exists"):
            warehouse_service.create_warehouse("West WH", "WH-EAST", "456 St", "LA", "CA")

    def test_create_empty_name(self, warehouse_service):
        with pytest.raises(ValueError, match="name is required"):
            warehouse_service.create_warehouse("", "WH-01", "123 St", "City", "ST")

    def test_create_invalid_capacity(self, warehouse_service):
        with pytest.raises(ValueError, match="positive"):
            warehouse_service.create_warehouse("WH", "WH-01", "123 St", "City", "ST", capacity=0)


class TestWarehouseLifecycle:
    def test_deactivate_empty_warehouse(self, warehouse_service):
        wh = warehouse_service.create_warehouse("WH", "WH-01", "123 St", "City", "ST")
        assert warehouse_service.deactivate_warehouse(wh.id) is True
        updated = warehouse_service.get_warehouse(wh.id)
        assert updated.is_active is False

    def test_deactivate_warehouse_with_stock(self, warehouse_service, stock_service):
        wh = warehouse_service.create_warehouse("WH", "WH-01", "123 St", "City", "ST")
        stock_service.add_inventory_item("prod-1", "SKU-001", wh.id, quantity=50)
        with pytest.raises(ValueError, match="existing stock"):
            warehouse_service.deactivate_warehouse(wh.id)

    def test_activate_warehouse(self, warehouse_service):
        wh = warehouse_service.create_warehouse("WH", "WH-01", "123 St", "City", "ST")
        warehouse_service.deactivate_warehouse(wh.id)
        assert warehouse_service.activate_warehouse(wh.id) is True
        updated = warehouse_service.get_warehouse(wh.id)
        assert updated.is_active is True


class TestWarehouseUtilization:
    def test_utilization_empty(self, warehouse_service):
        wh = warehouse_service.create_warehouse("WH", "WH-01", "123 St", "City", "ST", capacity=1000)
        util = warehouse_service.get_warehouse_utilization(wh.id)
        assert util["utilization_percent"] == 0.0
        assert util["total_stock"] == 0

    def test_utilization_with_stock(self, warehouse_service, stock_service):
        wh = warehouse_service.create_warehouse("WH", "WH-01", "123 St", "City", "ST", capacity=1000)
        stock_service.add_inventory_item("prod-1", "SKU-001", wh.id, quantity=250)
        util = warehouse_service.get_warehouse_utilization(wh.id)
        assert util["utilization_percent"] == 25.0
        assert util["total_stock"] == 250

    def test_utilization_nonexistent(self, warehouse_service):
        with pytest.raises(ValueError, match="not found"):
            warehouse_service.get_warehouse_utilization("bad-id")


class TestWarehouseQueries:
    def test_list_active_only(self, warehouse_service):
        wh1 = warehouse_service.create_warehouse("WH1", "WH-01", "St1", "City", "ST")
        wh2 = warehouse_service.create_warehouse("WH2", "WH-02", "St2", "City", "ST")
        warehouse_service.deactivate_warehouse(wh2.id)
        active = warehouse_service.list_warehouses(active_only=True)
        assert len(active) == 1
        assert active[0].id == wh1.id

    def test_get_by_code(self, warehouse_service):
        warehouse_service.create_warehouse("WH", "WH-EAST-01", "St", "City", "ST")
        found = warehouse_service.get_warehouse_by_code("WH-EAST-01")
        assert found is not None
        assert found.code == "WH-EAST-01"

