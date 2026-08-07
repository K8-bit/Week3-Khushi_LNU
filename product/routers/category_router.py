from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.schemas.category_schema import CategoryCreate, CategoryResponse
from product.services import category_service


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

#Create
@router.post(
    "",
    response_model=CategoryResponse,
    status_code=201,
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    try:
        return category_service.create_category(
            db=db,
            category_data=category,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

#Read
@router.get(
    "",
    response_model=list[CategoryResponse],
)
def get_categories(
    db: Session = Depends(get_db),
):
    return category_service.get_all_categories(db)
