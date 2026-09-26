from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.analytics import MonthlySummary
from app.services.analytics_service import get_monthly_summary


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/monthly",
    response_model=MonthlySummary,
)
def monthly_summary(
    user_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db),
):

    return get_monthly_summary(
        db=db,
        user_id=user_id,
        year=year,
        month=month,
    )