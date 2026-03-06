from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.core.exceptions import NotFoundException, ConflictException
from app.schemas.user import UserUpdate
from app.repositories.user_repository import UserRepository
from app.models.user import User


class UserService:
    """Service for user operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def get_by_id(self, user_id: int) -> User:
        """Get user by ID."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")
        return user
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """Get all users."""
        return await self.user_repo.get_all(skip=skip, limit=limit)
    
    async def update(
        self, 
        user_id: int, 
        user_data: UserUpdate
    ) -> User:
        """Update user information."""
        user = await self.get_by_id(user_id)
        
        update_dict = user_data.model_dump(exclude_unset=True)
        
        # Check for email conflict
        if "email" in update_dict and update_dict["email"] != user.email:
            if await self.user_repo.email_exists(update_dict["email"]):
                raise ConflictException("Email already registered")
        
        # Check for username conflict
        if "username" in update_dict and update_dict["username"] != user.username:
            if await self.user_repo.username_exists(update_dict["username"]):
                raise ConflictException("Username already taken")
        
        # Hash password if provided
        if "password" in update_dict:
            update_dict["hashed_password"] = get_password_hash(update_dict.pop("password"))
        
        updated_user = await self.user_repo.update(user_id, update_dict)
        return updated_user
    
    async def delete(self, user_id: int) -> bool:
        """Delete a user."""
        user = await self.get_by_id(user_id)
        return await self.user_repo.delete(user_id)
    
    async def deactivate(self, user_id: int) -> User:
        """Deactivate a user account."""
        return await self.user_repo.update(user_id, {"is_active": False})
    
    async def activate(self, user_id: int) -> User:
        """Activate a user account."""
        return await self.user_repo.update(user_id, {"is_active": True})
