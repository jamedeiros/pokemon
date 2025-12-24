from sqlmodel import Field, Relationship

from app.core.db import Model


class Edition(Model, table=True):
    """Class representing a Pokemon card edition."""

    name: str
    code: str
    year: str

    cards: list["Card"] = Relationship(back_populates="edition")

    def __str__(self) -> str:
        """Return a string representation of the Edition instance.

        :param self: The edition instance
        :type self: Edition
        """
        return f"{self.name} ({self.code})"


class Card(Model, table=True):
    """Class representing a Pokemon card."""

    card_id: str
    set_id: str
    name: str
    rarity: str

    edition_id: int = Field(foreign_key="edition.id")
    edition: "Edition" = Relationship(back_populates="cards")

    def __str__(self) -> str:
        """Return a string representation of the Card instance.

        :param self: The card instance
        :return: String representation of the card
        :rtype: str
        """
        return f"{self.name} ({self.card_id}/{self.set_id}) - Edition: {self.edition} - Rarity: {self.rarity}"

    @property
    def image_name(self) -> str:
        """Generate a standardized image name for the card.

        :param self: The card instance
        :return: Standardized image name
        :rtype: str
        """
        edition_code = self.edition.code if self.edition else "unknown"
        return f"{edition_code}_{self.card_id}_{self.set_id}.jpg"
