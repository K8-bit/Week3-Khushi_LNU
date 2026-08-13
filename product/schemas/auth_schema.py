from typing import Literal

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """Response returned after successful authentication."""

    access_token: str = Field(..., description="JWT access token")
    token_type: Literal["bearer"] = Field(
        default="bearer",
        description="Authentication scheme",
    )



class TokenData(BaseModel):
    """Claims extracted from a validated JWT."""

    sub: str = Field(..., description="Authenticated user identifier")
    role: str = Field(default="customer", description="User role")
