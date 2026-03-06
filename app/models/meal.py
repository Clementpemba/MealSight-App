from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text, Date, Time, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, date

from app.db.base import Base


class Meal(Base):
    """
    Meal records with images captured by parents.
    """
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    meal_type = Column(String(20), nullable=True)  # breakfast, lunch, dinner, snack
    image_url_before = Column(Text, nullable=True)
    image_url_after = Column(Text, nullable=True)
    meal_date = Column(Date, nullable=False, default=date.today, index=True)
    meal_time = Column(Time, nullable=False, default=lambda: datetime.now().time())
    total_calories = Column(Numeric(7, 2), nullable=True)
    total_protein_g = Column(Numeric(6, 2), nullable=True)
    total_carbs_g = Column(Numeric(6, 2), nullable=True)
    total_fat_g = Column(Numeric(6, 2), nullable=True)
    nutrition_score = Column(Integer, nullable=True)  # 0-100
    ai_feedback = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    child = relationship("Child", back_populates="meals")
    user = relationship("User", back_populates="meals")
    meal_foods = relationship("MealFood", back_populates="meal", lazy="selectin", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Meal(id={self.id}, child_id={self.child_id}, meal_type={self.meal_type})>"


class MealFood(Base):
    """
    Foods identified in each meal by AI.
    """
    __tablename__ = "meal_foods"
    
    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id", ondelete="CASCADE"), nullable=False, index=True)
    food_id = Column(Integer, ForeignKey("foods.id", ondelete="SET NULL"), nullable=True, index=True)
    food_name = Column(String(255), nullable=False)
    portion_size_g = Column(Numeric(7, 2), nullable=True)
    confidence_score = Column(Numeric(4, 2), nullable=True)  # 0-1
    calories = Column(Numeric(7, 2), nullable=True)
    protein_g = Column(Numeric(6, 2), nullable=True)
    carbs_g = Column(Numeric(6, 2), nullable=True)
    fat_g = Column(Numeric(6, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    meal = relationship("Meal", back_populates="meal_foods")
    
    def __repr__(self):
        return f"<MealFood(id={self.id}, food_name={self.food_name})>"
