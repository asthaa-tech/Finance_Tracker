from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.enums import CategorizationSource, TransactionType


class TransactionBase(BaseModel):
    category_id: int

    amount: Decimal = Field(
        gt=0
    )

    transaction_type: TransactionType

    description: str | None = None

    merchant_name: str | None = None

    transaction_date: date


class TransactionCreate(TransactionBase):
    user_id: int

    account_id: int | None = None


class TransactionUpdate(BaseModel):
    category_id: int | None = None

    account_id: int | None = None

    amount: Decimal | None = Field(
        default=None,
        gt=0,
    )

    transaction_type: TransactionType | None = None

    description: str | None = None

    merchant_name: str | None = None

    transaction_date: date | None = None


class TransactionResponse(TransactionBase):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    user_id: int

    account_id: int | None

    categorization_source: CategorizationSource

    categorization_confidence: Decimal | None

    external_transaction_id: str | None

    created_at: datetime


class TransactionListResponse(BaseModel):
    items: list[TransactionResponse]

    total: int

    page: int

    page_size: int

    pages: int