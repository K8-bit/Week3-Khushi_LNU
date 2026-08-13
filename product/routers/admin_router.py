from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from product.db.session import get_db
from product.models.category import Category
from product.models.order import Order
from product.models.product import Product
from product.models.user import User
from product.schemas.admin_schema import (
    AdminCategoryCreate,
    AdminCategoryUpdate,
    AdminProductCreate,
    AdminProductUpdate,
)
from product.schemas.user_schema import UserResponse, UserRoleUpdate
from product.services import user_service
from product.utils.auth_dependencies import get_current_user
from product.schemas.user_schema import (
    UserResponse,
    UserRoleUpdate,
)

from product.services import user_service

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


def get_user_role(user: User) -> str:
    """
    Supports the project's uppercase Role field and also supports
    lowercase role fields if they are used later.
    """

    role = getattr(
        user,
        "Role",
        getattr(user, "role", "customer"),
    )

    return str(role).strip().lower()


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Allow only users with the admin role."""

    if get_user_role(current_user) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


def require_order_staff(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Admin, support, and operations users can view all orders.
    """

    allowed_roles = {
        "admin",
        "support",
        "operations",
    }

    if get_user_role(current_user) not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or support access required",
        )

    return current_user


def product_to_response(product: Product) -> dict[str, Any]:
    """Convert a Product model to a safe API response."""

    return {
        "product_id": product.ProductID,
        "product_name": product.ProductName,
        "description": product.Description,
        "price": product.Price,
        "available_quantity": product.AvailableQuantity,
        "category_id": product.CategoryID,
        "is_active": getattr(product, "IsActive", True),
    }


def category_to_response(category: Category) -> dict[str, Any]:
    """Convert a Category model to a safe API response."""

    return {
        "category_id": category.CategoryID,
        "category_name": category.CategoryName,
        "is_active": getattr(category, "IsActive", True),
    }


@router.post(
    "/products",
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: AdminProductCreate,
    db: Session = Depends(get_db),
    _admin_user: User = Depends(require_admin),
):
    """Create a new product. Admin users only."""

    product_name = product_data.product_name.strip()

    existing_product = (
        db.query(Product)
        .filter(Product.ProductName == product_name)
        .first()
    )

    if existing_product is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with this name already exists",
        )

    category = (
        db.query(Category)
        .filter(
            Category.CategoryID == product_data.category_id,
        )
        .first()
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    product = Product(
        ProductName=product_name,
        Description=product_data.description,
        Price=Decimal(product_data.price),
        AvailableQuantity=product_data.available_quantity,
        CategoryID=product_data.category_id,
    )

    # This works if IsActive has been added to the Product model.
    if hasattr(Product, "IsActive"):
        setattr(product, "IsActive", True)

    try:
        db.add(product)
        db.commit()
        db.refresh(product)

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create product",
        ) from error

    return product_to_response(product)


@router.put(
    "/products/{product_id}",
)
def update_product(
    product_data: AdminProductUpdate,
    product_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    _admin_user: User = Depends(require_admin),
):
    """Update an existing product. Admin users only."""

    product = (
        db.query(Product)
        .filter(Product.ProductID == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if product_data.product_name is not None:
        new_name = product_data.product_name.strip()

        duplicate_product = (
            db.query(Product)
            .filter(
                Product.ProductName == new_name,
                Product.ProductID != product_id,
            )
            .first()
        )

        if duplicate_product is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product with this name already exists",
            )

        product.ProductName = new_name

    if product_data.description is not None:
        product.Description = product_data.description

    if product_data.price is not None:
        product.Price = Decimal(product_data.price)

    if product_data.available_quantity is not None:
        product.AvailableQuantity = product_data.available_quantity

    if product_data.category_id is not None:
        category = (
            db.query(Category)
            .filter(
                Category.CategoryID == product_data.category_id,
            )
            .first()
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        product.CategoryID = product_data.category_id

    try:
        db.commit()
        db.refresh(product)

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update product",
        ) from error

    return product_to_response(product)


@router.delete(
    "/products/{product_id}",
)
def deactivate_product(
    product_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    _admin_user: User = Depends(require_admin),
):
    """
    Deactivate a product.

    If the Product model has IsActive, a soft delete is performed.
    Otherwise, the product is physically deleted.
    """

    product = (
        db.query(Product)
        .filter(Product.ProductID == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    try:
        if hasattr(Product, "IsActive"):
            setattr(product, "IsActive", False)
            message = "Product deactivated successfully"
        else:
            db.delete(product)
            message = "Product deleted successfully"

        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to deactivate product",
        ) from error

    return {
        "message": message,
        "product_id": product_id,
    }


@router.post(
    "/categories",
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: AdminCategoryCreate,
    db: Session = Depends(get_db),
    _admin_user: User = Depends(require_admin),
):
    """Create a new category. Admin users only."""

    category_name = category_data.category_name.strip()

    existing_category = (
        db.query(Category)
        .filter(Category.CategoryName == category_name)
        .first()
    )

    if existing_category is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this name already exists",
        )

    category = Category(
        CategoryName=category_name,
    )

    if hasattr(Category, "IsActive"):
        setattr(category, "IsActive", True)

    try:
        db.add(category)
        db.commit()
        db.refresh(category)

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create category",
        ) from error

    return category_to_response(category)


@router.put(
    "/categories/{category_id}",
)
def update_category(
    category_data: AdminCategoryUpdate,
    category_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    _admin_user: User = Depends(require_admin),
):
    """Update a category. Admin users only."""

    category = (
        db.query(Category)
        .filter(Category.CategoryID == category_id)
        .first()
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    category_name = category_data.category_name.strip()

    duplicate_category = (
        db.query(Category)
        .filter(
            Category.CategoryName == category_name,
            Category.CategoryID != category_id,
        )
        .first()
    )

    if duplicate_category is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this name already exists",
        )

    category.CategoryName = category_name

    try:
        db.commit()
        db.refresh(category)

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update category",
        ) from error

    return category_to_response(category)


@router.get(
    "/orders",
)
def get_all_orders(
    db: Session = Depends(get_db),
    _staff_user: User = Depends(require_order_staff),
):
    """
    View all orders.

    Allowed roles:
    - admin
    - support
    - operations
    """

    orders = (
        db.query(Order)
        .order_by(Order.OrderDate.desc())
        .all()
    )

    return [
        {
            "order_id": order.OrderID,
            "user_id": order.UserID,
            "payment_method": order.PaymentMethod,
            "total_amount": order.TotalAmount,
            "order_date": order.OrderDate,
        }
        for order in orders
    ]



@router.patch(
    "/users/{user_id}/role",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user_role(
    role_data: UserRoleUpdate,
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
) -> User:
    """
    Change a user's role.

    Only an existing administrator can use this endpoint.
    """

    try:
        return user_service.update_user_role(
            db=db,
            user_id=user_id,
            role=role_data.role,
            acting_admin_id=current_admin.UserID,
        )

    except ValueError as error:
        message = str(error).lower()

        if "not found" in message:
            error_status = status.HTTP_404_NOT_FOUND
        elif (
            "admin" in message
            or "remain" in message
            or "invalid role" in message
        ):
            error_status = status.HTTP_409_CONFLICT
        else:
            error_status = status.HTTP_400_BAD_REQUEST

        raise HTTPException(
            status_code=error_status,
            detail=str(error),
        ) from error