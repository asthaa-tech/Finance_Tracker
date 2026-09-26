from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.family import (
    FamilyCreate,
    FamilyMemberCreate,
    FamilyMemberResponse,
    FamilyResponse,
)
from app.services.family_service import (
    add_family_member,
    create_family,
    get_family_members,
)


router = APIRouter(
    prefix="/families",
    tags=["Families"],
)


@router.post(
    "",
    response_model=FamilyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    family_data: FamilyCreate,
    owner_user_id: int,
    db: Session = Depends(get_db),
):

    try:
        return create_family(
            db=db,
            name=family_data.name,
            owner_user_id=owner_user_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "/{family_id}/members",
    response_model=FamilyMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_member(
    family_id: int,
    member_data: FamilyMemberCreate,
    db: Session = Depends(get_db),
):

    try:
        return add_family_member(
            db,
            family_id,
            member_data,
        )

    except ValueError as exc:
        status_code = (
            status.HTTP_409_CONFLICT
            if "already" in str(exc)
            else status.HTTP_404_NOT_FOUND
        )

        raise HTTPException(
            status_code=status_code,
            detail=str(exc),
        ) from exc


@router.get(
    "/{family_id}/members",
    response_model=list[FamilyMemberResponse],
)
def members(
    family_id: int,
    db: Session = Depends(get_db),
):

    return get_family_members(
        db,
        family_id,
    )