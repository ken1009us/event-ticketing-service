from sqlmodel import Session
from ..models.reservation import Reservation
from ..models.event import Event
from ..database import engine


def create_reservation(reservation: Reservation) -> tuple[Reservation, str]:
    with Session(engine) as session:
        event = session.get(Event, reservation.event_id)
        if not event:
            return None, "Event does not exist"
        if event.tickets_available < reservation.tickets_reserved:
            return (
                None,
                f"Only {event.tickets_available} tickets available, requested {reservation.tickets_reserved}.",
            )

        event.tickets_available -= reservation.tickets_reserved
        session.add(reservation)
        session.add(event)
        session.commit()

        return reservation, "Reservation created successfully"


def update_reservation(reservation_id: int, tickets_reserved: int):
    with Session(engine) as session:
        reservation = session.get(Reservation, reservation_id)
        if not reservation:
            return None, "Reservation not found"

        event = session.get(Event, reservation.event_id)
        additional_tickets_needed = tickets_reserved - reservation.tickets_reserved
        if additional_tickets_needed > event.tickets_available:
            return (
                None,
                f"Not enough tickets available. Only {event.tickets_available} left.",
            )

        event.tickets_available -= additional_tickets_needed
        reservation.tickets_reserved = tickets_reserved
        session.commit()

        return reservation, "Reservation updated successfully"


def cancel_reservation(reservation_id: int) -> tuple[bool, str]:
    with Session(engine) as session:
        reservation = session.get(Reservation, reservation_id)
        if not reservation:
            return False, "Reservation not found"

        event = session.get(Event, reservation.event_id)
        event.tickets_available += reservation.tickets_reserved
        session.delete(reservation)
        session.add(event)
        session.commit()

        return True, "Reservation cancelled successfully"
