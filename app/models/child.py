from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Child(Base, TimestampMixin):
    """
    Child being monitored for nutrition.
    """
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=True)  # male, female, other
    profile_image_url = Column(Text, nullable=True)
    height_cm = Column(Numeric(5, 2), nullable=True)
    weight_kg = Column(Numeric(5, 2), nullable=True)
    nutrition_status = Column(String(50), default="unknown")
    
    # Relationships
    user = relationship("User", back_populates="children")
    meals = relationship("Meal", back_populates="child", lazy="selectin", cascade="all, delete-orphan")
    daily_nutrition = relationship("DailyNutrition", back_populates="child", lazy="selectin", cascade="all, delete-orphan")
    growth_records = relationship("GrowthRecord", back_populates="child", lazy="selectin", cascade="all, delete-orphan")
    nutrition_alerts = relationship("NutritionAlert", back_populates="child", lazy="selectin", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Child(id={self.id}, name={self.name})>"
