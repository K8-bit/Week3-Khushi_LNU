from sqlalchemy.orm import Session

from product.models.category import Category


def create_category(db: Session, category: Category) -> Category:
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


#Get operation by id
def get_category_by_id(
    db: Session,
    category_id: int,
) -> Category | None:
    return (
        db.query(Category)
        .filter(Category.CategoryID == category_id)
        .first()
    )

#Get operation by name
def get_category_by_name(
    db: Session,
    category_name: str,
) -> Category | None:
    return (
        db.query(Category)
        .filter(Category.CategoryName == category_name)
        .first()
    )

#Get operation by categories
def get_all_categories(db: Session) -> list[Category]:
    return (
        db.query(Category)
        .order_by(Category.CategoryID)
        .all()
    )

