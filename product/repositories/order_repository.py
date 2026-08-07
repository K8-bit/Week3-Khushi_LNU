from sqlalchemy.orm import Session

from product.models.order import Order


def create_order(db: Session, order: Order) -> Order:
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order_by_id(
    db: Session,
    order_id: int,
) -> Order | None:
    return (
        db.query(Order)
        .filter(Order.OrderID == order_id)
        .first()
    )


def get_orders_by_user(
    db: Session,
    user_id: int,
) -> list[Order]:
    return (
        db.query(Order)
        .filter(Order.UserID == user_id)
        .order_by(Order.OrderDate.desc())
        .all()
    )


def get_all_orders(db: Session) -> list[Order]:
    return (
        db.query(Order)
        .order_by(Order.OrderDate.desc())
        .all()
    )
