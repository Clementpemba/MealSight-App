from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.child import Child
from app.repositories.base_repository import BaseRepository


class ChildRepository(BaseRepository[Child]):
    """Repository for Child model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Child)
    
    async def get_by_user(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Child]:
        """Get all children for a specific user."""
        result = await self.db.execute(
            select(Child)
            .where(Child.user_id == user_id)
            .order_by(Child.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_id_and_user(
        self, 
        child_id: int, 
        user_id: int
    ) -> Optional[Child]:
        """Get a child by ID for a specific user."""
        result = await self.db.execute(
            select(Child).where(
                Child.id == child_id,
                Child.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
    
    async def get_by_nutrition_status(
        self, 
        user_id: int, 
        status: str
    ) -> List[Child]:
        """Get children by nutrition status."""
        result = await self.db.execute(
            select(Child).where(
                Child.user_id == user_id,
                Child.nutrition_status == status
            )
        )
        return list(result.scalars().all())
    
    async def count_by_user(self, user_id: int) -> int:
        """Count children for a specific user."""
        return await self.count(user_id=user_id)
