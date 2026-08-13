from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AdminProductCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    price: Decimal = Field(..., gt=0)
    available_quantity: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)


class AdminProductUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
    )
    price: Decimal | None = Field(
        default=None,
        gt=0,
    )
    available_quantity: int | None = Field(
        default=None,
        ge=0,
    )
    category_id: int | None = Field(
        default=None,
        gt=0,
    )


class AdminCategoryCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )


class AdminCategoryUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )
