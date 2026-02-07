"""Tests for RevenueService."""
import pytest
from datetime import datetime
from analytics_app.services.revenue_service import RevenueService


@pytest.fixture
def revenue_service():
    return RevenueService()


@pytest.fixture
def service_with_data(revenue_service):
    now = datetime.utcnow()
    revenue_service.add_revenue("orders", 5000.00, date=now)
    revenue_service.add_revenue("orders", 3000.00, date=now)
    revenue_service.add_revenue("subscriptions", 1500.00, date=now)
    revenue_service.add_expense("shipping", 500.00, date=now)
    revenue_service.add_expense("refunds", 300.00, date=now)
    revenue_service.add_expense("operations", 1000.00, date=now)
    return revenue_service


class TestAddRevenue:
    def test_add_revenue(self, revenue_service):
        entry = revenue_service.add_revenue("orders", 1000.00)
        assert entry.source == "orders"
        assert entry.amount == 1000.00

    def test_reject_negative_amount(self, revenue_service):
        with pytest.raises(ValueError, match="negative"):
            revenue_service.add_revenue("orders", -100.00)

    def test_reject_empty_source(self, revenue_service):
        with pytest.raises(ValueError, match="source"):
            revenue_service.add_revenue("", 100.00)


class TestAddExpense:
    def test_add_expense(self, revenue_service):
        entry = revenue_service.add_expense("shipping", 200.00)
        assert entry.category == "shipping"
        assert entry.amount == 200.00

    def test_reject_negative_expense(self, revenue_service):
        with pytest.raises(ValueError, match="negative"):
            revenue_service.add_expense("shipping", -50.00)


class TestRevenueTotals:
    def test_total_revenue(self, service_with_data):
        total = service_with_data.get_total_revenue()
        assert total == 9500.00

    def test_total_expenses(self, service_with_data):
        total = service_with_data.get_total_expenses()
        assert total == 1800.00

    def test_net_revenue(self, service_with_data):
        net = service_with_data.get_net_revenue()
        assert net == 7700.00

    def test_profit_margin(self, service_with_data):
        margin = service_with_data.get_profit_margin()
        expected = round((7700.00 / 9500.00) * 100, 2)
        assert margin == expected


class TestRevenueBreakdown:
    def test_by_source(self, service_with_data):
        by_source = service_with_data.get_revenue_by_source()
        assert by_source["orders"] == 8000.00
        assert by_source["subscriptions"] == 1500.00

    def test_expenses_by_category(self, service_with_data):
        by_cat = service_with_data.get_expenses_by_category()
        assert by_cat["shipping"] == 500.00
        assert by_cat["refunds"] == 300.00
        assert by_cat["operations"] == 1000.00


class TestZeroRevenue:
    def test_profit_margin_zero_revenue(self, revenue_service):
        margin = revenue_service.get_profit_margin()
        assert margin == 0.0

    def test_net_revenue_zero(self, revenue_service):
        net = revenue_service.get_net_revenue()
        assert net == 0.0

