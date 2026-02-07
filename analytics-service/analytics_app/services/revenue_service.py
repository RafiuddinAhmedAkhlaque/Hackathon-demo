"""Revenue analytics service."""
from datetime import datetime, timedelta
from typing import List, Dict
from dataclasses import dataclass, field
import uuid


@dataclass
class RevenueEntry:
    source: str  # "orders", "subscriptions", "fees"
    amount: float
    currency: str = "USD"
    date: datetime = field(default_factory=datetime.utcnow)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class ExpenseEntry:
    category: str  # "shipping", "refunds", "operations", "marketing"
    amount: float
    description: str = ""
    date: datetime = field(default_factory=datetime.utcnow)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


class RevenueService:
    def __init__(self):
        self._revenues: List[RevenueEntry] = []
        self._expenses: List[ExpenseEntry] = []

    def add_revenue(self, source: str, amount: float, currency: str = "USD",
                    date: datetime = None) -> RevenueEntry:
        if amount < 0:
            raise ValueError("Revenue amount cannot be negative")
        if not source:
            raise ValueError("Revenue source is required")

        entry = RevenueEntry(source=source, amount=amount, currency=currency,
                             date=date or datetime.utcnow())
        self._revenues.append(entry)
        return entry

    def add_expense(self, category: str, amount: float, description: str = "",
                    date: datetime = None) -> ExpenseEntry:
        if amount < 0:
            raise ValueError("Expense amount cannot be negative")
        if not category:
            raise ValueError("Expense category is required")

        entry = ExpenseEntry(category=category, amount=amount, description=description,
                             date=date or datetime.utcnow())
        self._expenses.append(entry)
        return entry

    def get_total_revenue(self, start_date: datetime = None, end_date: datetime = None) -> float:
        revenues = self._filter_revenues(start_date, end_date)
        return round(sum(r.amount for r in revenues), 2)

    def get_total_expenses(self, start_date: datetime = None, end_date: datetime = None) -> float:
        expenses = self._filter_expenses(start_date, end_date)
        return round(sum(e.amount for e in expenses), 2)

    def get_net_revenue(self, start_date: datetime = None, end_date: datetime = None) -> float:
        total_rev = self.get_total_revenue(start_date, end_date)
        total_exp = self.get_total_expenses(start_date, end_date)
        return round(total_rev - total_exp, 2)

    def get_profit_margin(self, start_date: datetime = None, end_date: datetime = None) -> float:
        total_rev = self.get_total_revenue(start_date, end_date)
        if total_rev == 0:
            return 0.0
        net = self.get_net_revenue(start_date, end_date)
        return round((net / total_rev) * 100, 2)

    def get_revenue_by_source(self, start_date: datetime = None,
                              end_date: datetime = None) -> Dict[str, float]:
        revenues = self._filter_revenues(start_date, end_date)
        by_source: Dict[str, float] = {}
        for r in revenues:
            by_source[r.source] = by_source.get(r.source, 0) + r.amount
        return {k: round(v, 2) for k, v in by_source.items()}

    def get_expenses_by_category(self, start_date: datetime = None,
                                 end_date: datetime = None) -> Dict[str, float]:
        expenses = self._filter_expenses(start_date, end_date)
        by_cat: Dict[str, float] = {}
        for e in expenses:
            by_cat[e.category] = by_cat.get(e.category, 0) + e.amount
        return {k: round(v, 2) for k, v in by_cat.items()}

    def get_monthly_summary(self, year: int, month: int) -> Dict:
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1)
        else:
            end = datetime(year, month + 1, 1)

        return {
            "year": year,
            "month": month,
            "total_revenue": self.get_total_revenue(start, end),
            "total_expenses": self.get_total_expenses(start, end),
            "net_revenue": self.get_net_revenue(start, end),
            "profit_margin": self.get_profit_margin(start, end),
            "revenue_by_source": self.get_revenue_by_source(start, end),
            "expenses_by_category": self.get_expenses_by_category(start, end),
        }

    def _filter_revenues(self, start_date=None, end_date=None) -> List[RevenueEntry]:
        result = self._revenues
        if start_date:
            result = [r for r in result if r.date >= start_date]
        if end_date:
            result = [r for r in result if r.date <= end_date]
        return result

    def _filter_expenses(self, start_date=None, end_date=None) -> List[ExpenseEntry]:
        result = self._expenses
        if start_date:
            result = [e for e in result if e.date >= start_date]
        if end_date:
            result = [e for e in result if e.date <= end_date]
        return result

