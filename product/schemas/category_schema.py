from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class CategoryCreate(BaseModel):
    category_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        validation_alias=AliasChoices(
            "category_name",
            "CategoryName",
        ),
    )

    @field_validator("category_name")
    @classmethod
    def validate_category_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Category name is required")

        return value.title()

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


class CategoryUpdate(BaseModel):
    category_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        validation_alias=AliasChoices(
            "category_name",
            "CategoryName",
        ),
    )

    @field_validator("category_name")
    @classmethod
    def validate_category_name(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Category name cannot be empty")

        return value.title()

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


class CategoryResponse(BaseModel):
    category_id: int = Field(
        ...,
        validation_alias=AliasChoices(
            "category_id",
            "CategoryID",
        ),
    )

    category_name: str = Field(
        ...,
        validation_alias=AliasChoices(
            "category_name",
            "CategoryName",
        ),
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
