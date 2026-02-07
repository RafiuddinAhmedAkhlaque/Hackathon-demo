"""Tests for analytics utility functions."""
import pytest
from analytics_app.utils.aggregators import (
    group_by, sum_by, average_by, median_by, count_by, growth_rate, percentile,
)
from analytics_app.utils.date_utils import get_date_range, format_duration, generate_date_series
from datetime import datetime, timedelta


class TestGroupBy:
    def test_group_by_key(self):
        items = [
            {"category": "A", "value": 10},
            {"category": "B", "value": 20},
            {"category": "A", "value": 30},
        ]
        groups = group_by(items, "category")
        assert len(groups["A"]) == 2
        assert len(groups["B"]) == 1


class TestSumBy:
    def test_simple_sum(self):
        items = [{"amount": 10}, {"amount": 20}, {"amount": 30}]
        assert sum_by(items, "amount") == 60

    def test_grouped_sum(self):
        items = [
            {"cat": "A", "amount": 10},
            {"cat": "A", "amount": 20},
            {"cat": "B", "amount": 30},
        ]
        result = sum_by(items, "amount", "cat")
        assert result["A"] == 30
        assert result["B"] == 30


class TestAverageBy:
    def test_average(self):
        items = [{"value": 10}, {"value": 20}, {"value": 30}]
        assert average_by(items, "value") == 20.0

    def test_empty_list(self):
        assert average_by([], "value") == 0.0


class TestMedianBy:
    def test_median_odd(self):
        items = [{"v": 10}, {"v": 20}, {"v": 30}]
        assert median_by(items, "v") == 20.0

    def test_median_even(self):
        items = [{"v": 10}, {"v": 20}, {"v": 30}, {"v": 40}]
        assert median_by(items, "v") == 25.0


class TestCountBy:
    def test_count(self):
        items = [{"type": "A"}, {"type": "B"}, {"type": "A"}, {"type": "A"}]
        result = count_by(items, "type")
        assert result["A"] == 3
        assert result["B"] == 1


class TestGrowthRate:
    def test_positive_growth(self):
        assert growth_rate(150, 100) == 50.0

    def test_negative_growth(self):
        assert growth_rate(80, 100) == -20.0

    def test_zero_previous(self):
        assert growth_rate(100, 0) == 100.0

    def test_both_zero(self):
        assert growth_rate(0, 0) == 0.0


class TestDateUtils:
    def test_get_date_range_today(self):
        start, end = get_date_range("today")
        assert start.hour == 0
        assert start.minute == 0

    def test_get_date_range_invalid(self):
        with pytest.raises(ValueError, match="Invalid period"):
            get_date_range("invalid")

    def test_generate_date_series(self):
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 5)
        dates = generate_date_series(start, end, "day")
        assert len(dates) == 5


class TestFormatDuration:
    def test_seconds(self):
        assert format_duration(45) == "45s"

    def test_minutes(self):
        assert format_duration(150) == "2.5m"

    def test_hours(self):
        assert format_duration(7200) == "2.0h"

    def test_days(self):
        assert format_duration(172800) == "2.0d"

