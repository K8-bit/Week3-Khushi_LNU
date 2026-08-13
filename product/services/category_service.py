from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from product.models.category import Category
from product.repositories import category_repository
from product.schemas.category_schema import CategoryCreate


def create_category(
    db: Session,
    category_data: CategoryCreate,
) -> Category:
    """Create a category for an authorized administrator."""

    category_name = category_data.category_name.strip()

    if not category_name:
        raise ValueError("Category name is required")

    existing_category = category_repository.get_category_by_name(
        db=db,
        category_name=category_name,
    )

    if existing_category is not None:
        raise ValueError("Category already exists")

    category = Category(
        CategoryName=category_name,
    )

    try:
        return category_repository.create_category(
            db=db,
            category=category,
        )
    except IntegrityError as error:
        db.rollback()
        raise ValueError("Category already exists") from error


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



# def update_category(
#     db: Session,
#     category_id: int,
#     category_data: CategoryUpdate,
# ) -> Category:
#     category = category_repository.get_category_by_id(
#         db=db,
#         category_id=category_id,
#     )

#     if category is None:
#         raise ValueError("Category not found")

#     if category_data.category_name is not None:
#         category_name = category_data.category_name.strip()

#         existing_category = (
#             category_repository.get_category_by_name(
#                 db=db,
#                 category_name=category_name,
#             )
#         )

#         if (
#             existing_category is not None
#             and existing_category.CategoryID != category_id
#         ):
#             raise ValueError("Category already exists")

#         category.CategoryName = category_name

#     return category_repository.update_category(
#         db=db,
#         category=category,
#     )
