from fastapi import APIRouter, HTTPException
from ..models.user import User
from ..services.user_service import create_user, get_user, delete_user

router = APIRouter()


@router.post("/users/", response_model=User)
def create_user_endpoint(user: User):
    return create_user(user)


@router.get("/users/{user_id}", response_model=User)
def read_user_endpoint(user_id: int):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}", status_code=204)
def delete_user_endpoint(user_id: int):
    success, message = delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail=message)

    return {"message": message}
