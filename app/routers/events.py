from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..models.event import Event
from ..database import engine
from ..services import event_service

router = APIRouter()


@router.get("/events/", response_model=List[Event])
def read_events_endpoint():
    with Session(engine) as session:
        events = session.exec(select(Event)).all()

        return events


@router.post("/events/", response_model=Event, status_code=201)
def create_event_endpoint(event: Event):
    return event_service.create_event(event)


@router.delete("/events/{event_id}", status_code=204)
def delete_event_endpoint(event_id: int):
    success, message = event_service.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail=message)
    return {"message": "Event deleted successfully"}
