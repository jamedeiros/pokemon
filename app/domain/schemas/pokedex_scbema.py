from pydantic import BaseModel

from app.domain.models import Pokedex


class PokedexInput(BaseModel):
    """Class representing an input schema for Pokedex."""

    name: str


class PokedexResponse(BaseModel):
    """Class representing a response schema for pokedex."""

    id: int
    name: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, pokedex: Pokedex) -> "PokedexResponse":
        return cls(
            id=pokedex.id,
            name=pokedex.name,
        )
