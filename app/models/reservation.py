from typing import Optional
from sqlmodel import Field, SQLModel


class Reservation(SQLModel, table=True):
    """
    Represents a reservation made by a user for an event, detailing the user, event, and number of tickets reserved.

    Attributes:
        id (Optional[int]): The unique identifier for the reservation. Automatically generated if not provided.
        user_id (int): The identifier of the user who made the reservation. Links to the 'user.id' foreign key.
        event_id (int): The identifier of the event for which the reservation is made. Links to the 'event.id' foreign key.
        tickets_reserved (int): The number of tickets reserved by the user for the event.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    event_id: int = Field(foreign_key="event.id")
    tickets_reserved: int
