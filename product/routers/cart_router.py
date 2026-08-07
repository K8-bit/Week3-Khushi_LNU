from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session 

from product.db.session import get_db
from product.schemas.cart_schema import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartSummary,
)
from product.services import cart_service


router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


def raise_cart_error(error: ValueError) -> None:
    detail = str(error)

    not_found_messages = {
        "User not found",
        "Product not found",
        "Cart item not found",
        "Product in cart no longer exists",
    }

    error_status = (
        status.HTTP_404_NOT_FOUND
        if detail in not_found_messages
        else status.HTTP_400_BAD_REQUEST
    )

    raise HTTPException(
        status_code=error_status,
        detail=detail,
    )


@router.post(    #Create
    "/add",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
):
    try:
        return cart_service.add_to_cart(
            db=db,
            item_data=item,
        )
    except ValueError as error:
        raise_cart_error(error)


@router.get(    #Read
    "/{user_id}/summary",
    response_model=CartSummary,
)
def get_cart_summary(
    user_id: int,
    db: Session = Depends(get_db),
):
    try:
        return cart_service.get_cart_summary(
            db=db,
            user_id=user_id,
        )
    except ValueError as error:
        raise_cart_error(error)


@router.get(
    "/{user_id}",
    response_model=list[CartItemResponse],
)
def get_cart(
    user_id: int,
    db: Session = Depends(get_db),
):
    try:
        return cart_service.get_cart(
            db=db,
            user_id=user_id,
        )
    except ValueError as error:
        raise_cart_error(error)


@router.put(   #Update
    "/update/{cart_item_id}",
    response_model=CartItemResponse,
)
def update_cart_item(
    cart_item_id: int,
    item: CartItemUpdate,
    db: Session = Depends(get_db),
):
    try:
        return cart_service.update_cart_item(
            db=db,
            cart_item_id=cart_item_id,
            item_data=item,
        )
    except ValueError as error:
        raise_cart_error(error)


@router.delete(    #Delete
    "/remove/{cart_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
):
    try:
        cart_service.remove_cart_item(
            db=db,
            cart_item_id=cart_item_id,
        )
    except ValueError as error:
        raise_cart_error(error)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
