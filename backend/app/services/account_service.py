from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import (
    FinancialAccount,
    FinancialConnection,
    User,
)
from app.schemas.account import AccountCreate


def create_account(
    db: Session,
    account_data: AccountCreate,
) -> FinancialAccount:

    user = db.get(
        User,
        account_data.user_id,
    )

    if user is None:
        raise ValueError("User not found")

    account = FinancialAccount(
        **account_data.model_dump()
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return account


def get_user_accounts(
    db: Session,
    user_id: int,
) -> list[FinancialAccount]:

    statement = select(
        FinancialAccount
    ).where(
        FinancialAccount.user_id == user_id
    ).order_by(
        FinancialAccount.created_at.desc()
    )

    return list(
        db.scalars(statement).all()
    )


def create_connection(
    db: Session,
    account_id: int,
    provider_name: str,
) -> FinancialConnection:

    account = db.get(
        FinancialAccount,
        account_id,
    )

    if account is None:
        raise ValueError(
            "Financial account not found"
        )

    connection = FinancialConnection(
        account_id=account_id,
        provider_name=provider_name,
        status="pending",
    )

    db.add(connection)
    db.commit()
    db.refresh(connection)

    return connection