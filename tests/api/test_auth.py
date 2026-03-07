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
                "full_name": "New User",
                "email": "newuser@example.com",
                "phone": "+265991234567",
                "password": "securepassword123",
                "location": "Lilongwe, Malawi",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Registration successful"
        assert data["user"]["email"] == "newuser@example.com"
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["access_token_expires_in"] == 3600
        assert data["refresh_token_expires_in"] == 7776000
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient, test_user: dict):
        """Test registration with duplicate email."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "Different User",
                "email": test_user["email"],
                "password": "securepassword123",
            },
        )
        assert response.status_code == 409
    
    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user: dict):
        """Test successful login."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Login successful"
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["access_token_expires_in"] == 3600
        assert data["refresh_token_expires_in"] == 7776000
    
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, client: AsyncClient):
        """Test login with invalid credentials."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "invalid@example.com",
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_refresh_token(self, client: AsyncClient, test_user: dict):
        """Test refresh endpoint returns new access token only."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"email": test_user["email"], "password": test_user["password"]},
        )
        refresh_token = login_response.json()["refresh_token"]

        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token_expires_in"] == 3600
        assert "refresh_token" not in data

    @pytest.mark.asyncio
    async def test_me_endpoint(self, client: AsyncClient, auth_headers: dict):
        """Test /auth/me returns current user."""
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data

    @pytest.mark.asyncio
    async def test_logout(self, client: AsyncClient, test_user: dict, auth_headers: dict):
        """Test logout revokes refresh token."""
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"email": test_user["email"], "password": test_user["password"]},
        )
        refresh_token = login_response.json()["refresh_token"]

        response = await client.post(
            "/api/v1/auth/logout",
            headers=auth_headers,
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Logged out successfully"
