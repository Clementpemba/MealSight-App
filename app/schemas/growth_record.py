from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

from app.schemas.base import BaseSchema


class GrowthRecordBase(BaseSchema):
    """Base growth record schema."""
    
    child_id: int
    recorded_date: Optional[date] = None
    height_cm: Optional[Decimal] = Field(None, ge=0)
    weight_kg: Optional[Decimal] = Field(None, ge=0)
    head_circumference_cm: Optional[Decimal] = Field(None, ge=0)
    muac_cm: Optional[Decimal] = Field(None, ge=0, description="Mid-Upper Arm Circumference")
    notes: Optional[str] = None


class GrowthRecordCreate(GrowthRecordBase):
    """Growth record creation schema."""
    pass


class GrowthRecordUpdate(BaseSchema):
    """Growth record update schema."""
    
    recorded_date: Optional[date] = None
    height_cm: Optional[Decimal] = Field(None, ge=0)
    weight_kg: Optional[Decimal] = Field(None, ge=0)
    head_circumference_cm: Optional[Decimal] = Field(None, ge=0)
    muac_cm: Optional[Decimal] = Field(None, ge=0)
    notes: Optional[str] = None


class GrowthRecordResponse(BaseSchema):
    """Growth record response schema."""
    
    id: int
    child_id: int
    recorded_date: date
    height_cm: Optional[Decimal] = None
    weight_kg: Optional[Decimal] = None
    head_circumference_cm: Optional[Decimal] = None
    muac_cm: Optional[Decimal] = None
    notes: Optional[str] = None
    created_at: datetime


class GrowthTrendResponse(BaseSchema):
    """Growth trend data for charts."""
    
    child_id: int
    records: list[GrowthRecordResponse]
    height_trend: Optional[str] = None  # increasing, stable, decreasing
    weight_trend: Optional[str] = None
