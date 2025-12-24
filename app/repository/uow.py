from sqlmodel import Session

from app.domain.models import Card, Edition

from .repositories import CardRepository, EditionRepository


class UnitOfWork:
    def __init__(self, session: Session):
        self.cards = CardRepository(session, Card)
        self.editions = EditionRepository(session, Edition)
        self.session = session

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
