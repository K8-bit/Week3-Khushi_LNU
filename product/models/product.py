from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product.db.base import Base

if TYPE_CHECKING:  #solve the circular import error (import is skipped during runtime)
    from product.models.cart import CartItem
    from product.models.category import Category
    from product.models.order_detail import OrderDetail


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint(
            "Price > 0",
            name="ck_products_price_positive",
        ),
        CheckConstraint(
            "AvailableQuantity >= 0",
            name="ck_products_available_quantity_nonnegative",
        ),
    )

    ProductID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    ProductName: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    Description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    CategoryID: Mapped[int] = mapped_column(
        ForeignKey("categories.CategoryID"),
        nullable=False,
        index=True,
    )

    Price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )


   

    AvailableQuantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    ProductUrl: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
    )

    cart_items: Mapped[list["CartItem"]] = relationship(
        "CartItem",
        back_populates="product",
    )

    order_details: Mapped[list["OrderDetail"]] = relationship(
        "OrderDetail",
        back_populates="product",
    )
