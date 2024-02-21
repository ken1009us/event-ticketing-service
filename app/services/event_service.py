from sqlmodel import Session, select
from ..models.event import Event
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
        tuple: A tuple containing the newly created Event object and a success message.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add(event_data)
        return event_data, "Event created successfully"
        # try:
        #     session.add(event_data)
        #     await session.commit()
        #     await session.refresh(event_data)
        #     return event_data, "Event created successfully"

        # except Exception as e:
        #     await session.rollback()
        #     return None, f"Failed to create event: {str(e)}"


async def delete_event(event_id: int) -> tuple[bool, str]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            event = await session.get(Event, event_id)
            await session.delete(event)
        return True, "Event deleted successfully"

        # event = await session.get(Event, event_id)
        # if not event:
        #     return False, "Event not found"

        # try:
        #     session.delete(event)
        #     await session.commit()
        #     return True, "Event deleted successfully"

        # except Exception as e:
        #     await session.rollback()
        #     return None, f"Failed to delete event{event_id}: {str(e)}"
