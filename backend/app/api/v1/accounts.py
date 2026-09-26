from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.account import (
    AccountCreate,
    AccountResponse,
    ConnectionCreate,
    ConnectionResponse,
)
from app.services.account_service import (
    create_account,
    create_connection,
    get_user_accounts,
)


router = APIRouter(
    prefix="/accounts",
    tags=["Financial Accounts"],
)


@router.post(
    "",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    account_data: AccountCreate,
    db: Session = Depends(get_db),
):

    try:
        return create_account(
            db,
            account_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/user/{user_id}",
    response_model=list[AccountResponse],
)
def list_user_accounts(
    user_id: int,
    db: Session = Depends(get_db),
):

    return get_user_accounts(
        db,
        user_id,
    )


@router.post(
    "/{account_id}/connections",
    response_model=ConnectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def connect(
    account_id: int,
    connection_data: ConnectionCreate,
    db: Session = Depends(get_db),
):

    try:
        return create_connection(
            db=db,
            account_id=account_id,
            provider_name=connection_data.provider_name,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc