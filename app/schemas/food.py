from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

from app.schemas.base import BaseSchema


class FoodBase(BaseSchema):
    """Base food schema."""
    
    name: str = Field(..., min_length=1, max_length=255)
    local_name: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    calories_per_100g: Optional[Decimal] = Field(None, ge=0)
    protein_g: Optional[Decimal] = Field(None, ge=0)
    carbohydrates_g: Optional[Decimal] = Field(None, ge=0)
    fat_g: Optional[Decimal] = Field(None, ge=0)
    fiber_g: Optional[Decimal] = Field(None, ge=0)
    vitamin_a_mcg: Optional[Decimal] = Field(None, ge=0)
    vitamin_c_mg: Optional[Decimal] = Field(None, ge=0)
    iron_mg: Optional[Decimal] = Field(None, ge=0)
    calcium_mg: Optional[Decimal] = Field(None, ge=0)
    zinc_mg: Optional[Decimal] = Field(None, ge=0)
    image_url: Optional[str] = None


class FoodCreate(FoodBase):
    """Food creation schema."""
    pass


class FoodUpdate(BaseSchema):
    """Food update schema."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    local_name: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    calories_per_100g: Optional[Decimal] = Field(None, ge=0)
    protein_g: Optional[Decimal] = Field(None, ge=0)
    carbohydrates_g: Optional[Decimal] = Field(None, ge=0)
    fat_g: Optional[Decimal] = Field(None, ge=0)
    fiber_g: Optional[Decimal] = Field(None, ge=0)
    vitamin_a_mcg: Optional[Decimal] = Field(None, ge=0)
    vitamin_c_mg: Optional[Decimal] = Field(None, ge=0)
    iron_mg: Optional[Decimal] = Field(None, ge=0)
    calcium_mg: Optional[Decimal] = Field(None, ge=0)
    zinc_mg: Optional[Decimal] = Field(None, ge=0)
    image_url: Optional[str] = None


class FoodResponse(BaseSchema):
    """Food response schema."""
    
    id: int
    name: str
    local_name: Optional[str] = None
    category: Optional[str] = None
    calories_per_100g: Optional[Decimal] = None
    protein_g: Optional[Decimal] = None
    carbohydrates_g: Optional[Decimal] = None
    fat_g: Optional[Decimal] = None
    fiber_g: Optional[Decimal] = None
    vitamin_a_mcg: Optional[Decimal] = None
    vitamin_c_mg: Optional[Decimal] = None
    iron_mg: Optional[Decimal] = None
    calcium_mg: Optional[Decimal] = None
    zinc_mg: Optional[Decimal] = None
    image_url: Optional[str] = None
    created_at: datetime


class FoodSummary(BaseSchema):
    """Food summary for search results."""
    
    id: int
    name: str
    local_name: Optional[str] = None
    category: Optional[str] = None
    calories_per_100g: Optional[Decimal] = None
