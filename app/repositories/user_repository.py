from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email address."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_phone(self, phone: str) -> Optional[User]:
        """Get a user by phone number."""
        result = await self.db.execute(
            select(User).where(User.phone == phone)
        )
        return result.scalar_one_or_none()
    
    async def get_by_location(
        self, 
        location: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """Get all users in a location."""
        result = await self.db.execute(
            select(User)
            .where(User.location == location)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        return await self.exists(email=email)
    
    async def search_by_name(
        self, 
        name: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[User]:
        """Search users by name."""
        result = await self.db.execute(
            select(User)
            .where(User.full_name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
