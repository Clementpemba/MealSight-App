from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

from app.schemas.base import BaseSchema


class DailyNutritionBase(BaseSchema):
    """Base daily nutrition schema."""
    
    child_id: int
    date: date
    total_calories: Decimal = Field(default=0, ge=0)
    total_protein_g: Decimal = Field(default=0, ge=0)
    total_carbs_g: Decimal = Field(default=0, ge=0)
    total_fat_g: Decimal = Field(default=0, ge=0)
    total_fiber_g: Decimal = Field(default=0, ge=0)
    meals_count: int = Field(default=0, ge=0)
    nutrition_score: Optional[int] = Field(None, ge=0, le=100)
    recommendations: Optional[str] = None


class DailyNutritionCreate(DailyNutritionBase):
    """Daily nutrition creation schema."""
    pass


class DailyNutritionUpdate(BaseSchema):
    """Daily nutrition update schema."""
    
    total_calories: Optional[Decimal] = Field(None, ge=0)
    total_protein_g: Optional[Decimal] = Field(None, ge=0)
    total_carbs_g: Optional[Decimal] = Field(None, ge=0)
    total_fat_g: Optional[Decimal] = Field(None, ge=0)
    total_fiber_g: Optional[Decimal] = Field(None, ge=0)
    meals_count: Optional[int] = Field(None, ge=0)
    nutrition_score: Optional[int] = Field(None, ge=0, le=100)
    recommendations: Optional[str] = None


class DailyNutritionResponse(BaseSchema):
    """Daily nutrition response schema."""
    
    id: int
    child_id: int
    date: date
    total_calories: Decimal
    total_protein_g: Decimal
    total_carbs_g: Decimal
    total_fat_g: Decimal
    total_fiber_g: Decimal
    meals_count: int
    nutrition_score: Optional[int] = None
    recommendations: Optional[str] = None
    created_at: datetime


class WeeklyNutritionSummary(BaseSchema):
    """Weekly nutrition summary."""
    
    child_id: int
    start_date: date
    end_date: date
    avg_calories: Decimal
    avg_protein_g: Decimal
    avg_carbs_g: Decimal
    avg_fat_g: Decimal
    total_meals: int
    avg_nutrition_score: Optional[Decimal] = None
