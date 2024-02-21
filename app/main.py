from fastapi import FastAPI
from .routers import events, reservations, users
from .database import init_db

# Initialize FastAPI app instance
app = FastAPI()


async def app_lifespan(app: FastAPI):
    """
    Defines the lifespan of the FastAPI application.

    This asynchronous context manager is responsible for running startup and
    shutdown events. It ensures that the database is initialized when the app starts.

    Parameters:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: This function yields control back to the event loop until the app is
              terminated, at which point it can run shutdown tasks if necessary.
    """
    await init_db()
    yield


app.lifespan = app_lifespan

app.include_router(events.router)
app.include_router(reservations.router)
app.include_router(users.router)


@app.get("/")
async def read_root():
    """
    Root GET endpoint.

    Returns a dynamic and welcoming message as a JSON response. This endpoint is designed
    to make a great first impression by providing users with a glimpse into the capabilities
    and purpose of the event ticketing service, alongside instructions for getting started.

    Returns:
        dict: A dictionary with a welcoming message, service overview, and getting started instructions.
    """

    welcome_message = {
        "message": "🎉 Welcome to the Event Ticketing Service! 🎉",
        "description": "Your one-stop solution for browsing, booking, and managing event tickets with ease.",
        "instructions": {
            "explore_events": "GET /events/ - Discover upcoming events.",
            "book_tickets": "POST /reservations/ - Reserve your spot at your favorite events.",
            "manage_reservations": "GET /users/{user_id}/reservations - View and manage your bookings.",
        },
        "note": "Check out the API documentation for more details on how to use the service effectively.",
    }

    return welcome_message
