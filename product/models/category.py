from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product.db.base import Base

if TYPE_CHECKING:
    from product.models.product import Product


class Category(Base):
    __tablename__ = "categories"

    CategoryID: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    CategoryName: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    IsActive: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("TRUE"),
        index=True,
    )

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
    )
