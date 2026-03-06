from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.schemas.auth import Token, TokenRefresh
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    auth_service = AuthService(db)
    user = await auth_service.register(user_data)
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login and get access token."""
    auth_service = AuthService(db)
    tokens = await auth_service.login(form_data.username, form_data.password)
    return tokens


@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token."""
    auth_service = AuthService(db)
    tokens = await auth_service.refresh_token(token_data.refresh_token)
    return tokens


@router.post("/logout")
async def logout():
    """Logout current user (client-side token removal)."""
    return {"message": "Successfully logged out"}
