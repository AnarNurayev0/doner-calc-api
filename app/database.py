from sqlmodel import Session, create_engine
from .settings import settings
from typing import Annotated
from fastapi import Depends

DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    with Session(engine) as session:
        yield session

# === DATABASE DEPENDENCY ===
DatabaseDep = Annotated[Session, Depends(get_session)]