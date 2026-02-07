"""Tests for SalesService."""
import pytest
from datetime import datetime, timedelta
from analytics_app.services.sales_service import SalesService


@pytest.fixture
def sales_service():
    return SalesService()


@pytest.fixture
def service_with_data(sales_service):
    now = datetime.utcnow()
    sales_service.record_sale("ord-1", "prod-1", "Widget A", "cat-1", 2, 25.00, "cust-1", now)
    sales_service.record_sale("ord-1", "prod-2", "Widget B", "cat-1", 1, 50.00, "cust-1", now)
    sales_service.record_sale("ord-2", "prod-1", "Widget A", "cat-1", 3, 25.00, "cust-2", now)
    sales_service.record_sale("ord-3", "prod-3", "Gadget C", "cat-2", 1, 100.00, "cust-3", now - timedelta(days=5))
    return sales_service


class TestRecordSale:
    def test_record_sale_success(self, sales_service):
        record = sales_service.record_sale("ord-1", "prod-1", "Widget", "cat-1", 2, 10.00, "cust-1")
        assert record.total_amount == 20.00
        assert record.quantity == 2

    def test_reject_negative_quantity(self, sales_service):
        with pytest.raises(ValueError, match="positive"):
            sales_service.record_sale("ord-1", "prod-1", "Widget", "cat-1", -1, 10.00, "cust-1")

    def test_reject_negative_price(self, sales_service):
        with pytest.raises(ValueError, match="negative"):
            sales_service.record_sale("ord-1", "prod-1", "Widget", "cat-1", 1, -10.00, "cust-1")


class TestSalesQueries:
    def test_total_sales(self, service_with_data):
        total = service_with_data.get_total_sales()
        assert total == 275.00  # 50 + 50 + 75 + 100

    def test_sales_count(self, service_with_data):
        count = service_with_data.get_sales_count()
        assert count == 4

    def test_average_order_value(self, service_with_data):
        aov = service_with_data.get_average_order_value()
        # 3 orders: ord-1=$100, ord-2=$75, ord-3=$100 => avg=$91.67
        assert aov == pytest.approx(91.67, abs=0.01)


class TestTopProducts:
    def test_top_products(self, service_with_data):
        top = service_with_data.get_top_products(limit=2)
        assert len(top) == 2
        # Widget A has most revenue: 2*25 + 3*25 = 125
        assert top[0]["product_name"] == "Widget A"
        assert top[0]["total_revenue"] == 125.00

    def test_top_products_with_limit(self, service_with_data):
        top = service_with_data.get_top_products(limit=1)
        assert len(top) == 1


class TestSalesByCategory:
    def test_category_breakdown(self, service_with_data):
        by_cat = service_with_data.get_sales_by_category()
        assert "cat-1" in by_cat
        assert "cat-2" in by_cat
        assert by_cat["cat-1"] == 175.00  # 50 + 50 + 75
        assert by_cat["cat-2"] == 100.00


class TestCustomerSales:
    def test_customer_profile(self, service_with_data):
        profile = service_with_data.get_customer_sales("cust-1")
        assert profile["total_orders"] == 1
        assert profile["total_spent"] == 100.00

    def test_nonexistent_customer(self, service_with_data):
        profile = service_with_data.get_customer_sales("nonexistent")
        assert profile["total_orders"] == 0
        assert profile["total_spent"] == 0.0

