from sqlalchemy.orm import Session

from product.models.order_detail import OrderDetail


def create_order_detail(
    db: Session,
    order_detail: OrderDetail,
) -> OrderDetail:
    db.add(order_detail)
    db.commit()
    db.refresh(order_detail)
    return order_detail


def create_order_details(
    db: Session,
    order_details: list[OrderDetail],
) -> list[OrderDetail]:
    db.add_all(order_details)
    db.commit()

    for order_detail in order_details:
        db.refresh(order_detail)

    return order_details


def get_order_detail_by_id(
    db: Session,
    order_detail_id: int,
) -> OrderDetail | None:
    return (
        db.query(OrderDetail)
        .filter(
            OrderDetail.OrderDetailID == order_detail_id
        )
        .first()
    )


def get_order_details_by_order(
    db: Session,
    order_id: int,
) -> list[OrderDetail]:
    return (
        db.query(OrderDetail)
        .filter(OrderDetail.OrderID == order_id)
        .order_by(OrderDetail.OrderDetailID)
        .all()
    )


def get_all_order_details(
    db: Session,
) -> list[OrderDetail]:
    return (
        db.query(OrderDetail)
        .order_by(OrderDetail.OrderDetailID)
        .all()
    )


def delete_order_detail(
    db: Session,
    order_detail: OrderDetail,
) -> None:
    db.delete(order_detail)
    db.commit()


def delete_order_details_by_order(
    db: Session,
    order_id: int,
) -> None:
    (
        db.query(OrderDetail)
        .filter(OrderDetail.OrderID == order_id)
        .delete(synchronize_session=False)
    )
    db.commit()
