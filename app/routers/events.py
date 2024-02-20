from typing import List
from fastapi import APIRouter, HTTPException, status
from ..models.event import Event
from ..services.event_service import get_all_events, create_event, delete_event

router = APIRouter()


@router.get("/events/", response_model=List[Event])
def read_events_endpoint():
    reservations, message = get_all_events()
    if reservations is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return reservations


@router.post("/events/", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event_endpoint(event: Event):
    event_created, message = create_event(event)
    if not event_created:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return event_created


@router.delete("/events/{event_id}", status_code=204)
def delete_event_endpoint(event_id: int):
    success, message = delete_event(event_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return {"message": "Event deleted successfully"}
