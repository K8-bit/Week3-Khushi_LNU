import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    status,
)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.models.user import User
from product.schemas.category_schema import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from product.services import category_service
from product.utils.auth_dependencies import get_current_user


logger = logging.getLogger("shopping.categories")


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


admin_router = APIRouter(
    prefix="/admin/categories",
    tags=["Admin Categories"],
)


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    role = str(
        getattr(current_user, "Role", "customer")
    ).lower()

    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )

    return current_user


@router.get(
    "",
    response_model=list[CategoryResponse],
)
def get_categories(
    db: Session = Depends(get_db),
):
    return category_service.get_all_categories(db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    category = category_service.get_category_by_id(
        db=db,
        category_id=category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


@admin_router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    try:
        return category_service.create_category(
            db=db,
            category_data=category_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    except IntegrityError as error:
        logger.exception("category_create_integrity_error")

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists",
        ) from error

    except SQLAlchemyError as error:
        logger.exception("category_create_database_error")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create category",
        ) from error

