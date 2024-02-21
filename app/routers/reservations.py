from typing import List
from fastapi import APIRouter, HTTPException, status, Request
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
    """
    Retrieve a list of all reservations in the system.

    Raises:
        HTTPException: 404 Not Found if no reservations exist.

    Returns:
        List[Reservation]: A list of Reservation objects.
    """
    reservations, message = await get_all_reservations()
    if not reservations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return reservations


@router.post(
    "/reservations/", response_model=Reservation, status_code=status.HTTP_201_CREATED
)
async def create_reservation_endpoint(reservation: Reservation):
    """
    Create a new reservation in the system.

    Parameters:
        reservation (Reservation): The reservation data to create.

    Raises:
        HTTPException: 400 Bad Request if the reservation cannot be created.

    Returns:
        dict: A message and the created Reservation object.
    """
    reservation, message = await create_reservation(reservation)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return {"message": message, "reservation": reservation}


@router.put("/reservations/{reservation_id}", response_model=Reservation)
async def update_reservation_endpoint(reservation_id: int, request: Request):
    """
    Update a reservation's details by its ID.

    Parameters:
        reservation_id (int): The unique identifier of the reservation to update.
        request (Request): The request object containing the update details.

    Raises:
        HTTPException: 400 Bad Request if the necessary update details are missing or invalid.

    Returns:
        Reservation: The updated Reservation object.
    """
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


@router.delete("/reservations/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_reservation_endpoint(reservation_id: int):
    """
    Cancel a reservation by its ID.

    Parameters:
        reservation_id (int): The unique identifier of the reservation to cancel.

    Raises:
        HTTPException: 404 Not Found if the reservation does not exist.

    Returns:
        dict: A message indicating successful cancellation.
    """
    success, message = await cancel_reservation(reservation_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return {"message": "Reservation deleted successfully"}
