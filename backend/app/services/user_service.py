from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import User
from app.schemas.user import UserCreate
from app.models.models import User
from app.schemas.user import UserCreate

def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    user = User(
        **user_data.model_dump()
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists") from None

    db.refresh(user)

    return user
# def create_user(
#     db: Session,
#     user_data: UserCreate,
# ) -> User:
#     user = User(
#         **user_data.model_dump()
#     )

#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     return user


def get_users(
    db: Session,
) -> list[User]:
    statement = select(User).order_by(User.full_name)

    return list(db.scalars(statement).all())