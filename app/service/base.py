import abc
from typing import TypeVar

from pydantic import BaseModel
from sqlmodel import Session
from traitlets import Any

from app.core.db import Model
from app.libs import LigaPokemon
from app.repository import UnitOfWork
from app.service.exceptions import ObjectNotFoundError

Entity = TypeVar("Entity", bound=Model)
Input = TypeVar("Input", bound=BaseModel)


class BaseService[Entity, Input](abc.ABC):
    """Base service class providing common functionality for all services."""

    def __init__(
        self,
        *,
        session: Session,
        liga: LigaPokemon,
        entity_type: type[Entity],
        uow: UnitOfWork | None = None,
        fields_to_update: set[str] | None = None,
        immutable_fields: set[str] | None = None,
    ) -> None:
        """Initialize a BaseService instance."""
        self.liga = liga
        self.uow = uow or UnitOfWork(session)
        self.entity_type = entity_type
        self.fields_to_update = fields_to_update
        self.immutable_fields = immutable_fields or {
            "id",
        }

    @abc.abstractmethod
    def _to_entity(self, data: Input) -> Entity:
        """Validate and convert input data to an entity model.

        :param data: Input data to validate
        :return: Validated entity model
        """
        raise NotImplementedError

    def _validate_update(self, field: str, value: Any) -> None:  # noqa: B027
        """Validate updates to an entity field."""
        ...

    def _update_entity(self, entity: Entity, data: Input) -> Entity:
        """Apply updates from input data to an existing entity.

        :param entity: The existing entity to update
        :param data: Input data containing updates
        :return: Updated entity
        """
        updates = data.model_dump(exclude_unset=True)
        fields_to_update = self.get_fields_to_update() - self.immutable_fields

        for field, value in updates.items():
            if field in fields_to_update and hasattr(entity, field):
                self._validate_update(field, value)
                setattr(entity, field, value)

        return entity

    def get_fields_to_update(self) -> set[str]:
        """Get a dictionary of fields to update from the input data.

        :return: Dictionary of fields to update
        """
        if self.fields_to_update is not None:
            return self.fields_to_update

        return set(self.entity_type.model_fields.keys())

    def create(self, *, data: Input, commit: bool = True) -> Entity:
        """Create a new entity.

        :param data: Input data for the new entity
        :param commit: Whether to commit the transaction
        :return: The created entity
        """
        entity = self._to_entity(data)
        entity = self.uow.get_repository(self.entity_type).save(entity)

        if commit:
            self.uow.commit()

        return entity

    def update(self, id: int, data: Input, commit: bool = True) -> Entity:
        """Update an existing entity.

        :param id: The ID of the entity to update
        :param data: Input data for updating the entity
        :param commit: Whether to commit the transaction
        :return: The updated entity
        """
        repository = self.uow.get_repository(self.entity_type)
        entity = repository.get_by_id(id)

        if entity is None:
            raise ObjectNotFoundError("Entity not found.")

        entity = self._update_entity(entity, data)
        repository.save(entity)

        if commit:
            self.uow.commit()

        return entity

    def delete(self, id: int, commit: bool = True) -> None:
        """Delete an entity by its ID.

        :param id: The ID of the entity to delete
        :param commit: Whether to commit the transaction
        """
        repository = self.uow.get_repository(self.entity_type)
        entity = repository.get_by_id(id)

        if entity is None:
            raise ObjectNotFoundError("Entity not found.")

        repository.remove(id)

        if commit:
            self.uow.commit()

    def get_by_id(self, id: int) -> Entity:
        """Retrieve an entity by its ID.

        :param id: The ID of the entity to retrieve
        :return: The entity
        """
        entity = self.uow.get_repository(self.entity_type).get_by_id(id)
        if entity is None:
            raise ObjectNotFoundError("Entity not found.")
        return entity

    def get_list(
        self,
        *,
        page: int = 1,
        page_size: int = 100,
    ) -> tuple[list[Entity], int]:
        """Retrieve a list of entities with optional filtering and pagination.

        :param filters: A dictionary of filters to apply
        :param page: The page number for pagination
        :param page_size: The number of items per page
        :return: A tuple containing the list of entities and the total count
        """
        skip = (page - 1) * page_size
        limit = page_size
        return self.uow.get_repository(self.entity_type).list(skip=skip, limit=limit)
