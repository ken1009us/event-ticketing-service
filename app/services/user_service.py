from sqlmodel import Session
from ..models.user import User
from ..database import engine


def create_user(user: User) -> User:
    with Session(engine) as session:
        if not user:
            return None, "User not found"

        session.add(user)
        session.commit()
        session.refresh(user)

        return user, "User created successfully"


def get_user(user_id: int) -> User:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            return user
        else:
            return None


def delete_user(user_id: int) -> tuple[bool, str]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            return False, f"User {user_id} not found"

        session.delete(user)
        session.commit()
        return True, f"User {user_id} deleted successfully"
