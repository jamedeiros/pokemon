from typing import Any, TypeVar

from sqlmodel import Session, func, select

from .exceptions import UnknownFilterError

T = TypeVar("T")


class Repository[T]:
    def __init__(self, session: Session, entity: type[T]) -> None:
        self._session = session
        self._entity = entity

    def get_by_id(self, id: int) -> T | None:
        stmt = select(self._entity).where(self._entity.id == id)
        return self._session.exec(stmt).one_or_none()

    def list(self, filters: dict[str, Any] | None = None, skip: int = 0, limit: int = 100) -> tuple[list[T], int]:
        stmt = select(self._entity)
        count_stmt = select(func.count()).select_from(self._entity)

        if filters:
            for field, value in filters.items():
                if not hasattr(self._entity, field):
                    raise UnknownFilterError("Filtro inválido.")
                stmt = stmt.where(getattr(self._entity, field) == value)
                count_stmt = count_stmt.where(getattr(self._entity, field) == value)

        total = self._session.exec(count_stmt).one()
        items = self._session.exec(stmt.offset(skip).limit(limit)).all()

        return items, total

    def save(self, entity: T) -> T:
        self._session.add(entity)
        self._session.flush()
        self._session.refresh(entity)
        return entity

    def remove(self, id: int) -> None:
        entity = self.get_by_id(id=id)
        self._session.delete(entity)
        self._session.flush()
