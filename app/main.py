from fastapi import FastAPI

from app.api import api_router
from app.core.app_config import app

app.include_router(api_router)

if __name__ == "__main__":
    FastAPI.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
