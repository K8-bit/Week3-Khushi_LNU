from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.schemas.product_schema import ProductCreate, ProductResponse
from product.services import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),  #SQLAlchemy
):
    try:
        return product_service.create_product(
            db=db,
            product_data=product_data,
        )
    except ValueError as error:
        message = str(error)
        message_lower = message.lower()

        if "category" in message_lower:
            error_status = status.HTTP_404_NOT_FOUND
        elif "already exists" in message_lower:
            error_status = status.HTTP_409_CONFLICT
        else:
            error_status = status.HTTP_400_BAD_REQUEST

        raise HTTPException(
            status_code=error_status,
            detail=message,
        ) from error

#Retrieve the data
@router.get(   
    "",
    response_model=list[ProductResponse],
)
def get_products(
    db: Session = Depends(get_db),
):
    return product_service.get_all_products(db)


@router.get(
    "/search",
    response_model=list[ProductResponse],
)
def search_products(
    name: str | None = Query(
        default=None,
        description="Search by product name",
    ),
    category_id: int | None = Query(
        default=None,
        alias="category",
        gt=0,
        description="Filter by category ID",
    ),
    db: Session = Depends(get_db),
):
    return product_service.search_products(
        db=db,
        name=name,
        category_id=category_id,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    product = product_service.get_product_by_id(
        db=db,
        product_id=product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product
