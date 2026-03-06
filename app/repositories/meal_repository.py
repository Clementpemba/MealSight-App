from typing import Optional, List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.meal import Meal, MealFood
from app.repositories.base_repository import BaseRepository


class MealRepository(BaseRepository[Meal]):
    """Repository for Meal model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Meal)
    
    async def get_by_child(
        self, 
        child_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Meal]:
        """Get all meals for a specific child."""
        result = await self.db.execute(
            select(Meal)
            .where(Meal.child_id == child_id)
            .order_by(Meal.meal_date.desc(), Meal.meal_time.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_user(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Meal]:
        """Get all meals created by a specific user."""
        result = await self.db.execute(
            select(Meal)
            .where(Meal.user_id == user_id)
            .order_by(Meal.meal_date.desc(), Meal.meal_time.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_id_and_user(
        self, 
        meal_id: int, 
        user_id: int
    ) -> Optional[Meal]:
        """Get a meal by ID for a specific user."""
        result = await self.db.execute(
            select(Meal).where(
                and_(
                    Meal.id == meal_id,
                    Meal.user_id == user_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_by_child_and_date(
        self, 
        child_id: int, 
        meal_date: date
    ) -> List[Meal]:
        """Get meals for a child on a specific date."""
        result = await self.db.execute(
            select(Meal).where(
                and_(
                    Meal.child_id == child_id,
                    Meal.meal_date == meal_date
                )
            ).order_by(Meal.meal_time)
        )
        return list(result.scalars().all())
    
    async def get_by_date_range(
        self,
        child_id: int,
        start_date: date,
        end_date: date
    ) -> List[Meal]:
        """Get meals within a date range for a child."""
        result = await self.db.execute(
            select(Meal).where(
                and_(
                    Meal.child_id == child_id,
                    Meal.meal_date >= start_date,
                    Meal.meal_date <= end_date
                )
            ).order_by(Meal.meal_date.desc(), Meal.meal_time.desc())
        )
        return list(result.scalars().all())
    
    async def count_by_child(self, child_id: int) -> int:
        """Count meals for a specific child."""
        return await self.count(child_id=child_id)


class MealFoodRepository(BaseRepository[MealFood]):
    """Repository for MealFood model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, MealFood)
    
    async def get_by_meal(self, meal_id: int) -> List[MealFood]:
        """Get all foods for a specific meal."""
        result = await self.db.execute(
            select(MealFood)
            .where(MealFood.meal_id == meal_id)
            .order_by(MealFood.created_at)
        )
        return list(result.scalars().all())
    
    async def delete_by_meal(self, meal_id: int) -> int:
        """Delete all foods for a specific meal."""
        from sqlalchemy import delete
        result = await self.db.execute(
            delete(MealFood).where(MealFood.meal_id == meal_id)
        )
        await self.db.commit()
        return result.rowcount
        return list(result.scalars().all())
    
    async def count_by_user(self, user_id: int) -> int:
        """Count meals for a specific user."""
        return await self.count(user_id=user_id)
