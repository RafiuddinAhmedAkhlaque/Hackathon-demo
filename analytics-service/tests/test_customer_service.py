"""Tests for CustomerAnalyticsService."""
import pytest
from datetime import datetime, timedelta
from analytics_app.services.customer_service import CustomerAnalyticsService


@pytest.fixture
def customer_service():
    return CustomerAnalyticsService()


class TestTrackEvent:
    def test_track_purchase(self, customer_service):
        event = customer_service.track_event("cust-1", "purchase", {"amount": 50.00})
        assert event.customer_id == "cust-1"
        assert event.event_type == "purchase"

    def test_reject_empty_customer_id(self, customer_service):
        with pytest.raises(ValueError, match="Customer ID"):
            customer_service.track_event("", "purchase")

    def test_reject_invalid_event_type(self, customer_service):
        with pytest.raises(ValueError, match="Invalid event"):
            customer_service.track_event("cust-1", "invalid_type")


class TestCustomerProfile:
    def test_profile_with_events(self, customer_service):
        customer_service.track_event("cust-1", "visit")
        customer_service.track_event("cust-1", "purchase", {"amount": 100.00})
        customer_service.track_event("cust-1", "purchase", {"amount": 50.00})

        profile = customer_service.get_customer_profile("cust-1")
        assert profile["event_count"] == 3
        assert profile["purchase_count"] == 2
        assert profile["total_spent"] == 150.00

    def test_profile_no_events(self, customer_service):
        profile = customer_service.get_customer_profile("nonexistent")
        assert profile["event_count"] == 0


class TestSegmentation:
    def test_vip_segment(self, customer_service):
        for i in range(15):
            customer_service.track_event("vip-user", "purchase", {"amount": 100.00})
        segments = customer_service.get_customer_segments()
        assert "vip-user" in segments["vip"]

    def test_regular_segment(self, customer_service):
        for i in range(5):
            customer_service.track_event("regular-user", "purchase", {"amount": 10.00})
        segments = customer_service.get_customer_segments()
        assert "regular-user" in segments["regular"]

    def test_occasional_segment(self, customer_service):
        customer_service.track_event("occasional-user", "purchase", {"amount": 10.00})
        segments = customer_service.get_customer_segments()
        assert "occasional-user" in segments["occasional"]

    def test_inactive_segment(self, customer_service):
        customer_service.track_event("inactive-user", "visit")
        segments = customer_service.get_customer_segments()
        assert "inactive-user" in segments["inactive"]


class TestConversionRate:
    def test_conversion_rate(self, customer_service):
        customer_service.track_event("cust-1", "visit")
        customer_service.track_event("cust-2", "visit")
        customer_service.track_event("cust-3", "visit")
        customer_service.track_event("cust-1", "purchase", {"amount": 50})
        rate = customer_service.get_conversion_rate()
        assert rate == pytest.approx(33.33, abs=0.01)

    def test_conversion_rate_no_visitors(self, customer_service):
        assert customer_service.get_conversion_rate() == 0.0


class TestTopCustomers:
    def test_top_customers(self, customer_service):
        customer_service.track_event("cust-1", "purchase", {"amount": 500})
        customer_service.track_event("cust-2", "purchase", {"amount": 1000})
        customer_service.track_event("cust-3", "purchase", {"amount": 200})

        top = customer_service.get_top_customers(limit=2)
        assert len(top) == 2
        assert top[0]["customer_id"] == "cust-2"
        assert top[0]["total_spent"] == 1000.00


class TestEventCounts:
    def test_event_count_by_type(self, customer_service):
        customer_service.track_event("c1", "visit")
        customer_service.track_event("c1", "visit")
        customer_service.track_event("c1", "purchase", {"amount": 10})
        counts = customer_service.get_event_count_by_type()
        assert counts["visit"] == 2
        assert counts["purchase"] == 1

