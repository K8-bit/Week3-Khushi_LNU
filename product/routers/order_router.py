from typing import NoReturn

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    status,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.models.user import User
from product.schemas.order_schema import (
    OrderCreate,
    OrderHistoryResponse,
    OrderResponse,
)
from product.services import order_service
from product.utils.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/orders",
    tags=["Customer Orders"],
)


def require_customer(
    current_user: User = Depends(get_current_user),
) -> User:
    """Allow order operations only for active customers."""

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
            detail="Only customers can place and view orders",
        )

    return current_user


def raise_order_error(error: ValueError) -> NoReturn:
    """Convert order service errors into HTTP responses."""

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
    "/checkout",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Checkout the authenticated user's cart",
)
async def checkout(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer),
):
    try:
        return order_service.create_order(
            db=db,
            order_data=order_data,
            user_id=current_user.UserID,
        )

    except ValueError as error:
        raise_order_error(error)

    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to place the order",
        ) from error


@router.get(
    "/me",
    response_model=list[OrderHistoryResponse],
    summary="View the authenticated user's order history",
)
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer),
):
    try:
        return order_service.get_orders_by_user(
            db=db,
            user_id=current_user.UserID,
        )

    except ValueError as error:
        raise_order_error(error)


@router.get(
    "/details/{order_id}",
    response_model=OrderResponse,
    summary="View one order owned by the authenticated user",
)
def get_my_order_details(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer),
):
    order = order_service.get_order_by_id_for_user(
        db=db,
        order_id=order_id,
        user_id=current_user.UserID,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order
