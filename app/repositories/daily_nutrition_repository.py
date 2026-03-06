from typing import Optional, List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from decimal import Decimal

from app.models.daily_nutrition import DailyNutrition
from app.repositories.base_repository import BaseRepository


class DailyNutritionRepository(BaseRepository[DailyNutrition]):
    """Repository for DailyNutrition model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, DailyNutrition)
    
    async def get_by_child_and_date(
        self, 
        child_id: int, 
        date: date
    ) -> Optional[DailyNutrition]:
        """Get daily nutrition for a child on a specific date."""
        result = await self.db.execute(
            select(DailyNutrition).where(
                and_(
                    DailyNutrition.child_id == child_id,
                    DailyNutrition.date == date
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_by_child_date_range(
        self,
        child_id: int,
        start_date: date,
        end_date: date
    ) -> List[DailyNutrition]:
        """Get daily nutrition records within a date range."""
        result = await self.db.execute(
            select(DailyNutrition).where(
                and_(
                    DailyNutrition.child_id == child_id,
                    DailyNutrition.date >= start_date,
                    DailyNutrition.date <= end_date
                )
            ).order_by(DailyNutrition.date.desc())
        )
        return list(result.scalars().all())
    
    async def get_weekly_summary(
        self,
        child_id: int,
        start_date: date,
        end_date: date
    ) -> dict:
        """Get weekly nutrition summary."""
        result = await self.db.execute(
            select(
                func.avg(DailyNutrition.total_calories).label("avg_calories"),
                func.avg(DailyNutrition.total_protein_g).label("avg_protein"),
                func.avg(DailyNutrition.total_carbs_g).label("avg_carbs"),
                func.avg(DailyNutrition.total_fat_g).label("avg_fat"),
                func.sum(DailyNutrition.meals_count).label("total_meals"),
                func.avg(DailyNutrition.nutrition_score).label("avg_score"),
            ).where(
                and_(
                    DailyNutrition.child_id == child_id,
                    DailyNutrition.date >= start_date,
                    DailyNutrition.date <= end_date
                )
            )
        )
        row = result.one()
        return {
            "avg_calories": row.avg_calories or Decimal("0"),
            "avg_protein": row.avg_protein or Decimal("0"),
            "avg_carbs": row.avg_carbs or Decimal("0"),
            "avg_fat": row.avg_fat or Decimal("0"),
            "total_meals": row.total_meals or 0,
            "avg_score": row.avg_score,
        }
    
    async def upsert(
        self,
        child_id: int,
        date: date,
        data: dict
    ) -> DailyNutrition:
        """Insert or update daily nutrition record."""
        existing = await self.get_by_child_and_date(child_id, date)
        
        if existing:
            return await self.update(existing.id, data)
        else:
            data["child_id"] = child_id
            data["date"] = date
            return await self.create(data)
