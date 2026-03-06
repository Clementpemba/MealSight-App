from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from decimal import Decimal

from app.schemas.base import BaseSchema, TimestampSchema


class ChildBase(BaseSchema):
    """Base child schema."""
    
    name: str = Field(..., min_length=1, max_length=255)
    date_of_birth: date
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    height_cm: Optional[Decimal] = Field(None, ge=0)
    weight_kg: Optional[Decimal] = Field(None, ge=0)


class ChildCreate(ChildBase):
    """Child creation schema."""
    pass


class ChildUpdate(BaseSchema):
    """Child update schema."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    height_cm: Optional[Decimal] = Field(None, ge=0)
    weight_kg: Optional[Decimal] = Field(None, ge=0)
    profile_image_url: Optional[str] = None
    nutrition_status: Optional[str] = None


class ChildSummary(BaseSchema):
    """Child summary for nested responses."""
    
    id: int
    name: str
    date_of_birth: date
    gender: Optional[str] = None
    nutrition_status: Optional[str] = "unknown"


class ChildResponse(TimestampSchema):
    """Child response schema."""
    
    id: int
    user_id: int
    name: str
    date_of_birth: date
    gender: Optional[str] = None
    profile_image_url: Optional[str] = None
    height_cm: Optional[Decimal] = None
    weight_kg: Optional[Decimal] = None
    nutrition_status: Optional[str] = "unknown"


class ChildWithMealsResponse(ChildResponse):
    """Child response with recent meals."""
    
    meals: List["MealSummary"] = []


# Forward reference
from app.schemas.meal import MealSummary  # noqa
ChildWithMealsResponse.model_rebuild()
