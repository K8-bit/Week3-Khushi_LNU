from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product.db.base import Base

if TYPE_CHECKING:
    from product.models.cart import CartItem
    from product.models.order import Order


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "Role IN ('customer', 'admin', 'support', 'operations')",
            name="ck_users_role_valid",
        ),
    )

    UserID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    Name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    Email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    # Always store a hashed password.
    Password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    Mobile: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    # Supported roles:
    # customer, admin, support, operations
    Role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="customer",
        server_default=text("'customer'"),
        index=True,
    )

    IsActive: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("TRUE"),
        index=True,
    )

    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan",
    )

