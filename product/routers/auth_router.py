from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.schemas.auth_schema import TokenResponse
from product.services.user_service import authenticate_user
from product.utils.security import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/token",
    response_model=TokenResponse,
    summary="Login and generate an access token",
)
def login_for_access_token(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    #access to the db
    db: Annotated[ 
        Session,
        Depends(get_db),
    ],
) -> TokenResponse:
    """
    Use the user's email as the username.

    This endpoint receives:
    - username: user's email
    - password: user's password

    It returns a JWT access token.
    """

    user = authenticate_user(
        db=db,
        email=form_data.username.strip().lower(),
        password=form_data.password,
    )

    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={
            "sub": str(user.UserID),
            "role": str(user.Role).strip().lower(),
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
