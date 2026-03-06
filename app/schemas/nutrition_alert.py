from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.schemas.base import BaseSchema


class NutritionAlertBase(BaseSchema):
    """Base nutrition alert schema."""
    
    child_id: Optional[int] = None
    alert_type: str = Field(..., max_length=50)
    severity: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    title: str = Field(..., max_length=255)
    message: str


class NutritionAlertCreate(NutritionAlertBase):
    """Nutrition alert creation schema."""
    pass


class NutritionAlertUpdate(BaseSchema):
    """Nutrition alert update schema."""
    
    is_read: Optional[bool] = None


class NutritionAlertResponse(BaseSchema):
    """Nutrition alert response schema."""
    
    id: int
    user_id: int
    child_id: Optional[int] = None
    alert_type: str
    severity: Optional[str] = None
    title: str
    message: str
    is_read: bool
    created_at: datetime


class AlertStats(BaseSchema):
    """Alert statistics for a user."""
    
    total_alerts: int
    unread_count: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
