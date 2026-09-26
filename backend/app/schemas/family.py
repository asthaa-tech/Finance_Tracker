from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.enums import FamilyRole, MembershipStatus


class FamilyCreate(BaseModel):
    name: str


class FamilyResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    created_at: datetime


class FamilyMemberCreate(BaseModel):
    user_id: int
    role: FamilyRole = FamilyRole.MEMBER


class FamilyMemberResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    family_id: int
    user_id: int
    role: FamilyRole
    status: MembershipStatus
    created_at: datetime