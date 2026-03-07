from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.auth import (
    AuthSuccessResponse,
    LoginRequest,
    LogoutRequest,
    RefreshResponse,
    TokenRefresh,
)
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=AuthSuccessResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    auth_service = AuthService(db)
    user = await auth_service.register(user_data)
    return user


@router.post("/login", response_model=AuthSuccessResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login and get access token."""
    auth_service = AuthService(db)
    tokens = await auth_service.login(login_data.email, login_data.password)
    return tokens


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token."""
    auth_service = AuthService(db)
    tokens = await auth_service.refresh_token(token_data.refresh_token)
    return tokens


@router.post("/logout")
async def logout(
    logout_data: LogoutRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Logout current user and revoke refresh token."""
    auth_service = AuthService(db)
    await auth_service.logout(logout_data.refresh_token)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user's profile."""
    return current_user
