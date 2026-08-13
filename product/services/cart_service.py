from decimal import Decimal

from sqlalchemy.orm import Session

from product.models.cart import CartItem
from product.repositories import (
    cart_repository,
    product_repository,
    user_repository,
)
from product.schemas.cart_schema import (
    CartItemCreate,
    CartItemUpdate,
    CartSummary,
    CartSummaryItem,
)


def add_to_cart(
    db: Session,
    item_data: CartItemCreate,
    user_id: int,
) -> CartItem:
    """
    Add a product to the authenticated user's cart.

    The user_id comes from the JWT token, not from the request body.
    """

    if item_data.quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    user = user_repository.get_user_by_id(db, user_id)

    if user is None:
        raise ValueError("User not found")

    product = product_repository.get_product_by_id(
        db,
        item_data.product_id,
    )

    if product is None:
        raise ValueError("Product not found")

    # Works if IsActive exists in the model.
    # Defaults to True for older database models.
    if not getattr(product, "IsActive", True):
        raise ValueError("Product is inactive")

    existing_item = (
        cart_repository.get_cart_item_by_user_and_product(
            db,
            user_id,
            item_data.product_id,
        )
    )

    existing_quantity = (
        existing_item.Quantity
        if existing_item is not None
        else 0
    )

    requested_quantity = existing_quantity + item_data.quantity

    if requested_quantity > product.AvailableQuantity:
        raise ValueError("Quantity exceeds available stock")

    if existing_item is not None:
        existing_item.Quantity = requested_quantity

        return cart_repository.update_cart_item(
            db,
            existing_item,
        )

    cart_item = CartItem(
        UserID=user_id,
        ProductID=item_data.product_id,
        Quantity=item_data.quantity,
    )

    return cart_repository.add_cart_item(
        db,
        cart_item,
    )


def get_cart(
    db: Session,
    user_id: int,
) -> list[CartItem]:
    user = user_repository.get_user_by_id(db, user_id)

    if user is None:
        raise ValueError("User not found")

    return cart_repository.get_cart_items_by_user(
        db,
        user_id,
    )


def update_cart_item(
    db: Session,
    cart_item_id: int,
    item_data: CartItemUpdate,
    user_id: int,
) -> CartItem:
    """
    Update only a cart item owned by the authenticated user.
    """

    if item_data.quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    cart_item = cart_repository.get_cart_item_by_id_and_user(
        db,
        cart_item_id,
        user_id,
    )

    if cart_item is None:
        raise ValueError("Cart item not found")

    product = product_repository.get_product_by_id(
        db,
        cart_item.ProductID,
    )

    if product is None:
        raise ValueError("Product not found")

    if not getattr(product, "IsActive", True):
        raise ValueError("Product is inactive")

    if item_data.quantity > product.AvailableQuantity:
        raise ValueError("Quantity exceeds available stock")

    cart_item.Quantity = item_data.quantity

    return cart_repository.update_cart_item(
        db,
        cart_item,
    )


def remove_cart_item(
    db: Session,
    cart_item_id: int,
    user_id: int,
) -> None:
    """
    Delete only a cart item owned by the authenticated user.
    """

    cart_item = cart_repository.get_cart_item_by_id_and_user(
        db,
        cart_item_id,
        user_id,
    )

    if cart_item is None:
        raise ValueError("Cart item not found")

    cart_repository.remove_cart_item(
        db,
        cart_item,
    )


def get_cart_summary(
    db: Session,
    user_id: int,
) -> CartSummary:
    user = user_repository.get_user_by_id(db, user_id)

    if user is None:
        raise ValueError("User not found")

    cart_items = cart_repository.get_cart_items_by_user(
        db,
        user_id,
    )

    summary_items: list[CartSummaryItem] = []
    total_amount = Decimal("0.00")

    for cart_item in cart_items:
        product = product_repository.get_product_by_id(
            db,
            cart_item.ProductID,
        )

        if product is None:
            raise ValueError("Product in cart no longer exists")

        unit_price = Decimal(str(product.Price)).quantize(
            Decimal("0.01"),
        )

        line_total = (
            unit_price * cart_item.Quantity
        ).quantize(Decimal("0.01"))

        total_amount += line_total

        summary_items.append(
            CartSummaryItem(
                product_id=product.ProductID,
                product_name=product.ProductName,
                quantity=cart_item.Quantity,
                unit_price=unit_price,
                line_total=line_total,
            )
        )

    return CartSummary(
        user_id=user_id,
        items=summary_items,
        total_amount=total_amount.quantize(
            Decimal("0.01"),
        ),
    )
