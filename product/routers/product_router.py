from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.schemas.product_schema import ProductResponse
from product.services import product_service


router = APIRouter(
    prefix="/products",
    tags=["Customer Products"],
)


@router.get(
    "",
    response_model=list[ProductResponse],
    summary="Browse active products",
)
def get_products(
    db: Session = Depends(get_db),
):
    return product_service.get_all_products(db)


@router.get(
    "/search",
    response_model=list[ProductResponse],
    summary="Search active products",
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
    summary="View product details",
)
def get_product(
    product_id: int = Path(..., gt=0),
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
