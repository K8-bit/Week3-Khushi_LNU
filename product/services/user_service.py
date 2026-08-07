from sqlalchemy.orm import Session

from product.models.user import User
from product.repositories import user_repository
from product.schemas.user_schema import UserCreate, UserLogin


def create_user(db: Session, user_data: UserCreate) -> User:
    email = str(user_data.email).strip().lower()

    if user_repository.get_user_by_email(db, email):
        raise ValueError("Email already exists")

    user = User(
        Name=user_data.name,
        Email=email,
        Password=user_data.password,
        Mobile=user_data.mobile,
    )
    return user_repository.create_user(db, user)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return user_repository.get_user_by_id(db, user_id)


def login_user(db: Session, login_data: UserLogin):
    user = user_repository.get_user_by_email(db, str(login_data.email).strip().lower())

    if user is None or user.Password != login_data.password:
        raise ValueError("Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": user.UserID,
        "name": user.Name,
        "email": user.Email,
    }
