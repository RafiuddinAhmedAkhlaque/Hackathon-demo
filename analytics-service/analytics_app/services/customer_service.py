"""Customer analytics service."""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import uuid


@dataclass
class CustomerEvent:
    customer_id: str
    event_type: str  # "purchase", "visit", "signup", "review", "support_ticket"
    metadata: Dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


class CustomerAnalyticsService:
    def __init__(self):
        self._events: List[CustomerEvent] = []

    def track_event(self, customer_id: str, event_type: str,
                    metadata: Dict = None, timestamp: datetime = None) -> CustomerEvent:
        if not customer_id:
            raise ValueError("Customer ID is required")
        if not event_type:
            raise ValueError("Event type is required")

        valid_types = ["purchase", "visit", "signup", "review", "support_ticket", "cart_abandon"]
        if event_type not in valid_types:
            raise ValueError(f"Invalid event type: {event_type}. Must be one of: {valid_types}")

        event = CustomerEvent(
            customer_id=customer_id,
            event_type=event_type,
            metadata=metadata or {},
            timestamp=timestamp or datetime.utcnow(),
        )
        self._events.append(event)
        return event

    def get_customer_profile(self, customer_id: str) -> Dict:
        events = [e for e in self._events if e.customer_id == customer_id]
        if not events:
            return {"customer_id": customer_id, "event_count": 0}

        purchases = [e for e in events if e.event_type == "purchase"]
        total_spent = sum(e.metadata.get("amount", 0) for e in purchases)

        return {
            "customer_id": customer_id,
            "event_count": len(events),
            "purchase_count": len(purchases),
            "total_spent": round(total_spent, 2),
            "first_seen": min(e.timestamp for e in events).isoformat(),
            "last_seen": max(e.timestamp for e in events).isoformat(),
            "event_types": list(set(e.event_type for e in events)),
        }

    def get_customer_segments(self) -> Dict[str, List[str]]:
        """Segment customers based on behavior."""
        customer_data: Dict[str, Dict] = {}

        for event in self._events:
            if event.customer_id not in customer_data:
                customer_data[event.customer_id] = {"purchases": 0, "total_spent": 0.0, "visits": 0}

            if event.event_type == "purchase":
                customer_data[event.customer_id]["purchases"] += 1
                customer_data[event.customer_id]["total_spent"] += event.metadata.get("amount", 0)
            elif event.event_type == "visit":
                customer_data[event.customer_id]["visits"] += 1

        segments = {"vip": [], "regular": [], "occasional": [], "inactive": []}

        for cid, data in customer_data.items():
            if data["total_spent"] > 1000 or data["purchases"] > 10:
                segments["vip"].append(cid)
            elif data["purchases"] > 3:
                segments["regular"].append(cid)
            elif data["purchases"] > 0:
                segments["occasional"].append(cid)
            else:
                segments["inactive"].append(cid)

        return segments

    def get_retention_rate(self, period_days: int = 30) -> float:
        """Calculate customer retention rate over a period."""
        now = datetime.utcnow()
        period_start = now - timedelta(days=period_days)
        previous_start = period_start - timedelta(days=period_days)

        previous_customers = set(
            e.customer_id for e in self._events
            if previous_start <= e.timestamp < period_start
        )

        if not previous_customers:
            return 0.0

        returning = set(
            e.customer_id for e in self._events
            if period_start <= e.timestamp <= now
        ) & previous_customers

        return round((len(returning) / len(previous_customers)) * 100, 2)

    def get_conversion_rate(self) -> float:
        """Calculate visit to purchase conversion rate."""
        visitors = set(e.customer_id for e in self._events if e.event_type == "visit")
        buyers = set(e.customer_id for e in self._events if e.event_type == "purchase")

        if not visitors:
            return 0.0

        converted = visitors & buyers
        return round((len(converted) / len(visitors)) * 100, 2)

    def get_top_customers(self, limit: int = 10) -> List[Dict]:
        customer_totals: Dict[str, float] = {}
        for e in self._events:
            if e.event_type == "purchase":
                customer_totals[e.customer_id] = (
                    customer_totals.get(e.customer_id, 0) + e.metadata.get("amount", 0)
                )

        sorted_customers = sorted(customer_totals.items(), key=lambda x: x[1], reverse=True)
        return [
            {"customer_id": cid, "total_spent": round(total, 2)}
            for cid, total in sorted_customers[:limit]
        ]

    def get_event_count_by_type(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for e in self._events:
            counts[e.event_type] = counts.get(e.event_type, 0) + 1
        return counts

