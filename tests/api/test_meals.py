import pytest
from httpx import AsyncClient


class TestMealEndpoints:
    """Tests for meal endpoints."""
    
    @pytest.mark.asyncio
    async def test_create_meal(
        self, 
        client: AsyncClient, 
        auth_headers: dict
    ):
        """Test creating a new meal."""
        response = await client.post(
            "/api/v1/meals",
            headers=auth_headers,
            json={
                "name": "Breakfast Bowl",
                "description": "Healthy breakfast",
                "calories": 450,
                "protein": 25,
                "carbohydrates": 50,
                "fat": 15,
                "meal_type": "breakfast",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Breakfast Bowl"
        assert data["calories"] == 450
    
    @pytest.mark.asyncio
    async def test_get_meals(
        self, 
        client: AsyncClient, 
        auth_headers: dict
    ):
        """Test getting all user meals."""
        # Create a meal first
        await client.post(
            "/api/v1/meals",
            headers=auth_headers,
            json={"name": "Test Meal"},
        )
        
        response = await client.get(
            "/api/v1/meals",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    @pytest.mark.asyncio
    async def test_get_meal_by_id(
        self, 
        client: AsyncClient, 
        auth_headers: dict
    ):
        """Test getting a specific meal."""
        # Create a meal
        create_response = await client.post(
            "/api/v1/meals",
            headers=auth_headers,
            json={"name": "Specific Meal"},
        )
        meal_id = create_response.json()["id"]
        
        response = await client.get(
            f"/api/v1/meals/{meal_id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Specific Meal"
    
    @pytest.mark.asyncio
    async def test_update_meal(
        self, 
        client: AsyncClient, 
        auth_headers: dict
    ):
        """Test updating a meal."""
        # Create a meal
        create_response = await client.post(
            "/api/v1/meals",
            headers=auth_headers,
            json={"name": "Original Name"},
        )
        meal_id = create_response.json()["id"]
        
        response = await client.put(
            f"/api/v1/meals/{meal_id}",
            headers=auth_headers,
            json={"name": "Updated Name"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"
    
    @pytest.mark.asyncio
    async def test_delete_meal(
        self, 
        client: AsyncClient, 
        auth_headers: dict
    ):
        """Test deleting a meal."""
        # Create a meal
        create_response = await client.post(
            "/api/v1/meals",
            headers=auth_headers,
            json={"name": "To Delete"},
        )
        meal_id = create_response.json()["id"]
        
        response = await client.delete(
            f"/api/v1/meals/{meal_id}",
            headers=auth_headers,
        )
        assert response.status_code == 204
        
        # Verify deletion
        get_response = await client.get(
            f"/api/v1/meals/{meal_id}",
            headers=auth_headers,
        )
        assert get_response.status_code == 404
