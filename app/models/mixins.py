from datetime import datetime
from sqlalchemy import Column, Integer, DateTime


class TimestampMixin:
    """Mixin that adds created_at and updated_at columns."""
    
    created_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        nullable=False
    )
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )


class SoftDeleteMixin:
    """Mixin that adds soft delete functionality."""
    
    deleted_at = Column(DateTime, nullable=True)
    
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
