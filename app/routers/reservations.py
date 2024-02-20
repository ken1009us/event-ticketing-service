from typing import List
from fastapi import APIRouter, HTTPException, status
from ..models.reservation import Reservation
from ..services.booking_service import (
    create_reservation,
    update_reservation,
    cancel_reservation,
    get_all_reservations,
)

router = APIRouter()


@router.get("/reservations/", response_model=List[Reservation])
async def list_all_reservations():
    reservations, message = await get_all_reservations()
    if not reservations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return reservations


@router.post(
    "/reservations/", response_model=Reservation, status_code=status.HTTP_201_CREATED
)
async def create_reservation_endpoint(reservation: Reservation):
    reservation, message = await create_reservation(reservation)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return {"message": message, "reservation": reservation}


@router.put("/reservations/{reservation_id}", response_model=Reservation)
async def update_reservation_endpoint(reservation_id: int, request: Request):
    body = await request.json()
    user_id = body.get("user_id")
    tickets_reserved = body.get("tickets_reserved")

    if user_id is None or tickets_reserved is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing user_id or tickets_reserved in request body",
        )

    reservation, message = await update_reservation(
        reservation_id, user_id, tickets_reserved
    )
    if not reservation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return reservation


@router.delete("/reservations/{reservation_id}")
async def cancel_reservation_endpoint(reservation_id: int):
    success, message = await cancel_reservation(reservation_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return {"message": message}
