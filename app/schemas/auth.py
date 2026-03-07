from pydantic import BaseModel, EmailStr

from app.schemas.user import UserResponse


class Token(BaseModel):
    """Token response schema."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthUser(BaseModel):
    """Lightweight user payload included in auth responses."""

    id: int
    full_name: str
    email: EmailStr
    phone: str | None = None
    profile_image_url: str | None = None
    location: str | None = None
    created_at: str | None = None


class AuthSuccessResponse(BaseModel):
    """Register/login success response schema."""

    message: str
    user: UserResponse
    access_token: str
    refresh_token: str
    access_token_expires_in: int
    refresh_token_expires_in: int


class RefreshResponse(BaseModel):
    """Refresh token success response schema."""

    access_token: str
    access_token_expires_in: int


class LogoutRequest(BaseModel):
    """Logout request payload."""

    refresh_token: str


class LoginRequest(BaseModel):
    """Login request payload."""

    email: EmailStr
    password: str


class TokenPayload(BaseModel):
    """Token payload schema."""
    
    sub: str
    exp: int
    type: str


class TokenRefresh(BaseModel):
    """Token refresh request schema."""
    
    refresh_token: str
