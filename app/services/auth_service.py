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
from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository
from app.models.user import User


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def register(self, user_data: UserCreate) -> User:
        """Register a new user."""
        # Check if email exists
        if await self.user_repo.email_exists(user_data.email):
            raise ConflictException("Email already registered")
        
        # Create user
        hashed_password = get_password_hash(user_data.password)
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["password_hash"] = hashed_password
        
        user = await self.user_repo.create(user_dict)
        return user
    
    async def login(self, email: str, password: str) -> Token:
        """Authenticate user and return tokens."""
        user = await self.user_repo.get_by_email(email)
        
        if not user:
            raise UnauthorizedException("Invalid email or password")
        
        if not verify_password(password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")
        
        # Generate tokens
        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    async def refresh_token(self, refresh_token: str) -> Token:
        """Refresh access token using refresh token."""
        payload = decode_token(refresh_token)
        
        if payload is None:
            raise UnauthorizedException("Invalid refresh token")
        
        if payload.get("type") != "refresh":
            raise BadRequestException("Invalid token type")
        
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Invalid refresh token")
        
        user = await self.user_repo.get_by_id(int(user_id))
        if not user:
            raise UnauthorizedException("User not found")
        
        # Generate new tokens
        access_token = create_access_token(subject=user.id)
        new_refresh_token = create_refresh_token(subject=user.id)
        
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
