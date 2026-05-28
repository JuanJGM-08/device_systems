from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal


class UserBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[Literal["admin", "support", "user"]] = None
    is_active: Optional[bool] = None