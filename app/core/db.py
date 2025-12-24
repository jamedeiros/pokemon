from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, Session, SQLModel, create_engine

engine = create_engine(url="sqlite:///./pokemon.db", echo=True)
SessionLocal = sessionmaker(class_=Session, autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Criar uma dependência reutilizável
DbSession = Annotated[Session, Depends(get_session)]


class Model(SQLModel, table=False):
    """Base class for all database models."""

    id: int | None = Field(default=None, primary_key=True)
