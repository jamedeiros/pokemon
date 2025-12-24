from app.domain.models import Card
from app.domain.schemas import CardInput

from .base import BaseService
from .edition_service import EditionService


class CardService(BaseService):
    """Service class for card-related operations."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize a CardService instance.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        """
        super().__init__(*args, **kwargs)
        kwargs.update({"liga": self.liga})
        self.edition_service = EditionService(*args, **kwargs)

    def create_card(self, input_card: CardInput, commit: bool = True) -> Card:
        """Create a Pokémon card.

        :param input_card: CardInput object containing card_id, set_id, and edition
        :return: CardLoad object with card details
        """
        card_loaded = self.liga.get_card(input_card.card_id, input_card.set_id, input_card.edition_slug)

        card = self.uow.cards.get_by_identifiers(
            card_id=input_card.card_id, set_id=input_card.set_id, edition_slug=input_card.edition_slug
        )

        if card:
            # Card already exists
            return card

        edition = self.edition_service.get_or_create_edition(input_card.edition_slug, commit=False)

        card = Card.model_validate(
            {
                "card_id": card_loaded.card_id,
                "set_id": card_loaded.set_id,
                "name": card_loaded.name,
                "rarity": card_loaded.rarity,
                "edition_id": edition.id,
            }
        )

        card = self.uow.cards.save(card)

        if commit:
            self.uow.commit()

        return card

    def get_all_cards(self, page: int, page_size: int) -> tuple[list[Card], int]:
        """Retrieve all Pokémon cards.

        :return: List of Card objects
        """
        cards, total = self.uow.cards.list(skip=(page - 1) * page_size, limit=page_size)
        return cards, total
