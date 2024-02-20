from sqlmodel import Session, select
from ..models.event import Event
from ..database import engine


def get_all_events():
    with Session(engine) as session:
        events = session.exec(select(Event)).all()
        if not events:
            return None, "Events not found"
        return events, "Event found successfully"


def create_event(event_data: Event) -> tuple[Event, str]:
    with Session(engine) as session:
        session.add(event_data)
        session.commit()
        session.refresh(event_data)
        if not event_data:
            return None, "Events not found"
        return event_data, "Event created successfully"


def delete_event(event_id: int) -> tuple[bool, str]:
    with Session(engine) as session:
        event = session.get(Event, event_id)
        if not event:
            return False, "Event not found"

        session.delete(event)
        session.commit()

        return True, "Event deleted successfully"
