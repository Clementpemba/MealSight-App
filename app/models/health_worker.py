from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, date

from app.db.base import Base


class HealthWorker(Base):
    """
    Community health workers who monitor families.
    """
    __tablename__ = "health_workers"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    facility_name = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    assignments = relationship("HealthWorkerAssignment", back_populates="health_worker", lazy="selectin", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<HealthWorker(id={self.id}, email={self.email})>"


class HealthWorkerAssignment(Base):
    """
    Assignments linking health workers to families.
    """
    __tablename__ = "health_worker_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    health_worker_id = Column(Integer, ForeignKey("health_workers.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_date = Column(Date, default=date.today)
    is_active = Column(Boolean, default=True)
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('health_worker_id', 'user_id', name='uq_hw_assignment'),
    )
    
    # Relationships
    health_worker = relationship("HealthWorker", back_populates="assignments")
    user = relationship("User", back_populates="health_worker_assignments")
    
    def __repr__(self):
        return f"<HealthWorkerAssignment(id={self.id}, hw_id={self.health_worker_id}, user_id={self.user_id})>"
