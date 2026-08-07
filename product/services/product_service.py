from sqlalchemy.orm import Session

from product.models.category import Category
from product.models.product import Product
from product.repositories import product_repository
from product.schemas.product_schema import ProductCreate


def create_product(
    db: Session,
    product_data: ProductCreate,
) -> Product:
    category = (
        db.query(Category)
        .filter(
            Category.CategoryID == product_data.category_id
        )
        .first()
    )

    if category is None:
        raise ValueError("Category not found")

    existing_product = (
        product_repository.get_product_by_name(
            db=db,
            product_name=product_data.product_name,
        )
    )

    if existing_product is not None:
        raise ValueError("Product name already exists")

    product = Product(
        ProductName=product_data.product_name,
        Description=product_data.description,
        CategoryID=product_data.category_id,
        Price=product_data.price,
        AvailableQuantity=product_data.available_quantity,
        ProductUrl=(
            str(product_data.product_url)
            if product_data.product_url is not None
            else None
        ),
    )

    return product_repository.create_product(
        db=db,
        product=product,
    )


def get_product_by_id(
    db: Session,
    product_id: int,
) -> Product | None:
    return product_repository.get_product_by_id(
        db=db,
        product_id=product_id,
    )


def get_all_products(db: Session) -> list[Product]:
    return product_repository.get_all_products(db)


def search_products(
    db: Session,
    name: str | None = None,
    category_id: int | None = None,
) -> list[Product]:
    return product_repository.search_products(
        db=db,
        name=name,
        category_id=category_id,
    )
