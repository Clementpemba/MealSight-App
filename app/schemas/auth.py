from pydantic import BaseModel


class Token(BaseModel):
    """Token response schema."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema."""
    
    sub: str
    exp: int
    type: str


class TokenRefresh(BaseModel):
    """Token refresh request schema."""
    
    refresh_token: str
