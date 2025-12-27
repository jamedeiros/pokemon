from pydantic import BaseModel, field_validator

from app.domain.models.entities import Edition


class EditionLoad(BaseModel):
    """Class representing a load schema for Edition."""

    code: str
    name: str
    year: str

    @field_validator("name")
    @classmethod
    def clean_name(cls, v: str) -> str:
        """Clean the name."""
        return v.split(" (")[0].strip()

    @field_validator("year")
    @classmethod
    def clean_year(cls, v: str) -> str:
        """Clean the year."""
        return v.replace("(", "").replace(")", "").strip()


class EditionResponse(BaseModel):
    """Class representing a response schema for Pokemon edition."""

    id: int
    code: str
    name: str
    year: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, edition: Edition) -> "EditionResponse":
        return cls(
            id=edition.id,
            code=edition.code,
            name=edition.name,
            year=edition.year,
        )
