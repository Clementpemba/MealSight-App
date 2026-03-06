from sqlalchemy import Column, Integer, ForeignKey, Numeric, Date, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, date

from app.db.base import Base


class GrowthRecord(Base):
    """
    Child growth tracking over time (height, weight, MUAC).
    """
    __tablename__ = "growth_records"
    
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id", ondelete="CASCADE"), nullable=False, index=True)
    recorded_date = Column(Date, nullable=False, default=date.today, index=True)
    height_cm = Column(Numeric(5, 2), nullable=True)
    weight_kg = Column(Numeric(5, 2), nullable=True)
    head_circumference_cm = Column(Numeric(5, 2), nullable=True)
    muac_cm = Column(Numeric(5, 2), nullable=True)  # Mid-Upper Arm Circumference
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    child = relationship("Child", back_populates="growth_records")
    
    def __repr__(self):
        return f"<GrowthRecord(id={self.id}, child_id={self.child_id}, date={self.recorded_date})>"
