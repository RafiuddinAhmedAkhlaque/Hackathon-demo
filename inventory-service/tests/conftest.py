"""Shared test fixtures for inventory-service."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from repositories.stock_repository import StockRepository
from repositories.warehouse_repository import WarehouseRepository
from services.stock_service import StockService
from services.warehouse_service import WarehouseService
from services.alert_service import AlertService
from models.warehouse import Warehouse


@pytest.fixture
def stock_repo():
    return StockRepository()

@pytest.fixture
def warehouse_repo():
    return WarehouseRepository()

@pytest.fixture
def stock_service(stock_repo, warehouse_repo):
    return StockService(stock_repo, warehouse_repo)

@pytest.fixture
def warehouse_service(warehouse_repo, stock_repo):
    return WarehouseService(warehouse_repo, stock_repo)

@pytest.fixture
def alert_service(stock_repo):
    return AlertService(stock_repo)

@pytest.fixture
def sample_warehouse(warehouse_repo):
    wh = Warehouse(name="East Warehouse", code="WH-EAST-01",
                   address="123 Industrial Pkwy", city="Newark", state="NJ")
    return warehouse_repo.save(wh)

