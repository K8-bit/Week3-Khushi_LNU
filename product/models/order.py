from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product.db.base import Base

if TYPE_CHECKING:
    from product.models.order_detail import OrderDetail
    from product.models.user import User


class Order(Base):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "TotalAmount >= 0",
            name="ck_orders_total_amount_nonnegative",
        ),
        CheckConstraint(
            "OrderStatus IN "
            "('pending', 'confirmed', 'processing', "
            "'shipped', 'delivered', 'cancelled')",
            name="ck_orders_status_valid",
        ),
        CheckConstraint(
            "PaymentStatus IN "
            "('pending', 'paid', 'failed', 'refunded')",
            name="ck_orders_payment_status_valid",
        ),
    )

    OrderID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    UserID: Mapped[int] = mapped_column(
        ForeignKey("users.UserID"),
        nullable=False,
        index=True,
    )

    OrderDate: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )

    PaymentMethod: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    TotalAmount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    OrderStatus: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pending",
        server_default=text("'pending'"),
        index=True,
    )

    PaymentStatus: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pending",
        server_default=text("'pending'"),
        index=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="orders",
    )

    order_details: Mapped[list["OrderDetail"]] = relationship(
        "OrderDetail",
        back_populates="order",
        cascade="all, delete-orphan",
    )
