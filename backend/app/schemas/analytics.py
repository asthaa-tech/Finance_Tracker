from decimal import Decimal

from pydantic import BaseModel


class CategorySpending(BaseModel):
    category_id: int
    category_name: str
    amount: Decimal
    percentage: Decimal


class MonthlySummary(BaseModel):
    month: str

    total_income: Decimal

    total_expense: Decimal

    net_savings: Decimal

    savings_percentage: Decimal

    category_breakdown: list[CategorySpending]