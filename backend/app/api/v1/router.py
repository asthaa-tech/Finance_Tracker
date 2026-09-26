from fastapi import APIRouter

from app.api.v1.accounts import router as accounts_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.categories import router as categories_router
from app.api.v1.families import router as families_router
from app.api.v1.transactions import router as transactions_router
from app.api.v1.users import router as users_router


router = APIRouter(
    prefix="/api/v1",
)


router.include_router(users_router)

router.include_router(categories_router)

router.include_router(transactions_router)

router.include_router(families_router)

router.include_router(accounts_router)

router.include_router(analytics_router)