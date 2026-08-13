from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from product.models.user import User
from product.utils.security import verify_password


async def authenticate_user(
    db: AsyncSession,
    username: str,
    password: str,
) -> User | None:
    """Find a user by email and verify the supplied password."""

    result = await db.execute(
        select(User).where(User.Email == username)
    )

    user = result.scalar_one_or_none()

    if user is None:
        return None

    if not verify_password(
        password,
        user.Password,
    ):
        return None

    return user
