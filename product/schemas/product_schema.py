from decimal import Decimal

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
)


class ProductCreate(BaseModel):
    product_name: str = Field(
        ...,
        min_length=1,
        max_length=150,
        validation_alias=AliasChoices(
            "product_name",
            "ProductName",
        ),
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        validation_alias=AliasChoices(
            "description",
            "Description",
        ),
    )
    category_id: int = Field(
        ...,
        gt=0,
        validation_alias=AliasChoices(
            "category_id",
            "CategoryID",
        ),
    )
    price: Decimal = Field(
        ...,
        gt=0,
        max_digits=10,
        decimal_places=2,
        validation_alias=AliasChoices("price", "Price"),
    )
    available_quantity: int = Field(
        ...,
        ge=0,
        validation_alias=AliasChoices(
            "available_quantity",
            "AvailableQuantity",
        ),
    )
    product_url: HttpUrl | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "product_url",
            "ProductUrl",
        ),
    )

    @field_validator("product_name")
    @classmethod
    def normalize_product_name(cls, value: str) -> str:
        return value.strip().title()

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: Decimal) -> Decimal:
        if value > Decimal("999999.99"):
            raise ValueError("Price cannot exceed 999,999.99")

        return value

    model_config = ConfigDict(populate_by_name=True)


class ProductUpdate(BaseModel):
    product_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
        validation_alias=AliasChoices(
            "product_name",
            "ProductName",
        ),
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        validation_alias=AliasChoices(
            "description",
            "Description",
        ),
    )
    category_id: int | None = Field(
        default=None,
        gt=0,
        validation_alias=AliasChoices(
            "category_id",
            "CategoryID",
        ),
    )
    price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
        validation_alias=AliasChoices("price", "Price"),
    )
    available_quantity: int | None = Field(
        default=None,
        ge=0,
        validation_alias=AliasChoices(
            "available_quantity",
            "AvailableQuantity",
        ),
    )
    product_url: HttpUrl | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "product_url",
            "ProductUrl",
        ),
    )

    @field_validator("product_name")
    @classmethod
    def normalize_product_name(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return value.strip().title()

    model_config = ConfigDict(populate_by_name=True)


class ProductResponse(BaseModel):
    product_id: int = Field(
        ...,
        validation_alias=AliasChoices(
            "product_id",
            "ProductID",
        ),
    )
    product_name: str = Field(
        ...,
        validation_alias=AliasChoices(
            "product_name",
            "ProductName",
        ),
    )
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "description",
            "Description",
        ),
    )
    category_id: int = Field(
        ...,
        validation_alias=AliasChoices(
            "category_id",
            "CategoryID",
        ),
    )
    price: Decimal = Field(
        ...,
        validation_alias=AliasChoices("price", "Price"),
    )
    available_quantity: int = Field(
        ...,
        validation_alias=AliasChoices(
            "available_quantity",
            "AvailableQuantity",
        ),
    )
    product_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "product_url",
            "ProductUrl",
        ),
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
