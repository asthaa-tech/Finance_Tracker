from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.enums import AccountType, ConnectionStatus


class AccountCreate(BaseModel):
    user_id: int
    account_name: str
    account_type: AccountType
    provider_name: str | None = None
    identifier: str | None = None


class AccountResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    user_id: int
    account_name: str
    account_type: AccountType
    provider_name: str | None
    identifier: str | None
    is_active: bool
    created_at: datetime


class ConnectionCreate(BaseModel):
    provider_name: str


class ConnectionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    account_id: int
    provider_name: str
    status: ConnectionStatus
    external_account_id: str | None
    last_synced_at: datetime | None
    created_at: datetime