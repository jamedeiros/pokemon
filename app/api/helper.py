from typing import Never, TypeVar

from fastapi import HTTPException, status

from app.api.schemas import PageInfo, ResponseModel

T = TypeVar("T")


def ok(
    data: T | list[T],
    metadata: PageInfo | None = None,
) -> ResponseModel[T]:
    return ResponseModel(
        data=data,
        metadata=metadata,
    )


def fail(
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Never:
    raise HTTPException(
        status_code=status_code,
        detail=message,
    )
