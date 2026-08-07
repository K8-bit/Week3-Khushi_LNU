from sqlalchemy.orm import Session

from product.models.category import Category
from product.repositories import category_repository
from product.schemas.category_schema import CategoryCreate


def create_category(
    db: Session,
    category_data: CategoryCreate,
) -> Category:
    category_name = category_data.category_name.strip()

    existing_category = category_repository.get_category_by_name(
        db=db,
        category_name=category_name,
    )

    if existing_category:
        raise ValueError("Category already exists")

    category = Category(CategoryName=category_name)

    return category_repository.create_category(
        db=db,
        category=category,
    )


def get_all_categories(db: Session) -> list[Category]:
    return category_repository.get_all_categories(db=db)


def get_category_by_id(
    db: Session,
    category_id: int,
) -> Category | None:
    return category_repository.get_category_by_id(
        db=db,
        category_id=category_id,
    )
