from decimal import Decimal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class CartItemCreate(BaseModel):    #Request Model
    user_id: int = Field(
        ...,
        gt=0,
    )

    product_id: int = Field(
        ...,
        gt=0,
    )

    quantity: int = Field(
        ...,
        gt=0,
    )


class CartItemUpdate(BaseModel): 
    quantity: int = Field(
        ...,
        gt=0,
    )


class CartItemResponse(BaseModel):  #Response Model
    cart_item_id: int = Field(
        validation_alias=AliasChoices(
            "cart_item_id",
            "CartItemID",
        ),
    )

    user_id: int = Field(
        validation_alias=AliasChoices(
            "user_id",
            "UserID",
        ),
    )

    product_id: int = Field(
        validation_alias=AliasChoices(
            "product_id",
            "ProductID",
        ),
    )

    quantity: int = Field(
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
    items: list[CartSummaryItem] = Field(
        default_factory=list,
    )
    total_amount: Decimal
