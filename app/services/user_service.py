from sqlmodel import select
from ..models.user import User
from ..models.reservation import Reservation
from ..models.event import Event
from ..database import AsyncSessionLocal


async def get_all_users():
    """
    Fetch all users from the database.

    Returns:
        tuple: A tuple containing a list of User objects and a success message,
               or None and an error message if no users are found.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(User))
            users = result.scalars().all()
            if not users:
                return None, f"Users not found"

            return users, f"Found users"


async def get_user(user_id: int) -> tuple[User, str]:
    """
    Fetch a specific user by their user ID.

    Parameters:
        user_id (int): The unique identifier of the user.

    Returns:
        tuple: A tuple containing the User object and a success message,
               or None and an error message if the user is not found.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if not user:
                return None, f"User {user_id} not found"

            return user, f"Found user {user_id}"


async def create_user(user: User) -> User:
    """
    Create a new user in the database.

    Parameters:
        user (User): The user object to be added to the database.

    Returns:
        User: The created User object along with a success message.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add(user)
        return user, "User created successfully"

        # session.add(user)
        # await session.commit()
        # await session.refresh(user)

        # return user, "User created successfully"


async def delete_user(user_id: int) -> tuple[bool, str]:
    """
    Delete an existing user by their user ID.

    Parameters:
        user_id (int): The unique identifier of the user to delete.

    Returns:
        tuple: A tuple indicating whether the deletion was successful,
               and a corresponding message.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():

            reservations = await session.execute(
                select(Reservation).where(Reservation.user_id == user_id)
            )
            reservations = reservations.scalars().all()

            for reservation in reservations:
                event = await session.get(Event, reservation.event_id)
                if event:
                    event.tickets_available += reservation.tickets_reserved
                    await session.delete(reservation)

            user = await session.get(User, user_id)
            if not user:
                return False, f"User {user_id} not found"

            await session.delete(user)
        await session.commit()
        return True, f"User {user_id} deleted successfully"

        # user = await session.get(User, user_id)
        # if not user:
        #     return False, f"User {user_id} not found"

        # try:
        #     session.delete(user)
        #     await session.commit()
        #     return True, f"User {user_id} deleted successfully"

        # except Exception as e:
        #     await session.rollback()
        #     return None, f"Failed to create delete user{user_id}: {str(e)}"
