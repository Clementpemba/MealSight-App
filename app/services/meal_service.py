from typing import List
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException, ForbiddenException
from app.schemas.meal import MealCreate, MealUpdate
from app.repositories.meal_repository import MealRepository
from app.models.meal import Meal


class MealService:
    """Service for meal operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.meal_repo = MealRepository(db)
    
    async def create(self, meal_data: MealCreate, user_id: int) -> Meal:
        """Create a new meal."""
        meal_dict = meal_data.model_dump()
        meal_dict["user_id"] = user_id
        return await self.meal_repo.create(meal_dict)
    
    async def get_by_id(self, meal_id: int, user_id: int) -> Meal:
        """Get meal by ID, ensuring it belongs to the user."""
        meal = await self.meal_repo.get_by_id_and_user(meal_id, user_id)
        if not meal:
            raise NotFoundException(f"Meal with ID {meal_id} not found")
        return meal
    
    async def get_by_user(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Meal]:
        """Get all meals for a user."""
        return await self.meal_repo.get_by_user(user_id, skip=skip, limit=limit)
    
    async def update(
        self, 
        meal_id: int, 
        meal_data: MealUpdate, 
        user_id: int
    ) -> Meal:
        """Update a meal."""
        # Verify ownership
        await self.get_by_id(meal_id, user_id)
        
        update_dict = meal_data.model_dump(exclude_unset=True)
        updated_meal = await self.meal_repo.update(meal_id, update_dict)
        return updated_meal
    
    async def delete(self, meal_id: int, user_id: int) -> bool:
        """Delete a meal."""
        # Verify ownership
        await self.get_by_id(meal_id, user_id)
        return await self.meal_repo.delete(meal_id)
    
    async def upload_image(
        self, 
        meal_id: int, 
        file: UploadFile, 
        user_id: int
    ) -> Meal:
        """Upload an image for a meal."""
        # Verify ownership
        meal = await self.get_by_id(meal_id, user_id)
        
        # TODO: Implement actual file storage (S3, local, etc.)
        # For now, just store a placeholder URL
        # In production, you would:
        # 1. Validate file type
        # 2. Upload to storage service
        # 3. Get the URL
        
        image_url = f"/uploads/meals/{meal_id}/{file.filename}"
        
        updated_meal = await self.meal_repo.update(
            meal_id, 
            {"image_url": image_url}
        )
        return updated_meal
