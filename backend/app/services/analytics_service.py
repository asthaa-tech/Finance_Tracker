from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.models import Category, Transaction


def get_monthly_summary(
    db: Session,
    user_id: int,
    year: int,
    month: int,
):

    start_date = date(
        year,
        month,
        1,
    )

    if month == 12:
        end_date = date(
            year + 1,
            1,
            1,
        )
    else:
        end_date = date(
            year,
            month + 1,
            1,
        )

    income_statement = select(
        func.coalesce(
            func.sum(Transaction.amount),
            0,
        )
    ).where(
        Transaction.user_id == user_id,
        Transaction.transaction_type == "income",
        Transaction.transaction_date >= start_date,
        Transaction.transaction_date < end_date,
    )

    expense_statement = select(
        func.coalesce(
            func.sum(Transaction.amount),
            0,
        )
    ).where(
        Transaction.user_id == user_id,
        Transaction.transaction_type == "expense",
        Transaction.transaction_date >= start_date,
        Transaction.transaction_date < end_date,
    )

    total_income = db.scalar(
        income_statement
    ) or Decimal("0")

    total_expense = db.scalar(
        expense_statement
    ) or Decimal("0")

    net_savings = (
        total_income - total_expense
    )

    savings_percentage = (
        (net_savings / total_income) * 100
        if total_income > 0
        else Decimal("0")
    )

    category_statement = (
        select(
            Category.id,
            Category.name,
            func.sum(Transaction.amount),
        )
        .join(
            Transaction,
            Transaction.category_id == Category.id,
        )
        .where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date < end_date,
        )
        .group_by(
            Category.id,
            Category.name,
        )
        .order_by(
            func.sum(Transaction.amount).desc()
        )
    )

    category_rows = db.execute(
        category_statement
    ).all()

    category_breakdown = []

    for category_id, category_name, amount in category_rows:

        percentage = (
            (amount / total_expense) * 100
            if total_expense > 0
            else Decimal("0")
        )

        category_breakdown.append(
            {
                "category_id": category_id,
                "category_name": category_name,
                "amount": amount,
                "percentage": percentage,
            }
        )

    return {
        "month": f"{year:04d}-{month:02d}",
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": net_savings,
        "savings_percentage": savings_percentage,
        "category_breakdown": category_breakdown,
    }