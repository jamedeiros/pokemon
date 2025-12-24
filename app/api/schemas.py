from pydantic import BaseModel, Field


class PageInfo(BaseModel):
    total: int
    page: int
    page_size: int


class ErrorMessage(BaseModel):
    message: any

    model_config = {"arbitrary_types_allowed": True}


class ResponseModel[T](BaseModel):
    metadata: PageInfo | None = None
    data: T | list[T] | None = None
    error: ErrorMessage | None = None

    model_config = {"arbitrary_types_allowed": True}


class PageParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number (starts at 1)")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
