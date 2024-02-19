from fastapi import APIRouter, HTTPException
from ..models.reservation import Reservation
from ..services.booking_service import (
    create_reservation,
    update_reservation,
    cancel_reservation,
)

router = APIRouter()


@router.post("/reservations/", response_model=Reservation)
def create_reservation_endpoint(reservation: Reservation):
    reservation, message = create_reservation(reservation)
    if not reservation:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message, "reservation": reservation}


@router.put("/reservations/{reservation_id}", response_model=Reservation)
def update_reservation_endpoint(reservation_id: int, tickets_reserved: int):
    reservation, message = update_reservation(reservation_id, tickets_reserved)
    if not reservation:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message, "reservation": reservation}


@router.delete("/reservations/{reservation_id}")
def cancel_reservation_endpoint(reservation_id: int):
    success, message = cancel_reservation(reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail=message)
    return {"message": message}