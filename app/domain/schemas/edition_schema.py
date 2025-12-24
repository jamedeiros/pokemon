from pydantic import BaseModel, field_validator


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
