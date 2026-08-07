from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product.db.base import Base

if TYPE_CHECKING:   #solve the circular import error (import is skipped during runtime)
    from product.models.cart import CartItem
    from product.models.order import Order


class User(Base):
    __tablename__ = "users"

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
    Password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    Mobile: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
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

