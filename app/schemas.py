from pydantic import BaseModel
from datetime import datetime

class DonerCreate(BaseModel):
    doner_name: str
    meat_type: str
    price: float

class DonerOut(DonerCreate):
    id: int
    created_at: datetime

