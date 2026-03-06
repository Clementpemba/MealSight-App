from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class NutritionAlert(Base):
    """
    Alerts and notifications for nutrition issues.
    """
    __tablename__ = "nutrition_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    child_id = Column(Integer, ForeignKey("children.id", ondelete="CASCADE"), nullable=True, index=True)
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=True)  # low, medium, high, critical
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="nutrition_alerts")
    child = relationship("Child", back_populates="nutrition_alerts")
    
    def __repr__(self):
        return f"<NutritionAlert(id={self.id}, title={self.title})>"
