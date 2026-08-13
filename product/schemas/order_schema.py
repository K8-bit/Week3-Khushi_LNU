from datetime import datetime
from decimal import Decimal

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class OrderCreate(BaseModel):
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
        value = value.strip()

        if not value:
            raise ValueError("Payment method is required")

        return value

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


class OrderBaseResponse(BaseModel):
    order_id: int = Field(
        ...,
        validation_alias=AliasChoices(
            "order_id",
            "OrderID",
        ),
    )

    user_id: int = Field(
        ...,
        validation_alias=AliasChoices(
            "user_id",
            "UserID",
        ),
    )

    order_date: datetime | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "order_date",
            "OrderDate",
        ),
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
        validation_alias=AliasChoices(
            "total_amount",
            "TotalAmount",
        ),
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class OrderResponse(OrderBaseResponse):
    pass


class OrderHistoryResponse(OrderBaseResponse):
    pass
