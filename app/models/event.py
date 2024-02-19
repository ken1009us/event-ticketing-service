from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    date_time: datetime
    tickets_total: int
    tickets_available: int
