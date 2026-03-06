from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class User(Base, TimestampMixin):
    """
    Parent/caregiver who uses the MealSight app.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    profile_image_url = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    
    # Relationships
    children = relationship("Child", back_populates="user", lazy="selectin", cascade="all, delete-orphan")
    meals = relationship("Meal", back_populates="user", lazy="selectin", cascade="all, delete-orphan")
    nutrition_alerts = relationship("NutritionAlert", back_populates="user", lazy="selectin", cascade="all, delete-orphan")
    health_worker_assignments = relationship("HealthWorkerAssignment", back_populates="user", lazy="selectin", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
