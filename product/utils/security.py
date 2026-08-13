from datetime import datetime, timedelta, timezone
from typing import Any
import os

from dotenv import load_dotenv
from jwt import decode, encode
from pwdlib import PasswordHash


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is missing. Add it to the .env file."
    )

ALGORITHM = os.getenv("ALGORITHM", "HS256")

TOKEN_EXPIRE_MINUTES = int(
    os.getenv("TOKEN_EXPIRE_MINUTES", "30")
)

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a password before storing it."""

    return password_hash.hash(password)

#Salt and Parameter
def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Verify a plain password against its stored hash."""

    try:
        return password_hash.verify(
            plain_password,
            hashed_password,
        )
    except Exception:
        return False


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT access token."""

    payload = data.copy()

    expire_at = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    )

    payload["exp"] = expire_at


    return encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict[str, Any]:
    """Decode and validate a JWT access token."""

    return decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )
