from sqlmodel import select

from app.domain.models import Card, Edition

from .base import Repository


class EditionRepository(Repository[Edition]):
    def get_by_code(self, code: str) -> Edition:
        stmt = select(self._entity).where(self._entity.code == code)
        return self._session.exec(stmt).one_or_none()


class CardRepository(Repository[Card]):
    def get_by_identifiers(self, card_id: str, set_id: str, edition_slug: str) -> Card:
        stmt = (
            select(self._entity)
            .where(self._entity.card_id == card_id)
            .where(self._entity.set_id == set_id)
            .where(self._entity.edition.has(Edition.code == edition_slug))
        )
        return self._session.exec(stmt).one_or_none()
