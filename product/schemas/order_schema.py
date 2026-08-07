from datetime import datetime
from decimal import Decimal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator


VALID_PAYMENT_METHODS = frozenset(
    {
        "card",
        "cash",
        "cash_on_delivery",
        "paypal",
        "upi",
    }
)


class OrderCreate(BaseModel):
    user_id: int = Field(
        ...,
        gt=0,
        validation_alias=AliasChoices("user_id", "UserID"),
    )
    payment_method: str = Field(
        ...,
        min_length=1,
        max_length=50,
        validation_alias=AliasChoices(
            "payment_method",
            "PaymentMethod",
        ),
    )

    @field_validator("payment_method")
    @classmethod
    def validate_payment_method(cls, value: str) -> str:
        normalized_value = value.strip().lower()

        if normalized_value not in VALID_PAYMENT_METHODS:
            valid_methods = ", ".join(sorted(VALID_PAYMENT_METHODS))
            raise ValueError(
                f"Payment method must be one of: {valid_methods}"
            )

        return normalized_value

    model_config = ConfigDict(populate_by_name=True)


class OrderDetailResponse(BaseModel):
    order_detail_id: int = Field(
        ...,
        validation_alias=AliasChoices(
            "order_detail_id",
            "OrderDetailID",
        ),
    )
    order_id: int = Field(
        ...,
        validation_alias=AliasChoices("order_id", "OrderID"),
    )
    product_id: int = Field(
        ...,
        validation_alias=AliasChoices("product_id", "ProductID"),
    )
    quantity: int = Field(
        ...,
        gt=0,
        validation_alias=AliasChoices("quantity", "Quantity"),
    )
    price: Decimal = Field(
        ...,
        gt=0,
        validation_alias=AliasChoices("price", "Price"),
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class OrderFields(BaseModel):
    order_id: int = Field(
        ...,
        validation_alias=AliasChoices("order_id", "OrderID"),
    )
    user_id: int = Field(
        ...,
        validation_alias=AliasChoices("user_id", "UserID"),
    )
    order_date: datetime = Field(
        ...,
        validation_alias=AliasChoices("order_date", "OrderDate"),
    )
    payment_method: str = Field(
        ...,
        validation_alias=AliasChoices(
            "payment_method",
            "PaymentMethod",
        ),
    )
    total_amount: Decimal = Field(
        ...,
        ge=0,
        validation_alias=AliasChoices(
            "total_amount",
            "TotalAmount",
        ),
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class OrderHistoryResponse(OrderFields):
    pass


class OrderResponse(OrderFields):
    order_details: list[OrderDetailResponse] = Field(
        default_factory=list,
        validation_alias=AliasChoices(
            "order_details",
            "OrderDetails",
        ),
    )
