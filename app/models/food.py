from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime
from datetime import datetime

from app.db.base import Base


class Food(Base):
    """
    Local foods database with nutritional information.
    """
    __tablename__ = "foods"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    local_name = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)
    calories_per_100g = Column(Numeric(7, 2), nullable=True)
    protein_g = Column(Numeric(6, 2), nullable=True)
    carbohydrates_g = Column(Numeric(6, 2), nullable=True)
    fat_g = Column(Numeric(6, 2), nullable=True)
    fiber_g = Column(Numeric(6, 2), nullable=True)
    vitamin_a_mcg = Column(Numeric(8, 2), nullable=True)
    vitamin_c_mg = Column(Numeric(6, 2), nullable=True)
    iron_mg = Column(Numeric(6, 2), nullable=True)
    calcium_mg = Column(Numeric(7, 2), nullable=True)
    zinc_mg = Column(Numeric(6, 2), nullable=True)
    image_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Food(id={self.id}, name={self.name})>"
