from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import Model, engine


def init_models() -> None:
    """Initialize the database models by dropping and recreating all tables.

    This function uses the SQLAlchemy engine to drop all tables defined in Model.metadata
    and then recreates them. Intended for development and testing purposes.
    """
    Model.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN201, ARG001
    """FastAPI lifespan event handler.

    Initializes the database tables at application startup.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.

    Yields
    ------
    None

    """
    init_models()
    yield


app = FastAPI(
    title="API Gateway",
    description="A API Gateway for managing microservices",
    # openapi_url=f"{settings.API_VERSION_STR}/openapi.json",
    version="1.0.0",
    # debug=settings.DEBUG,
    lifespan=lifespan,
)


# Add CORS middleware first (will be processed last, ensuring proper CORS handling)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)
