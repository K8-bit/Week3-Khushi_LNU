from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product.db.base import Base

if TYPE_CHECKING:   #solve the circular import error (import is skipped during runtime)
    from product.models.product import Product
    from product.models.user import User


class CartItem(Base):
    __tablename__ = "cart_items"

    __table_args__ = (
        CheckConstraint(
            "Quantity > 0",
            name="ck_cart_items_quantity_positive",
        ),
    )

    CartItemID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    UserID: Mapped[int] = mapped_column(
        ForeignKey("users.UserID"),
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
        default=1,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="cart_items",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="cart_items",
    )
