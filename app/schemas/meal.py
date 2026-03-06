from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time, datetime
from decimal import Decimal

from app.schemas.base import BaseSchema


# ============================================================================
# MEAL FOOD SCHEMAS
# ============================================================================

class MealFoodBase(BaseSchema):
    """Base meal food schema."""
    
    food_name: str = Field(..., min_length=1, max_length=255)
    food_id: Optional[int] = None
    portion_size_g: Optional[Decimal] = Field(None, ge=0)
    confidence_score: Optional[Decimal] = Field(None, ge=0, le=1)
    calories: Optional[Decimal] = Field(None, ge=0)
    protein_g: Optional[Decimal] = Field(None, ge=0)
    carbs_g: Optional[Decimal] = Field(None, ge=0)
    fat_g: Optional[Decimal] = Field(None, ge=0)


class MealFoodCreate(MealFoodBase):
    """Meal food creation schema."""
    pass


class MealFoodResponse(MealFoodBase):
    """Meal food response schema."""
    
    id: int
    meal_id: int
    created_at: datetime


# ============================================================================
# MEAL SCHEMAS
# ============================================================================

class MealBase(BaseSchema):
    """Base meal schema."""
    
    child_id: int
    meal_type: Optional[str] = Field(None, pattern="^(breakfast|lunch|dinner|snack)$")
    meal_date: Optional[date] = None
    meal_time: Optional[time] = None
    notes: Optional[str] = None


class MealCreate(MealBase):
    """Meal creation schema."""
    
    foods: Optional[List[MealFoodCreate]] = []


class MealUpdate(BaseSchema):
    """Meal update schema."""
    
    meal_type: Optional[str] = Field(None, pattern="^(breakfast|lunch|dinner|snack)$")
    meal_date: Optional[date] = None
    meal_time: Optional[time] = None
    notes: Optional[str] = None
    total_calories: Optional[Decimal] = Field(None, ge=0)
    total_protein_g: Optional[Decimal] = Field(None, ge=0)
    total_carbs_g: Optional[Decimal] = Field(None, ge=0)
    total_fat_g: Optional[Decimal] = Field(None, ge=0)
    nutrition_score: Optional[int] = Field(None, ge=0, le=100)
    ai_feedback: Optional[str] = None


class MealSummary(BaseSchema):
    """Meal summary for nested responses."""
    
    id: int
    meal_type: Optional[str] = None
    meal_date: date
    meal_time: Optional[time] = None
    total_calories: Optional[Decimal] = None
    nutrition_score: Optional[int] = None


class MealResponse(BaseSchema):
    """Meal response schema."""
    
    id: int
    child_id: int
    user_id: int
    meal_type: Optional[str] = None
    image_url_before: Optional[str] = None
    image_url_after: Optional[str] = None
    meal_date: date
    meal_time: Optional[time] = None
    total_calories: Optional[Decimal] = None
    total_protein_g: Optional[Decimal] = None
    total_carbs_g: Optional[Decimal] = None
    total_fat_g: Optional[Decimal] = None
    nutrition_score: Optional[int] = None
    ai_feedback: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime


class MealWithFoodsResponse(MealResponse):
    """Meal response with identified foods."""
    
    meal_foods: List[MealFoodResponse] = []
