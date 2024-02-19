from sqlmodel import Session
from ..models.event import Event
from ..database import engine


def create_event(event_data: Event) -> Event:
    with Session(engine) as session:
        session.add(event_data)
        session.commit()
        session.refresh(event_data)

        return event_data


def delete_event(event_id: int) -> tuple[bool, str]:
    with Session(engine) as session:
        event = session.get(Event, event_id)
        if not event:
            return False, "Event not found"

        session.delete(event)
        session.commit()

        return True, "Event deleted successfully"
