from sqlalchemy import func
from sqlalchemy.orm import Session

from product.models.user import User


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    return (
        db.query(User)
        .filter(User.UserID == user_id)
        .first()
    )


def get_all_users(db: Session) -> list[User]:
    return (
        db.query(User)
        .order_by(User.UserID)
        .all()
    )


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    return (
        db.query(User)
        .filter(func.lower(User.Email) == email.strip().lower())
        .first()
    )


def update_user(db: Session, user: User) -> User:
    """Save changes made to a user."""
    db.commit()
    db.refresh(user)
    return user


def count_active_admins(db: Session) -> int:
    """Return the number of active administrators."""
    return (
        db.query(User)
        .filter(
            User.Role == "admin",
            User.IsActive.is_(True),
        )
        .count()
    )
