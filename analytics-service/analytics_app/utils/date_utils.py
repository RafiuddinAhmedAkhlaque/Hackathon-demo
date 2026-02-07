"""Date utility functions for analytics."""
from datetime import datetime, timedelta
from typing import List, Tuple


def get_date_range(period: str) -> Tuple[datetime, datetime]:
    """Get start and end dates for common periods."""
    now = datetime.utcnow()
    periods = {
        "today": (now.replace(hour=0, minute=0, second=0, microsecond=0), now),
        "yesterday": (
            (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0),
            now.replace(hour=0, minute=0, second=0, microsecond=0),
        ),
        "last_7_days": (now - timedelta(days=7), now),
        "last_30_days": (now - timedelta(days=30), now),
        "last_90_days": (now - timedelta(days=90), now),
        "this_month": (now.replace(day=1, hour=0, minute=0, second=0, microsecond=0), now),
        "this_year": (now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0), now),
    }

    if period not in periods:
        raise ValueError(f"Invalid period: {period}. Valid: {list(periods.keys())}")

    return periods[period]


def generate_date_series(start_date: datetime, end_date: datetime, interval: str = "day") -> List[datetime]:
    """Generate a series of dates between start and end."""
    dates = []
    current = start_date

    if interval == "day":
        delta = timedelta(days=1)
    elif interval == "week":
        delta = timedelta(weeks=1)
    elif interval == "hour":
        delta = timedelta(hours=1)
    else:
        raise ValueError(f"Invalid interval: {interval}")

    while current <= end_date:
        dates.append(current)
        current += delta

    return dates


def format_duration(seconds: float) -> str:
    """Format a duration in seconds to a human-readable string."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f}h"
    else:
        days = seconds / 86400
        return f"{days:.1f}d"

