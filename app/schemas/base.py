from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields."""
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PaginationParams(BaseModel):
    """Pagination parameters."""
    
    skip: int = 0
    limit: int = 100
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    
    total: int
    skip: int
    limit: int
    items: list
