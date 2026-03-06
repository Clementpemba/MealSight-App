from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, TYPE_CHECKING
from datetime import date, datetime

from app.schemas.base import BaseSchema

if TYPE_CHECKING:
    from app.schemas.user import UserResponse


# ============================================================================
# HEALTH WORKER SCHEMAS
# ============================================================================

class HealthWorkerBase(BaseSchema):
    """Base health worker schema."""
    
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    facility_name: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)


class HealthWorkerCreate(HealthWorkerBase):
    """Health worker creation schema."""
    
    password: str = Field(..., min_length=8, max_length=100)


class HealthWorkerUpdate(BaseSchema):
    """Health worker update schema."""
    
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    facility_name: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class HealthWorkerResponse(BaseSchema):
    """Health worker response schema."""
    
    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    facility_name: Optional[str] = None
    location: Optional[str] = None
    is_verified: bool
    created_at: datetime


# ============================================================================
# HEALTH WORKER ASSIGNMENT SCHEMAS
# ============================================================================

class AssignmentBase(BaseSchema):
    """Base assignment schema."""
    
    user_id: int


class AssignmentCreate(AssignmentBase):
    """Assignment creation schema."""
    pass


class AssignmentResponse(BaseSchema):
    """Assignment response schema."""
    
    id: int
    health_worker_id: int
    user_id: int
    assigned_date: date
    is_active: bool


class AssignmentWithUserResponse(AssignmentResponse):
    """Assignment with user details."""
    
    user: Optional["UserResponse"] = None


class HealthWorkerWithAssignmentsResponse(HealthWorkerResponse):
    """Health worker with their assignments."""
    
    assignments: List[AssignmentResponse] = []


# Rebuild models to resolve forward references
from app.schemas.user import UserResponse  # noqa
AssignmentWithUserResponse.model_rebuild()
