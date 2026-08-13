from sqlalchemy.orm import Session

from product.models.user import User
from product.repositories import user_repository
from product.schemas.user_schema import UserCreate
from product.utils.security import hash_password, verify_password
from product.utils.logging_config import logger


ALLOWED_ROLES = {
    "customer",
    "admin",
    "support"
}


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    email = user_data.email.strip().lower()
    password = user_data.password

    if user_repository.get_user_by_email(db, email):
        raise ValueError("Email already exists")

    user = User(
        Name=user_data.name.strip(),
        Email=email,
        Password=hash_password(password),
        Mobile=user_data.mobile.strip(),
        # Public registration must always create a customer.
        Role="customer",
        IsActive=True,
    )

    return user_repository.create_user(db, user)


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    normalized_email = email.strip().lower()
    logger.info(
            "Login attempt for email=%s",
            normalized_email,
        )
 

    user = user_repository.get_user_by_email(
        db=db,
        email=normalized_email,
    )

    if user is None:
        return None

    if not verify_password(password, user.Password):
        return None

    if not user.IsActive:
        return None

    return user


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    return user_repository.get_user_by_id(
        db=db,
        user_id=user_id,
    )


def update_user_role(
    db: Session,
    user_id: int,
    role: str,
    acting_admin_id: int,
) -> User:
    """
    Update a user's role.

    Only an administrator should be able to call this service.
    The router enforces the administrator authorization.
    """

    new_role = str(role).strip().lower()

    if new_role not in ALLOWED_ROLES:
        raise ValueError(
            "Invalid role. Allowed roles are: "
            "customer, admin, support"
        )

    user = user_repository.get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise ValueError("User not found")

    # Prevent an admin from removing their own administrator access.
    if user.UserID == acting_admin_id and new_role != "admin":
        raise ValueError(
            "An administrator cannot remove their own admin role"
        )

    # Prevent removal of the last active administrator.
    if (
        user.Role == "admin"
        and new_role != "admin"
        and user.IsActive
        and user_repository.count_active_admins(db) <= 1
    ):
        raise ValueError(
            "At least one active administrator must remain"
        )

    user.Role = new_role

    return user_repository.update_user(
        db=db,
        user=user,
    )
