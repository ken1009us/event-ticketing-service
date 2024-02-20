from sqlmodel import select
from ..models.user import User
from ..database import AsyncSessionLocal


async def get_all_users():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(User))
            users = result.scalars().all()
            if not users:
                return None, f"Users not found"

            return users, f"Found users"


async def get_user(user_id: int) -> tuple[User, str]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if not user:
                return None, f"User {user_id} not found"

            return user, f"Found user {user_id}"


async def create_user(user: User) -> User:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add(user)
        return user, "User created successfully"

        # session.add(user)
        # await session.commit()
        # await session.refresh(user)

        # return user, "User created successfully"


async def delete_user(user_id: int) -> tuple[bool, str]:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            await session.delete(user)
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
