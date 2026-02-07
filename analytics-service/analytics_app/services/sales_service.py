"""Sales analytics service."""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import uuid


@dataclass
class SaleRecord:
    order_id: str
    product_id: str
    product_name: str
    category_id: str
    quantity: int
    unit_price: float
    total_amount: float
    customer_id: str
    sale_date: datetime
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


class SalesService:
    def __init__(self):
        self._records: List[SaleRecord] = []

    def record_sale(self, order_id: str, product_id: str, product_name: str,
                    category_id: str, quantity: int, unit_price: float,
                    customer_id: str, sale_date: datetime = None) -> SaleRecord:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if unit_price < 0:
            raise ValueError("Unit price cannot be negative")

        record = SaleRecord(
            order_id=order_id,
            product_id=product_id,
            product_name=product_name,
            category_id=category_id,
            quantity=quantity,
            unit_price=unit_price,
            total_amount=round(quantity * unit_price, 2),
            customer_id=customer_id,
            sale_date=sale_date or datetime.utcnow(),
        )
        self._records.append(record)
        return record

    def get_total_sales(self, start_date: datetime = None, end_date: datetime = None) -> float:
        records = self._filter_by_date(start_date, end_date)
        return round(sum(r.total_amount for r in records), 2)

    def get_sales_count(self, start_date: datetime = None, end_date: datetime = None) -> int:
        records = self._filter_by_date(start_date, end_date)
        return len(records)

    def get_average_order_value(self, start_date: datetime = None, end_date: datetime = None) -> float:
        records = self._filter_by_date(start_date, end_date)
        if not records:
            return 0.0

        order_totals: Dict[str, float] = {}
        for r in records:
            order_totals[r.order_id] = order_totals.get(r.order_id, 0) + r.total_amount

        total = sum(order_totals.values())
        return round(total / len(order_totals), 2)

    def get_top_products(self, limit: int = 10, start_date: datetime = None,
                         end_date: datetime = None) -> List[Dict]:
        records = self._filter_by_date(start_date, end_date)
        product_sales: Dict[str, Dict] = {}

        for r in records:
            if r.product_id not in product_sales:
                product_sales[r.product_id] = {
                    "product_id": r.product_id,
                    "product_name": r.product_name,
                    "total_quantity": 0,
                    "total_revenue": 0.0,
                }
            product_sales[r.product_id]["total_quantity"] += r.quantity
            product_sales[r.product_id]["total_revenue"] += r.total_amount

        sorted_products = sorted(
            product_sales.values(),
            key=lambda x: x["total_revenue"],
            reverse=True,
        )
        return sorted_products[:limit]

    def get_sales_by_category(self, start_date: datetime = None,
                              end_date: datetime = None) -> Dict[str, float]:
        records = self._filter_by_date(start_date, end_date)
        category_totals: Dict[str, float] = {}

        for r in records:
            category_totals[r.category_id] = category_totals.get(r.category_id, 0) + r.total_amount

        return {k: round(v, 2) for k, v in category_totals.items()}

    def get_daily_sales(self, days: int = 30) -> List[Dict]:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        records = self._filter_by_date(start_date, end_date)

        daily: Dict[str, float] = {}
        for r in records:
            day_key = r.sale_date.strftime("%Y-%m-%d")
            daily[day_key] = daily.get(day_key, 0) + r.total_amount

        return [{"date": k, "total": round(v, 2)} for k, v in sorted(daily.items())]

    def get_customer_sales(self, customer_id: str) -> Dict:
        records = [r for r in self._records if r.customer_id == customer_id]
        if not records:
            return {"customer_id": customer_id, "total_orders": 0, "total_spent": 0.0}

        order_ids = set(r.order_id for r in records)
        total_spent = sum(r.total_amount for r in records)

        return {
            "customer_id": customer_id,
            "total_orders": len(order_ids),
            "total_spent": round(total_spent, 2),
            "total_items": sum(r.quantity for r in records),
            "average_order_value": round(total_spent / len(order_ids), 2),
        }

    def _filter_by_date(self, start_date: datetime = None,
                        end_date: datetime = None) -> List[SaleRecord]:
        records = self._records
        if start_date:
            records = [r for r in records if r.sale_date >= start_date]
        if end_date:
            records = [r for r in records if r.sale_date <= end_date]
        return records

