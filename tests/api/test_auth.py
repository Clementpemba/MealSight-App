import pytest
from httpx import AsyncClient


class TestAuthEndpoints:
    """Tests for authentication endpoints."""
    
    @pytest.mark.asyncio
    async def test_register_user(self, client: AsyncClient):
        """Test user registration."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "securepassword123",
                "full_name": "New User",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert "hashed_password" not in data
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient, test_user: dict):
        """Test registration with duplicate email."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": test_user["email"],
                "username": "differentuser",
                "password": "securepassword123",
            },
        )
        assert response.status_code == 409
    
    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user: dict):
        """Test successful login."""
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user["email"],
                "password": test_user["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, client: AsyncClient):
        """Test login with invalid credentials."""
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": "invalid@example.com",
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401
