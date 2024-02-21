from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    Represents a user of the event ticketing system, with a unique identifier and a name.

    Attributes:
        id (Optional[int]): The unique identifier for the user. Automatically generated if not provided.
        name (str): The name of the user.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
