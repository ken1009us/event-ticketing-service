from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings

DATABASE_URL = f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """
    Initialize the database by creating all tables defined in SQLModel models.

    This function should be called at the start of the application to ensure that
    the database schema is correctly set up before handling any operations. It uses
    the `run_sync` method to run synchronous SQLModel metadata creation in an asynchronous
    context provided by `engine.begin()`.

    Raises:
        Exception: If there is an issue creating the tables in the database.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
