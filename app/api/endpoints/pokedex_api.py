from fastapi import APIRouter, status

from app.api.deps import PaginationDep
from app.api.helper import ok
from app.api.schemas import PageInfo, ResponseModel
from app.core.db import DbSession
from app.domain.models import Pokedex
from app.domain.schemas.pokedex_scbema import PokedexResponse
from app.service.pokedex_service import PokedexService

router = APIRouter()


ResponsePokedex = ResponseModel[Pokedex]
ResponsePokedexList = ResponseModel[list[Pokedex]]


@router.post("/pokedexes", summary="Post Pokedex", response_model=ResponsePokedex, status_code=status.HTTP_201_CREATED)
def post_pokedex(input_pokedex: Pokedex, session: DbSession) -> ResponsePokedex:
    """Create a Pokémon pokedex by its ID, set ID, and edition."""
    service = PokedexService(session)
    pokedex = service.create_pokedex(input_pokedex)
    return ok(data=PokedexResponse.from_model(pokedex))


@router.get("/pokedexes", summary="Get all pokedexes", response_model=ResponsePokedexList)
def list_pokedexes(
    pagination: PaginationDep,
    session: DbSession,
) -> ResponsePokedexList:
    """Retrieve all pokedexes."""
    service = PokedexService(session)
    pokedexes, total = service.get_all_pokedexes(page=pagination.page, page_size=pagination.page_size)
    return ok(
        data=[PokedexResponse.from_model(pokedex) for pokedex in pokedexes],
        metadata=PageInfo(
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
        ),
    )
