import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {
            "message": "🎉 Welcome to the Event Ticketing Service! 🎉",
            "description": "Your one-stop solution for browsing, booking, and managing event tickets with ease.",
            "instructions": {
                "explore_events": "GET /events/ - Discover upcoming events.",
                "book_tickets": "POST /reservations/ - Reserve your spot at your favorite events.",
                "manage_reservations": "GET /users/{user_id}/reservations - View and manage your bookings.",
            },
            "note": "Check out the API documentation for more details on how to use the service effectively.",
        }
