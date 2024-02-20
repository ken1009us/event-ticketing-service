from typing import List
from fastapi import APIRouter, HTTPException, status
from ..models.user import User
from ..models.reservation import Reservation
from ..services.user_service import create_user, get_user, delete_user
from ..services.booking_service import get_reservations_by_user

router = APIRouter()

@router.get("/users/{user_id}", response_model=User)
def read_user_endpoint(user_id: int):
    user = get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/users/{user_id}/reservations", response_model=List[Reservation])
def get_user_reservations(user_id: int):
    reservations, message = get_reservations_by_user(user_id)
    if not reservations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return reservations


@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: User):
    user, message = create_user(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    return user


@router.delete("/users/{user_id}", status_code=204)
def delete_user_endpoint(user_id: int):
    success, message = delete_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return {"message": message}
