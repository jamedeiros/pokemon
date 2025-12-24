from sqlmodel import Session

from app.libs import LigaPokemon
from app.repository import UnitOfWork


class BaseService:
    """Base service class providing common functionality for all services."""

    def __init__(self, session: Session, liga: LigaPokemon | None = None, uow: UnitOfWork | None = None) -> None:
        """Initialize a BaseService instance."""
        self.liga = liga or LigaPokemon()
        self.uow = uow or UnitOfWork(session)
