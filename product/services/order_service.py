import logging
from decimal import Decimal

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from product.models.cart import CartItem
from product.models.order import Order
from product.models.order_detail import OrderDetail
from product.models.product import Product
from product.repositories import (
    cart_repository,
    order_repository,
    product_repository,
    user_repository,
)
from product.schemas.order_schema import OrderCreate


logger = logging.getLogger("shopping.orders")


def create_order(
    db: Session,
    order_data: OrderCreate,
    user_id: int,
) -> Order:
    """Create an order for the authenticated user."""

    user = user_repository.get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise ValueError("User not found")

    cart_items = cart_repository.get_cart_items_by_user(
        db,
        user_id,
    )

    if not cart_items:
        raise ValueError("Cart is empty")

    total_amount = Decimal("0.00")

    products_in_order: list[
        tuple[Product, CartItem, Decimal]
    ] = []

    for cart_item in cart_items:
        product = product_repository.get_product_by_id(
            db,
            cart_item.ProductID,
        )

        if product is None:
            raise ValueError(
                "Product in cart no longer exists",
            )

        if not getattr(product, "IsActive", True):
            raise ValueError(
                f"Product {product.ProductName} is inactive",
            )

        if cart_item.Quantity <= 0:
            raise ValueError(
                "Cart quantity must be greater than zero",
            )

        if cart_item.Quantity > product.AvailableQuantity:
            raise ValueError(
                f"Not enough stock for {product.ProductName}",
            )

        unit_price = Decimal(
            str(product.Price),
        ).quantize(Decimal("0.01"))

        total_amount += unit_price * cart_item.Quantity

        products_in_order.append(
            (
                product,
                cart_item,
                unit_price,
            ),
        )

    try:
        order = Order(
            UserID=user_id,
            PaymentMethod=order_data.payment_method,
            TotalAmount=total_amount,
            OrderStatus="pending",
            PaymentStatus="pending",
        )

        db.add(order)
        db.flush()

        for product, cart_item, unit_price in products_in_order:
            db.add(
                OrderDetail(
                    order=order,
                    product=product,
                    Quantity=cart_item.Quantity,
                    Price=unit_price,
                )
            )

            product.AvailableQuantity -= cart_item.Quantity
            db.delete(cart_item)

        db.commit()
        db.refresh(order)

        logger.info(
            "order_created",
            extra={
                "order_id": order.OrderID,
                "user_id": user_id,
                "total_amount": str(total_amount),
            },
        )

        return order

    except SQLAlchemyError:
        db.rollback()

        logger.exception(
            "order_creation_failed",
            extra={"user_id": user_id},
        )

        raise


def get_order_by_id(
    db: Session,
    order_id: int,
) -> Order | None:
    return order_repository.get_order_by_id(
        db,
        order_id,
    )


def get_order_by_id_for_user(
    db: Session,
    order_id: int,
    user_id: int,
) -> Order | None:
    return order_repository.get_order_by_id_for_user(
        db,
        order_id,
        user_id,
    )


def get_orders_by_user(
    db: Session,
    user_id: int,
) -> list[Order]:
    user = user_repository.get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise ValueError("User not found")

    return order_repository.get_orders_by_user(
        db,
        user_id,
    )


def get_all_orders(
    db: Session,
) -> list[Order]:
    return order_repository.get_all_orders(db)
