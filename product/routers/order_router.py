from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.schemas.order_schema import (
    OrderCreate,
    OrderHistoryResponse,
    OrderResponse,
)
from product.services import order_service


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


def service_error_to_http(error: ValueError) -> HTTPException:
    message = str(error)
    message_lower = message.lower()

    if (
        "not found" in message_lower
        or "no longer exists" in message_lower
    ):
        error_status = status.HTTP_404_NOT_FOUND
    elif "stock" in message_lower:
        error_status = status.HTTP_409_CONFLICT
    else:
        error_status = status.HTTP_400_BAD_REQUEST

    return HTTPException(
        status_code=error_status,
        detail=message,
    )


@router.post(
    "/checkout",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def checkout(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
):
    try:
        return order_service.create_order(
            db,
            order_data,
        )
    except ValueError as error:
        raise service_error_to_http(error) from error
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to place the order",
        ) from error


@router.get(
    "/details/{order_id}",
    response_model=OrderResponse,
)
def get_order_details(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    order = order_service.get_order_by_id(
        db,
        order_id,
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order


@router.get(
    "/{user_id}",
    response_model=list[OrderHistoryResponse],
)
def get_order_history(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    try:
        return order_service.get_orders_by_user(
            db,
            user_id,
        )
    except ValueError as error:
        raise service_error_to_http(error) from error
