from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, AliasChoices


UserRole = Literal[
    "customer",
    "admin",
    "support",
    "operations",
]


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    mobile: str = Field(..., min_length=7, max_length=20)

    model_config = ConfigDict(
        populate_by_name=True,
    )


class UserRoleUpdate(BaseModel):
    role: Literal[
        "customer",
        "admin",
        "support"
    ]
class UserResponse(BaseModel):
    user_id: int = Field(validation_alias="UserID")
    name: str = Field(validation_alias="Name")
    email: EmailStr = Field(validation_alias="Email")
    mobile: str = Field(validation_alias="Mobile")
    role: UserRole = Field(
        default="customer",
        validation_alias="Role",
    )
    is_active: bool = Field(
        default=True,
        validation_alias="IsActive",
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class UserLogin(BaseModel):
    email: EmailStr = Field(
        ...,
        validation_alias=AliasChoices("email", "Email"),
    )

    password: str = Field(
        ...,
        min_length=1,
        validation_alias=AliasChoices("password", "Password"),
    )

    model_config = ConfigDict(
        populate_by_name=True,
    )

class LoginResponse(BaseModel):
    message: str
    user_id: int
    name: str
    email: EmailStr
    role: UserRole
