from pydantic import AliasChoices, BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    mobile: str = Field(..., min_length=10, max_length=15)


class UserResponse(BaseModel):
    user_id: int = Field(validation_alias=AliasChoices("user_id", "UserID"))
    name: str = Field(validation_alias=AliasChoices("name", "Name"))
    email: EmailStr = Field(validation_alias=AliasChoices("email", "Email"))
    mobile: str = Field(validation_alias=AliasChoices("mobile", "Mobile"))

    model_config = ConfigDict(from_attributes=True)  #orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class LoginResponse(BaseModel):
    message: str
    user_id: int
    name: str
    email: EmailStr
