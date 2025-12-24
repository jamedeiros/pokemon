from app.domain.models import Edition

from .base import BaseService


class EditionService(BaseService):
    """Service class for managing Edition entities."""

    def get_or_create_edition(self, slug: str, commit: bool = True) -> Edition:
        """Retrieve an Edition by its slug or create it if it doesn't exist.

        :param slug: The slug of the edition to retrieve
        :return: Edition object if found, else None
        """
        edition = self.uow.editions.get_by_code(slug)

        if edition is None:
            # Edition does not exist, create it
            edition_data = self.liga.get_edition()
            edition = Edition.model_validate(edition_data)
            edition = self.uow.editions.save(edition)

            if commit:
                self.uow.commit()

        return edition
