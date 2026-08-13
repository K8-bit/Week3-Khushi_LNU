from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product.db.base import Base

if TYPE_CHECKING:
    from product.models.order import Order
    from product.models.product import Product


class OrderDetail(Base):
    __tablename__ = "order_details"

    __table_args__ = (
        CheckConstraint(
            "Quantity > 0",
            name="ck_order_details_quantity_positive",
        ),
        CheckConstraint(
            "Price > 0",
            name="ck_order_details_price_positive",
        ),
    )

    OrderDetailID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    OrderID: Mapped[int] = mapped_column(
        ForeignKey("orders.OrderID", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ProductID: Mapped[int] = mapped_column(
        ForeignKey("products.ProductID"),
        nullable=False,
        index=True,
    )

    Quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    Price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="order_details",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="order_details",
    )
