from sqlalchemy.orm import Session

from product.models.product import Product


def create_product(db: Session, product: Product) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product_by_id(
    db: Session,
    product_id: int,
) -> Product | None:
    return (
        db.query(Product)
        .filter(Product.ProductID == product_id)
        .first()
    )


def get_product_by_name(
    db: Session,
    product_name: str,
) -> Product | None:
    return (
        db.query(Product)
        .filter(Product.ProductName == product_name)
        .first()
    )


def get_all_products(db: Session) -> list[Product]:
    return (
        db.query(Product)
        .order_by(Product.ProductID)
        .all()
    )


def search_products(
    db: Session,
    name: str | None = None,
    category_id: int | None = None,
) -> list[Product]:
    query = db.query(Product)

    if name:
        query = query.filter(
            Product.ProductName.ilike(f"%{name.strip()}%")
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
