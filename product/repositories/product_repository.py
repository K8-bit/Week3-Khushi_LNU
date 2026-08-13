from sqlalchemy import func
from sqlalchemy.orm import Session

from product.models.product import Product


def create_product(
    db: Session,
    product: Product,
) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product_by_id(
    db: Session,
    product_id: int,
    include_inactive: bool = False,
) -> Product | None:
    query = (
        db.query(Product)
        .filter(Product.ProductID == product_id)
    )

    if not include_inactive:
        query = query.filter(Product.IsActive.is_(True))

    return query.first()


def get_product_by_name(
    db: Session,
    product_name: str,
) -> Product | None:
    """Check all products, including inactive products, for duplicates."""

    normalized_name = product_name.strip().lower()

    return (
        db.query(Product)
        .filter(
            func.lower(Product.ProductName) == normalized_name
        )
        .first()
    )


def get_all_products(
    db: Session,
    include_inactive: bool = False,
) -> list[Product]:
    query = db.query(Product)

    if not include_inactive:
        query = query.filter(Product.IsActive.is_(True))

    return (
        query
        .order_by(Product.ProductID)
        .all()
    )


def search_products(
    db: Session,
    name: str | None = None,
    category_id: int | None = None,
) -> list[Product]:
    query = db.query(Product).filter(
        Product.IsActive.is_(True)
    )

    if name:
        query = query.filter(
            Product.ProductName.ilike(
                f"%{name.strip()}%"
            )
        )

    if category_id is not None:
        query = query.filter(
            Product.CategoryID == category_id
        )

    return (
        query
        .order_by(Product.ProductID)
        .all()
    )
