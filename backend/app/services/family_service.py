from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import (
    Family,
    FamilyMembership,
    User,
)
from app.schemas.family import FamilyMemberCreate


def create_family(
    db: Session,
    name: str,
    owner_user_id: int,
) -> Family:

    user = db.get(
        User,
        owner_user_id,
    )

    if user is None:
        raise ValueError("User not found")

    family = Family(
        name=name,
    )

    db.add(family)
    db.flush()

    membership = FamilyMembership(
        family_id=family.id,
        user_id=owner_user_id,
        role="owner",
        status="active",
    )

    db.add(membership)

    db.commit()
    db.refresh(family)

    return family


def add_family_member(
    db: Session,
    family_id: int,
    member_data: FamilyMemberCreate,
) -> FamilyMembership:

    family = db.get(
        Family,
        family_id,
    )

    if family is None:
        raise ValueError("Family not found")

    user = db.get(
        User,
        member_data.user_id,
    )

    if user is None:
        raise ValueError("User not found")

    existing = db.scalar(
        select(FamilyMembership).where(
            FamilyMembership.family_id == family_id,
            FamilyMembership.user_id == member_data.user_id,
        )
    )

    if existing is not None:
        raise ValueError(
            "User is already a member of this family"
        )

    membership = FamilyMembership(
        family_id=family_id,
        user_id=member_data.user_id,
        role=member_data.role.value,
        status="active",
    )

    db.add(membership)
    db.commit()
    db.refresh(membership)

    return membership


def get_family_members(
    db: Session,
    family_id: int,
) -> list[FamilyMembership]:

    statement = select(
        FamilyMembership
    ).where(
        FamilyMembership.family_id == family_id,
        FamilyMembership.status == "active",
    )

    return list(
        db.scalars(statement).all()
    )