from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product.db.base import Base

if TYPE_CHECKING:   #solve the circular import error (import is skipped during runtime)
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

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
    )
