from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    decode_token,
)
from app.core.exceptions import (
    UnauthorizedException,
    ConflictException,
    BadRequestException,
)
from app.core.config import settings
from app.schemas.auth import AuthSuccessResponse, RefreshResponse
from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository
from app.models.user import User


REVOKED_REFRESH_TOKENS: set[str] = set()


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def register(self, user_data: UserCreate) -> AuthSuccessResponse:
        """Register a new user and return auth payload."""
        # Check if email exists
        if await self.user_repo.email_exists(user_data.email):
            raise ConflictException("Email already registered")
        
        # Create user
        hashed_password = get_password_hash(user_data.password)
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["password_hash"] = hashed_password
        
        user = await self.user_repo.create(user_dict)

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        return AuthSuccessResponse(
            message="Registration successful",
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token_expires_in=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )
    
    async def login(self, email: str, password: str) -> AuthSuccessResponse:
        """Authenticate user and return tokens."""
        user = await self.user_repo.get_by_email(email)
        
        if not user:
            raise UnauthorizedException("Invalid email or password")
        
        if not verify_password(password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")
        
        # Generate tokens
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)
        
        return AuthSuccessResponse(
            message="Login successful",
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token_expires_in=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )
    
    async def refresh_token(self, refresh_token: str) -> RefreshResponse:
        """Refresh access token using refresh token."""
        if refresh_token in REVOKED_REFRESH_TOKENS:
            raise UnauthorizedException("Invalid or expired refresh token")

        payload = decode_token(refresh_token)
        
        if payload is None:
            raise UnauthorizedException("Invalid or expired refresh token")
        
        if payload.get("type") != "refresh":
            raise BadRequestException("Invalid token type")
        
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Invalid or expired refresh token")
        
        user = await self.user_repo.get_by_id(int(user_id))
        if not user:
            raise UnauthorizedException("User not found")
        
        REVOKED_REFRESH_TOKENS.add(refresh_token)
        access_token = create_access_token(subject=user.id)

        return RefreshResponse(
            access_token=access_token,
            access_token_expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def logout(self, refresh_token: str) -> None:
        """Invalidate a refresh token."""
        REVOKED_REFRESH_TOKENS.add(refresh_token)
