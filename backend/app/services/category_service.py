from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Category
from app.schemas.category import CategoryCreate


def create_category(
    db: Session,
    category_data: CategoryCreate,
) -> Category:
    category = Category(
        **category_data.model_dump()
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(
    db: Session,
) -> list[Category]:
    statement = select(Category).order_by(Category.name)

    return list(db.scalars(statement).all())