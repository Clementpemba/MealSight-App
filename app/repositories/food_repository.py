from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.models.food import Food
from app.repositories.base_repository import BaseRepository


class FoodRepository(BaseRepository[Food]):
    """Repository for Food model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Food)
    
    async def search(
        self, 
        query: str, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Food]:
        """Search foods by name or local name."""
        result = await self.db.execute(
            select(Food)
            .where(
                or_(
                    Food.name.ilike(f"%{query}%"),
                    Food.local_name.ilike(f"%{query}%")
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_category(
        self, 
        category: str, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Food]:
        """Get foods by category."""
        result = await self.db.execute(
            select(Food)
            .where(Food.category == category)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_categories(self) -> List[str]:
        """Get all unique food categories."""
        result = await self.db.execute(
            select(Food.category)
            .where(Food.category.isnot(None))
            .distinct()
        )
        return [row[0] for row in result.all()]
    
    async def get_by_name(self, name: str) -> Optional[Food]:
        """Get food by exact name match."""
        result = await self.db.execute(
            select(Food).where(Food.name == name)
        )
        return result.scalar_one_or_none()
