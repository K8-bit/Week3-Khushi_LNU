from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):  #Request Model
    category_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )


class CategoryResponse(BaseModel):  #Response Model
    category_id: int = Field(
        validation_alias="CategoryID",
    )

    category_name: str = Field(
        validation_alias="CategoryName",
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
