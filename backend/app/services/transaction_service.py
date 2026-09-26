from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.models import Category, FinancialAccount, Transaction, User
from app.schemas.enums import TransactionType
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
)


def create_transaction(
    db: Session,
    transaction_data: TransactionCreate,
) -> Transaction:

    user = db.get(
        User,
        transaction_data.user_id,
    )

    if user is None:
        raise ValueError("User not found")

    category = db.get(
        Category,
        transaction_data.category_id,
    )

    if category is None:
        raise ValueError("Category not found")

    if transaction_data.account_id is not None:
        account = db.get(
            FinancialAccount,
            transaction_data.account_id,
        )

        if account is None:
            raise ValueError("Financial account not found")

        if account.user_id != transaction_data.user_id:
            raise ValueError(
                "Financial account does not belong to user"
            )

    transaction = Transaction(
        **transaction_data.model_dump()
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


def get_transactions(
    db: Session,
    user_id: int,
    category_id: int | None = None,
    transaction_type: TransactionType | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Transaction], int]:

    statement = select(Transaction).where(
        Transaction.user_id == user_id
    )

    if category_id is not None:
        statement = statement.where(
            Transaction.category_id == category_id
        )

    if transaction_type is not None:
        statement = statement.where(
            Transaction.transaction_type == transaction_type.value
        )

    if start_date is not None:
        statement = statement.where(
            Transaction.transaction_date >= start_date
        )

    if end_date is not None:
        statement = statement.where(
            Transaction.transaction_date <= end_date
        )

    count_statement = select(
        func.count()
    ).select_from(
        statement.subquery()
    )

    total = db.scalar(count_statement) or 0

    statement = statement.order_by(
        Transaction.transaction_date.desc(),
        Transaction.id.desc(),
    )

    statement = statement.offset(
        (page - 1) * page_size
    ).limit(page_size)

    transactions = list(
        db.scalars(statement).all()
    )

    return transactions, total


def get_transaction(
    db: Session,
    transaction_id: int,
) -> Transaction | None:
    return db.get(
        Transaction,
        transaction_id,
    )


def update_transaction(
    db: Session,
    transaction: Transaction,
    transaction_data: TransactionUpdate,
) -> Transaction:

    update_data = transaction_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            transaction,
            field,
            value,
        )

    db.commit()
    db.refresh(transaction)

    return transaction


def delete_transaction(
    db: Session,
    transaction: Transaction,
) -> None:

    db.delete(transaction)
    db.commit()