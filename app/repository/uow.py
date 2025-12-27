from sqlmodel import Session

from app.domain.models import Card, Edition, Pokedex

from .repositories import CardRepository, EditionRepository, PokedexRepository


class UnitOfWork:
    def __init__(self, session: Session):
        self.cards = CardRepository(session, Card)
        self.editions = EditionRepository(session, Edition)
        self.pokedexes = PokedexRepository(session, Pokedex)
        self.session = session

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def get_repository(self, entity_type: type) -> object:
        if entity_type == Card:
            return self.cards
        elif entity_type == Edition:
            return self.editions
        elif entity_type == Pokedex:
            return self.pokedexes
        else:
            raise ValueError("Unknown entity type for repository retrieval.")
