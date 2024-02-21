import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the event ticketing service."}