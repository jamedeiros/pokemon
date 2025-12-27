from app.domain.models import Card
from app.domain.schemas import CardInput
from app.libs.ligapokemon import LigaPokemon

from .base import BaseService
from .edition_service import EditionService


class CardService(BaseService[Card, CardInput]):
    """Service class for card-related operations."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize a CardService instance.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        """
        kwargs.update({"liga": LigaPokemon()})
        super().__init__(*args, **kwargs)
        self.edition_service = EditionService(*args, **kwargs)

    def _to_entity(self, data: CardInput) -> Card:
        """Convert CardInput data to a Card entity.
        :param data: CardInput data
        :return: Card entity
        """
        return Card.model_validate(
            {
                "card_id": data.card_id,
                "set_id": data.set_id,
                "name": data.name,
                "rarity": data.rarity,
                "edition_id": data.edition_id,
            }
        )

    def _update_entity(self, entity: Card, data: CardInput) -> Card:
        """Update an existing Card entity with CardInput data.
        :param entity: Existing Card entity
        :param data: CardInput data
        :return: Updated Card entity
        """
        entity.name = data.name
        entity.rarity = data.rarity
        return entity

    def create(self, *, data: CardInput, commit: bool = True) -> Card:
        """Create a Pokémon card.

        :param data: CardInput object containing card_id, set_id, and edition
        :return: CardLoad object with card details
        """
        card_loaded = self.liga.get_card(data.card_id, data.set_id, data.edition_slug)

        card = self.uow.cards.get_by_identifiers(
            card_id=data.card_id, set_id=data.set_id, edition_slug=data.edition_slug
        )

        if card:
            # Card already exists
            return card

        edition = self.edition_service.get_or_create_edition(data.edition_slug, commit=False)

        card_loaded.update({"edition_id": edition.id})
        card = self._to_entity(data=card_loaded)

        card = self.uow.cards.save(card)

        if commit:
            self.uow.commit()

        return card
