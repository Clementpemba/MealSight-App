import pytest
from httpx import AsyncClient


class TestUserEndpoints:
    """Tests for user endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_current_user(
        self, 
        client: AsyncClient, 
        auth_headers: dict,
        test_user: dict
    ):
        """Test getting current user info."""
        response = await client.get(
            "/api/v1/users/me",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user["email"]
        assert data["username"] == test_user["username"]
    
    @pytest.mark.asyncio
    async def test_get_current_user_unauthorized(self, client: AsyncClient):
        """Test getting current user without auth."""
        response = await client.get("/api/v1/users/me")
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_update_current_user(
        self, 
        client: AsyncClient, 
        auth_headers: dict
    ):
        """Test updating current user info."""
        response = await client.put(
            "/api/v1/users/me",
            headers=auth_headers,
            json={"full_name": "Updated Name"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
