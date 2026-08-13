import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError,
)
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.repositories import user_repository
from product.utils.security import decode_access_token


logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(
    auto_error=False,
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
):
    """Read the bearer token and return the authenticated user."""

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    token = credentials.credentials.strip()

    # Makes the code tolerant if "Bearer " was accidentally pasted
    # into Swagger's HTTPBearer value field.
    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    try:
        payload = decode_access_token(token)

        subject = payload.get("sub")

        if subject is None:
            raise ValueError("Token subject is missing")

        user_id = int(subject)

    except ExpiredSignatureError as error:
        logger.warning("JWT token has expired")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from error

    except InvalidSignatureError as error:
        logger.warning("JWT signature is invalid")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from error

    except (
        DecodeError,
        InvalidTokenError,
        ValueError,
        TypeError,
    ) as error:
        logger.warning("JWT token could not be decoded")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from error

    user = user_repository.get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    if not user.IsActive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user
