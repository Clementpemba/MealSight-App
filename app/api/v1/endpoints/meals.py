from typing import List
from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.schemas.meal import MealCreate, MealResponse, MealUpdate
from app.services.meal_service import MealService

router = APIRouter()


@router.post("", response_model=MealResponse, status_code=status.HTTP_201_CREATED)
async def create_meal(
    meal_data: MealCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new meal entry."""
    meal_service = MealService(db)
    meal = await meal_service.create(meal_data, user_id=current_user.id)
    return meal


@router.get("", response_model=List[MealResponse])
async def get_user_meals(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all meals for current user."""
    meal_service = MealService(db)
    meals = await meal_service.get_by_user(
        user_id=current_user.id, 
        skip=skip, 
        limit=limit
    )
    return meals


@router.get("/{meal_id}", response_model=MealResponse)
async def get_meal(
    meal_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific meal by ID."""
    meal_service = MealService(db)
    meal = await meal_service.get_by_id(meal_id, user_id=current_user.id)
    return meal


@router.put("/{meal_id}", response_model=MealResponse)
async def update_meal(
    meal_id: int,
    meal_data: MealUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a meal entry."""
    meal_service = MealService(db)
    meal = await meal_service.update(meal_id, meal_data, user_id=current_user.id)
    return meal


@router.delete("/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal(
    meal_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a meal entry."""
    meal_service = MealService(db)
    await meal_service.delete(meal_id, user_id=current_user.id)
    return None


@router.post("/{meal_id}/image", response_model=MealResponse)
async def upload_meal_image(
    meal_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload an image for a meal."""
    meal_service = MealService(db)
    meal = await meal_service.upload_image(
        meal_id, 
        file, 
        user_id=current_user.id
    )
    return meal
