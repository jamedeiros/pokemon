from typing import Annotated

from fastapi.params import Depends

from .schemas import PageParams


def pagination_parameters(page: int = 1, page_size: int = 20) -> PageParams:
    return PageParams(page=page, page_size=page_size)


PaginationDep = Annotated[PageParams, Depends(pagination_parameters)]
