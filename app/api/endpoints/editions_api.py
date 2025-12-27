from fastapi import APIRouter, status

from app.api.deps import PaginationDep
from app.api.helper import ok
from app.api.schemas import PageInfo, ResponseModel
from app.core.db import DbSession
from app.domain.schemas.edition_schema import EditionLoad, EditionResponse
from app.service import EditionService

router = APIRouter(prefix="/editions")


ResponseEdition = ResponseModel[EditionResponse]
ResponseEditionList = ResponseModel[list[EditionResponse]]


@router.post("", summary="Create a new edition", response_model=ResponseEdition, status_code=status.HTTP_201_CREATED)
def create_edition(input_edition: EditionLoad, session: DbSession) -> ResponseEdition:
    """Create a new edition."""
    service = EditionService(session)
    edition = service.create(data=input_edition)
    return ok(data=EditionResponse.from_model(edition))


@router.put(
    "/{edition_id}",
    summary="Update an existing edition",
    response_model=ResponseEdition,
    status_code=status.HTTP_200_OK,
)
def update_edition(edition_id: int, input_edition: EditionLoad, session: DbSession) -> ResponseEdition:
    """Update an existing edition by its ID."""
    service = EditionService(session)
    edition = service.update(id=edition_id, data=input_edition)
    return ok(data=EditionResponse.from_model(edition))


@router.get("/{edition_id}", summary="Get an edition by ID", response_model=ResponseEdition)
def get_edition(edition_id: int, session: DbSession) -> ResponseEdition:
    """Retrieve an edition by its ID."""
    service = EditionService(session)
    edition = service.get_by_id(id=edition_id)
    return ok(data=EditionResponse.from_model(edition))


@router.get("", summary="Get all editions", response_model=ResponseEditionList)
def list_editions(pagination: PaginationDep, session: DbSession) -> ResponseEditionList:
    """Retrieve all editions."""
    service = EditionService(session)
    editions, total = service.get_list(page=pagination.page, page_size=pagination.page_size)
    return ok(
        data=[EditionResponse.from_model(edition) for edition in editions],
        metadata=PageInfo(
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
        ),
    )
