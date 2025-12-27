from sqlmodel import Field, Relationship, SQLModel

from app.core.db import Model
from app.domain.schemas.edition_schema import EditionLoad


class PokedexEntry(SQLModel, table=True):
    """Class representing an entry in a Pokedex."""

    pokedex_id: int | None = Field(default=None, foreign_key="pokedex.id", primary_key=True)
    card_id: int | None = Field(default=None, foreign_key="card.id", primary_key=True)


class Edition(Model, table=True):
    """Class representing a Pokemon card edition."""

    name: str
    code: str
    year: str

    cards: list["Card"] = Relationship(back_populates="edition")

    @classmethod
    def from_data(cls, data: EditionLoad) -> "Edition":
        """Create an Edition instance from a data dictionary.

        :param cls: The Edition class
        :type cls: Edition
        :param data: A dictionary containing edition data
        :type data: EditionLoad
        :return: An Edition instance
        :rtype: Edition
        """
        return cls.model_validate(
            {
                "name": data.name,
                "code": data.code,
                "year": data.year,
            }
        )

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

    pokedexes: list["Pokedex"] = Relationship(back_populates="cards", link_model=PokedexEntry)

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


class Pokedex(Model, table=True):
    """Class representing a Pokedex."""

    name: str

    cards: list["Card"] = Relationship(back_populates="pokedexes", link_model=PokedexEntry)

    def __str__(self) -> str:
        """Return a string representation of the Pokedex instance.

        :param self: The pokedex instance
        :return: String representation of the pokedex
        :rtype: str
        """
        return f"Pokedex: {self.name}"
