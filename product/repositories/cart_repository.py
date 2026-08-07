from sqlalchemy.orm import Session

from product.models.cart import CartItem


def add_cart_item(
    db: Session,
    cart_item: CartItem,
) -> CartItem:
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


def get_cart_item_by_id(
    db: Session,
    cart_item_id: int,
) -> CartItem | None:
    return (
        db.query(CartItem)
        .filter(CartItem.CartItemID == cart_item_id)
        .first()
    )


def get_cart_item_by_user_and_product(
    db: Session,
    user_id: int,
    product_id: int,
) -> CartItem | None:
    return (
        db.query(CartItem)
        .filter(
            CartItem.UserID == user_id,
            CartItem.ProductID == product_id,
        )
        .first()
    )


def get_cart_items_by_user(
    db: Session,
    user_id: int,
) -> list[CartItem]:
    return (
        db.query(CartItem)
        .filter(CartItem.UserID == user_id)
        .order_by(CartItem.CartItemID)
        .all()
    )


def update_cart_item(
    db: Session,
    cart_item: CartItem,
) -> CartItem:
    db.commit()
    db.refresh(cart_item)
    return cart_item


def remove_cart_item(
    db: Session,
    cart_item: CartItem,
) -> None:
    db.delete(cart_item)
    db.commit()
