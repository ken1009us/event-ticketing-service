from typing import List
from fastapi import APIRouter, HTTPException, status
from ..models.event import Event
from ..services.event_service import get_all_events, create_event, delete_event

router = APIRouter()


@router.get("/events/", response_model=List[Event])
async def read_events_endpoint():
    """
    Retrieves a list of all events.

    Returns:
        List[Event]: A list of event instances.

    Raises:
        HTTPException: A 404 error if no events are found.
    """
    events, message = await get_all_events()
    if events is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return events


@router.post("/events/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event_endpoint(event: Event):
    """
    Creates a new event.

    Parameters:
        event (Event): The event data to create.

    Returns:
        Event: The created event instance.

    Raises:
        HTTPException: A 400 error if the event could not be created.
    """
    event_created, message = await create_event(event)
    if not event_created:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return event_created


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_endpoint(event_id: int):
    """
    Deletes an event by its ID.

    Parameters:
        event_id (int): The unique identifier of the event to delete.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: A 404 error if the event is not found or could not be deleted.
    """
    success, message = await delete_event(event_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return {"message": "Event deleted successfully"}
