from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

from app.schemas.base import BaseSchema, TimestampSchema


class UserBase(BaseSchema):
    """Base user schema."""
    
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=255)


class UserCreate(UserBase):
    """User creation schema."""
    
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseSchema):
    """User update schema."""
    
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=255)
    profile_image_url: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(TimestampSchema):
    """User response schema."""
    
    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    profile_image_url: Optional[str] = None
    location: Optional[str] = None


class UserWithChildrenResponse(UserResponse):
    """User response with children list."""
    
    children: List["ChildSummary"] = []


# Forward reference for circular import
from app.schemas.child import ChildSummary  # noqa
UserWithChildrenResponse.model_rebuild()
