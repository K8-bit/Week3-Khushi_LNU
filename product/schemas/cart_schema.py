from decimal import Decimal

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
)


class CartItemCreate(BaseModel):
    product_id: int = Field(
        ...,
        gt=0,
        validation_alias=AliasChoices(
            "product_id",
            "ProductID",
        ),
    )

    quantity: int = Field(
        ...,
        gt=0,
        validation_alias=AliasChoices(
            "quantity",
            "Quantity",
        ),
    )

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


class CartItemUpdate(BaseModel):
    quantity: int = Field(
        ...,
        gt=0,
        validation_alias=AliasChoices(
            "quantity",
            "Quantity",
        ),
    )

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


class CartItemResponse(BaseModel):
    cart_item_id: int = Field(
        ...,
        validation_alias=AliasChoices(
            "cart_item_id",
            "CartItemID",
        ),
    )

    user_id: int = Field(
        ...,
        validation_alias=AliasChoices(
            "user_id",
            "UserID",
        ),
    )

    product_id: int = Field(
        ...,
        validation_alias=AliasChoices(
            "product_id",
            "ProductID",
        ),
    )

    quantity: int = Field(
        ...,
        validation_alias=AliasChoices(
            "quantity",
            "Quantity",
        ),
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class CartSummaryItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal


class CartSummary(BaseModel):
    user_id: int
    items: list[CartSummaryItem]
    total_amount: Decimal
