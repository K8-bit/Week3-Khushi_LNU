from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.models.user import User
from product.schemas.user_schema import UserCreate, UserResponse
from product.services import user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)



@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)

def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> User:
    """Register a new user."""

    try:
        return user_service.create_user(
            db,
            user_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> User:
    """Get user details by ID."""

    user = user_service.get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
