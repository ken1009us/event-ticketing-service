from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    """
    Represents an event entity with details about the event.

    Attributes:
        id (Optional[int]): The unique identifier of the event. Defaults to None.
        name (str): The name of the event. Indexed for faster searches.
        description (str): A brief description of the event.
        date_time (datetime): The date and time when the event is scheduled to take place.
        tickets_total (int): The total number of tickets available for the event.
        tickets_available (int): The number of tickets still available for purchase.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    date_time: datetime
    tickets_total: int
    tickets_available: int
