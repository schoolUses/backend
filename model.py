from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[UUID] = uuid4
    name: str
    gender: str

class Board(BaseModel):
    date: datetime
    message: str
    