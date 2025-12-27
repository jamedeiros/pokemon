from sqlmodel import Session

from app.domain.models import Edition
from app.domain.schemas import EditionLoad
from app.libs.ligapokemon import LigaPokemon
from app.repository.uow import UnitOfWork

from .base import BaseService


class EditionService(BaseService[Edition, EditionLoad]):
    """Service class for managing Edition entities."""

    def __init__(
        self,
        *,
        session: Session,
        liga: LigaPokemon | None = None,
        uow: UnitOfWork | None = None,
    ) -> None:
        """Initialize an EditionService instance.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        """
        super().__init__(
            session=session,
            liga=liga or LigaPokemon(),
            entity_type=Edition,
            fields_to_update={"name", "code", "year"},
            uow=uow,
        )

    def _to_entity(self, data: EditionLoad) -> Edition:
        """Convert EditionLoad data to an Edition entity.

        :param data: EditionLoad data
        :return: Edition entity
        """
        return Edition.from_data(data)

    def get_or_create_edition(self, code: str, commit: bool = True) -> Edition:
        """Retrieve an Edition by its code or create it if it doesn't exist.

        :param code: The code of the edition to retrieve
        :return: Edition object if found, else None
        """
        repository = self.uow.get_repository(self.entity_type)
        edition = repository.get_by_code(code)

        if edition is None:
            # Edition does not exist, create it
            edition_data = self.liga.get_edition()
            edition = Edition.model_validate(edition_data)
            edition = repository.save(edition)

            if commit:
                self.uow.commit()

        return edition
