from fastapi import APIRouter, status

from app.api.deps import PaginationDep
from app.api.helper import ok
from app.api.schemas import PageInfo, ResponseModel
from app.core.db import DbSession
from app.domain.schemas import CardInput, CardResponse
from app.service import CardService

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


ResponseCard = ResponseModel[CardResponse]
ResponseCardList = ResponseModel[list[CardResponse]]


@router.post("/cards", summary="Post Pokémon card", response_model=ResponseCard, status_code=status.HTTP_201_CREATED)
def post_card(input_card: CardInput, session: DbSession) -> ResponseCard:
    """Create a Pokémon card by its ID, set ID, and edition."""
    service = CardService(session)
    card = service.create_card(input_card)
    return ok(data=CardResponse.from_model(card))


@router.get("/cards", summary="Get all Pokémon cards", response_model=ResponseCardList)
def list_cards(
    pagination: PaginationDep,
    session: DbSession,
) -> ResponseCardList:
    """Retrieve all Pokémon cards."""
    service = CardService(session)
    cards, total = service.get_all_cards(page=pagination.page, page_size=pagination.page_size)
    return ok(
        data=[CardResponse.from_model(card) for card in cards],
        metadata=PageInfo(
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
        ),
    )


# 037  159  JTG
