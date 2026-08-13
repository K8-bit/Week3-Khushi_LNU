from typing import NoReturn

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.models.user import User
from product.schemas.cart_schema import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartSummary,
)
from product.services import cart_service
from product.utils.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/cart",
    tags=["Customer Cart"],
)


def require_customer(
    current_user: User = Depends(get_current_user),
) -> User:
    """Allow cart operations only for active customers."""

    if not getattr(current_user, "IsActive", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    role = str(
        getattr(current_user, "Role", "customer")
    ).lower()

    if role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can manage a cart",
        )

    return current_user


def raise_cart_error(error: ValueError) -> NoReturn:
    """Convert service errors into suitable HTTP responses."""

    message = str(error)
    message_lower = message.lower()

    if (
        "not found" in message_lower
        or "no longer exists" in message_lower
    ):
        error_status = status.HTTP_404_NOT_FOUND

    elif (
        "stock" in message_lower
        or "inactive" in message_lower
    ):
        error_status = status.HTTP_409_CONFLICT

    else:
        error_status = status.HTTP_400_BAD_REQUEST

    raise HTTPException(
        status_code=error_status,
        detail=message,
    )


@router.post(
    "/add",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a product to the authenticated user's cart",
)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer),
):
    try:
        return cart_service.add_to_cart(
            db=db,
            item_data=item,
            user_id=current_user.UserID,
        )
    except ValueError as error:
        raise_cart_error(error)


@router.get(
    "",
    response_model=list[CartItemResponse],
    summary="View the authenticated user's cart",
)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer),
):
    try:
        return cart_service.get_cart(
            db=db,
            user_id=current_user.UserID,
        )
    except ValueError as error:
        raise_cart_error(error)


@router.get(
    "/summary",
    response_model=CartSummary,
    summary="View the authenticated user's cart summary",
)
def get_cart_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer),
):
    try:
        return cart_service.get_cart_summary(
            db=db,
            user_id=current_user.UserID,
        )
    except ValueError as error:
        raise_cart_error(error)


@router.put(
    "/update/{cart_item_id}",
    response_model=CartItemResponse,
    summary="Update a cart item owned by the authenticated user",
)
def update_cart_item(
    cart_item_id: int,
    item: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer),
):
    try:
        return cart_service.update_cart_item(
            db=db,
            cart_item_id=cart_item_id,
            item_data=item,
            user_id=current_user.UserID,
        )
    except ValueError as error:
        raise_cart_error(error)


@router.delete(
    "/remove/{cart_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a cart item owned by the authenticated user",
)
def remove_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer),
):
    try:
        cart_service.remove_cart_item(
            db=db,
            cart_item_id=cart_item_id,
            user_id=current_user.UserID,
        )
    except ValueError as error:
        raise_cart_error(error)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
