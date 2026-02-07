"""Data aggregation utilities for analytics."""
from typing import List, Dict, Any, Callable
from collections import defaultdict
import statistics


def group_by(items: List[Dict], key: str) -> Dict[str, List[Dict]]:
    """Group a list of dicts by a key."""
    groups: Dict[str, List[Dict]] = defaultdict(list)
    for item in items:
        group_key = str(item.get(key, "unknown"))
        groups[group_key].append(item)
    return dict(groups)


def sum_by(items: List[Dict], value_key: str, group_key: str = None) -> Any:
    """Sum values, optionally grouped by a key."""
    if group_key:
        groups = group_by(items, group_key)
        return {k: round(sum(item.get(value_key, 0) for item in v), 2) for k, v in groups.items()}
    return round(sum(item.get(value_key, 0) for item in items), 2)


def average_by(items: List[Dict], value_key: str) -> float:
    """Calculate average of a value across items."""
    values = [item.get(value_key, 0) for item in items]
    if not values:
        return 0.0
    return round(statistics.mean(values), 2)


def median_by(items: List[Dict], value_key: str) -> float:
    """Calculate median of a value across items."""
    values = [item.get(value_key, 0) for item in items]
    if not values:
        return 0.0
    return round(statistics.median(values), 2)


def percentile(items: List[Dict], value_key: str, pct: float) -> float:
    """Calculate a percentile value."""
    values = sorted(item.get(value_key, 0) for item in items)
    if not values:
        return 0.0
    idx = int(len(values) * pct / 100)
    idx = min(idx, len(values) - 1)
    return round(values[idx], 2)


def count_by(items: List[Dict], group_key: str) -> Dict[str, int]:
    """Count items grouped by a key."""
    counts: Dict[str, int] = defaultdict(int)
    for item in items:
        key = str(item.get(group_key, "unknown"))
        counts[key] += 1
    return dict(counts)


def growth_rate(current: float, previous: float) -> float:
    """Calculate growth rate as a percentage."""
    if previous == 0:
        return 0.0 if current == 0 else 100.0
    return round(((current - previous) / previous) * 100, 2)

