from sqlalchemy import Column, Integer, ForeignKey, Numeric, Date, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class DailyNutrition(Base):
    """
    Daily nutrition summary per child.
    """
    __tablename__ = "daily_nutrition"
    
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    total_calories = Column(Numeric(8, 2), default=0)
    total_protein_g = Column(Numeric(7, 2), default=0)
    total_carbs_g = Column(Numeric(7, 2), default=0)
    total_fat_g = Column(Numeric(7, 2), default=0)
    total_fiber_g = Column(Numeric(6, 2), default=0)
    meals_count = Column(Integer, default=0)
    nutrition_score = Column(Integer, nullable=True)  # 0-100
    recommendations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('child_id', 'date', name='uq_daily_nutrition_child_date'),
    )
    
    # Relationships
    child = relationship("Child", back_populates="daily_nutrition")
    
    def __repr__(self):
        return f"<DailyNutrition(id={self.id}, child_id={self.child_id}, date={self.date})>"
