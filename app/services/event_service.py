from sqlmodel import select
from ..models.event import Event
from ..models.reservation import Reservation
from ..database import AsyncSessionLocal


async def get_all_events():
    """
    Retrieves all events from the database.

    Returns:
        tuple: A tuple containing a list of Event objects if found, and a corresponding message.
               Returns None and an error message if no events are found.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(Event))
            events = result.scalars().all()
            if not events:
                return None, "Events not found"

            return events, "Event found successfully"


async def create_event(event_data: Event) -> tuple[Event, str]:
    """
    Creates a new event and saves it to the database.

    Parameters:
        event_data (Event): The event data to save.

    Returns:
        tuple: A tuple indicating whether the deletion was successful,
               and a corresponding message.
    """
    async with AsyncSessionLocal() as session:
        try:
            async with session.begin():
                session.add(event_data)
            return event_data, "Event created successfully"
        except Exception as e:
            return None, f"Failed to create event: {e}"


async def delete_event(event_id: int) -> tuple[bool, str]:
    """
    Deletes an event identified by its ID.

    Parameters:
        event_id (int): The unique identifier of the event to delete.

    Returns:
        tuple: A tuple indicating whether the deletion was successful,
               and a corresponding message.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            event = await session.get(Event, event_id)
            if not event:
                return False, "Event not found"

            reservations = await session.execute(
                select(Reservation).where(Reservation.event_id == event_id)
            )

            for reservation in reservations.scalars():
                await session.delete(reservation)

            await session.delete(event)

        return True, "Event deleted successfully"
