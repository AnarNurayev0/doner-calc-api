from sqlmodel import Field, SQLModel, TIMESTAMP, text
from datetime import datetime

class Doners(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    doner_name: str = Field(nullable=False)
    meat_type: str = Field(nullable=False)
    price: float = Field(nullable=False)
    created_at: datetime = Field(sa_type=TIMESTAMP(timezone=True),
                                nullable=False,
                                sa_column_kwargs={"server_default": text("now()")})
