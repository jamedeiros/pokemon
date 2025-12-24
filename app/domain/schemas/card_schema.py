from pydantic import BaseModel, field_validator

from app.domain.models.entities import Card


class CardLoad(BaseModel):
    """Class representing a load schema for Pokemon card."""

    id: int | None = None
    card_id: str
    set_id: str
    name: str
    rarity: str
    edition_code: str

    @field_validator("name")
    @classmethod
    def clean_name(cls, v: str) -> str:
        """Clean the name."""
        return v.split(" (")[0].strip()

    @field_validator("rarity")
    @classmethod
    def clean_rarity(cls, v: str) -> str:
        """Clean the rarity."""
        return v.split("\n")[0].strip()


class CardInput(BaseModel):
    """Class representing an input schema for Pokemon card."""

    card_id: str
    set_id: str
    edition_slug: str


class CardResponse(BaseModel):
    """Class representing a response schema for Pokemon card."""

    id: int
    card_id: str
    set_id: str
    name: str
    rarity: str
    edition_code: str
    edition_name: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, card: Card) -> "CardResponse":
        return cls(
            id=card.id,
            card_id=card.card_id,
            set_id=card.set_id,
            name=card.name,
            rarity=card.rarity,
            edition_code=card.edition.code,
            edition_name=card.edition.name,
        )
