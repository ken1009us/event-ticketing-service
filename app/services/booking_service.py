from sqlmodel import select
from ..models.reservation import Reservation
from ..models.user import User
from ..models.event import Event
from ..database import AsyncSessionLocal


async def get_all_reservations():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(Reservation))
            reservations = result.scalars().all()
            return reservations, (
                "Reservations found successfully"
                if reservations
                else (None, "Reservations not found")
            )


async def get_reservations_by_user(user_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(Reservation).where(Reservation.user_id == user_id)
            )
            reservations = result.scalars().all()
            return reservations, (
                f"Reservations found for user ID {user_id}"
                if reservations
                else (None, f"No reservations found for user ID {user_id}")
            )


async def create_reservation(reservation: Reservation) -> tuple[Reservation, str]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            if reservation.tickets_reserved < 1:
                return (
                    None,
                    f"Number of reserved ticket must be at least one.",
                )

            event = await session.get(Event, reservation.event_id)
            if not event:
                return None, "Event not found"

            if event.tickets_available < reservation.tickets_reserved:
                return (
                    None,
                    f"Only {event.tickets_available} tickets available, requested {reservation.tickets_reserved}.",
                )
            event.tickets_available -= reservation.tickets_reserved
            session.add(reservation)
            session.add(event)
        return reservation, "Reservation created successfully"


async def update_reservation(reservation_id: int, user_id: int, tickets_reserved: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            reservation = await session.get(Reservation, reservation_id)
            if not reservation or reservation.user_id != user_id:
                return None, "Reservation not found or user mismatch"

            event = await session.get(Event, reservation.event_id)
            if tickets_reserved < 1:
                return (
                    None,
                    f"Number of reserved ticket must be at least one.",
                )
            additional_tickets_needed = tickets_reserved - reservation.tickets_reserved
            if additional_tickets_needed > event.tickets_available:
                return (
                    None,
                    f"Not enough tickets available. Only {event.tickets_available} left.",
                )

            event.tickets_available -= additional_tickets_needed
            reservation.tickets_reserved = tickets_reserved
        return reservation, "Reservation updated successfully"


async def cancel_reservation(reservation_id: int) -> tuple[bool, str]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            reservation = await session.get(Reservation, reservation_id)
            if not reservation:
                return False, "Reservation not found"

            event = await session.get(Event, reservation.event_id)
            if not event:
                return False, f"Event for reservation {reservation_id} not found"

            event.tickets_available += reservation.tickets_reserved
            await session.delete(reservation)
        return True, "Reservation cancelled successfully"
