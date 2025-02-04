import pytest
from httpx import ASGITransport, AsyncClient
from .main import app
from fastapi.testclient import TestClient


client = TestClient(app)

@pytest.mark.anyio
async def test_number_data_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        response = await async_client.get("/api/classify-number?number=3")
        assert response.status_code == 200
        assert response.json()["number"] == 3
        assert response.json()["is_prime"] == True
        assert response.json()["is_perfect"] == False
        assert response.json()["properties"] == ["armstrong", "odd"]
        
        
@pytest.mark.anyio
async def test_number_cached_data_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        for i in range(3):
            response = await async_client.get("/api/classify-number?number=4")
            assert response.status_code == 200
            assert response.json()["number"] == 4
            assert response.json()["is_prime"] == False
            assert response.json()["properties"] == ["armstrong", "even"]
            
@pytest.mark.anyio
async def test_negative_number_data_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        response = await async_client.get("/api/classify-number?number=-563")
        assert response.status_code == 200
        assert response.json()["number"] == -563
        assert response.json()["is_prime"] == False
        assert response.json()["digit_sum"] == 4
        assert response.json()["properties"] == ["odd"]
        
@pytest.mark.anyio
async def test_non_integer_failure():
    values = [2.5, "a", "2187^%", "^^"]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        for value in values:
            response = await async_client.get(f"/api/classify-number?number={value}")
            assert response.status_code == 422
            assert response.json()["number"] == str(value)
            assert response.json()["error"] == True
            
@pytest.mark.anyio
async def test_invalid_parameter_failure():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        response = await async_client.get("/api/classify-number")
        assert response.status_code == 422
        assert response.json()["number"] == "Unprocessable Entity"
        assert response.json()["error"] == True
            
            
                