from sqlmodel import select
from ..models.reservation import Reservation
from ..models.user import User
from ..models.event import Event
from ..database import AsyncSessionLocal


async def get_all_reservations():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Reservation))
        reservations = result.scalars().all()
        if not reservations:
            return None, "Reservations not found"
        return reservations, "Reservations found successfully"


async def get_reservations_by_user(user_id: int):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            return None, "User not found"

        result = await session.execute(
            select(Reservation).where(Reservation.user_id == user_id)
        )
        reservations = result.scalars().all()

        if not reservations:
            return None, f"No reservations found for user ID {user_id}"

        return reservations, "Reservation found by userID"


async def create_reservation(reservation: Reservation) -> tuple[Reservation, str]:
    async with AsyncSessionLocal() as session:
        event = await session.get(Event, reservation.event_id)
        if not event:
            return None, "Event does not exist"
        if event.tickets_available < reservation.tickets_reserved:
            return (
                None,
                f"Only {event.tickets_available} tickets available, requested {reservation.tickets_reserved}.",
            )

        event.tickets_available -= reservation.tickets_reserved
        try:
            session.add(reservation)
            session.add(event)
            await session.commit()
            return reservation, "Reservation created successfully"

        except Exception as e:
            await session.rollback()
            return None, f"Failed to create reservation: {str(e)}"


async def update_reservation(reservation_id: int, user_id: int, tickets_reserved: int):
    async with AsyncSessionLocal() as session:
        reservation = await session.get(Reservation, reservation_id)
        if not reservation or reservation.user_id != user_id:
            return None, "Reservation not found or user mismatch"

        event = await session.get(Event, reservation.event_id)
        additional_tickets_needed = tickets_reserved - reservation.tickets_reserved
        if additional_tickets_needed > event.tickets_available:
            return (
                None,
                f"Not enough tickets available. Only {event.tickets_available} left.",
            )

        event.tickets_available -= additional_tickets_needed
        reservation.tickets_reserved = tickets_reserved
        await session.commit()

        return reservation, "Reservation updated successfully"


async def cancel_reservation(reservation_id: int) -> tuple[bool, str]:
    async with AsyncSessionLocal() as session:
        reservation = await session.get(Reservation, reservation_id)
        if not reservation:
            return False, "Reservation not found"

        event = await session.get(Event, reservation.event_id)
        event.tickets_available += reservation.tickets_reserved
        try:
            session.delete(reservation)
            session.add(event)
            await session.commit()

            return True, "Reservation cancelled successfully"

        except Exception as e:
            await session.rollback()
            return None, f"Failed to cancel reservation: {str(e)}"
